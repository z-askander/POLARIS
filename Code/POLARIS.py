# =============================================================================
#  POLARIS — Application de supervision d'un banc d'essai
#
#  Copyright (c) 2026 ASKANDER Zakaria.
#
#  Auteur      : ASKANDER Zakaria
#  Créé le     : 28/08/2026
#  Version     : 1.0
#
# =============================================================================
import sys
import os
import csv
import time
import queue
import collections
from datetime import datetime
from collections import deque

import numpy as np
import pyqtgraph as pg

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QThread, Signal, Slot, Qt, QTimer, QSettings
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QMessageBox,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QScrollArea, QLabel, QSizePolicy, QTabWidget,
    QColorDialog,
)


import propar

try:
    import serial
    _serial_ok = True
except ImportError:
    _serial_ok = False

try:
    from simple_pid import PID as SimplePID
    _pid_ok = True
except ImportError:
    _pid_ok = False

try:
    import nidaqmx
    from nidaqmx.constants import TerminalConfiguration, AcquisitionType
    from nidaqmx.stream_readers import AnalogMultiChannelReader
except Exception as _nidaqmx_err:
    nidaqmx = None
    _nidaqmx_import_error = _nidaqmx_err

from UI_POLARIS      import Ui_PolarisMainWindow
from UI_BRONKHORST_RDM import Ui_DeviceTile

# ── Configuration globale pyqtgraph ─────────────────────────────────────────
pg.setConfigOptions(antialias=True)
# ── Optimisations gros volumes ───────────────────────────────────────────
# Antialiasing désactivé (trop coûteux sur de longues séries de points).
pg.setConfigOptions(antialias=False)
# Le downsampling automatique 'peak' n'est PAS une option globale de PyQtGraph
# (setConfigOptions(autoDownsample=...) lève KeyError) : il est activé COURBE PAR
# COURBE via setDownsampling(auto=True, method='peak') — voir
# SauermannController._init_graph(). Effet identique, et le script reste exécutable.

# ── Constantes Bronkhorst ────────────────────────────────────────────────────
COLOR_MEASURE     = "#0A8DF1"
COLOR_VALVE       = "#F50B0B"
COLOR_BG          = "#F8F8F8"

# ── Constantes Julabo ────────────────────────────────────────────────────────
_DEFAULT_BAUDRATE = 4800
_DEFAULT_POLL_MS  = 1000


# =============================================================================
# AXES TEMPORELS PARTAGÉS
# =============================================================================

class RealTimeAxis(pg.AxisItem):
    """Axe X HH:MM — Bronkhorst."""
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(v).strftime("%H:%M") for v in values]


class DateAxis(pg.AxisItem):
    """Axe X DD/MM HH:MM — Julabo & Sauermann."""
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(v).strftime("%d/%m %H:%M") for v in values]


# =============================================================================
# ██████  BRONKHORST
# =============================================================================

class ScanWorker(QThread):
    """Scanne le bus pour trouver les appareils connectés."""
    progress     = Signal(int)
    device_found = Signal(dict)
    error        = Signal(str)

    def __init__(self, port: str, addresses: list):
        super().__init__()
        self.port      = port
        self.addresses = addresses
        self._stop     = False

    def run(self):
        try:
            inst = propar.instrument(self.port)
        except Exception as e:
            self.error.emit(f"Erreur port COM : {e}")
            return

        total = len(self.addresses)
        for i, addr in enumerate(self.addresses):
            if self._stop:
                break
            self.progress.emit(int((i / total) * 100))
            inst.address = addr
            try:
                cap = inst.readParameter(21)
                if cap is not None:
                    device = {
                        "address":  addr,
                        "model":    str(inst.readParameter(115) or "?"),
                        "fluid":    str(inst.readParameter(25)  or "?"),
                        "capacity": float(cap),
                        "unit":     str(inst.readParameter(129) or "?"),
                    }
                    self.device_found.emit(device)
            except Exception:
                pass

        self.progress.emit(100)

    def stop(self):
        self._stop = True


class SerialWorker(QThread):
    """Lecture continue et écriture prioritaire sur le bus RS-485."""
    data_updated = Signal(int, dict)
    node_status  = Signal(int, bool)   # (adresse, connecté) — via paramètre ID 1
    error_msg    = Signal(str)

    def __init__(self, port: str, active_nodes: list):
        super().__init__()
        self.port         = port
        self.active_nodes = active_nodes
        self.cmd_queue    = queue.Queue()
        self._stop        = False

    def add_command(self, address: int, parameter: int, value):
        self.cmd_queue.put({"addr": address, "param": parameter, "val": value})

    def run(self):
        try:
            inst = propar.instrument(self.port)
        except Exception as e:
            self.error_msg.emit(f"Erreur d'ouverture Propar : {e}")
            return

        node_index = 0
        while not self._stop:
            while not self.cmd_queue.empty():
                cmd = self.cmd_queue.get()
                inst.address = cmd["addr"]
                try:
                    inst.writeParameter(cmd["param"], cmd["val"])
                except Exception as e:
                    self.error_msg.emit(f"Erreur écriture (Nœud {cmd['addr']}) : {e}")

            if self.active_nodes:
                addr         = self.active_nodes[node_index]
                inst.address = addr
                # Test de connexion/identification via le paramètre ID 1 :
                # lecture réussie et non nulle → RDM connecté (LED verte),
                # échec ou None → déconnecté (LED grise).
                try:
                    ident     = inst.readParameter(1)
                    connected = ident is not None
                except Exception:
                    connected = False
                self.node_status.emit(addr, connected)

                if connected:
                    try:
                        data = {
                            "measure": inst.readParameter(8),
                            "valve":   inst.readParameter(55),
                            "temp":    inst.readParameter(142),
                        }
                        self.data_updated.emit(addr, data)
                    except Exception:
                        pass
                node_index = (node_index + 1) % len(self.active_nodes)

            time.sleep(0.05)

    def stop(self):
        self._stop = True


class DeviceTile(QWidget):
    """Représente un seul appareil Bronkhorst avec graphique temps réel."""
    send_setpoint_signal = Signal(int, float)
    _MAX_POINTS          = 4800

    def __init__(self, device_info: dict, window_s: int = 60,
                 show_numeric: bool = True, show_graph: bool = True):
        super().__init__()
        self.ui = Ui_DeviceTile()
        self.ui.setupUi(self)

        self.address  = device_info["address"]
        self.capacity = device_info["capacity"]
        self.unit     = device_info["unit"]
        self.window_s = window_s
        self._t0      = time.monotonic()

        # Affichage sélectif demandé par l'utilisateur après le scan
        self._show_numeric = bool(show_numeric)
        self._show_graph   = bool(show_graph)

        self._t_buf       = collections.deque(maxlen=self._MAX_POINTS)
        self._measure_buf = collections.deque(maxlen=self._MAX_POINTS)
        self._valve_buf   = collections.deque(maxlen=self._MAX_POINTS)
        # Consigne utilisateur (en unité réelle) tracée sur l'axe gauche, comme
        # la consigne du Julabo. `_setpoint_real` = dernière consigne ENVOYÉE
        # (bouton « Envoyer ») ; le buffer suit la mesure point par point.
        self._setpoint_buf  = collections.deque(maxlen=self._MAX_POINTS)
        self._setpoint_real = 0.0

        self.ui.group_box.setTitle(f"Débitmètre  —  Adresse {self.address}")
        self.ui.lbl_model.setText(device_info["model"])
        self.ui.lbl_fluid.setText(device_info["fluid"])
        self.ui.spin_setpoint_unit.setMaximum(self.capacity)
        self.ui.spin_setpoint_unit.setSuffix(f"  {self.unit}")

        self.ui.spin_setpoint_pct.valueChanged.connect(self._sync_unit)
        self.ui.spin_setpoint_unit.valueChanged.connect(self._sync_pct)
        self.ui.btn_send.clicked.connect(self._emit_setpoint)
        # Autorisation des modifications (envoi de consignes) pour cet appareil,
        # pilotée par la colonne « Modifications » du panneau de sélection.
        self._modif_enabled = True

        # ── Résolution des conteneurs (numérique / graphique) ──────────────
        # Calculés une seule fois ; servent au masquage RÉVERSIBLE via
        # set_display_mode (montrer/cacher sans détruire ni vider les buffers).
        self._graph_built = False
        try:
            self._graph_holder = self.ui.plot_placeholder_layout.parentWidget()
        except Exception:
            self._graph_holder = None

        _num_names = ("lbl_model", "lbl_fluid", "lbl_measure_pct", "lbl_measure_unit",
                      "lbl_diag", "spin_setpoint_pct", "spin_setpoint_unit", "btn_send")
        self._numeric_widgets = [w for w in (getattr(self.ui, n, None) for n in _num_names)
                                 if w is not None]
        gb  = getattr(self.ui, "group_box", None)
        anc = self._common_ancestor(self._numeric_widgets)
        # Conteneur numérique dédié si l'ancêtre commun n'englobe pas le graphique.
        if (anc is not None and anc is not self and anc is not gb
                and not self._is_descendant(self._graph_holder, anc)):
            self._numeric_container = anc
        else:
            self._numeric_container = None

        # Application initiale de l'affichage (réversible, construit le graphe si
        # demandé). Les buffers sont déjà créés et ne sont jamais vidés ici.
        self.set_display_mode(self._show_numeric, self._show_graph)

    # ── Masquage sélectif (numérique / graphique) ────────────────────────
    @staticmethod
    def _is_descendant(widget, ancestor) -> bool:
        if widget is None or ancestor is None:
            return False
        w = widget
        while w is not None:
            if w is ancestor:
                return True
            w = w.parentWidget()
        return False

    @staticmethod
    def _common_ancestor(widgets):
        widgets = [w for w in widgets if w is not None]
        if not widgets:
            return None
        chains = []
        for w in widgets:
            chain, x = [], w
            while x is not None:
                chain.append(x)
                x = x.parentWidget()
            chains.append(chain)
        rest = [set(c) for c in chains[1:]]
        for cand in chains[0]:
            if all(cand in s for s in rest):
                return cand
        return None

    # ── Affichage RÉVERSIBLE (numérique / graphique) ─────────────────────
    def set_display_mode(self, show_numeric: bool, show_graph: bool):
        """Affiche/masque dynamiquement le bloc numérique et/ou le graphique,
        SANS détruire la tuile, sans toucher à l'acquisition et SANS vider les
        buffers (`_t_buf`, `_measure_buf`, `_valve_buf`).

        Le graphique est construit paresseusement la première fois qu'il est
        demandé (s'il n'avait pas été bâti au démarrage)."""
        show_numeric = bool(show_numeric)
        show_graph   = bool(show_graph)
        self._show_numeric = show_numeric
        self._show_graph   = show_graph

        # Graphique : construction différée si nécessaire, puis (dé)masquage.
        if show_graph and not self._graph_built:
            self._build_graph()
        self._set_graph_visible(show_graph)

        # Bloc numérique : (dé)masquage réversible.
        self._set_numeric_visible(show_numeric)

        # Si plus rien n'est demandé, on masque la tuile entière (l'acquisition
        # et le remplissage des buffers se poursuivent malgré tout) ; sinon on
        # la réaffiche.
        self.setVisible(show_numeric or show_graph)

        # ── Adaptation de la taille de la tuile ──────────────────────────────
        # La hauteur est dérivée du CONTENU réel (sizeHint) pour ne jamais
        # tronquer le bas de la tuile ; on applique seulement un plancher.
        #   • Numérique seul  → tuile compacte (hauteur = contenu numérique) qui
        #                       peut se placer à deux par ligne (« Preferred »).
        #   • Graphique inclus → pleine hauteur/largeur (« Expanding »), au moins
        #                       la hauteur du contenu complet (numérique + graphe).
        self.ensurePolished()
        # Recalcule la géométrie après (dé)masquage pour un sizeHint à jour
        # (un widget masqué ne doit plus compter dans la hauteur du contenu).
        for _lay in (self.layout(),
                     self.ui.group_box.layout() if hasattr(self.ui, "group_box") else None):
            if _lay is not None:
                _lay.invalidate()
                _lay.activate()
        hint_h = self.sizeHint().height() + 8   # petite marge anti-troncature
        if show_graph:
            # La hauteur est pilotée par le CONTENU RÉEL (hint_h = sizeHint, qui
            # inclut déjà le bloc numérique éventuel + le graphe compact AVEC son
            # axe X). On applique seulement un petit plancher de sécurité (200 px)
            # contre un sizeHint dégénéré : ce plancher est volontairement SOUS la
            # hauteur naturelle d'une tuile graphique (≈ graphe 170 + marges), il
            # ne crée donc AUCUN vide blanc en bas. Aucun maximum n'est fixé (un
            # plafond trop bas rognerait l'axe X) ; la grille est alignée en haut
            # (AlignTop) et la politique verticale « Preferred » empêche l'étirement
            # en « giga-tuile ». Le trop-plein éventuel passe par le défilement.
            self.setMinimumHeight(max(200, hint_h))
            self.setMaximumHeight(16777215)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        else:
            self.setMinimumHeight(0)
            self.setMaximumHeight(16777215)
            # Hauteur fixe = contenu numérique complet (plancher 140 px).
            self.setFixedHeight(max(140, hint_h))
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Rafraîchit immédiatement le graphe nouvellement affiché avec
        # l'historique déjà accumulé (aucune donnée perdue).
        if show_graph and self._graph_built and len(self._t_buf) >= 2:
            self._refresh_graph(self._t_buf[-1])

    def _set_graph_visible(self, visible: bool):
        if self._graph_holder is not None:
            self._graph_holder.setVisible(visible)
        plot = getattr(self, "_plot", None)
        if plot is not None:
            plot.setVisible(visible)

    def _set_numeric_visible(self, visible: bool):
        if self._numeric_container is not None:
            self._numeric_container.setVisible(visible)
        else:
            for w in self._numeric_widgets:
                w.setVisible(visible)

    def _sync_unit(self, val_pct):
        self.ui.spin_setpoint_unit.blockSignals(True)
        self.ui.spin_setpoint_unit.setValue((val_pct / 100.0) * self.capacity)
        self.ui.spin_setpoint_unit.blockSignals(False)

    def _sync_pct(self, val_unit):
        if self.capacity > 0:
            self.ui.spin_setpoint_pct.blockSignals(True)
            self.ui.spin_setpoint_pct.setValue((val_unit / self.capacity) * 100.0)
            self.ui.spin_setpoint_pct.blockSignals(False)

    def set_modifications_enabled(self, enabled: bool):
        """Active/désactive l'envoi de consignes (« modifications ») pour cet
        appareil. Désactivé → le bouton « Envoyer » est grisé et inopérant."""
        self._modif_enabled = bool(enabled)
        if hasattr(self.ui, "btn_send"):
            self.ui.btn_send.setEnabled(self._modif_enabled)

    def _emit_setpoint(self):
        # Garde-fou : si les modifications sont désactivées pour cet appareil,
        # l'envoi est ignoré (le bouton est normalement déjà grisé).
        if not getattr(self, "_modif_enabled", True):
            return
        # Consigne tracée = valeur envoyée, exprimée dans l'unité réelle (même
        # échelle que l'axe gauche « Mesure »).
        self._setpoint_real = float(self.ui.spin_setpoint_unit.value())
        self.send_setpoint_signal.emit(self.address, self.ui.spin_setpoint_pct.value())

    def _build_graph(self):
        if getattr(self, "_graph_built", False):
            return
        self._plot = pg.PlotWidget(
            axisItems={'bottom': RealTimeAxis(orientation='bottom')},
            background=COLOR_BG
        )
        # Graphe compact et BORNÉ en hauteur : il ne doit jamais s'étirer pour
        # remplir tout l'écran. On fixe une plage 160–200 px (on garde ≥ ~30 px
        # en bas pour l'axe X, sinon il disparaît) ET une politique verticale
        # « Preferred » au lieu d'« Expanding » : sans ça, le graphe grandissait
        # pour occuper tout l'espace vertical disponible de la tuile.
        self._plot.setMinimumHeight(160)
        self._plot.setMaximumHeight(200)
        self._plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._plot.showGrid(x=True, y=True, alpha=0.25)
        self._plot.setLabel("bottom", "")
        self._plot.setLabel("left", f"Mesure ({self.unit})", color=COLOR_MEASURE)
        self._plot.setYRange(0, self.capacity, padding=0)
        self._plot.getViewBox().setMouseEnabled(y=False)

        self._curve_measure = self._plot.plot(
            pen=pg.mkPen(COLOR_MEASURE, width=2),
            name=f"Mesure ({self.unit})",
        )

        # Consigne utilisateur sur le MÊME axe gauche que la mesure (unité réelle,
        # plage 0…capacity). Orange pointillé, comme la consigne du Julabo.
        self._curve_setpoint = self._plot.plot(
            pen=pg.mkPen(color=(255, 165, 0), width=2,
                         style=QtCore.Qt.DashLine),
            name=f"Consigne ({self.unit})",
        )

        self._plot.showAxis("right")
        self._plot.getAxis("right").setLabel("Valve (%)", color=COLOR_VALVE)

        self._vb_valve = pg.ViewBox()
        self._plot.scene().addItem(self._vb_valve)
        self._plot.getAxis("right").linkToView(self._vb_valve)
        self._vb_valve.setXLink(self._plot)
        self._vb_valve.setYRange(0, 100, padding=0)
        self._vb_valve.setMouseEnabled(y=False)

        self._curve_valve = pg.PlotDataItem(
            pen=pg.mkPen(COLOR_VALVE, width=2),
            name="Valve (%)",
        )
        self._vb_valve.addItem(self._curve_valve)

        self._plot.getViewBox().sigResized.connect(self._sync_vb_geometry)
        self._sync_vb_geometry()

        legend = self._plot.addLegend(offset=(10, 10))
        legend.addItem(self._curve_measure,  f"Mesure ({self.unit})")
        legend.addItem(self._curve_setpoint, f"Consigne ({self.unit})")
        legend.addItem(self._curve_valve,    "Valve (%)")

        self.ui.plot_placeholder_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.plot_placeholder_layout.addWidget(self._plot)
        self._graph_built = True

    def _sync_vb_geometry(self):
        self._vb_valve.setGeometry(self._plot.getViewBox().sceneBoundingRect())
        self._vb_valve.linkedViewChanged(self._plot.getViewBox(), self._vb_valve.XAxis)

    def set_window(self, seconds: int):
        self.window_s = seconds

    @Slot(dict)
    def update_data(self, data: dict):
        t_now = time.time()

        measure_real = measure_pct = 0.0
        if data["measure"] is not None:
            measure_pct  = (data["measure"] / 32000.0) * 100.0
            measure_real = (data["measure"] / 32000.0) * self.capacity

        valve_pct = 0.0
        if data["valve"] is not None:
            valve_pct = (data["valve"] / 16777215.0) * 100.0

        temp_str = "--"
        if data["temp"] is not None:
            temp_str = f"{data['temp']:.1f}"

        self.ui.lbl_measure_pct.setText(f"{measure_pct:.2f} %")
        self.ui.lbl_measure_unit.setText(f"{measure_real:.3f}  {self.unit}")
        self.ui.lbl_diag.setText(f"Valve : {valve_pct:.1f} %   |   Temp : {temp_str} °C")

        self._t_buf.append(t_now)
        self._measure_buf.append(measure_real)
        self._valve_buf.append(valve_pct)
        self._setpoint_buf.append(self._setpoint_real)
        if self._show_graph:
            self._refresh_graph(t_now)

    def _refresh_graph(self, t_now: float):
        if len(self._t_buf) < 2:
            return
        t_arr = np.fromiter(self._t_buf,       dtype=np.float64, count=len(self._t_buf))
        m_arr = np.fromiter(self._measure_buf,  dtype=np.float64, count=len(self._measure_buf))
        v_arr = np.fromiter(self._valve_buf,    dtype=np.float64, count=len(self._valve_buf))
        s_arr = np.fromiter(self._setpoint_buf, dtype=np.float64, count=len(self._setpoint_buf))

        self._curve_measure.setData(t_arr, m_arr)
        self._curve_setpoint.setData(t_arr, s_arr)
        self._curve_valve.setData(t_arr, v_arr)
        self._plot.setXRange(t_now - self.window_s, t_now, padding=0.02)


