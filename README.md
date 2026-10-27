# POLARIS 🌌
**Pollutant & Operational Long-term Atmospheric Regulation Instrumental System**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green?logo=qt&logoColor=white)
![Hardware](https://img.shields.io/badge/Hardware-Modbus%20%7C%20Propar%20%7C%20DAQ-orange)
![Status](https://img.shields.io/badge/Status-Deployed-success)

## 📝 Présentation

**POLARIS** est une application logicielle de type SCADA développée en Python, conçue pour la supervision d'instruments industriels et la régulation automatique en boucle fermée. Développé initialement pour l'INERIS, ce système pilote des boucles de dopage de gaz et assure la régulation PID de l'humidité en temps réel.

L'application centralise l'acquisition de données, la communication multi-protocoles avec les équipements physiques, et offre une interface utilisateur (IHM) fluide et non-bloquante capable de fonctionner en continu sur de longues périodes sans perte de performance.

## ✨ Fonctionnalités Clés

- **Supervision Temps Réel :** Tableau de bord interactif pour le suivi des variables physiques (température, humidité, débits gazeux).
- **Régulation PID (Boucle Fermée) :** Algorithme PID intégré pour l'asservissement précis et dynamique de l'humidité relative dans les installations industrielles.
- **Architecture Multithread :** Découplage strict entre l'interface graphique (PySide6) et les processus d'acquisition matérielle (I/O bloquantes) garantissant un taux de rafraîchissement optimal.
- **Communication Multi-Protocoles :** Interfaçage simultané avec divers instruments de mesure et actionneurs via Modbus, Propar, et cartes d'acquisition (DAQ).
- **Visualisation Haute Performance :** Tracé dynamique de milliers de points de données en direct grâce à `pyqtgraph`.
- **Traitement & Enregistrement :** Export des données structurées et traitement à la volée via `NumPy`, `Pandas`, et la bibliothèque native `csv` pour assurer la traçabilité des essais métrologiques.

## 🛠️ Stack Technique

- **Langage Principal :** Python 3
- **Interface Graphique (GUI) :** PySide6 et **Qt Designer** pour la modélisation visuelle des fenêtres (fichiers `.ui`).
- **Visualisation de Données :** pyqtgraph
- **Traitement & Stockage :** NumPy, Pandas, module standard `csv`
- **Communication Matérielle :** 
  * `pyserial` (Liaisons RS-232 / RS-485)
  * `nidaqmx` (Cartes d'acquisition National Instruments)
  * Protocoles industriels : Modbus, Propar

## 🏗️ Architecture Logicielle

Le logiciel repose sur un modèle de conception asynchrone pensé pour la stabilité industrielle :

1. **Couche IHM (Main Thread) :** Gère exclusivement le rendu visuel PySide6 et les interactions utilisateur.
2. **Couche d'Acquisition (Workers/QThread) :** Des threads dédiés interrogent les capteurs (NI DAQ, Modbus) et gèrent la communication série en arrière-plan.
3. **Couche de Régulation (PID Worker) :** Calcule les corrections de commande à appliquer aux actionneurs en fonction de la consigne d'humidité et des retours capteurs.
4. **Signaux/Slots Qt :** Assurent une communication *thread-safe* entre les capteurs matériels et l'interface graphique.

## 📸 Captures d'écran

### Interface de l'application en cours d'exécution
![Tableau de bord de POLARIS](docs/images/dashboard_polaris.png)

### Conception de l'IHM avec Qt Designer
![Vue de la structure UI dans Qt Designer](docs/images/qt_designer_view.png)

## 🚀 Installation & Lancement

### Prérequis
- Python 3.10 ou supérieur
- Pilotes matériels spécifiques (ex: NI-DAQmx si utilisation d'une carte National Instruments)