class BronkhorstController(QtCore.QObject):
    """Onglet Bronkhorst — ex FlowSuiteClone.

    Nouveau flux ergonomique :
        1. SCAN  → les appareils détectés sont listés dans un panneau de
           configuration (adresse + modèle lu au paramètre 115), sans rien
           afficher dans la zone principale ni démarrer d'acquisition.
        2. CHOIX → pour chaque appareil, deux cases indépendantes :
           « Afficher les paramètres numériques » et « Afficher le graphique ».
        3. APPLIQUER → génère uniquement les tuiles choisies (numérique seul,
           graphique seul, ou tuile complète) et démarre le worker série pour
           les seuls nœuds validés.
    """
    led_changed = QtCore.Signal(str)   # couleur CSS : vert/rouge/gris
    rdm_status        = QtCore.Signal(int, bool)   # (adresse, connecté) → LED RDM
    rdm_nodes_changed = QtCore.Signal(list)        # nœuds acquis → panneau LED dashboard

    def __init__(self, ui_instance: Ui_PolarisMainWindow, main_window: QMainWindow):
        super().__init__(main_window)
        self.ui = ui_instance
        self.main_window = main_window  # Référence à la fenêtre principale

        self.tiles:           dict[int, DeviceTile] = {}
        self.scanned_devices: dict[int, dict]       = {}   # adresse → device_info
        self.config_rows:     dict[int, dict]       = {}   # adresse → {checkboxes}
        self.config_panel = None    # QGroupBox de configuration (liste d'attente)
        self._cfg_grid    = None
        self._cfg_apply   = None
        self._cfg_empty   = None

        self.scan_worker:     ScanWorker   | None = None
        self.serial_worker:   SerialWorker | None = None
        self.csv_manager = None   # gestionnaire CSV centralisé (défini par MainApp)

        # Grille adaptative d'accueil des tuiles (créée à la 1re application).
        self._grid_host  = None   # QWidget hôte inséré dans tiles_layout
        self._tiles_grid = None   # QGridLayout : placement compact/pleine largeur

        self.ui.btn_scan.clicked.connect(self._start_scan)
        self.ui.spin_window.valueChanged.connect(self._update_graph_window)

        # Bouton « Sélection » déjà présent dans le .ui (btn_selection) : on le
        # relie simplement à la réouverture du panneau de configuration à chaud
        # (sans couper le SerialWorker ni perdre les buffers).
        if hasattr(self.ui, "btn_selection"):
            self.ui.btn_selection.setToolTip(
                "Modifier l'affichage (numérique / graphique) sans couper l'acquisition")
            self.ui.btn_selection.clicked.connect(self._on_selection_clicked)

        # Restaure le dernier port COM utilisé (mémorisé entre deux sessions).
        self._load_settings()

    # ── Persistance du port COM (mémorisation inter-sessions) ─────────────
    def _settings(self) -> QSettings:
        # Même organisation/application que les autres contrôleurs : les clés
        # cohabitent dans le même stockage QSettings.
        return QSettings("SIC320", "USB6003_Monitor")

    def _load_settings(self):
        """Recharge le dernier port COM Bronkhorst (défaut « COM7 »)."""
        s = self._settings()
        if hasattr(self.ui, "input_port"):
            self.ui.input_port.setText(s.value("bronkhorst/port", "COM7"))

    def _save_settings(self):
        """Mémorise le port COM Bronkhorst courant pour la prochaine session."""
        if hasattr(self.ui, "input_port"):
            s = self._settings()
            s.setValue("bronkhorst/port", self.ui.input_port.text())

    # ── Utilitaire : vider la zone principale ────────────────────────────
    def _clear_main_zone(self):
        for i in reversed(range(self.ui.tiles_layout.count())):
            item = self.ui.tiles_layout.itemAt(i)
            w = item.widget() if item is not None else None
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self.tiles.clear()
        self.config_panel = None
        self._cfg_grid    = None
        self._cfg_apply   = None
        self._cfg_empty   = None
        self.config_rows.clear()
        # L'hôte de grille a été détruit avec les enfants de tiles_layout.
        self._grid_host  = None
        self._tiles_grid = None

    # ════════════════════════════════════════════════════════════════════
    #   PHASE 1 — SCAN
    # ════════════════════════════════════════════════════════════════════
    def _start_scan(self):
        # Stopper d'éventuels threads en cours
        for worker in (self.scan_worker, self.serial_worker):
            if worker and worker.isRunning():
                worker.stop()
                worker.wait()
        self.serial_worker = None

        port = self.ui.input_port.text().strip()
        if not port:
            QMessageBox.warning(self.main_window, "Port manquant",
                                "Entrez un port COM valide.")
            return

        # Port valide → on le mémorise pour la prochaine session.
        self._save_settings()

        # Réinitialiser la zone principale + l'état
        self._clear_main_zone()
        self.scanned_devices.clear()

        # Panneau de configuration (liste d'attente), vide au départ
        self._build_config_panel()

        # Scan des adresses 1 à 127 du bus RS-485
        all_addresses = list(range(1, 128))

        self.ui.btn_scan.setEnabled(False)
        self.ui.lbl_status.setText("Scan en cours… (adresses 1 à 127)")
        self.ui.progress_bar.setValue(0)

        self.scan_worker = ScanWorker(port, all_addresses)
        self.scan_worker.progress.connect(self.ui.progress_bar.setValue)
        self.scan_worker.device_found.connect(self._on_device_found)
        self.scan_worker.error.connect(self._show_error)
        self.scan_worker.finished.connect(self._on_scan_finished)
        self.scan_worker.start()

    # ── Panneau de configuration (liste des appareils) ───────────────────
    def _build_config_panel(self):
        panel = QtWidgets.QGroupBox("Configuration de l'affichage")
        vbox  = QtWidgets.QVBoxLayout(panel)

        info = QtWidgets.QLabel(
            "Appareils détectés sur le bus. Pour chaque module, cochez ce que "
            "vous souhaitez afficher, puis cliquez sur « Appliquer ».")
        info.setWordWrap(True)
        info.setStyleSheet("color:#555;")
        vbox.addWidget(info)

        grid = QtWidgets.QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(0)   # 0 → bandes zébrées continues (voir _add_config_row)
        # Colonnes 0-1 : libellés simples. Colonnes 2-4 (cases) : libellé + deux
        # petits boutons « Tout » / « Aucun » propres à la colonne.
        lbl0 = QtWidgets.QLabel("Adresse");        lbl0.setStyleSheet("font-weight:bold;")
        lbl1 = QtWidgets.QLabel("Modèle (P115)");  lbl1.setStyleSheet("font-weight:bold;")
        grid.addWidget(lbl0, 0, 0)
        grid.addWidget(lbl1, 0, 1)
        grid.addWidget(self._make_col_header("Numérique",     "numeric"), 0, 2)
        grid.addWidget(self._make_col_header("Graphique",     "graph"),   0, 3)
        grid.addWidget(self._make_col_header("Modifications", "modif"),   0, 4)
        vbox.addLayout(grid)

        self._cfg_empty = QtWidgets.QLabel("  (recherche en cours…)")
        self._cfg_empty.setStyleSheet("color:#999; font-style:italic;")
        vbox.addWidget(self._cfg_empty)

        # Barre de boutons : plus de « Tout cocher / décocher » globaux (ils sont
        # désormais par colonne dans l'en-tête). On ne garde que « Appliquer ».
        btns   = QtWidgets.QHBoxLayout()
        self._cfg_apply = QtWidgets.QPushButton("Appliquer")
        self._cfg_apply.setStyleSheet("font-weight:bold; padding:4px 18px;")
        self._cfg_apply.setEnabled(False)
        self._cfg_apply.clicked.connect(self._on_apply_config)
        btns.addStretch(1)
        btns.addWidget(self._cfg_apply)
        vbox.addLayout(btns)

        self.config_panel = panel
        self._cfg_grid     = grid
        self.ui.tiles_layout.addWidget(panel)

    def _make_col_header(self, title: str, key: str) -> QtWidgets.QWidget:
        """En-tête d'une colonne de cases : libellé + boutons « Tout » / « Aucun »
        qui cochent/décochent uniquement cette colonne (`key` ∈ numeric/graph/modif)."""
        w = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(2)
        lbl = QtWidgets.QLabel(title)
        lbl.setStyleSheet("font-weight:bold;")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(lbl)
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(3)
        b_all  = QtWidgets.QPushButton("Tout")
        b_none = QtWidgets.QPushButton("Aucun")
        for b in (b_all, b_none):
            b.setStyleSheet("padding:1px 6px; font-size:11px;")
        b_all.clicked.connect(lambda: self._set_column_checks(key, True))
        b_none.clicked.connect(lambda: self._set_column_checks(key, False))
        h.addStretch(1); h.addWidget(b_all); h.addWidget(b_none); h.addStretch(1)
        v.addLayout(h)
        return w

    @Slot(dict)
    def _on_device_found(self, device_info: dict):
        addr = int(device_info["address"])
        if addr in self.scanned_devices:
            return
        self.scanned_devices[addr] = device_info

        if self.config_panel is None:
            self._build_config_panel()
        if self._cfg_empty is not None:
            self._cfg_empty.hide()

        # Nœud 13 : modifications DÉSACTIVÉES par défaut (case « Modifications »
        # décochée) → son bouton « Envoyer » sera inopérant tant qu'on ne la
        # coche pas.
        self._add_config_row(addr, device_info, num_checked=True, graph_checked=True,
                             modif_checked=(addr != 13))

    def _add_config_row(self, addr: int, device_info: dict,
                        num_checked: bool = True, graph_checked: bool = True,
                        modif_checked: bool = True):
        """Ajoute une ligne (adresse + modèle + 3 cases : numérique / graphique /
        modifications) au panneau de configuration, avec l'état initial fourni."""
        row = self._cfg_grid.rowCount()

        # Zébrage : cadre de fond couvrant les 5 colonnes, ajouté AVANT les
        # cellules (peint DERRIÈRE), transparent aux clics.
        stripe = QtWidgets.QFrame()
        stripe.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        bg = "#F0F0F0" if (row % 2 == 1) else "#FFFFFF"
        stripe.setStyleSheet(f"background-color:{bg};")
        stripe.setMinimumHeight(28)
        self._cfg_grid.addWidget(stripe, row, 0, 1, 5)

        lbl_addr  = QtWidgets.QLabel(str(addr))
        lbl_model = QtWidgets.QLabel(str(device_info.get("model", "?")))
        chk_num   = QtWidgets.QCheckBox()
        chk_graph = QtWidgets.QCheckBox()
        chk_modif = QtWidgets.QCheckBox()
        chk_num.setChecked(bool(num_checked))
        chk_graph.setChecked(bool(graph_checked))
        chk_modif.setChecked(bool(modif_checked))
        chk_num.setToolTip("Afficher le bloc des valeurs numériques de cet appareil")
        chk_graph.setToolTip("Afficher le graphique temps réel de cet appareil")
        chk_modif.setToolTip("Autoriser l'envoi de consignes (le bouton « Envoyer » "
                             "de la tuile). Décoché → envoi désactivé.")

        self._cfg_grid.addWidget(lbl_addr,  row, 0)
        self._cfg_grid.addWidget(lbl_model, row, 1)
        self._cfg_grid.addWidget(chk_num,   row, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self._cfg_grid.addWidget(chk_graph, row, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self._cfg_grid.addWidget(chk_modif, row, 4, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.config_rows[addr] = {"numeric": chk_num, "graph": chk_graph,
                                  "modif": chk_modif}

    def _set_column_checks(self, key: str, state: bool):
        """Coche/décoche toutes les cases d'UNE colonne (numeric/graph/modif)."""
        for r in self.config_rows.values():
            chk = r.get(key)
            if chk is not None:
                chk.setChecked(state)

    def _on_scan_finished(self):
        self.led_changed.emit("#2ECC71")   # bus joignable → vert
        self.ui.btn_scan.setEnabled(True)

        n = len(self.scanned_devices)
        if n == 0:
            self.ui.lbl_status.setText("Scan terminé — aucun appareil détecté.")
            if self._cfg_empty is not None:
                self._cfg_empty.setText("  Aucun appareil détecté sur le bus.")
                self._cfg_empty.show()
            if self._cfg_apply is not None:
                self._cfg_apply.setEnabled(False)
            return

        self.ui.lbl_status.setText(
            f"Scan terminé — {n} appareil(s). Choisissez l'affichage puis « Appliquer »."
        )
        if self._cfg_apply is not None:
            self._cfg_apply.setEnabled(True)

    # ════════════════════════════════════════════════════════════════════
    #   SÉLECTION À CHAUD (sans couper le SerialWorker)
    # ════════════════════════════════════════════════════════════════════
    def _on_selection_clicked(self):
        """Rouvre le panneau de configuration d'affichage pour modifier à la
        volée ce qui est montré (numérique / graphique), SANS toucher au
        `SerialWorker` (l'acquisition et les buffers restent intacts)."""
        if not self.scanned_devices:
            QMessageBox.information(
                self.main_window, "Sélection",
                "Aucun appareil détecté. Lancez d'abord un scan.")
            return
        if self.config_panel is not None:
            return   # panneau déjà ouvert

        # Construit le panneau à partir de TOUS les appareils détectés au scan
        # (et non plus seulement de ceux actuellement affichés) : ainsi aucun
        # RDM n'est « perdu ». Un appareil détecté mais non sélectionné reste
        # listé et peut être ajouté plus tard. Chaque ligne est pré-cochée selon
        # l'état d'affichage ACTUEL de sa tuile si elle existe, sinon décochée
        # (appareil détecté mais pas encore affiché).
        self._build_config_panel()
        if self._cfg_empty is not None:
            self._cfg_empty.hide()
        for addr in sorted(self.scanned_devices.keys()):
            info = self.scanned_devices[addr]
            tile = self.tiles.get(addr)
            self._add_config_row(
                addr, info,
                num_checked=(tile._show_numeric if tile is not None else False),
                graph_checked=(tile._show_graph if tile is not None else False),
                modif_checked=(tile._modif_enabled if tile is not None
                               else (addr != 13)))
        if self._cfg_apply is not None:
            self._cfg_apply.setEnabled(True)
        for tile in self.tiles.values():
            tile.hide()
        self.ui.lbl_status.setText(
            "Sélection de l'affichage — l'acquisition continue en arrière-plan.")

    def _remove_config_panel(self):
        """Retire le panneau de configuration de la zone principale et remet à
        zéro ses références (sans toucher aux tuiles ni au worker)."""
        if self.config_panel is not None:
            self.config_panel.setParent(None)
            self.config_panel.deleteLater()
        self.config_panel = None
        self._cfg_grid    = None
        self._cfg_apply   = None
        self._cfg_empty   = None
        self.config_rows.clear()

    # ════════════════════════════════════════════════════════════════════
    #   GRILLE ADAPTATIVE DES TUILES
    # ════════════════════════════════════════════════════════════════════
    def _ensure_tiles_grid(self):
        """Crée (une fois) l'hôte de grille et l'insère dans tiles_layout.
        Les deux colonnes ont un facteur d'étirement égal : une tuile compacte
        occupe une demi-largeur, une grande tuile (span 2) toute la largeur."""
        if self._tiles_grid is not None:
            return
        self._grid_host  = QtWidgets.QWidget()
        self._tiles_grid = QtWidgets.QGridLayout(self._grid_host)
        self._tiles_grid.setContentsMargins(0, 0, 0, 0)
        self._tiles_grid.setHorizontalSpacing(8)
        self._tiles_grid.setVerticalSpacing(8)
        self._tiles_grid.setColumnStretch(0, 1)
        self._tiles_grid.setColumnStretch(1, 1)
        # Alignement en haut : les petites tuiles ne s'étirent pas verticalement.
        self._tiles_grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ui.tiles_layout.addWidget(self._grid_host)

    def _relayout_tiles(self):
        """(Re)positionne toutes les tuiles dans la grille selon leur mode
        d'affichage courant. Algorithme :
          • Numérique seul  → placé à (row, col) puis col++ ; à col==2 on passe
                              à la ligne suivante (2 petites tuiles par ligne).
          • Graphique inclus → occupe toute la largeur : si une ligne est
                              entamée (col==1) on la termine d'abord, puis la
                              grande tuile est placée en (row, 0) avec span 2.
        Les tuiles ne sont jamais détruites : on ne fait que les repositionner."""
        self._ensure_tiles_grid()
        grid = self._tiles_grid

        # Détacher toutes les tuiles de la grille (sans les supprimer).
        for tile in self.tiles.values():
            grid.removeWidget(tile)

        row = col = 0
        for addr in sorted(self.tiles.keys()):
            tile = self.tiles[addr]
            sn, sg = tile._show_numeric, tile._show_graph

            if not (sn or sg):
                tile.hide()            # rien à afficher pour cet appareil
                continue

            if sg:
                # Grande tuile (graphique seul ou complet) → pleine largeur.
                if col == 1:           # terminer une ligne compacte entamée
                    row += 1
                    col = 0
                grid.addWidget(tile, row, 0, 1, 2)
                row += 1
                col = 0
            else:
                # Petite tuile (numérique seul) → 2 par ligne.
                grid.addWidget(tile, row, col)
                col += 1
                if col == 2:
                    col = 0
                    row += 1
            tile.show()

    # ════════════════════════════════════════════════════════════════════
    #   PHASE 3 — APPLIQUER
    # ════════════════════════════════════════════════════════════════════
    def _on_apply_config(self):
        # État courant des cases pour TOUTES les lignes listées (numérique,
        # graphique, modifications).
        selection = [(addr, r["numeric"].isChecked(), r["graph"].isChecked(),
                      r["modif"].isChecked())
                     for addr, r in self.config_rows.items()]

        # Appareils désirés = au moins une case d'affichage cochée.
        desired      = [(a, sn, sg, sm) for (a, sn, sg, sm) in selection if sn or sg]
        desired_addr = {a for a, _, _, _ in desired}

        if not desired:
            QMessageBox.information(
                self.main_window, "Aucune sélection",
                "Cochez au moins une option (numérique ou graphique) "
                "pour au moins un appareil avant d'appliquer.")
            return

        # 1) Retirer les tuiles des appareils désormais décochés. L'appareil
        #    reste dans scanned_devices → il pourra être ré-ajouté plus tard.
        for addr in list(self.tiles.keys()):
            if addr not in desired_addr:
                tile = self.tiles.pop(addr)
                if self._tiles_grid is not None:
                    self._tiles_grid.removeWidget(tile)
                tile.setParent(None)
                tile.deleteLater()

        # 2) Créer les tuiles manquantes (appareils nouvellement cochés) et
        #    mettre à jour l'affichage de celles qui existent déjà. On applique
        #    aussi l'état « modifications » (autorisation d'envoi de consignes).
        for addr, sn, sg, sm in desired:
            tile = self.tiles.get(addr)
            if tile is None:
                info = self.scanned_devices[addr]
                tile = DeviceTile(info, window_s=self.ui.spin_window.value(),
                                  show_numeric=sn, show_graph=sg)
                tile.send_setpoint_signal.connect(self._handle_setpoint)
                self.tiles[addr] = tile
            else:
                tile.set_display_mode(sn, sg)   # show()/hide() réversible
            tile.set_modifications_enabled(sm)  # active/grise le bouton « Envoyer »

        # 3) Repositionner la grille et révéler les tuiles (retire le panneau).
        self._relayout_tiles()
        self._remove_config_panel()

        # 4) (Re)démarrer l'acquisition UNIQUEMENT si l'ensemble des nœuds a
        #    changé. Un simple basculement numérique/graphique sur les mêmes
        #    appareils ne coupe pas le worker (buffers et acquisition préservés).
        new_nodes = sorted(desired_addr)
        running   = (self.serial_worker is not None
                     and self.serial_worker.isRunning())
        cur_nodes = sorted(self.serial_worker.active_nodes) if running else None

        if new_nodes != cur_nodes:
            if running:
                self.serial_worker.stop()
                self.serial_worker.wait()
            port = self.ui.input_port.text().strip()
            self.serial_worker = SerialWorker(port, new_nodes)
            self.serial_worker.data_updated.connect(self._distribute_data)
            self.serial_worker.error_msg.connect(self._show_error)
            # Relais de l'état de connexion par RDM (paramètre ID 1) vers le
            # dashboard, et notification de la nouvelle liste de nœuds acquis
            # pour (re)construire le panneau de LED RDM.
            self.serial_worker.node_status.connect(self.rdm_status)
            self.serial_worker.start()
            self.rdm_nodes_changed.emit(list(new_nodes))

        self.led_changed.emit("#2ECC71")
        n_visible = sum(1 for t in self.tiles.values()
                        if t._show_numeric or t._show_graph)
        self.ui.lbl_status.setText(
            f"{len(self.tiles)} appareil(s) en acquisition "
            f"({n_visible} affiché(s)).")

    # ════════════════════════════════════════════════════════════════════
    #   ACQUISITION / DISTRIBUTION (inchangé)
    # ════════════════════════════════════════════════════════════════════
    @Slot(int, float)
    def _handle_setpoint(self, address: int, value_pct: float):
        if self.serial_worker:
            self.serial_worker.add_command(address, 9, int((value_pct / 100.0) * 32000))

    @Slot(int, dict)
    def get_valve_pct(self, addr: int) -> float:
        """Retourne la dernière position de valve connue pour une adresse (0-100%).
        Utilisé par PIDController pour le démarrage sans à-coup."""
        tile = self.tiles.get(addr)
        if tile is not None and tile._valve_buf:
            return tile._valve_buf[-1]   # dernière valeur en %
        return 50.0   # valeur de repli si adresse inconnue ou buffer vide

    def _distribute_data(self, address: int, data: dict):
        if address in self.tiles:
            self.tiles[address].update_data(data)

        # Enregistrement CSV centralisé : on mémorise la dernière mesure du nœud
        # (l'écriture effective est cadencée par les blocs Sauermann).
        if self.csv_manager is not None and self.csv_manager.is_active:
            info  = self.scanned_devices.get(address, {})
            cap   = float(info.get("capacity", 0.0) or 0.0)
            meas  = data.get("measure")
            if meas is not None:
                measure_pct  = (meas / 32000.0) * 100.0
                measure_real = (meas / 32000.0) * cap
            else:
                measure_pct = measure_real = None
            self.csv_manager.update_bronkhorst(address, measure_pct, measure_real)

    def get_active_nodes(self):
        """Liste [(adresse, modèle), …] des nœuds actuellement en acquisition.
        Utilisée pour figer les colonnes Bronkhorst du fichier CSV global."""
        nodes = []
        for addr in sorted(self.tiles.keys()):
            info = self.scanned_devices.get(addr, {})
            nodes.append((addr, str(info.get("model", "?"))))
        return nodes

    def _update_graph_window(self, value: int):
        for tile in self.tiles.values():
            tile.set_window(value)

    @Slot(str)
    def _show_error(self, msg: str):
        self.led_changed.emit("#E74C3C")   # erreur → rouge
        QMessageBox.warning(self.main_window, "Erreur RS-485", msg)

    def cleanup(self):
        """Arrêt propre de tous les threads."""
        for worker in (self.scan_worker, self.serial_worker):
            if worker and worker.isRunning():
                worker.stop()
                worker.wait()


# =============================================================================
# ██████  JULABO
# =============================================================================

class JulaboSerial:
    def __init__(self, port: str, baudrate: int = _DEFAULT_BAUDRATE, timeout: float = 2.0):
        self._port     = port
        self._baudrate = baudrate
        self._timeout  = timeout
        self._ser      = None

    def open(self):
        if not _serial_ok:
            raise ImportError("pyserial n'est pas installé.")
        self._ser = serial.Serial(
            port=self._port, baudrate=self._baudrate,
            bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE, rtscts=True, timeout=self._timeout
        )
        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

    def close(self):
        if self._ser and self._ser.is_open:
            try:
                self._ser.close()
            except Exception:
                pass
        self._ser = None

    @property
    def is_open(self) -> bool:
        return self._ser is not None and self._ser.is_open

    def _send_command(self, cmd: str) -> str | None:
        if not self.is_open:
            return None
        try:
            self._ser.reset_input_buffer()
            self._ser.write((cmd + "\r\n").encode("ascii"))
            line = self._ser.readline()
            if not line:
                return None
            return line.decode("ascii", errors="replace").strip()
        except Exception:
            return None

    def _write_command(self, cmd: str) -> bool:
        """Envoie une commande d'écriture (out_...).

        Le Julabo NE renvoie AUCUNE réponse à ces commandes : le succès doit donc
        se juger sur la bonne écriture série, et non sur la réception d'une ligne.
        L'ancienne logique attendait une réponse (readline) qui n'arrivait jamais,
        d'où un faux « échec » signalé alors que la commande passait bien — en plus
        de bloquer jusqu'au timeout à chaque envoi.
        """
        if not self.is_open:
            return False
        try:
            self._ser.reset_input_buffer()
            self._ser.write((cmd + "\r\n").encode("ascii"))
            self._ser.flush()
            return True
        except Exception:
            return False

    def _query_float(self, cmd: str) -> float | None:
        raw = self._send_command(cmd)
        if raw is None:
            return None
        try:
            return float(raw)
        except ValueError:
            return None

    def read_temp_internal(self) -> float | None: return self._query_float("in_pv_00")
    def read_temp_external(self) -> float | None: return self._query_float("in_pv_02")
    def read_power(self)         -> float | None: return self._query_float("in_pv_01")
    def read_pump(self)          -> float | None: return self._query_float("in_sp_27")
    def read_bath_level(self)    -> float | None: return self._query_float("in_pv_16")
    def read_setpoint(self)      -> float | None: return self._query_float("in_sp_00")

    def write_setpoint(self, value: float) -> bool:
        return self._write_command(f"out_sp_00 {value:.2f}")

    def start(self) -> bool:
        return self._write_command("out_mode_05 1")

    def stop(self) -> bool:
        return self._write_command("out_mode_05 0")


class JulaboWorker(QtCore.QObject):
    new_data  = QtCore.Signal(float, object, object, object, object, object, object)
    connected = QtCore.Signal(bool)
    error     = QtCore.Signal(str)
    finished  = QtCore.Signal()

    def __init__(self, port: str, baudrate: int = _DEFAULT_BAUDRATE,
                 poll_interval_ms: int = _DEFAULT_POLL_MS):
        super().__init__()
        self._port             = port
        self._baudrate         = baudrate
        self._poll_interval_ms = poll_interval_ms
        self._julabo           = JulaboSerial(port, baudrate)
        self._timer            = None
        self._stop             = False

    @QtCore.Slot()
    def run(self):
        try:
            self._julabo.open()
            self._stop = False
            self.connected.emit(True)
        except Exception as e:
            self.connected.emit(False)
            self.error.emit(f"Impossible d'ouvrir {self._port} : {e}")
            self.finished.emit()
            return

        self._timer = QtCore.QTimer()
        self._timer.setInterval(self._poll_interval_ms)
        self._timer.timeout.connect(self._poll)
        self._timer.start()
        self._poll()

        loop = QtCore.QEventLoop()
        self._event_loop = loop
        loop.exec()

        if self._timer:
            self._timer.stop()
            self._timer = None
        self._julabo.close()
        self.finished.emit()

    @QtCore.Slot()
    def _poll(self):
        if self._stop:
            if self._timer:
                self._timer.stop()
            if hasattr(self, "_event_loop"):
                self._event_loop.quit()
            return
        try:
            t          = time.time()
            t_int      = self._julabo.read_temp_internal()
            t_ext      = self._julabo.read_temp_external()
            pressure   = self._julabo.read_power()
            pump_speed = self._julabo.read_pump()
            level      = self._julabo.read_bath_level()
            setpoint   = self._julabo.read_setpoint()
            self.new_data.emit(t, t_int, t_ext, pressure, pump_speed, level, setpoint)
        except Exception as e:
            self.error.emit(f"Erreur de polling JULABO : {e}")

    def stop(self):
        self._stop = True
        if hasattr(self, "_event_loop"):
            QtCore.QMetaObject.invokeMethod(
                self._event_loop, "quit", QtCore.Qt.QueuedConnection
            )

    @QtCore.Slot(float)
    def set_setpoint(self, value: float):
        if self._julabo.is_open:
            if not self._julabo.write_setpoint(value):
                self.error.emit("Échec de l'écriture du setpoint")

    @QtCore.Slot()
    def start_julabo(self):
        if self._julabo.is_open:
            if not self._julabo.start():
                self.error.emit("Échec de la commande START (out_mode_05 1)")

    @QtCore.Slot()
    def stop_julabo(self):
        if self._julabo.is_open:
            if not self._julabo.stop():
                self.error.emit("Échec de la commande STOP (out_mode_05 0)")


class JulaboController(QtCore.QObject):
    """Onglet Julabo — ex JulaboApp."""
    _COLOR_INT = (231, 76, 60)
    _COLOR_EXT = (52, 152, 219)

    _setpoint_requested = QtCore.Signal(float)
    _start_requested    = QtCore.Signal()
    _stop_requested     = QtCore.Signal()

    # Signal vers le dashboard : t_int, t_ext, setpoint
    data_ready  = QtCore.Signal(object, object, object)
    led_changed = QtCore.Signal(str)   # couleur CSS : vert/rouge/gris

    def __init__(self, ui_instance: Ui_PolarisMainWindow, main_window: QMainWindow):
        super().__init__(main_window)
        self.ui = ui_instance
        self.main_window = main_window  # Référence à la fenêtre principale

        self._worker       = None
        self._thread       = None
        self._is_connected = False

        _default_win_s = 30 * 60.0
        _poll_s        = _DEFAULT_POLL_MS / 1000.0
        self._max_pts  = max(int(_default_win_s / _poll_s) + 10, 50)
        self._t_buf    = deque(maxlen=self._max_pts)
        self._tint_buf = deque(maxlen=self._max_pts)
        self._text_buf = deque(maxlen=self._max_pts)
        self._tsp_buf  = deque(maxlen=self._max_pts)
        # Instant (epoch s) du dernier point AJOUTÉ au graphe. Sert à décimer
        # l'empilage à la cadence d'affichage définie dans l'onglet Sauermann.
        self._last_graph_t = None
        self._value_labels = [
            self.ui.lblTInt, self.ui.lblTExt, self.ui.lblPressure,
            self.ui.lblPumpSpeed, self.ui.lblLevel, self.ui.lblSetpoint,
        ]

        self._init_graphs()
        self._set_led(False)

        self.ui.btnConnect.clicked.connect(self._on_connect)
        self.ui.btnDisconnect.clicked.connect(self._on_disconnect)
        self.ui.btnApplySp.clicked.connect(self._on_apply_setpoint)
        self.ui.btnStart.clicked.connect(self._on_start)
        self.ui.btnStop.clicked.connect(self._on_stop)
        self.ui.spinWindow.valueChanged.connect(self._on_window_changed)

        self._load_settings()

    def _init_graphs(self):
        self.graphWidget = pg.GraphicsLayoutWidget()
        self.graphWidget.setBackground('w')

        layout = QHBoxLayout(self.ui.plotContainer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphWidget)

        self._plot_ext = self.graphWidget.addPlot(
            row=0, col=0,
            axisItems={'bottom': DateAxis(orientation='bottom')}
        )
        self._plot_ext.setTitle(
            "<span style='color:#3498db; font-weight:bold'>T° Externe</span>"
            " &nbsp;/&nbsp; "
            "<span style='color:#e74c3c; font-weight:bold'>T° Interne</span>"
        )
        self._plot_ext.setLabel("left", "T° Externe (°C)", color=self._COLOR_EXT)
        self._plot_ext.showGrid(x=True, y=True, alpha=0.3)
        self._plot_ext.getAxis("left").setPen(pg.mkPen(self._COLOR_EXT, width=1))

        self._curve_ext = self._plot_ext.plot(
            pen=pg.mkPen(self._COLOR_EXT, width=2), name="T° externe (°C)"
        )

        self._vb_int = pg.ViewBox()
        self._plot_ext.scene().addItem(self._vb_int)

        axis_right = pg.AxisItem("right")
        axis_right.setLabel("T° Interne (°C)", color=self._COLOR_INT)
        axis_right.setPen(pg.mkPen(self._COLOR_INT, width=1))
        self._plot_ext.layout.addItem(axis_right, 2, 3)
        axis_right.linkToView(self._vb_int)
        self._axis_right = axis_right

        self._vb_int.setXLink(self._plot_ext)
        self._plot_ext.vb.sigResized.connect(self._sync_views)

        self._curve_int = pg.PlotDataItem(
            pen=pg.mkPen(self._COLOR_INT, width=2), name="T° interne (°C)"
        )
        self._vb_int.addItem(self._curve_int)

        self._curve_sp = pg.PlotDataItem(
            pen=pg.mkPen(color=(255, 165, 0), width=2,
                         style=QtCore.Qt.DashLine),
            name="Consigne (°C)",
        )
        self._plot_ext.addItem(self._curve_sp)

        legend = self._plot_ext.addLegend(offset=(10, 10))
        legend.addItem(self._curve_ext, "T° externe (°C)")
        legend.addItem(self._curve_int, "T° interne (°C)")
        legend.addItem(self._curve_sp,  "Consigne (°C)")
        self._sync_views()

    def _sync_views(self):
        self._vb_int.setGeometry(self._plot_ext.vb.sceneBoundingRect())

    def _set_led(self, on: bool):
        color = "#2ECC71" if on else "#bbb"
        self.ui.lblConnLed.setStyleSheet(
            f"border:1px solid #888; border-radius:6px; background:{color};"
        )
        self.led_changed.emit(color)

    def _on_connect(self):
        if not _serial_ok:
            QMessageBox.critical(self.main_window, "Erreur",
                                 "pyserial introuvable. Installez-le : pip install pyserial")
            return
        if self._thread is not None and self._thread.isRunning():
            return

        port = self.ui.linePort.text().strip()
        if not port:
            QMessageBox.warning(self.main_window, "Port manquant", "Veuillez saisir un port série.")
            return

        self._reset_buffers()
        self._worker = JulaboWorker(port=port, baudrate=_DEFAULT_BAUDRATE,
                                    poll_interval_ms=_DEFAULT_POLL_MS)
        self._thread = QtCore.QThread(self)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.connected.connect(self._on_worker_connected)
        self._worker.new_data.connect(self._on_new_data)
        self._worker.error.connect(self._on_worker_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.finished.connect(self._on_thread_finished)

        self._setpoint_requested.connect(self._worker.set_setpoint)
        self._start_requested.connect(self._worker.start_julabo)
        self._stop_requested.connect(self._worker.stop_julabo)

        self.ui.btnConnect.setEnabled(False)
        self.ui.linePort.setEnabled(False)
        self._thread.start()

    def _on_disconnect(self):
        if self._worker:
            self._worker.stop()
        if self._thread:
            self._thread.quit()
            self._thread.wait(3000)

    @QtCore.Slot(bool)
    def _on_worker_connected(self, ok: bool):
        if ok:
            self._is_connected = True
            self._set_led(True)
            self.ui.lblConnStatus.setText(
                f"Connecté — {self.ui.linePort.text()} @ {_DEFAULT_BAUDRATE} baud"
            )
            self.ui.btnDisconnect.setEnabled(True)
            self.ui.btnApplySp.setEnabled(True)
            self.ui.btnStart.setEnabled(True)
            self.ui.btnStop.setEnabled(True)
            self._save_settings()
        else:
            self._restore_disconnected_ui()

    def _on_thread_finished(self):
        self._worker = self._thread = None
        self._is_connected = False
        self._restore_disconnected_ui()

    def _restore_disconnected_ui(self):
        self._set_led(False)
        self.ui.lblConnStatus.setText("Déconnecté")
        self.ui.btnConnect.setEnabled(True)
        self.ui.btnDisconnect.setEnabled(False)
        self.ui.btnApplySp.setEnabled(False)
        self.ui.btnStart.setEnabled(False)
        self.ui.btnStop.setEnabled(False)
        self.ui.linePort.setEnabled(True)
        for lbl in self._value_labels:
            lbl.setText("—")

    def _display_period_s(self) -> float:
        """Période (en secondes) entre deux points du graphe, synchronisée sur
        les paramètres « points affichés » de l'onglet Sauermann (spinBlocSec +
        comboDispUnit). Reprend EXACTEMENT la formule de _effective_bloc_sec()
        de SauermannController, de sorte que les deux graphes affichent des
        points à la même cadence (ex. 1 point/min → 60 s)."""
        try:
            rate     = float(self.ui.spinBlocSec.value())
            unit_idx = self.ui.comboDispUnit.currentIndex()   # 0 = par sec, 1 = par min
        except Exception:
            return 1.0   # repli : cadence 1 s si les widgets Sauermann sont absents
        blocks_per_sec = rate if unit_idx == 0 else rate / 60.0
        return 1.0 / blocks_per_sec if blocks_per_sec > 0 else 1.0

    @QtCore.Slot(float, object, object, object, object, object, object)
    def _on_new_data(self, t, t_int, t_ext, pressure, pump_speed, level, setpoint):
        def fmt(v, decimals=2):
            return f"{v:.{decimals}f}" if v is not None else "ERR"

        # Valeurs numériques : rafraîchies à CHAQUE poll (temps réel).
        self.ui.lblTInt.setText(fmt(t_int))
        self.ui.lblTExt.setText(fmt(t_ext))
        self.ui.lblPressure.setText(fmt(pressure))
        self.ui.lblPumpSpeed.setText(fmt(pump_speed))
        self.ui.lblLevel.setText(fmt(level))
        self.ui.lblSetpoint.setText(fmt(setpoint))

        # Graphe : on n'ajoute un point QUE si la période d'affichage (calée sur
        # l'onglet Sauermann) est écoulée depuis le dernier point tracé. La
        # période est relue à chaque appel → un changement de « points affichés »
        # est pris en compte immédiatement.
        period = self._display_period_s()
        if self._last_graph_t is None or (t - self._last_graph_t) >= period - 1e-6:
            self._last_graph_t = t
            self._t_buf.append(t)
            self._tint_buf.append(t_int if t_int is not None else float('nan'))
            self._text_buf.append(t_ext if t_ext is not None else float('nan'))
            self._tsp_buf.append(setpoint  if setpoint  is not None else float('nan'))
            self._refresh_plots()

            # Émission vers le dashboard DANS la porte de décimation : la courbe
            # Julabo du dashboard reçoit ainsi un point à la même cadence que le
            # graphe de l'onglet Julabo (et que les voies Sauermann), au lieu
            # d'un point par poll (~1/s). Les libellés numériques, eux, restent
            # rafraîchis à chaque poll (plus haut dans la méthode).
            self.data_ready.emit(t_int, t_ext, setpoint)

    def _refresh_plots(self):
        if len(self._t_buf) == 0:
            return

        t    = np.array(self._t_buf,    dtype=float)
        yint = np.array(self._tint_buf, dtype=float)
        yext = np.array(self._text_buf, dtype=float)

        ysp = np.array(self._tsp_buf, dtype=float)
        self._curve_int.setData(t, yint)
        self._curve_ext.setData(t, yext)
        self._curve_sp.setData(t, ysp)

        if t.size > 1:
            right = t[-1]
            left  = max(right - self.ui.spinWindow.value() * 60.0, t[0])
            self._plot_ext.setXRange(left, right, padding=0.0)

        finite_ext = yext[np.isfinite(yext)]
        finite_sp  = ysp[np.isfinite(ysp)]
        all_left   = np.concatenate([finite_ext, finite_sp]) if finite_sp.size > 0 else finite_ext
        if all_left.size > 0:
            ymin, ymax = float(all_left.min()), float(all_left.max())
            if (ymax - ymin) < 1.0:
                center = (ymax + ymin) / 2.0
                ymin, ymax = center - 0.5, center + 0.5
            self._plot_ext.getViewBox().setYRange(ymin, ymax, padding=0.05)

        finite_int = yint[np.isfinite(yint)]
        if finite_int.size > 0:
            ymin, ymax = float(finite_int.min()), float(finite_int.max())
            if (ymax - ymin) < 1.0:
                center = (ymax + ymin) / 2.0
                ymin, ymax = center - 0.5, center + 0.5
            self._vb_int.setYRange(ymin, ymax, padding=0.05)

    @QtCore.Slot()
    def _on_apply_setpoint(self):
        if self._worker and self._is_connected:
            self._setpoint_requested.emit(self.ui.spinSetpoint.value())

    @QtCore.Slot()
    def _on_start(self):
        if self._worker and self._is_connected:
            self._start_requested.emit()

    @QtCore.Slot()
    def _on_stop(self):
        if self._worker and self._is_connected:
            self._stop_requested.emit()

    @QtCore.Slot(int)
    def _on_window_changed(self, minutes: int):
        poll_s  = _DEFAULT_POLL_MS / 1000.0
        new_max = max(int(minutes * 60.0 / poll_s) + 10, 50)
        self._max_pts  = new_max
        self._t_buf    = deque(self._t_buf,    maxlen=new_max)
        self._tint_buf = deque(self._tint_buf, maxlen=new_max)
        self._text_buf = deque(self._text_buf, maxlen=new_max)
        self._tsp_buf  = deque(self._tsp_buf,  maxlen=new_max)
        self._refresh_plots()

    def _reset_buffers(self):
        self._t_buf.clear()
        self._tint_buf.clear()
        self._text_buf.clear()
        self._curve_int.setData([], [])
        self._curve_ext.setData([], [])
        self._tsp_buf.clear()
        self._curve_sp.setData([], [])

    @QtCore.Slot(str)
    def _on_worker_error(self, msg: str):
        self.ui.lblConnStatus.setText(f"Erreur : {msg}")
        self.led_changed.emit("#E74C3C")   # erreur → rouge

    def cleanup(self):
        self._on_disconnect()

    def _settings(self) -> QSettings:
        return QSettings("SIC320", "USB6003_Monitor")

    def _load_settings(self):
        s = self._settings()
        self.ui.linePort.setText(s.value("julabo/port", "COM8"))
        self.ui.spinWindow.setValue(int(s.value("julabo/window_min", 30)))

    def _save_settings(self):
        s = self._settings()
        s.setValue("julabo/port",       self.ui.linePort.text())
        s.setValue("julabo/window_min", int(self.ui.spinWindow.value()))


# =============================================================================
# ██████  SAUERMANN
# =============================================================================

def _convert_0_10(v, out_min, out_max):
    return out_min + (np.clip(v, 0.0, 10.0) / 10.0) * (out_max - out_min)


class AcqWorker(QtCore.QObject):
    new_block = QtCore.Signal(np.ndarray, float)
    synced    = QtCore.Signal(float)
    finished  = QtCore.Signal()
    error     = QtCore.Signal(str)

    def __init__(self, device="dev1", first_ai=0, nb_voies=4,
                 fs=20.0, bloc_sec=0.5, vmin=0.0, vmax=10.0, sync_unit="s"):
        super().__init__()
        self.device    = device
        self.first_ai  = first_ai
        self.nb_voies  = nb_voies
        self.fs        = float(fs)
        self.bloc_sec  = float(bloc_sec)
        self.bloc      = max(int(self.fs * self.bloc_sec), 10)
        self.vmin      = vmin
        self.vmax      = vmax
        self.sync_unit = sync_unit
        self._stop     = False
        self._task     = None

    @QtCore.Slot()
    def run(self):
        if nidaqmx is None:
            self.error.emit(f"nidaqmx introuvable : {str(_nidaqmx_import_error)}")
            self.finished.emit()
            return

        now    = time.time()
        period = 60.0 if self.sync_unit == "min" else 1.0
        delay  = period - (now % period)
        if delay < 0.01:
            delay += period
        t_ref = round((now + delay) / period) * period
        time.sleep(delay)
        self.synced.emit(t_ref)

        chans = f"{self.device}/ai{self.first_ai}:{self.first_ai + self.nb_voies - 1}"
        try:
            with nidaqmx.Task() as task:
                self._task = task
                task.ai_channels.add_ai_voltage_chan(
                    chans, terminal_config=TerminalConfiguration.DIFF,
                    min_val=self.vmin, max_val=self.vmax
                )
                task.timing.cfg_samp_clk_timing(
                    rate=self.fs, sample_mode=AcquisitionType.CONTINUOUS,
                    samps_per_chan=self.bloc
                )
                reader    = AnalogMultiChannelReader(task.in_stream)
                t_start   = t_ref
                bloc_idx  = 0
                while not self._stop:
                    buf     = np.zeros((self.nb_voies, self.bloc), dtype=np.float64)
                    timeout = self.bloc / self.fs + 1.0
                    reader.read_many_sample(buf, number_of_samples_per_channel=self.bloc,
                                            timeout=timeout)
                    t_block   = t_start + bloc_idx * (self.bloc / self.fs) + (self.bloc - 1) / self.fs
                    bloc_idx += 1
                    self.new_block.emit(buf, t_block)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self._task = None
            self.finished.emit()

    def stop(self):
        self._stop = True
        if self._task is not None:
            try:
                self._task.stop()
            except Exception:
                pass


class SauermannController(QtCore.QObject):
    """Onglet Sauermann — ex MainWindow."""

    # Signal émis à chaque nouveau bloc : vals corrigés [4], vals bruts [4]
    data_ready  = QtCore.Signal(list, list)
    led_changed = QtCore.Signal(str)   # couleur CSS : vert/rouge/gris

    # Capacité du tableau NumPy pré-alloué en mode 'fixed' (~11 jours @ 0.5 s/point)
    _FIXED_CAPACITY = 2_000_000

    def __init__(self, ui_instance: Ui_PolarisMainWindow, main_window: QMainWindow):
        super().__init__(main_window)
        self.ui = ui_instance
        self.main_window = main_window  # Référence à la fenêtre principale

        self.nb_voies           = 4
        self.current_mode       = 'fixed'
        self.follow_x           = True
        self.fixed_y            = [False] * self.nb_voies
        self.y_min              = [0.0,  0.0,   0.0,  0.0]
        self.y_max              = [3.0, 50.0, 100.0, 50.0]
        self.rolling_window_sec = 600.0
        self._updating_view     = False

        self.corr_mode = [0, 0, 0, 0]
        self.corr_a    = [1.0, 1.0, 1.0, 1.0]
        self.corr_b    = [0.0, 0.0, 0.0, 0.0]
        self.corr_c    = [0.0, 0.0, 0.0, 0.0]
        self.corr_d    = [0.0, 0.0, 0.0, 0.0]

        self.corr_mode_names = {
            0: "Aucune", 1: "Linéaire (ax + b)",
            2: "Quadratique (ax² + bx + c)", 3: "Cubique (ax³ + bx² + cx + d)",
        }

        self.param_names = ["Vitesse", "Température", "Humidité", "Pression"]
        self.param_units = ["m/s", "°C", "%RH", "Pa"]
        self.conv_min    = [0.0, 0.0,   0.0,  0.0]
        self.conv_max    = [3.0, 50.0, 100.0, 50.0]

        self.worker = None
        self.thread = None

        QtWidgets.QApplication.setStyle("Fusion")
        self._init_graph()
        self._init_logic()
        if hasattr(self.ui, "btnStopAcq"):
            self.ui.btnStopAcq.setEnabled(False)

        self._load_settings()
        self._apply_settings(apply_ranges=True)
        self._update_all_labels()
        self._apply_param_metadata_to_ui()
        self._rebuild_legends()

    def _safe_int(self, v, d=0):
        try:
            return int(v)
        except Exception:
            return d

    def _init_graph(self):
        self.colors = [(255, 165, 0), (231, 76, 60), (52, 152, 219), (46, 204, 113)]

        self.lblDate      = getattr(self.ui, "lblDate", None)
        self.btnStartRec  = getattr(self.ui, "btnStartRec", None)
        self.btnStopRec   = getattr(self.ui, "btnStopRec", None)
        self.lblRecStatus = getattr(self.ui, "lblRecStatus", None)
        self.lblRecLed    = getattr(self.ui, "lblRecLed", None)
        self.lblAcqLed    = getattr(self.ui, "lblAcqLed", None)
        if self.lblAcqLed is not None:
            self.lblAcqLed.setStyleSheet("border:1px solid #888; border-radius:6px; background:#bbb;")

        self.lblValues     = [getattr(self.ui, f"lblValue{i}")     for i in range(4)]
        self.lblValuesCorr = [getattr(self.ui, f"lblValueCorr{i}") for i in range(4)]
        self.btnColors     = [getattr(self.ui, f"btnColor{i}")     for i in range(4)]

        self.btnFollow = self.ui.btnFollow
        self.btnFollow.setCheckable(True)
        self.btnFollow.setChecked(True)
        self.btnFollow.setToolTip("Suivre automatiquement le défilement")
        self.btnFollow.toggled.connect(self._on_toggle_follow)

        self.graph_widget = pg.GraphicsLayoutWidget()
        self.graph_widget.setBackground('w')
        lay = QtWidgets.QVBoxLayout(self.ui.plotContainerMain)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.graph_widget)

        self.plots      = []
        self.curves     = []
        self.crosshairs = []
        self.legends    = []

        index = 0
        for row in range(2):
            for col in range(2):
                p = self.graph_widget.addPlot(
                    row=row, col=col,
                    axisItems={'bottom': DateAxis(orientation='bottom')}
                )
                p.showGrid(x=True, y=True, alpha=0.3)
                p.setLabel("left", "")

                curve = p.plot(
                    pen=pg.mkPen(self.colors[index], width=2),
                    name=f"{self.param_names[index]} ({self.param_units[index]})"
                )
                # Downsampling auto 'peak' + découpage à la vue : indispensable pour
                # afficher de très longues acquisitions sans geler l'interface.
                curve.setDownsampling(auto=True, method='peak')
                curve.setClipToView(True)

                vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen("#666", width=1))
                hline = pg.InfiniteLine(angle=0,  movable=False, pen=pg.mkPen("#666", width=1))
                p.addItem(vline, ignoreBounds=True)

                legend = p.addLegend()
                legend.clear()
                legend.addItem(curve, curve.name())

                self.plots.append(p)
                self.curves.append(curve)
                self.crosshairs.append((vline, hline))
                self.legends.append(legend)
                index += 1

        self.graph_widget.scene().sigMouseMoved.connect(self._on_mouse_moved)

        self.t_buffer  = []
        self.y_buffers = [[] for _ in range(4)]

        for i in range(4):
            self._apply_button_color(i)

    def _rebuild_legends(self):
        for i in range(4):
            self.legends[i].clear()
            self.legends[i].addItem(self.curves[i],
                                    f"{self.param_names[i]} ({self.param_units[i]})")

    def _setup_storage(self, mode):
        self.current_mode = mode
        if mode == 'rolling':
            bloc_sec = max(float(self._effective_bloc_sec()), 0.1)
            max_pts  = max(int(self.rolling_window_sec / bloc_sec) + 5, 50)
            self.t_buffer  = deque(maxlen=max_pts)
            self.y_buffers = [deque(maxlen=max_pts) for _ in range(4)]
        else:
            # Mode 'fixed' : tableaux NumPy pré-alloués (remplis de NaN pour ne rien
            # tracer tant que les cases ne sont pas écrites) + pointeur d'index.
            self.t_buffer  = np.full(self._FIXED_CAPACITY, np.nan, dtype=float)
            self.y_buffers = [np.full(self._FIXED_CAPACITY, np.nan, dtype=float)
                              for _ in range(4)]
            self.ptr       = 0

        for c in self.curves:
            c.setData([], [])
        self.ui.lblCross.setText("—")

    def _init_logic(self):
        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self._update_time)
        self.clock_timer.start()
        self._update_time()

        for i in range(4):
            self.btnColors[i].clicked.connect(lambda _, idx=i: self._choose_color(idx))

        self.csv_file        = None
        self.csv_writer      = None
        self.csv_meta_file   = None
        self.csv_meta_writer = None
        self.csv_manager     = None   # gestionnaire CSV global (défini par MainApp)
        self.meta_calib_start  = None
        self.meta_calib_active = False
        self.meta_bloc_counter = 0
        self._pending_csv_path  = None
        self._pending_meta_path = None

        # Enregistrement CSV désormais centralisé et piloté depuis l'onglet
        # Dashboard (boutons « Start CSV » / « Stop CSV »). Les boutons locaux,
        # s'ils existent encore dans l'IHM, sont neutralisés.
        for _b in (self.btnStartRec, self.btnStopRec):
            if _b is not None:
                _b.setEnabled(False)
                _b.setToolTip("Enregistrement piloté depuis l'onglet Dashboard")

        self.ui.btnSaveImage.clicked.connect(self._save_graph_image)

        for i in range(4):
            self.ui.__dict__[f"editName{i}"].textChanged.connect(self._update_all_labels)
            self.ui.__dict__[f"editUnit{i}"].textChanged.connect(self._update_all_labels)

        if hasattr(self.ui, "btnApplyParams"):
            self.ui.btnApplyParams.clicked.connect(self._apply_params)

        if hasattr(self.ui, "btnStopAcq"):
            self.ui.btnStopAcq.clicked.connect(self._stop_acquisition)

        self.ui.btnApplySettings.clicked.connect(
            lambda: self._apply_settings(apply_ranges=True, save=True)
        )

    def _update_time(self):
        if self.lblDate is not None:
            self.lblDate.setText(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    def _choose_color(self, idx):
        col = QColorDialog.getColor(QtGui.QColor(*self.colors[idx]), self.main_window, "Couleur du tracé")
        if col.isValid():
            self.colors[idx] = (col.red(), col.green(), col.blue())
            self.curves[idx].setPen(pg.mkPen(self.colors[idx], width=2))
            self._apply_button_color(idx)
            self._refresh_plot()

    def _apply_button_color(self, idx):
        r, g, b = self.colors[idx]
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        fg  = "white" if lum < 140 else "black"
        btn = self.btnColors[idx]
        btn.setStyleSheet(
            f"QPushButton#btnColor{idx} {{"
            f" background-color: rgb({r},{g},{b}); color: {fg}; border: 1px solid #888; }}"
        )

    def _effective_fs(self) -> float:
        fs_val   = float(self.ui.spinFs.value())
        unit_idx = self.ui.comboFsUnit.currentIndex()
        return max(fs_val if unit_idx == 0 else fs_val / 60.0, 0.1)

    def _effective_bloc_sec(self) -> float:
        rate      = float(self.ui.spinBlocSec.value())
        unit_idx  = self.ui.comboDispUnit.currentIndex()
        blocks_per_sec = rate if unit_idx == 0 else rate / 60.0
        return 1.0 / blocks_per_sec if blocks_per_sec > 0 else 0.5

    def _start_acquisition(self):
        if self.thread is not None and self.thread.isRunning():
            return
        fs        = self._effective_fs()
        bloc_sec  = self._effective_bloc_sec()
        sync_unit = "min" if self.ui.comboDispUnit.currentIndex() == 1 else "s"

        self.worker = AcqWorker(device="dev1", first_ai=0, nb_voies=4,
                                fs=fs, bloc_sec=bloc_sec,
                                vmin=0.0, vmax=10.0, sync_unit=sync_unit)
        self.thread = QtCore.QThread(self)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.synced.connect(self._on_worker_synced)
        self.worker.new_block.connect(self._on_new_block)
        self.worker.error.connect(self._on_acq_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

        if hasattr(self.ui, "btnStopAcq"):
            self.ui.btnStopAcq.setEnabled(True)
        if hasattr(self.ui, "btnApplyParams"):
            self.ui.btnApplyParams.setEnabled(False)
        # Verrouillage de sécurité : on bloque l'accès aux paramètres de graphe
        # (fréquence d'échantillonnage, nombre de points, mode de graphe…),
        # regroupés dans le QGroupBox « groupAcq », pour empêcher toute
        # modification en pleine acquisition. Réactivé dans _stop_acquisition.
        # NB : l'onglet des réglages « tabSettings » n'est PAS verrouillé ici ;
        # il l'est uniquement pendant l'enregistrement CSV (start_csv_external /
        # _stop_csv), et non au simple démarrage de l'acquisition.
        if hasattr(self.ui, "groupAcq"):
            self.ui.groupAcq.setEnabled(False)
        if self.lblAcqLed is not None:
            self.lblAcqLed.setStyleSheet(
                "border:1px solid #888; border-radius:6px; background:#2ECC71;"
            )
        self.led_changed.emit("#2ECC71")   # acquisition active → vert

    def _stop_acquisition(self):
        if self.worker:
            self.worker.stop()
        if self.thread:
            try:
                self.thread.quit()
                self.thread.wait(2000)
            except Exception:
                pass
        self.worker = None
        self.thread = None
        if hasattr(self.ui, "btnStopAcq"):
            self.ui.btnStopAcq.setEnabled(False)
        if hasattr(self.ui, "btnApplyParams"):
            self.ui.btnApplyParams.setEnabled(True)
        # Déverrouillage : l'acquisition est arrêtée, on rend de nouveau les
        # paramètres de graphe (groupAcq) accessibles — symétrique de
        # _start_acquisition. L'onglet « tabSettings » n'est pas touché ici : il
        # est géré par le flux d'enregistrement CSV.
        if hasattr(self.ui, "groupAcq"):
            self.ui.groupAcq.setEnabled(True)
        if self.lblAcqLed is not None:
            self.lblAcqLed.setStyleSheet(
                "border:1px solid #888; border-radius:6px; background:#bbb;"
            )
        self.led_changed.emit("#bbb")      # acquisition arrêtée → gris

    def _apply_params(self):
        new_mode = 'rolling' if self.ui.comboGraphMode.currentIndex() == 1 else 'fixed'
        unit_idx = self.ui.comboRollingUnit.currentIndex()
        factor   = {0: 1.0, 1: 60.0}.get(unit_idx, 3600.0)
        self.rolling_window_sec = float(self.ui.spinRollingSec.value()) * factor

        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
            self.thread.wait()
        self.thread = None
        self.worker = None

        self._setup_storage(new_mode)
        self._start_acquisition()
        self.main_window.statusBar().showMessage("Paramètres appliqués", 2000)
        if self.follow_x:
            self._scroll_to_live()
        self._save_settings()

    @QtCore.Slot(np.ndarray, float)
    def _on_new_block(self, data, t_block):
        if self._pending_meta_path is not None:
            n_samples = data.shape[1]
            fs        = self._effective_fs()
            t_first   = t_block - (n_samples - 1) / fs
            self._on_worker_synced(t_first)

        v        = [_convert_0_10(data[i], float(self.conv_min[i]), float(self.conv_max[i]))
                    for i in range(4)]
        raw_vals = [float(np.nanmean(v[i])) for i in range(4)]

        vals = []
        for i in range(4):
            y = raw_vals[i]
            mode = int(self.corr_mode[i])
            a, b, c, d = (float(x[i]) for x in (self.corr_a, self.corr_b, self.corr_c, self.corr_d))
            if mode == 1: y = a * y + b
            elif mode == 2: y = a * y**2 + b * y + c
            elif mode == 3: y = a * y**3 + b * y**2 + c * y + d
            vals.append(float(y))

        for i in range(4):
            self.lblValues[i].setText(f"{raw_vals[i]:.2f}")
            if self.corr_mode[i] == 0:
                self.lblValuesCorr[i].setText("")
            else:
                self.lblValuesCorr[i].setText(f"{vals[i]:.2f}")

        self._append_point(t_block, vals)

        # Signal vers le dashboard
        self.data_ready.emit(vals, raw_vals)

        if self.meta_calib_active and self.csv_meta_writer:
            if self.meta_calib_start is None:
                self.meta_calib_start = t_block
            elapsed = t_block - self.meta_calib_start
            if elapsed <= 60.0:
                self.meta_bloc_counter += 1
                bloc_num  = self.meta_bloc_counter
                n_samples = data.shape[1]
                fs        = self._effective_fs()
                t_first   = t_block - (n_samples - 1) / fs
                for s in range(n_samples):
                    t_s   = t_first + s / fs
                    ts_s  = datetime.fromtimestamp(t_s).strftime('%Y/%m/%d %H:%M:%S.%f')[:-3]
                    row_s = [bloc_num, s + 1, ts_s]
                    for i in range(4):
                        raw_s = float(v[i][s])
                        y     = raw_s
                        mode  = int(self.corr_mode[i])
                        a, b, c, d = (float(x[i]) for x in
                                      (self.corr_a, self.corr_b, self.corr_c, self.corr_d))
                        if mode == 1: y = a * y + b
                        elif mode == 2: y = a * y**2 + b * y + c
                        elif mode == 3: y = a * y**3 + b * y**2 + c * y + d
                        row_s.append(f"{raw_s:.6f}".replace('.', ','))
                        row_s.append(f"{y:.6f}".replace('.', ',') if mode != 0 else "")
                    for i in range(4):
                        if s == 0:
                            row_s.append(f"{raw_vals[i]:.6f}".replace('.', ','))
                            row_s.append(f"{vals[i]:.6f}".replace('.', ',')
                                         if self.corr_mode[i] != 0 else "")
                        else:
                            row_s += ["", ""]
                    self.csv_meta_writer.writerow(row_s)
                self.csv_meta_file.flush()
            else:
                self.meta_calib_active = False

        # Fichier de mesures global (acq_polaris) : une ligne par bloc Sauermann.
        # Le CsvManager y ajoute les colonnes Bronkhorst/Julabo (valeur fraîche ou
        # vide selon la période du bloc).
        if self.csv_manager is not None and self.csv_manager.is_active:
            bloc_sec = max(float(self._effective_bloc_sec()), 1e-3)
            # data.shape[1] = nombre d'échantillons lus par la carte NI-DAQ sur
            # ce bloc (compteur « nb_val_voieX » du CSV).
            self.csv_manager.write_block_row(
                t_block, raw_vals, vals, self.corr_mode, bloc_sec,
                n_sau=int(data.shape[1]))

    def _valid_view(self):
        """Retourne (t_valide, [y0..y3]) selon le mode de stockage courant.

        - Mode 'fixed' : tranche [:ptr] des tableaux NumPy pré-alloués (zéro copie).
        - Mode 'rolling' / état initial : conversion du deque/liste en tableau NumPy.
        """
        if isinstance(self.t_buffer, np.ndarray):
            n  = getattr(self, 'ptr', 0)
            t  = self.t_buffer[:n]
            ys = [yb[:n] for yb in self.y_buffers]
            return t, ys
        t  = np.asarray(self.t_buffer, dtype=float)
        ys = [np.asarray(yb, dtype=float) for yb in self.y_buffers]
        return t, ys

    def _append_point(self, t_point, y_points):
        if isinstance(self.t_buffer, np.ndarray):
            # Mode 'fixed' : insertion directe à l'index courant (pas de réallocation).
            if self.ptr >= self._FIXED_CAPACITY:
                # Sécurité tableau plein : on décale d'un bloc (anneau) pour libérer
                # de la place tout en conservant l'historique le plus récent.
                shift = max(self._FIXED_CAPACITY // 10, 1)
                self.t_buffer = np.roll(self.t_buffer, -shift)
                self.t_buffer[-shift:] = np.nan
                for i in range(4):
                    self.y_buffers[i] = np.roll(self.y_buffers[i], -shift)
                    self.y_buffers[i][-shift:] = np.nan
                self.ptr -= shift
            self.t_buffer[self.ptr] = float(t_point)
            for i in range(4):
                self.y_buffers[i][self.ptr] = float(y_points[i])
            self.ptr += 1
        else:
            # Mode 'rolling' (ou état initial) : deque/liste.
            self.t_buffer.append(float(t_point))
            for i in range(4):
                self.y_buffers[i].append(float(y_points[i]))
        self._refresh_plot()

    def _refresh_plot(self):
        t, ys = self._valid_view()
        if t.size == 0:
            return

        if self.follow_x and t.size > 0:
            right = t[-1]
            left  = (max(right - self.rolling_window_sec, t[0])
                     if self.current_mode == 'rolling' else t[0])
            self._updating_view = True
            try:
                for p in self.plots:
                    p.setXRange(left, right, padding=0.0)
            finally:
                self._updating_view = False

        for i in range(4):
            y = ys[i]
            self.curves[i].setVisible(y.size > 0)
            self.plots[i].getAxis("left").setVisible(True)
            if y.size > 0:
                self.curves[i].setData(t, y)
                if self.fixed_y[i]:
                    ymin = float(self.y_min[i])
                    ymax = float(self.y_max[i])
                    if ymin >= ymax:
                        ymax = ymin + 1e-3
                        self.y_max[i] = ymax
                        spin = getattr(self.ui, f"spinYMax{i}")
                        spin.blockSignals(True)
                        spin.setValue(ymax)
                        spin.blockSignals(False)
                    vb = self.plots[i].getViewBox()
                    self._updating_view = True
                    try:
                        vb.setYRange(ymin, ymax, padding=0)
                    finally:
                        self._updating_view = False
                else:
                    if np.isfinite(y).any():
                        ymin, ymax = float(np.nanmin(y)), float(np.nanmax(y))
                        if ymin == ymax:
                            pad   = 0.5 if ymax == 0 else abs(ymax) * 0.05
                            ymin -= pad
                            ymax += pad
                        vb = self.plots[i].getViewBox()
                        self._updating_view = True
                        try:
                            vb.setYRange(ymin, ymax, padding=0)
                        finally:
                            self._updating_view = False
            else:
                self.curves[i].setData([], [])

    def _on_mouse_moved(self, pos):
        t, ys = self._valid_view()
        for i, p in enumerate(self.plots):
            if p.sceneBoundingRect().contains(pos):
                mp          = p.vb.mapSceneToView(pos)
                x           = mp.x()
                vline, hline = self.crosshairs[i]
                vline.setPos(x)
                if t.size > 1:
                    idx = int(np.clip(np.searchsorted(t, x), 0, t.size - 1))
                    if idx > 0 and abs(t[idx] - x) > abs(t[idx - 1] - x):
                        idx -= 1
                    if (idx < ys[i].size
                            and np.isfinite(t[idx]) and np.isfinite(ys[i][idx])):
                        val    = float(ys[i][idx])
                        dt_str = datetime.fromtimestamp(float(t[idx])).strftime("%d/%m %H:%M")
                        self.ui.lblCross.setText(
                            f"{dt_str}  |  {self.param_names[i]} : {val:.2f} {self.param_units[i]}"
                        )
                    else:
                        self.ui.lblCross.setText("—")
                return
        self.ui.lblCross.setText("—")

    def _on_toggle_follow(self, checked: bool):
        self.follow_x = checked
        if checked:
            self._scroll_to_live()

    def _scroll_to_live(self):
        t, _ = self._valid_view()
        if t.size < 2:
            return
        right = t[-1]
        left  = (max(right - self.rolling_window_sec, t[0])
                 if self.current_mode == 'rolling' else t[0])
        self._updating_view = True
        try:
            for p in self.plots:
                p.setXRange(left, right, padding=0.0)
        finally:
            self._updating_view = False

    def _apply_settings(self, apply_ranges: bool = True, save: bool = False):
        for i in range(4):
            chk    = getattr(self.ui, f"chkYFix{i}")
            sp_min = getattr(self.ui, f"spinYMin{i}")
            sp_max = getattr(self.ui, f"spinYMax{i}")
            self.fixed_y[i] = chk.isChecked()
            self.y_min[i]   = float(sp_min.value())
            self.y_max[i]   = float(sp_max.value())

            cmb  = getattr(self.ui, f"comboCorr{i}")
            sp_a = getattr(self.ui, f"spinCorrA{i}")
            sp_b = getattr(self.ui, f"spinCorrB{i}")
            sp_c = getattr(self.ui, f"spinCorrC{i}")
            sp_d = getattr(self.ui, f"spinCorrD{i}")
            self.corr_mode[i] = int(cmb.currentIndex())
            self.corr_a[i]    = float(sp_a.value())
            self.corr_b[i]    = float(sp_b.value())
            self.corr_c[i]    = float(sp_c.value())
            self.corr_d[i]    = float(sp_d.value())

            ed_name = getattr(self.ui, f"editName{i}")
            ed_unit = getattr(self.ui, f"editUnit{i}")
            sp_cmin = getattr(self.ui, f"spinConvMin{i}")
            sp_cmax = getattr(self.ui, f"spinConvMax{i}")
            self.param_names[i] = ed_name.text().strip() or self.param_names[i]
            self.param_units[i] = ed_unit.text().strip() or self.param_units[i]
            self.conv_min[i]    = float(sp_cmin.value())
            self.conv_max[i]    = float(sp_cmax.value())

        self.current_mode       = 'rolling' if self.ui.comboGraphMode.currentIndex() == 1 else 'fixed'
        self.rolling_window_sec = float(self.ui.spinRollingSec.value()) * (
            60.0 if self.ui.comboRollingUnit.currentIndex() == 1 else 1.0
        )

        for i in range(4):
            self.plots[i].setLabel("left", "")
        self._rebuild_legends()

        for i in range(4):
            lbl_corr  = getattr(self.ui, f"lblName{i}_2")
            val_corr  = getattr(self.ui, f"lblValueCorr{i}")
            unit_corr = getattr(self.ui, f"lblUnit{i}_2")
            if self.corr_mode[i] == 0:
                lbl_corr.hide(); val_corr.hide(); unit_corr.hide()
            else:
                lbl_corr.show(); val_corr.show(); unit_corr.show()
                lbl_corr.setText(f"{self.param_names[i]} corrigé :")

        if apply_ranges:
            self._refresh_plot()
        if save:
            self._save_settings()
        self.main_window.statusBar().showMessage("Réglages appliqués", 2000)

    def _apply_param_metadata_to_ui(self):
        for i in range(4):
            grp      = getattr(self.ui, f"group{i}")
            lbl_name = getattr(self.ui, f"lblName{i}")
            lbl_unit = getattr(self.ui, f"lblUnit{i}")
            grp.setTitle(f"{self.param_names[i]} ({self.param_units[i]})")
            lbl_name.setText(f"{self.param_names[i]} :")
            lbl_unit.setText(self.param_units[i])
            getattr(self.ui, f"lblName{i}_2").setText(f"{self.param_names[i]} corrigé :")
        for i in range(4):
            if hasattr(self.ui, f"lblVoie{i}"):
                getattr(self.ui, f"lblVoie{i}").setText(self.param_names[i])
            if hasattr(self.ui, f"lblCVoie{i}"):
                getattr(self.ui, f"lblCVoie{i}").setText(self.param_names[i])
            self.plots[i].setLabel("left", "")

    def _update_all_labels(self):
        for i in range(4):
            txtn = self.ui.__dict__[f"editName{i}"].text().strip()
            txtu = self.ui.__dict__[f"editUnit{i}"].text().strip()
            if txtn: self.param_names[i] = txtn
            if txtu: self.param_units[i] = txtu
        self._apply_param_metadata_to_ui()
        self._rebuild_legends()

    def _save_graph_image(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main_window, "Exporter le graphe", "graphe.png", "Images (*.png)"
        )
        if not path:
            return
        try:
            pix = self.graph_widget.grab()
            pix.save(path, 'PNG')
            self.main_window.statusBar().showMessage(f"Image enregistrée : {os.path.basename(path)}", 3000)
        except Exception as e:
            QMessageBox.critical(self.main_window, "Export image", f"Échec de l'enregistrement : {e}")

    def _set_rec_led(self, on: bool):
        if self.lblRecLed is None:
            return
        style = ("border:1px solid #888; border-radius:6px; background:#2ecc71;"
                 if on else "border:1px solid #888; border-radius:6px; background:#bbb;")
        self.lblRecLed.setStyleSheet(style)

    def _set_rec_status(self, text: str):
        """Met à jour le libellé de statut d'enregistrement s'il existe encore."""
        if self.lblRecStatus is not None:
            self.lblRecStatus.setText(text)

    def start_csv_external(self, meta_path: str):
        """Démarre l'enregistrement des MÉTADONNÉES Sauermann (fichier inchangé),
        déclenché par le gestionnaire CSV centralisé. Le fichier de mesures global
        (acq_polaris) est géré par le CsvManager ; ici on ne s'occupe que des
        métadonnées, dont l'ouverture est différée au prochain bord de bloc pour
        conserver la synchronisation temporelle existante."""
        if self.csv_meta_writer or self._pending_meta_path:
            return
        self._pending_meta_path = meta_path
        self._set_rec_status("En attente du prochain bord de seconde/minute…")
        self.ui.tabSettings.setEnabled(False)

    def stop_csv_external(self):
        """Arrêt déclenché par le gestionnaire CSV centralisé (Dashboard)."""
        self._stop_csv()

    @QtCore.Slot(float)
    def _on_worker_synced(self, t_ref: float):
        if not self._pending_meta_path:
            return
        meta_path = self._pending_meta_path
        self._pending_meta_path = None
        try:
            self._start_metadata_csv(meta_path, t_ref)
            self._set_rec_status(f"Enregistrement : actif → {os.path.basename(meta_path)}")
            self._set_rec_led(True)
        except Exception as e:
            QMessageBox.critical(self.main_window, "Erreur CSV", str(e))

    def _stop_csv(self):
        self._pending_csv_path  = None
        self._pending_meta_path = None
        self.ui.tabSettings.setEnabled(True)

        if self.csv_meta_file:
            try:
                self.csv_meta_file.close()
            except Exception:
                pass
            self.csv_meta_file   = None
            self.csv_meta_writer = None
        self.meta_calib_active = False

        self._set_rec_status("Enregistrement : inactif")
        self._set_rec_led(False)

    def _start_metadata_csv(self, path, t_ref: float = None):
        self.csv_meta_file   = open(path, "w", newline="", encoding="utf-8")
        self.csv_meta_writer = csv.writer(self.csv_meta_file, delimiter=';')

        fs_val        = float(self.ui.spinFs.value())
        bl_val        = float(self.ui.spinBlocSec.value())
        fs_unit_label = "mesures/min" if self.ui.comboFsUnit.currentIndex() == 1 else "mesures/s"
        bl_unit_label = "par min" if self.ui.comboDispUnit.currentIndex() == 1 else "par sec"
        ts_debut = (datetime.fromtimestamp(t_ref).strftime("%Y/%m/%d %H:%M:%S")
                    if t_ref is not None else datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

        self.csv_meta_writer.writerow(["Date début acquisition", ts_debut])
        self.csv_meta_writer.writerow(["Fréquence échantillonnage : ", f"{fs_val:.4g} {fs_unit_label}"])
        self.csv_meta_writer.writerow(["Points affichés : ", f"{bl_val:.4g} {bl_unit_label}"])
        self.csv_meta_writer.writerow([])

        # Liste des RDMs Bronkhorst en acquisition, insérée AVANT la section des
        # voies analogiques. Les nœuds acquis sont les tuiles actives ; nom,
        # fluide, capacité et unité sont lus dans scanned_devices (paramètres
        # P115 / P25 / P21 / P129 relevés au scan).
        bro = getattr(self.main_window, "bronkhorst_ctrl", None)
        self.csv_meta_writer.writerow(["RDMs (débitmètres Bronkhorst)"])
        self.csv_meta_writer.writerow(["Nœud", "Nom", "Fluide", "Capacité", "Unité"])
        tiles = getattr(bro, "tiles", None) if bro is not None else None
        if tiles:
            scanned = getattr(bro, "scanned_devices", {}) or {}
            for addr in sorted(tiles.keys()):
                info = scanned.get(addr, {})
                self.csv_meta_writer.writerow([
                    addr,
                    info.get("model", "?"),
                    info.get("fluid", "?"),
                    info.get("capacity", "?"),
                    info.get("unit", "?"),
                ])
        else:
            self.csv_meta_writer.writerow(["(aucun)"])
        self.csv_meta_writer.writerow([])

        # Paramètres PID actuels (lus dans l'onglet PID via l'UI partagée).
        def _uiv(name, default=""):
            w = getattr(self.ui, name, None)
            if w is None:
                return default
            try:
                return w.value()
            except Exception:
                try:
                    return w.currentText()
                except Exception:
                    return default
        try:
            pid_active = self.ui.chkPidActive.isChecked()
        except Exception:
            pid_active = False
        self.csv_meta_writer.writerow(["Régulation PID (paramètres actuels)"])
        self.csv_meta_writer.writerow(["État", "Active" if pid_active else "Inactive"])
        self.csv_meta_writer.writerow(["Kp", _uiv("spinPidKp")])
        self.csv_meta_writer.writerow(["Ki", _uiv("spinPidKi")])
        self.csv_meta_writer.writerow(["Kd", _uiv("spinPidKd")])
        self.csv_meta_writer.writerow(["Consigne (cible HR)", _uiv("spinPidConsigne")])
        self.csv_meta_writer.writerow(["Période de boucle (s)", _uiv("spinPidLoop")])
        self.csv_meta_writer.writerow(["Voie d'entrée (HR)", _uiv("comboPidVoie")])
        self.csv_meta_writer.writerow(["Adresse RDM (sortie)", _uiv("spinPidAddr")])
        self.csv_meta_writer.writerow([])

        self.csv_meta_writer.writerow([
            "Voie", "Nom", "Unité", "Conv min", "Conv max",
            "Correction mode", "Coeff A", "Coeff B", "Coeff C", "Coeff D"
        ])
        for i in range(4):
            self.csv_meta_writer.writerow([
                i, self.param_names[i], self.param_units[i],
                self.conv_min[i], self.conv_max[i],
                self.corr_mode_names.get(self.corr_mode[i], "Inconnu"),
                self.corr_a[i], self.corr_b[i], self.corr_c[i], self.corr_d[i],
            ])

        self.csv_meta_writer.writerow([])
        header = ["bloc", "n_echantillon", "timestamp"]
        for i in range(4):
            header += [f"{self.param_names[i]}({self.param_units[i]})",
                       f"{self.param_names[i]}({self.param_units[i]})_corr"]
        for i in range(4):
            header += [f"moyenne_brute_{self.param_names[i]}",
                       f"moyenne_corrigee_{self.param_names[i]}"]
        self.csv_meta_writer.writerow(header)
        self.csv_meta_file.flush()

        self.meta_calib_start  = None
        self.meta_calib_active = True
        self.meta_bloc_counter = 0

    def _on_acq_error(self, msg):
        QMessageBox.critical(self.main_window, "Erreur acquisition", msg)

    def cleanup(self):
        """Arrêt propre de tous les threads."""
        self._stop_acquisition()
        self._stop_csv()
        if hasattr(self, "clock_timer"):
            self.clock_timer.stop()
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(2000)
        self._save_settings()

    def _settings(self) -> QSettings:
        return QSettings("SIC320", "USB6003_Monitor")

    def _load_settings(self):
        s = self._settings()
        self.current_mode = s.value("graph/mode", "fixed")
        self.ui.comboGraphMode.setCurrentIndex(1 if self.current_mode == "rolling" else 0)
        self.rolling_window_sec = float(s.value("graph/rolling_sec", 600.0))

        ru     = self.ui.comboRollingUnit.currentIndex()
        factor = {0: 1.0, 1: 60.0}.get(ru, 3600.0)
        self.ui.spinRollingSec.setValue(self.rolling_window_sec / factor)

        self.follow_x = (s.value("graph/follow_x", "true") == "true")
        self.btnFollow.setChecked(self.follow_x)

        self.ui.comboFsUnit.setCurrentIndex(self._safe_int(s.value("acq/fs_unit", 0)))
        self.ui.spinFs.setValue(float(s.value("acq/fs", 20.0)))
        self.ui.comboDispUnit.setCurrentIndex(self._safe_int(s.value("acq/bloc_unit", 0)))
        self.ui.spinBlocSec.setValue(float(s.value("acq/bloc_rate", 2.0)))

        def_names = ["Vitesse", "Température", "Humidité", "Pression"]
        def_units = ["m/s", "°C", "%RH", "Pa"]
        def_cmin  = [0.0, 0.0, 0.0, 0.0]
        def_cmax  = [3.0, 50.0, 100.0, 50.0]
        for i in range(4):
            self.param_names[i] = s.value(f"param/vo{i}/name", def_names[i])
            self.param_units[i] = s.value(f"param/vo{i}/unit", def_units[i])
            self.conv_min[i]    = float(s.value(f"param/vo{i}/conv_min", def_cmin[i]))
            self.conv_max[i]    = float(s.value(f"param/vo{i}/conv_max", def_cmax[i]))
            getattr(self.ui, f"editName{i}").setText(self.param_names[i])
            getattr(self.ui, f"editUnit{i}").setText(self.param_units[i])
            getattr(self.ui, f"spinConvMin{i}").setValue(self.conv_min[i])
            getattr(self.ui, f"spinConvMax{i}").setValue(self.conv_max[i])

            self.fixed_y[i] = (s.value(f"y/vo{i}/fixed", "false") == "true")
            self.y_min[i]   = float(s.value(f"y/vo{i}/min", def_cmin[i]))
            self.y_max[i]   = float(s.value(f"y/vo{i}/max", def_cmax[i]))
            getattr(self.ui, f"chkYFix{i}").setChecked(self.fixed_y[i])
            getattr(self.ui, f"spinYMin{i}").setValue(self.y_min[i])
            getattr(self.ui, f"spinYMax{i}").setValue(self.y_max[i])

            self.corr_mode[i] = self._safe_int(s.value(f"corr/vo{i}/mode", 0))
            self.corr_a[i]    = float(s.value(f"corr/vo{i}/a", 1.0))
            self.corr_b[i]    = float(s.value(f"corr/vo{i}/b", 0.0))
            self.corr_c[i]    = float(s.value(f"corr/vo{i}/c", 0.0))
            self.corr_d[i]    = float(s.value(f"corr/vo{i}/d", 0.0))
            getattr(self.ui, f"comboCorr{i}").setCurrentIndex(self.corr_mode[i])
            getattr(self.ui, f"spinCorrA{i}").setValue(self.corr_a[i])
            getattr(self.ui, f"spinCorrB{i}").setValue(self.corr_b[i])
            getattr(self.ui, f"spinCorrC{i}").setValue(self.corr_c[i])
            getattr(self.ui, f"spinCorrD{i}").setValue(self.corr_d[i])

        # Réglages Y des courbes Julabo T° int/ext du dashboard (persistés au
        # même endroit que les voies analogiques). On lit/écrit directement les
        # widgets (ces voies ne passent pas par un « Appliquer »). hasattr par
        # sécurité si l'UI n'a pas encore été recompilée avec ces widgets.
        for suffix, dmin, dmax in (("Tint", 0.0, 100.0), ("Text", 0.0, 100.0)):
            chk = getattr(self.ui, f"chkYFix{suffix}", None)
            if chk is None:
                continue
            key = f"y/jul_{suffix.lower()}"
            chk.setChecked(s.value(f"{key}/fixed", "false") == "true")
            getattr(self.ui, f"spinYMin{suffix}").setValue(
                float(s.value(f"{key}/min", dmin)))
            getattr(self.ui, f"spinYMax{suffix}").setValue(
                float(s.value(f"{key}/max", dmax)))

    def _save_settings(self):
        s = self._settings()
        s.setValue("graph/mode",       self.current_mode)
        s.setValue("graph/rolling_sec", self.rolling_window_sec)
        s.setValue("graph/follow_x",   "true" if self.follow_x else "false")
        s.setValue("acq/fs_unit",      self.ui.comboFsUnit.currentIndex())
        s.setValue("acq/fs",           float(self.ui.spinFs.value()))
        s.setValue("acq/bloc_unit",    self.ui.comboDispUnit.currentIndex())
        s.setValue("acq/bloc_rate",    float(self.ui.spinBlocSec.value()))
        s.setValue("acq/rolling_unit", self.ui.comboRollingUnit.currentIndex())
        for i in range(4):
            s.setValue(f"y/vo{i}/fixed",    "true" if self.fixed_y[i] else "false")
            s.setValue(f"y/vo{i}/min",      self.y_min[i])
            s.setValue(f"y/vo{i}/max",      self.y_max[i])
            s.setValue(f"corr/vo{i}/mode",  int(self.corr_mode[i]))
            s.setValue(f"corr/vo{i}/a",     float(self.corr_a[i]))
            s.setValue(f"corr/vo{i}/b",     float(self.corr_b[i]))
            s.setValue(f"corr/vo{i}/c",     float(self.corr_c[i]))
            s.setValue(f"corr/vo{i}/d",     float(self.corr_d[i]))
            s.setValue(f"param/vo{i}/name",     self.param_names[i])
            s.setValue(f"param/vo{i}/unit",     self.param_units[i])
            s.setValue(f"param/vo{i}/conv_min", self.conv_min[i])
            s.setValue(f"param/vo{i}/conv_max", self.conv_max[i])

        # Réglages Y des courbes Julabo T° int/ext du dashboard.
        for suffix in ("Tint", "Text"):
            chk = getattr(self.ui, f"chkYFix{suffix}", None)
            if chk is None:
                continue
            key = f"y/jul_{suffix.lower()}"
            s.setValue(f"{key}/fixed", "true" if chk.isChecked() else "false")
            s.setValue(f"{key}/min", float(getattr(self.ui, f"spinYMin{suffix}").value()))
            s.setValue(f"{key}/max", float(getattr(self.ui, f"spinYMax{suffix}").value()))


# =============================================================================
# ██████  APPLICATION PRINCIPALE — 4 onglets
# =============================================================================

class DetachedWindow(QMainWindow):
    def __init__(self, widget, title, icon, original_tab_widget, original_index, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.widget           = widget
        self.original_tab_widget = original_tab_widget
        self.original_index   = original_index   # position d'origine dans tabsMain
        self.original_icon    = icon

        self.setCentralWidget(self.widget)
        self.widget.show()
        self.resize(1000, 700)
        self._apply_stylesheet()

    def closeEvent(self, event):
        # Réinsérer à la position d'origine (pas juste addTab à la fin)
        idx = min(self.original_index, self.original_tab_widget.count())
        self.original_tab_widget.insertTab(idx, self.widget,
                                           self.original_icon,
                                           self.windowTitle())
        self.original_tab_widget.setCurrentIndex(idx)
        self.widget.show()
        super().closeEvent(event)

    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #F2F2F2;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            QLabel { background: transparent; }
        """)

class DashboardController(QtCore.QObject):
    """Contrôleur du dashboard — utilise tabDashboard déjà présent dans Ui_PolarisMainWindow.

    Graphe multi-courbes (4 voies Sauermann + 2 voies Julabo Tint/Text), chaque
    courbe ayant sa propre échelle Y indépendante. Les contrôles (cases « Courbe »
    et « Éch. », sélecteurs « Côté » Gauche/Droite, pastilles de couleur) sont
    définis dans le fichier .ui (Qt Designer) ; ce contrôleur ne fait que les
    relier au graphe.

    Une barre de curseur (comme l'onglet Sauermann) affiche, au survol :
        date heure  |  voie : valeur unité
    pour la courbe la plus proche du pointeur.
    """

    # Colonne « virtuelle » du ViewBox central dans la grille graphique.
    _CENTER_COL = 1000

    # (clé, libellé par défaut, couleur, index Sauermann)
    _CHANNELS_DEF = [
        ("V1",   "V1",      "#E67E22", 0),
        ("V2",   "V2",      "#27AE60", 1),
        ("V3",   "V3",      "#3498DB", 2),
        ("V4",   "V4",      "#E74C3C", 3),
        ("TINT", "T° int",  "#9B59B6", None),
        ("TEXT", "T° ext",  "#16A085", None),
    ]

    def __init__(self, ui_instance: Ui_PolarisMainWindow, main_window: QMainWindow):
        super().__init__(main_window)
        self.ui = ui_instance
        self.main_window = main_window
        self.csv_manager = None   # gestionnaire CSV centralisé (défini par MainApp)
        self._rdm_slot = {}       # adresse RDM → indice de slot LED (1..12)
        self._RDM_LED_SLOTS = 12  # 12 LEDs : 3 sections de 4 (liquides / humide / gazeux)
        # Mapping FIXE adresse RDM → emplacement de LED (par catégorie) :
        #   Polluants liquides : 3, 4, 5, 6      → LEDs 1-4
        #   Air humide         : 7, 8, 9, 10     → LEDs 5-8
        #   Polluants gazeux   : 11, 12, 14, 15  → LEDs 9-12
        # L'adresse 13 est volontairement ABSENTE (aucune LED).
        self._RDM_ADDR_SLOTS = {
            3: 1,  4: 2,  5: 3,  6: 4,
            7: 5,  8: 6,  9: 7,  10: 8,
            11: 9, 12: 10, 14: 11, 15: 12,
        }

        # Références directes aux labels Sauermann — panneau header
        self._lbl_vals = [
            self.ui.lblSauTempVal,
            self.ui.lblSauVitVal,
            self.ui.lblSauPresVal,
            self.ui.lblSauHumVal,
        ]

        # Labels V1–V4 (panelVoies) + lblSauXxxName (panneau header)
        self._lbl_voies = [
            self.ui.lblV1,
            self.ui.lblV2,
            self.ui.lblV3,
            self.ui.lblV4,
        ]
        self._lbl_sau_names = [
            self.ui.lblSauTempName,
            self.ui.lblSauVitName,
            self.ui.lblSauPresName,
            self.ui.lblSauHumName,
        ]

        # Labels d'unité (pour la barre de curseur) — un par voie
        self._unit_lbls = {
            "V1":   getattr(self.ui, "lblSauTempUnit", None),
            "V2":   getattr(self.ui, "lblSauVitUnit",  None),
            "V3":   getattr(self.ui, "lblSauPresUnit", None),
            "V4":   getattr(self.ui, "lblSauHumUnit",  None),
            "TINT": getattr(self.ui, "lblJulTintUnit", None),
            "TEXT": getattr(self.ui, "lblJulTextUnit", None),
        }

        # Initialisation + connexion live : editNameX → lblVX + lblSauXxxName
        for i, (lbl_voie, lbl_sau) in enumerate(
                zip(self._lbl_voies, self._lbl_sau_names)):
            edit = getattr(self.ui, f"editName{i}")
            nom  = edit.text() or f"V{i+1}"
            lbl_voie.setText(nom)
            lbl_sau.setText(f"{nom} :")

            def _on_name_changed(text, lv=lbl_voie, ls=lbl_sau, idx=i):
                n = text or f"V{idx+1}"
                lv.setText(n)
                ls.setText(f"{n} :")
                self._on_sau_name_changed(idx, n)

            edit.textChanged.connect(_on_name_changed)

        # ── Structures de voies + liaison contrôles .ui + graphe ───────────
        self._channels: dict[str, dict] = {}
        self._order: list[str] = [c[0] for c in self._CHANNELS_DEF]
        self._swatch_keys: dict[object, str] = {}
        self._max_pts = 6000

        self._build_channel_records()
        self._bind_controls()
        self._build_graph()
        self._wire_controls()

        # Boutons d'enregistrement CSV centralisé
        self.ui.btnStartCsv.clicked.connect(self._on_start_csv)
        self.ui.btnStopCsv.clicked.connect(self._on_stop_csv)
        self.ui.btnStopCsv.setEnabled(False)

        # Rafraîchissement périodique du graphe
        self._dirty = False
        self._timer = QTimer(self)
        self._timer.setInterval(400)
        self._timer.timeout.connect(self._refresh_graph)
        self._timer.start()

    # ════════════════════════════════════════════════════════════════════
    #   ENREGISTREMENT CSV CENTRALISÉ (Sauermann + Julabo + Bronkhorst)
    # ════════════════════════════════════════════════════════════════════
    def _on_start_csv(self):
        if self.csv_manager is None or self.csv_manager.is_active:
            return
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self.main_window, "Choisir le dossier d'enregistrement CSV")
        if not directory:
            return
        if self.csv_manager.start(directory):
            self.ui.btnStartCsv.setEnabled(False)
            self.ui.btnStopCsv.setEnabled(True)

    def _on_stop_csv(self):
        if self.csv_manager is None or not self.csv_manager.is_active:
            return
        self.csv_manager.stop()
        self.ui.btnStartCsv.setEnabled(True)
        self.ui.btnStopCsv.setEnabled(False)

    # ════════════════════════════════════════════════════════════════════
    #   CONSTRUCTION
    # ════════════════════════════════════════════════════════════════════
    def _build_channel_records(self):
        for key, label, color, sau_idx in self._CHANNELS_DEF:
            self._channels[key] = {
                "label":   label,
                "color":   color,
                "side":    "left",     # ajusté depuis le combo .ui dans _bind_controls
                "sau_idx": sau_idx,
                "t":       deque(maxlen=self._max_pts),
                "y":       deque(maxlen=self._max_pts),
                "chk_curve": None, "chk_scale": None,
                "swatch": None, "combo": None,
                "vb": None, "ax": None, "curve": None, "marker": None,
                "incol": None, "in_layout": False,
            }
        # Libellé des voies Sauermann = nom saisi (editName) si présent
        for i in range(4):
            edit = getattr(self.ui, f"editName{i}", None)
            if edit is not None and edit.text().strip():
                self._channels[f"V{i+1}"]["label"] = edit.text().strip()

    def _bind_controls(self):
        """Relie les widgets du .ui (cases, combos, pastilles) à chaque voie."""
        mapping = {
            "V1":   ("chkScaleV1",   "chkCurveV1",   "lblColorV1",   "comboSideV1"),
            "V2":   ("chkScaleV2",   "chkCurveV2",   "lblColorV2",   "comboSideV2"),
            "V3":   ("chkScaleV3",   "chkCurveV3",   "lblColorV3",   "comboSideV3"),
            "V4":   ("chkScaleV4",   "chkCurveV4",   "lblColorV4",   "comboSideV4"),
            "TINT": ("chkScaleTint", "chkCurveTint", "lblColorTint", "comboSideTint"),
            "TEXT": ("chkScaleText", "chkCurveText", "lblColorText", "comboSideText"),
        }
        for key, (sc, cv, sw, cb) in mapping.items():
            ch = self._channels[key]
            ch["chk_scale"] = getattr(self.ui, sc)
            ch["chk_curve"] = getattr(self.ui, cv)
            ch["swatch"]    = getattr(self.ui, sw)
            ch["combo"]     = getattr(self.ui, cb)
            # Côté = défini par le combo du .ui (0=Gauche, 1=Droite)
            ch["side"] = "left" if ch["combo"].currentIndex() == 0 else "right"
            self._setup_swatch(ch["swatch"], key)
            self._paint_swatch(key)

    def _setup_swatch(self, swatch, key: str):
        swatch.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        swatch.setToolTip("Cliquer pour choisir la couleur")
        swatch.installEventFilter(self)
        self._swatch_keys[swatch] = key

    def _paint_swatch(self, key: str):
        ch = self._channels[key]
        ch["swatch"].setStyleSheet(
            f"background:{ch['color']}; border:1px solid #555; border-radius:3px;"
        )

    # ── Graphe pyqtgraph multi-axes ──────────────────────────────────────
    def _build_graph(self):
        self.graphWidget = pg.GraphicsLayoutWidget()
        self.graphWidget.setBackground('w')

        if hasattr(self.ui, "lblGraphPlaceholder"):
            self.ui.lblGraphPlaceholder.hide()
        self.ui.layGraph.addWidget(self.graphWidget)

        gl = self.graphWidget.ci
        self._glayout = gl

        # ViewBox « hôte » (référence de géométrie + axe X temps)
        self._host_vb = pg.ViewBox()
        self._host_vb.setMouseEnabled(x=True, y=False)
        gl.addItem(self._host_vb, row=0, col=self._CENTER_COL)

        self._bottom_axis = DateAxis(orientation='bottom')
        self._bottom_axis.linkToView(self._host_vb)
        gl.addItem(self._bottom_axis, row=1, col=self._CENTER_COL)

        self._host_vb.sigResized.connect(self._sync_views)

        # Ligne verticale du curseur
        self._vline = pg.InfiniteLine(angle=90, movable=False,
                                      pen=pg.mkPen("#666", width=1))
        self._host_vb.addItem(self._vline, ignoreBounds=True)

        # Grille de fond (style Sauermann) : lignes de repère en X (temps) et Y.
        # Le graphe dashboard est multi-axes (un ViewBox par voie) : il n'a pas
        # de PlotItem exposant showGrid(). On ajoute donc un GridItem sur le
        # ViewBox hôte, placé DERRIÈRE les courbes (Z faible). On fixe la plage Y
        # de l'hôte à [0, 1] pour des lignes horizontales stables et régulières
        # (l'hôte ne porte aucune courbe : sa plage Y ne sert qu'à la grille).
        self._grid = pg.GridItem()
        self._grid.setZValue(-1000)
        try:
            self._grid.setPen(pg.mkPen((190, 190, 190), width=1))
        except Exception:
            pass
        try:
            self._grid.setTextPen(None)      # pas de texte d'échelle sur la grille
        except Exception:
            pass
        self._host_vb.addItem(self._grid, ignoreBounds=True)
        self._host_vb.setYRange(0, 1, padding=0)

        # Un ViewBox + axe + courbe + marqueur par voie
        for key in self._order:
            ch = self._channels[key]
            vb = pg.ViewBox()
            vb.setMouseEnabled(x=True, y=False)
            gl.scene().addItem(vb)
            vb.setXLink(self._host_vb)
            ch["vb"] = vb

            curve = pg.PlotCurveItem(pen=pg.mkPen(ch["color"], width=2))
            vb.addItem(curve)
            ch["curve"] = curve

            marker = pg.ScatterPlotItem(size=9, brush=pg.mkBrush(ch["color"]),
                                        pen=pg.mkPen('w', width=1))
            marker.setZValue(10)
            marker.setVisible(False)
            vb.addItem(marker)
            ch["marker"] = marker

            ax = self._make_axis(key)
            ch["ax"] = ax
            ch["incol"] = self._col_for(key)
            if ch["chk_scale"].isChecked():
                gl.addItem(ax, row=0, col=ch["incol"])
                ch["in_layout"] = True

            curve.setVisible(ch["chk_curve"].isChecked())

        # Survol souris → barre de curseur
        self.graphWidget.scene().sigMouseMoved.connect(self._on_mouse_moved)
        self._sync_views()

    def _make_axis(self, key: str) -> pg.AxisItem:
        ch = self._channels[key]
        ax = pg.AxisItem(orientation=ch["side"])
        ax.linkToView(ch["vb"])
        ax.setLabel(self._axis_label(key), color=ch["color"])   # « Nom (unité) »
        ax.setPen(pg.mkPen(ch["color"], width=1))
        ax.setTextPen(ch["color"])
        ch["_ax_label_cache"] = self._axis_label(key)
        return ax

    def _col_for(self, key: str) -> int:
        ch  = self._channels[key]
        idx = self._order.index(key)
        if ch["side"] == "left":
            return self._CENTER_COL - 1 - idx
        return self._CENTER_COL + 1 + idx

    def _sync_views(self):
        r = self._host_vb.sceneBoundingRect()
        for key in self._order:
            vb = self._channels[key]["vb"]
            if vb is not None:
                vb.setGeometry(r)
                vb.linkedViewChanged(self._host_vb, vb.XAxis)

    # ── Connexions des contrôles ─────────────────────────────────────────
    def _wire_controls(self):
        for key in self._order:
            ch = self._channels[key]
            ch["chk_curve"].toggled.connect(
                lambda checked, k=key: self._on_curve_toggled(k, checked))
            ch["chk_scale"].toggled.connect(
                lambda checked, k=key: self._on_scale_toggled(k, checked))
            ch["combo"].currentIndexChanged.connect(
                lambda _idx, k=key: self._on_side_changed(k))

    # ════════════════════════════════════════════════════════════════════
    #   HANDLERS CONTRÔLES
    # ════════════════════════════════════════════════════════════════════
    def _on_curve_toggled(self, key: str, checked: bool):
        self._channels[key]["curve"].setVisible(checked)

    def _on_scale_toggled(self, key: str, checked: bool):
        ch = self._channels[key]
        if checked and not ch["in_layout"]:
            self._glayout.addItem(ch["ax"], row=0, col=ch["incol"])
            ch["in_layout"] = True
        elif not checked and ch["in_layout"]:
            self._glayout.removeItem(ch["ax"])
            ch["in_layout"] = False
        self._sync_views()

    def _on_side_changed(self, key: str):
        ch = self._channels[key]
        new_side = "left" if ch["combo"].currentIndex() == 0 else "right"
        if new_side == ch["side"]:
            return
        ch["side"] = new_side

        if ch["in_layout"]:
            self._glayout.removeItem(ch["ax"])
        ch["ax"].setParent(None)

        ch["ax"]    = self._make_axis(key)
        ch["incol"] = self._col_for(key)
        if ch["chk_scale"].isChecked():
            self._glayout.addItem(ch["ax"], row=0, col=ch["incol"])
            ch["in_layout"] = True
        else:
            ch["in_layout"] = False
        self._sync_views()

    def _pick_color(self, key: str):
        ch      = self._channels[key]
        initial = QtGui.QColor(ch["color"])
        col     = QtWidgets.QColorDialog.getColor(
            initial, self.ui.panelVoies, f"Couleur — {ch['label']}")
        if not col.isValid():
            return
        ch["color"] = col.name()
        self._paint_swatch(key)
        ch["curve"].setPen(pg.mkPen(ch["color"], width=2))
        ch["marker"].setBrush(pg.mkBrush(ch["color"]))
        ax = ch["ax"]
        ax.setLabel(self._axis_label(key), color=ch["color"])   # « Nom (unité) »
        ax.setPen(pg.mkPen(ch["color"], width=1))
        ax.setTextPen(ch["color"])

    def _on_sau_name_changed(self, sau_idx: int, name: str):
        key = f"V{sau_idx+1}"
        ch  = self._channels.get(key)
        if not ch:
            return
        ch["label"] = name
        if ch["ax"] is not None:
            ch["ax"].setLabel(self._axis_label(key), color=ch["color"])  # « Nom (unité) »
            ch["_ax_label_cache"] = self._axis_label(key)

    def eventFilter(self, obj, ev):
        if (ev.type() == QtCore.QEvent.Type.MouseButtonPress
                and obj in self._swatch_keys):
            self._pick_color(self._swatch_keys[obj])
            return True
        return super().eventFilter(obj, ev)

    # ── Barre de curseur (date heure | voie : valeur unité) ──────────────
    def _unit_for(self, key: str) -> str:
        lbl = self._unit_lbls.get(key)
        if lbl is None:
            return ""
        txt = lbl.text().strip()
        return "" if txt in ("--", "—") else txt

    def _axis_label(self, key: str) -> str:
        """Libellé d'axe d'une voie = « Nom (unité) ». L'unité est ajoutée entre
        parenthèses si elle est connue, sinon on garde juste le nom."""
        ch = self._channels[key]
        unit = self._unit_for(key)
        return f'{ch["label"]} ({unit})' if unit else ch["label"]

    def _refresh_axis_labels(self):
        """Réapplique le libellé « Nom (unité) » sur chaque axe si l'unité (ou le
        nom) a changé. Le cache évite d'appeler setLabel à chaque rafraîchissement."""
        for key in self._order:
            ch = self._channels.get(key)
            if not ch or ch.get("ax") is None:
                continue
            lbl = self._axis_label(key)
            if ch.get("_ax_label_cache") != lbl:
                ch["ax"].setLabel(lbl, color=ch["color"])
                ch["_ax_label_cache"] = lbl

    def _on_mouse_moved(self, pos):
        if not self._host_vb.sceneBoundingRect().contains(pos):
            for key in self._order:
                self._channels[key]["marker"].setVisible(False)
            self.ui.lblDashCross.setText("—")
            return

        x = self._host_vb.mapSceneToView(pos).x()
        self._vline.setPos(x)
        cursor_y = pos.y()

        best = None  # (dist_scene_y, key, value, t_sample)
        for key in self._order:
            ch = self._channels[key]
            self._channels[key]["marker"].setVisible(False)
            if not ch["chk_curve"].isChecked() or len(ch["t"]) == 0:
                continue
            t = np.asarray(ch["t"], dtype=float)
            n = len(t)
            idx = int(np.clip(np.searchsorted(t, x), 0, n - 1))
            if idx > 0 and abs(t[idx] - x) > abs(t[idx - 1] - x):
                idx -= 1
            yv = ch["y"][idx]
            if yv is None:
                continue
            yv = float(yv)
            sp = ch["vb"].mapViewToScene(QtCore.QPointF(float(t[idx]), yv))
            dist = abs(sp.y() - cursor_y)
            if best is None or dist < best[0]:
                best = (dist, key, yv, float(t[idx]))

        if best is None:
            self.ui.lblDashCross.setText("—")
            return

        _, key, yv, tt = best
        ch = self._channels[key]
        ch["marker"].setData([tt], [yv])
        ch["marker"].setVisible(True)
        dt_str = datetime.fromtimestamp(tt).strftime("%d/%m %H:%M:%S")
        unit   = self._unit_for(key)
        txt    = f"{dt_str}  |  {ch['label']} : {yv:.2f} {unit}".rstrip()
        self.ui.lblDashCross.setText(txt)

    # ════════════════════════════════════════════════════════════════════
    #   RAFRAÎCHISSEMENT DU GRAPHE
    # ════════════════════════════════════════════════════════════════════
    def _fixed_range_for(self, key, ch):
        """Renvoie (ymin, ymax) si la voie a une échelle Y « fixe », sinon None.

        - Voies analogiques Sauermann (ch['sau_idx'] non None) : on lit les
          réglages APPLIQUÉS du contrôleur Sauermann (fixed_y / y_min / y_max),
          comme le graphe Sauermann.
        - Voies Julabo T° int/ext : on lit en direct les widgets dédiés de
          l'onglet Réglages (chkYFix{Tint,Text} / spinYMin.. / spinYMax..).
        """
        sau_idx = ch.get("sau_idx")
        if sau_idx is not None:
            sau = getattr(self.main_window, "sauermann_ctrl", None)
            if sau is not None:
                try:
                    if sau.fixed_y[sau_idx]:
                        return float(sau.y_min[sau_idx]), float(sau.y_max[sau_idx])
                except Exception:
                    pass
            return None

        # Voies Julabo du dashboard → widgets dédiés (lecture en direct).
        wmap = {
            "TINT": ("chkYFixTint", "spinYMinTint", "spinYMaxTint"),
            "TEXT": ("chkYFixText", "spinYMinText", "spinYMaxText"),
        }
        names = wmap.get(key)
        if names:
            try:
                chk  = getattr(self.ui, names[0])
                smin = getattr(self.ui, names[1])
                smax = getattr(self.ui, names[2])
                if chk.isChecked():
                    return float(smin.value()), float(smax.value())
            except Exception:
                pass
        return None

    def _refresh_graph(self):
        if not self._dirty:
            return
        self._dirty = False

        # Met à jour « Nom (unité) » sur les axes si une unité a changé (no-op
        # si rien n'a bougé grâce au cache).
        self._refresh_axis_labels()

        t_min = None
        t_max = None
        for key in self._order:
            ch = self._channels[key]
            if len(ch["t"]) == 0:
                continue
            ch["curve"].setData(list(ch["t"]), list(ch["y"]))
            t0, t1 = ch["t"][0], ch["t"][-1]
            t_min = t0 if t_min is None else min(t_min, t0)
            t_max = t1 if t_max is None else max(t_max, t1)
            ys = [v for v in ch["y"] if v is not None]
            if ys:
                # Échelle Y fixe éventuelle : voies analogiques Sauermann (via
                # sau_idx) OU voies Julabo T° int/ext (via leurs widgets dédiés
                # dans l'onglet Réglages). _fixed_range_for renvoie (ymin, ymax)
                # si « fixe » est actif pour cette voie, sinon None → auto-échelle.
                rng = self._fixed_range_for(key, ch)
                if rng is not None:
                    ch["vb"].setYRange(rng[0], rng[1], padding=0)
                else:
                    lo, hi = min(ys), max(ys)
                    # Échelle minimale de 1 par voie (comme Julabo) : si
                    # l'amplitude des données est < 1, on centre sur une plage
                    # de largeur exactement 1 pour éviter un axe « écrasé ».
                    if (hi - lo) < 1.0:
                        center = (hi + lo) / 2.0
                        lo, hi = center - 0.5, center + 0.5
                    ch["vb"].setYRange(lo, hi, padding=0.12)

        if t_min is not None and t_max is not None:
            if t_max - t_min < 1.0:
                t_max = t_min + 1.0
            self._host_vb.setXRange(t_min, t_max, padding=0.02)
        self._sync_views()

    # ════════════════════════════════════════════════════════════════════
    #   SLOTS LEDs
    # ════════════════════════════════════════════════════════════════════
    @QtCore.Slot(str)
    def on_sau_led(self, color: str):
        self.ui.ledSauermann.setStyleSheet(
            f"border:1px solid #555; border-radius:9px; background:{color};"
        )

    @QtCore.Slot(str)
    def on_bro_led(self, color: str):
        self.ui.ledBronkhorst.setStyleSheet(
            f"border:1px solid #555; border-radius:9px; background:{color};"
        )

    @QtCore.Slot(str)
    def on_jul_led(self, color: str):
        self.ui.ledJulabo.setStyleSheet(
            f"border:1px solid #555; border-radius:9px; background:{color};"
        )

    @QtCore.Slot(str)
    def on_pid_led(self, color: str):
        # LED d'état de la régulation PID sur le dashboard (vert = actif,
        # gris = inactif), à côté des LED de communication.
        self.ui.ledPid.setStyleSheet(
            f"border:1px solid #555; border-radius:9px; background:{color};"
        )

    # ── LED de connexion par RDM (panneau « LEDs RDMs ») ──────────────────
    def _paint_rdm_led(self, k: int, connected: bool):
        led = getattr(self.ui, f"ledRdm{k}", None)
        if led is not None:
            color = "#2ECC71" if connected else "#bbb"
            led.setStyleSheet(
                f"background:{color}; border:1px solid #555; border-radius:10px;"
            )

    @QtCore.Slot(list)
    def set_rdm_leds(self, addresses=None):
        """Affiche le gabarit FIXE des LED RDM selon le mapping adresse→catégorie
        (Polluants liquides / Air humide / Polluants gazeux) et remet toutes les
        LED au gris. Chaque emplacement porte en permanence son numéro d'adresse.
        Les statuts (vert = connecté) arrivent ensuite via on_rdm_status.
        L'adresse 13 n'a aucune LED (absente du mapping)."""
        self._rdm_slot = dict(self._RDM_ADDR_SLOTS)   # mapping fixe adresse → slot
        for addr, k in self._RDM_ADDR_SLOTS.items():
            lbl = getattr(self.ui, f"lblRdmNum{k}", None)
            led = getattr(self.ui, f"ledRdm{k}", None)
            if lbl is None or led is None:
                continue
            lbl.setText(str(addr))          # numéro d'adresse fixe
            lbl.setVisible(True)
            led.setVisible(True)
            self._paint_rdm_led(k, False)   # gris ; on_rdm_status re-verdira

    @QtCore.Slot(int, bool)
    def on_rdm_status(self, addr: int, connected: bool):
        """Met la LED du RDM `addr` en vert (connecté) ou gris (déconnecté)."""
        k = self._rdm_slot.get(int(addr))
        if k is not None:
            self._paint_rdm_led(k, connected)

    # ════════════════════════════════════════════════════════════════════
    #   SLOTS DONNÉES
    # ════════════════════════════════════════════════════════════════════
    @QtCore.Slot(list, list)
    def on_sau_data(self, vals_corriges: list, vals_bruts: list):
        """Reçoit les données Sauermann : labels + courbes V1..V4."""
        t_now = time.time()
        for i, lbl in enumerate(self._lbl_vals):
            if lbl is None:
                continue
            val = None
            if i < len(vals_corriges) and vals_corriges[i] is not None:
                val = vals_corriges[i]
            elif i < len(vals_bruts):
                val = vals_bruts[i]
            lbl.setText(f"{val:.2f}" if val is not None else "--")

            ch = self._channels.get(f"V{i+1}")
            if ch is not None and val is not None:
                ch["t"].append(t_now)
                ch["y"].append(float(val))
                self._dirty = True

    @QtCore.Slot(object, object, object)
    def on_jul_data(self, t_int, t_ext, setpoint):
        """Reçoit les données Julabo : labels + courbes Tint / Text."""
        def fmt(v):
            return f"{v:.2f}" if v is not None else "--"

        self.ui.lblJulTintVal.setText(fmt(t_int))
        self.ui.lblJulTextVal.setText(fmt(t_ext))
        self.ui.lblJulConsVal.setText(fmt(setpoint))

        # Enregistrement CSV centralisé : on mémorise la dernière donnée Julabo
        # (l'écriture est cadencée par les blocs Sauermann, pas ici).
        if self.csv_manager is not None and self.csv_manager.is_active:
            self.csv_manager.update_julabo(t_int, t_ext, setpoint)

        t_now = time.time()
        for key, val in (("TINT", t_int), ("TEXT", t_ext)):
            ch = self._channels.get(key)
            if ch is not None and val is not None:
                ch["t"].append(t_now)
                ch["y"].append(float(val))
                self._dirty = True


# ╔══════════════════════════════════════════════════════════════════════╗
# ║                        MODULE PID                                   ║
# ╚══════════════════════════════════════════════════════════════════════╝

class PIDWorker(QtCore.QObject):
    """Worker PID — tourne dans un QThread séparé.

    Calcule la sortie PID depuis les données Sauermann et émet
    setpoint_command vers BronkhorstController — pas de connexion
    série propre, utilise le port déjà géré par Bronkhorst.
    """

    status_changed   = QtCore.Signal(str, bool)  # (message, actif)
    setpoint_command = QtCore.Signal(int, float)  # (adresse, pct 0-100)
    error            = QtCore.Signal(str)
    finished         = QtCore.Signal()

    def __init__(self, addr: int,
                 Kp: float, Ki: float, Kd: float,
                 consigne: float, sample_time: float,
                 initial_valve: float = 50.0):
        super().__init__()
        self._addr          = addr
        self._Kp            = Kp
        self._Ki            = Ki
        self._Kd            = Kd
        self._consigne      = consigne
        self._sample_time   = sample_time
        self._initial_valve = initial_valve   # position valve au démarrage
        self._running       = False
        self._last_value    = None
        self._voie_idx      = 0

    @QtCore.Slot(list, list)
    def on_new_value(self, vals_corriges: list, vals_bruts: list):
        """Reçoit la mesure depuis SauermannController."""
        val = vals_corriges[self._voie_idx]
        if val is None:
            val = vals_bruts[self._voie_idx]
        self._last_value = val

    @QtCore.Slot()
    def run(self):
        """Démarre le PID — pas de connexion série ici."""
        if not _pid_ok:
            self.error.emit("simple_pid non installé : pip install simple_pid")
            self.finished.emit()
            return

        self._pid = SimplePID(
            self._Kp, self._Ki, self._Kd,
            setpoint=self._consigne
        )
        self._pid.output_limits = (0.0, 100.0)
        self._pid.sample_time   = self._sample_time

        # Bumpless transfer : intégrateur initialisé à la valve actuelle
        # → la valve ne repasse pas par 0% au démarrage
        self._pid.set_auto_mode(True, last_output=self._initial_valve)

        self._running = True
        self.status_changed.emit(
            f"PID actif — valve init : {self._initial_valve:.1f}%", True
        )

        self._timer = QTimer()
        self._timer.setInterval(int(self._sample_time * 1000))
        self._timer.timeout.connect(self._step)
        self._timer.start()

    def _step(self):
        """Un cycle PID : mesure → calcul → signal vers Bronkhorst."""
        if not self._running or self._last_value is None:
            return
        try:
            humidite = self._last_value
            sortie   = self._pid(humidite) or 0.0
            sortie   = max(0.0, min(100.0, sortie))

            # Déléguer l'écriture au SerialWorker Bronkhorst via signal
            self.setpoint_command.emit(self._addr, sortie)

            erreur = self._consigne - humidite
            self.status_changed.emit(
                f"HR={humidite:.1f}%  Err={erreur:+.1f}%  Valve={sortie:.1f}%", True
            )
        except Exception as e:
            self.error.emit(f"Erreur cycle PID : {e}")

    @QtCore.Slot()
    def stop(self):
        self._running = False
        if hasattr(self, '_timer'):
            self._timer.stop()
        # Fermer la valve à 0% via le même canal
        self.setpoint_command.emit(self._addr, 0.0)
        self.status_changed.emit("Inactif", False)
        self.finished.emit()


class PIDController(QtCore.QObject):
    """Contrôleur de l'onglet PID — section Régulation PID."""

    _start_requested = QtCore.Signal()
    _stop_requested  = QtCore.Signal()
    led_changed      = QtCore.Signal(str)   # état PID → LED du dashboard

    def __init__(self, ui_instance: Ui_PolarisMainWindow,
                 main_window: QMainWindow,
                 sau_ctrl, bro_ctrl):
        super().__init__(main_window)
        self.ui        = ui_instance
        self._sau_ctrl = sau_ctrl
        self._bro_ctrl = bro_ctrl   # pour router les setpoints via SerialWorker
        self._worker   = None
        self._thread   = None

        self._set_led(False)

        # La case « Activer / Désactiver » pilote ENTIÈREMENT la régulation :
        # cochée, elle applique les paramètres et démarre le PID ; décochée, elle
        # l'arrête. (Plus de boutons Appliquer / Annuler.)
        self.ui.chkPidActive.stateChanged.connect(self._on_checkbox)

        # Voie HR (humidité) par défaut = V3 (index 2) au lieu de V1 (index 0).
        try:
            if self.ui.comboPidVoie.count() > 2:
                self.ui.comboPidVoie.setCurrentIndex(2)
        except Exception:
            pass

    # ── LED helper ─────────────────────────────────────────────────────
    def _set_led(self, active: bool):
        color = "#2ECC71" if active else "#bbb"
        self.ui.lblPidLed.setStyleSheet(
            f"border:1px solid #888; border-radius:6px; background:{color};"
        )
        # Répercute l'état (actif/inactif) sur la LED PID du dashboard.
        self.led_changed.emit(color)

    # ── Checkbox ────────────────────────────────────────────────────────
    def _on_checkbox(self, state):
        if state == 2:   # Checked
            self._on_apply()
        else:
            self._on_cancel()

    # ── Appliquer ───────────────────────────────────────────────────────
    def _on_apply(self):
        if self._worker is not None:
            self._on_cancel()   # arrêter l'ancien si actif

        # Récupérer les paramètres UI
        Kp          = self.ui.spinPidKp.value()
        Ki          = self.ui.spinPidKi.value()
        Kd          = self.ui.spinPidKd.value()
        consigne    = self.ui.spinPidConsigne.value()
        sample_time = self.ui.spinPidLoop.value()
        voie_idx    = self.ui.comboPidVoie.currentIndex()
        addr        = self.ui.spinPidAddr.value()

        # Lire position valve actuelle pour bumpless transfer
        initial_valve = self._bro_ctrl.get_valve_pct(addr)

        self._worker = PIDWorker(addr, Kp, Ki, Kd, consigne, sample_time,
                                 initial_valve=initial_valve)
        self._worker._voie_idx = voie_idx

        self._thread = QThread(self)
        self._worker.moveToThread(self._thread)

        # Connexions cycle de vie
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._worker.finished.connect(self._on_worker_finished)

        # Données Sauermann → PID
        self._sau_ctrl.data_ready.connect(self._worker.on_new_value)

        # Sortie PID → SerialWorker Bronkhorst (même port, pas de conflit)
        self._worker.setpoint_command.connect(self._bro_ctrl._handle_setpoint)

        # Statut → UI
        self._worker.status_changed.connect(self._on_status)
        self._worker.error.connect(self._on_error)

        self._thread.start()

        # Reflète l'état actif sur la case, sans re-déclencher son slot.
        self.ui.chkPidActive.blockSignals(True)
        self.ui.chkPidActive.setChecked(True)
        self.ui.chkPidActive.blockSignals(False)

    # ── Annuler ─────────────────────────────────────────────────────────
    def _on_cancel(self):
        if self._worker is not None:
            QtCore.QMetaObject.invokeMethod(self._worker, "stop",
                                            QtCore.Qt.ConnectionType.QueuedConnection)

    # ── Slots worker ────────────────────────────────────────────────────
    @QtCore.Slot(str, bool)
    def _on_status(self, msg: str, active: bool):
        self.ui.lblPidStatus.setText(msg)
        self._set_led(active)

    @QtCore.Slot(str)
    def _on_error(self, msg: str):
        self.ui.lblPidStatus.setText(f"⚠ {msg}")
        self._set_led(False)
        QMessageBox.warning(None, "PID — Erreur", msg)

    def _on_worker_finished(self):
        if self._sau_ctrl and self._worker:
            try:
                self._sau_ctrl.data_ready.disconnect(self._worker.on_new_value)
            except Exception:
                pass
        self._worker = None
        self._thread = None
        self.ui.chkPidActive.blockSignals(True)
        self.ui.chkPidActive.setChecked(False)
        self.ui.chkPidActive.blockSignals(False)
        self._set_led(False)

    def cleanup(self):
        """Arrêt propre à la fermeture de l'application."""
        if self._worker is not None:
            self._on_cancel()
            if self._thread:
                self._thread.quit()
                self._thread.wait(2000)

class CsvManager(QtCore.QObject):
    """Enregistrement CSV centralisé dans DEUX fichiers seulement :

        • metadata_sauermann_AAAA-MM-JJ_HH-MM.csv  (logique Sauermann inchangée)
        • acq_polaris_AAAA-MM-JJ_HH-MM.csv         (fichier de mesures global)

    Le fichier de mesures est cadencé EXCLUSIVEMENT par les blocs de l'onglet
    Sauermann (paramètre « Points affichés ») : une ligne est écrite à chaque
    bloc validé. Les colonnes suivent strictement l'ordre :

        timestamp ; voie1 ; voie1_corr ; … ; voie4 ; voie4_corr ;
        mesure_%_noeud_[X]_[Modele] ; mesure_unite_noeud_[X]_[Modele] (par nœud) ;
        t_int ; t_ext ; consigne

    À chaque bloc, on récupère la DERNIÈRE valeur connue du Julabo et de chaque
    module Bronkhorst ; mais si l'instrument n'a pas envoyé de donnée fraîche
    pendant la période du bloc, ses colonnes restent vides (`;;`) pour ne pas
    répéter de vieilles mesures.

    Format Excel FR : séparateur « ; », virgule décimale, flush à chaque ligne.
    """

    def __init__(self, main_window, sauermann_ctrl, bronkhorst_ctrl, parent=None):
        super().__init__(parent)
        self.main_window     = main_window
        self.sauermann_ctrl  = sauermann_ctrl
        self.bronkhorst_ctrl = bronkhorst_ctrl
        self._active   = False
        self.directory = None
        self.timestamp = None
        self._file     = None
        self._writer   = None
        self._bro_nodes = []        # [(addr, model, unit), …] figé au démarrage
        # Accumulateurs sur la période d'un bloc (listes + compteur d'échantillons
        # valides), vidés/remis à zéro après chaque écriture :
        self._jul_acc = {"t_int": [], "t_ext": [], "consigne": [], "count": 0}
        self._bro_acc = {}          # addr -> {"pct": [...], "real": [...], "count": 0}

    @property
    def is_active(self) -> bool:
        return self._active

    @staticmethod
    def _fr(value, fmt: str = "{:.4f}") -> str:
        """Formate un nombre pour Excel FR (virgule décimale) ; '' si None."""
        if value is None:
            return ""
        try:
            return fmt.format(float(value)).replace('.', ',')
        except (TypeError, ValueError):
            return ""

    @staticmethod
    def _mean(values):
        """Moyenne d'une liste de valeurs numériques ; None si la liste est vide."""
        if not values:
            return None
        return sum(values) / len(values)

    # ── En-tête dynamique (dépend des nœuds Bronkhorst actifs) ───────────
    def _build_header(self) -> list:
        header = ["timestamp"]
        # Sauermann : valeur brute, valeur corrigée, nb d'échantillons du bloc
        for i in range(4):
            header += [f"voie{i+1}", f"voie{i+1}_corr", f"nb_val_voie{i+1}"]
        # Bronkhorst : [Modèle]_pct, [Modèle]_[Unité], nb_val_noeud_[Addr]
        for addr, model, unit in self._bro_nodes:
            header += [f"{model}_pct", f"{model}_{unit}", f"nb_val_noeud_{addr}"]
        # Julabo : températures + consigne + nb d'échantillons du bloc
        header += ["t_int", "t_ext", "consigne", "nb_val_julabo"]
        return header

    # ── Démarrage / arrêt ────────────────────────────────────────────────
    def start(self, directory: str) -> bool:
        if self._active:
            return False
        self.directory = directory
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        meas_path = os.path.join(directory, f"acq_polaris_{self.timestamp}.csv")
        meta_path = os.path.join(directory, f"metadata_sauermann_{self.timestamp}.csv")

        # Figer la liste des nœuds Bronkhorst actifs (adresse, modèle P115, unité
        # P129) au moment du démarrage — sert au nommage des colonnes.
        self._bro_nodes = []
        if self.bronkhorst_ctrl is not None and hasattr(self.bronkhorst_ctrl, "get_active_nodes"):
            scanned = getattr(self.bronkhorst_ctrl, "scanned_devices", {}) or {}
            for addr, model in self.bronkhorst_ctrl.get_active_nodes():
                unit = str(scanned.get(addr, {}).get("unit", "") or "")
                self._bro_nodes.append((addr, model, unit))
        self._jul_acc = {"t_int": [], "t_ext": [], "consigne": [], "count": 0}
        self._bro_acc = {}

        try:
            self._file   = open(meas_path, "w", newline="", encoding="utf-8")
            self._writer = csv.writer(self._file, delimiter=';')
            self._writer.writerow(self._build_header())
            self._file.flush()
        except Exception as e:
            QMessageBox.critical(self.main_window, "Erreur CSV", str(e))
            self._close_file()
            return False

        # Sauermann : fichier de métadonnées (inchangé), déclenché ici. Le fichier
        # s'ouvre au prochain bord de bloc, comme avant, pour la synchro temporelle.
        if self.sauermann_ctrl is not None:
            try:
                self.sauermann_ctrl.start_csv_external(meta_path)
            except Exception as e:
                QMessageBox.critical(self.main_window, "Erreur CSV", str(e))
                self._close_file()
                return False

        self._active = True
        return True

    def stop(self):
        if not self._active and self._file is None:
            return
        if self.sauermann_ctrl is not None:
            try:
                self.sauermann_ctrl.stop_csv_external()
            except Exception:
                pass
        self._close_file()
        self._active = False

    def _close_file(self):
        if self._file is not None:
            try:
                self._file.flush()
                self._file.close()
            except Exception:
                pass
        self._file = None
        self._writer = None

    # ── Accumulation des valeurs reçues pendant le bloc courant ──────────
    def update_julabo(self, t_int, t_ext, consigne):
        """Accumule les données Julabo reçues durant la période du bloc courant.
        Chaque champ est accumulé indépendamment (seules les valeurs numériques
        non nulles sont ajoutées) et le compteur d'échantillons est incrémenté
        d'une unité par relevé valide ; la moyenne est calculée au prochain bloc."""
        if not self._active:
            return
        if t_int is None and t_ext is None and consigne is None:
            return
        if t_int is not None:
            self._jul_acc["t_int"].append(float(t_int))
        if t_ext is not None:
            self._jul_acc["t_ext"].append(float(t_ext))
        if consigne is not None:
            self._jul_acc["consigne"].append(float(consigne))
        self._jul_acc["count"] += 1   # +1 par relevé Julabo valide reçu

    def update_bronkhorst(self, addr, measure_pct, measure_real):
        """Accumule les mesures d'un nœud Bronkhorst durant la période du bloc
        courant et incrémente son compteur d'échantillons (moyenne + reset au
        prochain bloc)."""
        if not self._active:
            return
        acc = self._bro_acc.setdefault(addr, {"pct": [], "real": [], "count": 0})
        valid = False
        if measure_pct is not None:
            acc["pct"].append(float(measure_pct))
            valid = True
        if measure_real is not None:
            acc["real"].append(float(measure_real))
            valid = True
        if valid:
            acc["count"] += 1   # +1 par mesure valide reçue pour ce nœud

    # ── Écriture d'une ligne, cadencée par un bloc Sauermann ─────────────
    def write_block_row(self, t_block, raw_vals, vals, corr_modes,
                        bloc_sec=None, n_sau=None):
        """Écrit une ligne du fichier global. Appelée à chaque bloc Sauermann.

        Chaque instrument fournit, en plus de ses valeurs moyennées, le NOMBRE
        d'échantillons réels lus/moyennés pendant le pas de temps :
          • Sauermann  : n_sau (échantillons lus par la carte NI-DAQ sur le bloc,
                         p. ex. data.shape[1]) — identique pour les 4 voies.
          • Bronkhorst : compteur par nœud (acc["count"]).
          • Julabo     : compteur global (jul["count"]).
        Après écriture, listes vidées ET compteurs remis à zéro pour le bloc
        suivant. Colonnes vides si aucune donnée fraîche (compteur = 0).
        (bloc_sec n'est plus utilisé : le vidage borne la fenêtre au bloc.)
        """
        if not self._active or self._writer is None:
            return

        ts    = datetime.fromtimestamp(t_block).strftime('%Y/%m/%d %H:%M:%S')
        n_sau = int(n_sau) if n_sau is not None else 0
        row   = [ts]

        # 4 voies Sauermann : brute, corrigée, nb d'échantillons du bloc.
        for i in range(4):
            row.append(self._fr(raw_vals[i], "{:.6f}"))
            row.append(self._fr(vals[i], "{:.6f}") if corr_modes[i] != 0 else "")
            row.append(str(n_sau))

        # Bronkhorst par nœud : moyenne %, moyenne unité réelle, nb d'échantillons.
        for addr, _model, _unit in self._bro_nodes:
            acc = self._bro_acc.get(addr)
            if acc and (acc["pct"] or acc["real"]):
                row.append(self._fr(self._mean(acc["pct"]), "{:.2f}"))    # mesure %
                row.append(self._fr(self._mean(acc["real"]), "{:.4f}"))   # unité réelle
                row.append(str(acc["count"]))
                acc["pct"].clear()
                acc["real"].clear()
                acc["count"] = 0
            else:
                row += ["", "", "0"]

        # Julabo : moyennes t_int/t_ext/consigne + nb d'échantillons du bloc.
        jul = self._jul_acc
        if jul["t_int"] or jul["t_ext"] or jul["consigne"]:
            row.append(self._fr(self._mean(jul["t_int"])))      # t_int
            row.append(self._fr(self._mean(jul["t_ext"])))      # t_ext
            row.append(self._fr(self._mean(jul["consigne"])))   # consigne
            row.append(str(jul["count"]))
            jul["t_int"].clear()
            jul["t_ext"].clear()
            jul["consigne"].clear()
            jul["count"] = 0
        else:
            row += ["", "", "", "0"]

        try:
            self._writer.writerow(row)
            self._file.flush()
        except Exception:
            pass


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PolarisMainWindow()
        self.ui.setupUi(self)

        # --- Les contrôleurs habituels ---
        self.bronkhorst_ctrl = BronkhorstController(self.ui, self)
        self.julabo_ctrl = JulaboController(self.ui, self)
        self.sauermann_ctrl = SauermannController(self.ui, self)

        # --- Dashboard ---
        self.dashboard_ctrl = DashboardController(self.ui, self)
        # tabDashboard est déjà dans tabsMain via UI_POLARIS.py

        # Connexion : données Sauermann → labels dashboard
        self.sauermann_ctrl.data_ready.connect(self.dashboard_ctrl.on_sau_data)

        # Connexion : données Julabo → labels dashboard
        self.julabo_ctrl.data_ready.connect(self.dashboard_ctrl.on_jul_data)

        # Connexions LEDs dashboard
        self.sauermann_ctrl.led_changed.connect(self.dashboard_ctrl.on_sau_led)
        self.bronkhorst_ctrl.led_changed.connect(self.dashboard_ctrl.on_bro_led)
        self.julabo_ctrl.led_changed.connect(self.dashboard_ctrl.on_jul_led)

        # --- PID ---
        self.pid_ctrl = PIDController(self.ui, self, self.sauermann_ctrl, self.bronkhorst_ctrl)
        # LED d'état PID (actif/inactif) sur le dashboard, à côté des LED de comm.
        self.pid_ctrl.led_changed.connect(self.dashboard_ctrl.on_pid_led)

        # LED de connexion par RDM (panneau « LEDs RDMs » du dashboard) :
        # la liste des nœuds acquis (re)construit le panneau, et l'état de
        # connexion (paramètre ID 1) allume chaque LED en vert/gris.
        self.bronkhorst_ctrl.rdm_nodes_changed.connect(self.dashboard_ctrl.set_rdm_leds)
        self.bronkhorst_ctrl.rdm_status.connect(self.dashboard_ctrl.on_rdm_status)
        # Gabarit initial : les 12 emplacements de LED RDM sont affichés en gris
        # (aucun RDM encore acquis). Ils passent au vert au fur et à mesure que
        # les RDM correspondants répondent (paramètre ID 1).
        self.dashboard_ctrl.set_rdm_leds([])

        # --- Enregistrement CSV centralisé (piloté depuis le Dashboard) ---
        self.csv_manager = CsvManager(self, self.sauermann_ctrl, self.bronkhorst_ctrl)
        self.dashboard_ctrl.csv_manager  = self.csv_manager
        self.bronkhorst_ctrl.csv_manager = self.csv_manager
        self.sauermann_ctrl.csv_manager  = self.csv_manager

        self._apply_stylesheet()

        # --- NOUVEAU : Gestion du détachement ---
        # On garde une liste des fenêtres ouvertes pour éviter qu'elles ne soient détruites par le Garbage Collector
        self.detached_windows = [] 
        
        # On connecte le double-clic sur un onglet à notre fonction
        self.ui.tabsMain.tabBarDoubleClicked.connect(self._detach_tab)

        # ── Démarrage global « un clic » (bouton Dashboard btnStart_2) ───────
        # Le couplage est centralisé ici car MainApp possède les références vers
        # TOUS les contrôleurs (Sauermann, Bronkhorst, Julabo). Chaque contrôleur
        # lance ses propres QThreads ; _on_global_start ne fait qu'émettre les
        # ordres de démarrage, sans jamais bloquer l'IHM.
        self.ui.btnStart_2.clicked.connect(self._on_global_start)
        self.ui.btnStop_2.clicked.connect(self._on_global_stop)
        self.ui.btnStop_2.setEnabled(False)

    def _on_global_start(self):
        """Séquence d'initialisation globale déclenchée par btnStart_2.

        Orchestration (non bloquante) :
          a) Sauermann  : applique les paramètres et démarre l'acquisition NI-DAQ
                          (carte « dev1 ») dans son QThread.
          b) Bronkhorst : force le port COM7 puis lance le scan du bus RS-485,
                          qui s'exécute dans un ScanWorker (QThread) en fond.
          c) Julabo     : ouvre la liaison série dans un JulaboWorker (QThread).
        Chaque contrôleur gère son propre thread : aucun appel bloquant ici.
        """
        # 1) CONFIRMATION — avant TOUT démarrage. On construit la boîte à la main
        #    pour garantir les libellés exacts « Oui » / « Annuler » (les boutons
        #    standard seraient traduits selon la locale système).
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Confirmation")
        confirm.setIcon(QMessageBox.Icon.Question)
        confirm.setText(
            "Êtes-vous sûr de lancer l'acquisition avec les paramètres actuels ?")
        btn_oui     = confirm.addButton("Oui",     QMessageBox.ButtonRole.AcceptRole)
        btn_annuler = confirm.addButton("Annuler", QMessageBox.ButtonRole.RejectRole)
        confirm.setDefaultButton(btn_oui)
        confirm.exec()
        # Si l'utilisateur n'a pas cliqué « Oui » (Annuler ou fermeture), on
        # abandonne immédiatement : aucun démarrage, l'IHM reste inchangée.
        if confirm.clickedButton() is not btn_oui:
            return

        # 2) Séquence de démarrage habituelle.
        # Anti double-démarrage : on neutralise Start et on arme Stop AVANT de
        # lancer la séquence (le réarmement se fait via un futur _on_global_stop).
        self.ui.btnStart_2.setEnabled(False)
        self.ui.btnStop_2.setEnabled(True)

        # a) SAUERMANN — déclenche la même logique que le bouton « Appliquer les
        #    paramètres » : (ré)initialise le stockage puis démarre l'AcqWorker.
        try:
            self.sauermann_ctrl._apply_params()
        except Exception as e:
            QMessageBox.warning(self, "Démarrage Sauermann", str(e))

        # b) BRONKHORST — on respecte le port mémorisé (rechargé à l'init) ;
        #    COM7 n'est plus qu'un secours si le champ est vide. _start_scan()
        #    crée un ScanWorker (QThread) : retour immédiat.
        try:
            if not self.bronkhorst_ctrl.ui.input_port.text().strip():
                self.bronkhorst_ctrl.ui.input_port.setText("COM7")
            self.bronkhorst_ctrl._start_scan()
        except Exception as e:
            QMessageBox.warning(self, "Démarrage Bronkhorst", str(e))

        # c) JULABO — même logique : on garde le port mémorisé, COM8 en secours
        #    si le champ est vide, puis on ouvre la liaison série (worker threadé).
        try:
            if not self.julabo_ctrl.ui.linePort.text().strip():
                self.julabo_ctrl.ui.linePort.setText("COM8")
            self.julabo_ctrl._on_connect()
        except Exception as e:
            QMessageBox.warning(self, "Démarrage Julabo", str(e))

        # 3) Invitation à choisir les RDMs (bouton « OK » unique). exec() est
        #    modal et bloquant : la suite ne s'exécute qu'après le clic sur OK.
        info = QMessageBox(self)
        info.setWindowTitle("Sélection des RDMs")
        info.setIcon(QMessageBox.Icon.Information)
        info.setText(
            "Veuillez sélectionner les RDMs à afficher dans l'onglet Bronkhorst")
        info.setStandardButtons(QMessageBox.StandardButton.Ok)
        info.exec()

        # 4) Dès le clic sur OK, on bascule sur l'onglet contenant « Bronkhorst ».
        self._switch_to_tab("Bronkhorst")

    def _switch_to_tab(self, keyword: str) -> bool:
        """Active dans `tabsMain` le premier onglet dont le titre contient
        `keyword` (comparaison insensible à la casse). Renvoie True si un onglet
        correspondant a été trouvé et activé, False sinon (aucune erreur : si
        l'onglet est absent ou détaché, on ne fait rien)."""
        tabs = self.ui.tabsMain
        key  = keyword.lower()
        for i in range(tabs.count()):
            if key in tabs.tabText(i).lower():
                tabs.setCurrentIndex(i)
                return True
        return False

    def _on_global_stop(self):
        """Arrêt global déclenché par btnStop_2 : stoppe proprement les trois
        instruments (et la régulation PID si active), puis réarme btnStart_2.

        Symétrique de _on_global_start. Chaque arrêt est isolé dans son propre
        try/except : l'échec d'un instrument n'empêche pas l'arrêt des autres.
        Les méthodes appelées rejoignent leurs threads avec des temporisations
        bornées (wait avec timeout) : l'IHM ne peut pas se figer durablement.
        """
        # Réarmement immédiat des boutons (anti double-clic) : Stop neutralisé,
        # Start de nouveau disponible pour un prochain démarrage global.
        self.ui.btnStop_2.setEnabled(False)
        self.ui.btnStart_2.setEnabled(True)

        # PID en premier : il consomme la mesure Sauermann et pilote les valves
        # Bronkhorst ; on l'annule avant de couper ces instruments.
        try:
            self.pid_ctrl._on_cancel()
        except Exception as e:
            QMessageBox.warning(self, "Arrêt PID", str(e))

        # a) SAUERMANN — arrête l'AcqWorker et son thread.
        try:
            self.sauermann_ctrl._stop_acquisition()
        except Exception as e:
            QMessageBox.warning(self, "Arrêt Sauermann", str(e))

        # b) BRONKHORST — arrête le scan ET l'acquisition série (threads RS-485).
        try:
            self.bronkhorst_ctrl.cleanup()
        except Exception as e:
            QMessageBox.warning(self, "Arrêt Bronkhorst", str(e))

        # c) JULABO — ferme la liaison série (worker threadé).
        try:
            self.julabo_ctrl._on_disconnect()
        except Exception as e:
            QMessageBox.warning(self, "Arrêt Julabo", str(e))

        self.statusBar().showMessage("Arrêt global effectué.", 3000)

    def closeEvent(self, event):
        """Fermeture propre : on stoppe l'enregistrement CSV (fermeture des
        fichiers) puis les threads des instruments, pour éviter toute perte de
        données."""
        try:
            if getattr(self, "csv_manager", None) is not None:
                self.csv_manager.stop()
        except Exception:
            pass
        for ctrl in ("pid_ctrl", "sauermann_ctrl", "julabo_ctrl", "bronkhorst_ctrl"):
            obj = getattr(self, ctrl, None)
            if obj is not None and hasattr(obj, "cleanup"):
                try:
                    obj.cleanup()
                except Exception:
                    pass
        super().closeEvent(event)

    def _detach_tab(self, index):
        """Reçoit le double-clic et diffère l'action pour ne pas faire planter l'affichage."""
        if index == -1:
            return 
        
        # QTimer.singleShot(0, ...) exécute la fonction juste après la fin du double-clic
        QTimer.singleShot(0, lambda: self._execute_detach(index))

    def _execute_detach(self, index):
        """Effectue le vrai détachement en toute sécurité."""
        if index >= self.ui.tabsMain.count() or index < 0:
            return

        # 1. On récupère widget, titre, icône et position d'origine
        widget = self.ui.tabsMain.widget(index)
        title  = self.ui.tabsMain.tabText(index)
        icon   = self.ui.tabsMain.tabIcon(index)

        # 2. On retire l'onglet du QTabWidget
        self.ui.tabsMain.removeTab(index)

        # 3. On détache du parent Qt
        widget.setParent(None)

        # 4. Création de la fenêtre flottante avec index d'origine
        new_win = DetachedWindow(widget, title, icon, self.ui.tabsMain, index, self)
        self.detached_windows.append(new_win)
        new_win.show()
    # ── Feuille de style globale ──────────────────────────────────────────

    def _apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #F2F2F2;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            QLabel {
                background: transparent;}
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background: #F8F8F8;
            }
            QTabBar::tab {
                background: #E0E0E0;
                border: 1px solid #BBBBBB;
                border-bottom: none;
                border-radius: 4px 4px 0 0;
                padding: 6px 16px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                border-color: #999999;
                color: #0066CC;
            }
            QTabBar::tab:hover:!selected { background: #D4D4D4; }
            QGroupBox {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
                color: #222222;
                font-weight: bold;
            }

            QPushButton {
                background-color: #E1E1E1;
                border: 1px solid #AAAAAA;
                border-radius: 4px;
                padding: 5px 14px;
            }
            QPushButton:hover   { background-color: #D0D0D0; }
            QPushButton:pressed { background-color: #BBBBBB; }
            QPushButton:disabled { color: #999999; }
            QProgressBar {
                border: 1px solid #BBBBBB;
                border-radius: 3px;
                height: 8px;
            }
            QProgressBar::chunk { background-color: #0078D4; border-radius: 3px; }
            QScrollArea { border: none; }
        """)


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()