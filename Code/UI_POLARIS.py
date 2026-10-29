# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'POLARISxgTZeQ.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

class Ui_PolarisMainWindow(object):
    def setupUi(self, PolarisMainWindow):
        if not PolarisMainWindow.objectName():
            PolarisMainWindow.setObjectName(u"PolarisMainWindow")
        PolarisMainWindow.resize(1190, 818)
        self.centralwidget = QWidget(PolarisMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rootLayout = QVBoxLayout(self.centralwidget)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.tabsMain = QTabWidget(self.centralwidget)
        self.tabsMain.setObjectName(u"tabsMain")
        self.tabsMain.setTabPosition(QTabWidget.TabPosition.North)
        self.tabsMain.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabsMain.setMovable(False)
        self.tabDashboard = QWidget()
        self.tabDashboard.setObjectName(u"tabDashboard")
        self.layoutDashboard = QVBoxLayout(self.tabDashboard)
        self.layoutDashboard.setSpacing(6)
        self.layoutDashboard.setObjectName(u"layoutDashboard")
        self.layoutDashboard.setContentsMargins(8, 8, 8, 8)
        self.topBarLayout_2 = QHBoxLayout()
        self.topBarLayout_2.setSpacing(6)
        self.topBarLayout_2.setObjectName(u"topBarLayout_2")
        self.panelSauermann = QGroupBox(self.tabDashboard)
        self.panelSauermann.setObjectName(u"panelSauermann")
        self.panelSauermann.setMinimumSize(QSize(260, 150))
        self.laySauermann = QVBoxLayout(self.panelSauermann)
        self.laySauermann.setSpacing(4)
        self.laySauermann.setObjectName(u"laySauermann")
        self.gridSauermann = QGridLayout()
        self.gridSauermann.setObjectName(u"gridSauermann")
        self.gridSauermann.setHorizontalSpacing(8)
        self.gridSauermann.setVerticalSpacing(2)
        self.lblSauTempName = QLabel(self.panelSauermann)
        self.lblSauTempName.setObjectName(u"lblSauTempName")

        self.gridSauermann.addWidget(self.lblSauTempName, 0, 0, 1, 1)

        self.lblSauTempVal = QLabel(self.panelSauermann)
        self.lblSauTempVal.setObjectName(u"lblSauTempVal")
        self.lblSauTempVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridSauermann.addWidget(self.lblSauTempVal, 0, 1, 1, 1)

        self.lblSauTempUnit = QLabel(self.panelSauermann)
        self.lblSauTempUnit.setObjectName(u"lblSauTempUnit")

        self.gridSauermann.addWidget(self.lblSauTempUnit, 0, 2, 1, 1)

        self.lblSauVitName = QLabel(self.panelSauermann)
        self.lblSauVitName.setObjectName(u"lblSauVitName")

        self.gridSauermann.addWidget(self.lblSauVitName, 1, 0, 1, 1)

        self.lblSauVitVal = QLabel(self.panelSauermann)
        self.lblSauVitVal.setObjectName(u"lblSauVitVal")
        self.lblSauVitVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridSauermann.addWidget(self.lblSauVitVal, 1, 1, 1, 1)

        self.lblSauVitUnit = QLabel(self.panelSauermann)
        self.lblSauVitUnit.setObjectName(u"lblSauVitUnit")

        self.gridSauermann.addWidget(self.lblSauVitUnit, 1, 2, 1, 1)

        self.lblSauPresName = QLabel(self.panelSauermann)
        self.lblSauPresName.setObjectName(u"lblSauPresName")

        self.gridSauermann.addWidget(self.lblSauPresName, 2, 0, 1, 1)

        self.lblSauPresVal = QLabel(self.panelSauermann)
        self.lblSauPresVal.setObjectName(u"lblSauPresVal")
        self.lblSauPresVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridSauermann.addWidget(self.lblSauPresVal, 2, 1, 1, 1)

        self.lblSauPresUnit = QLabel(self.panelSauermann)
        self.lblSauPresUnit.setObjectName(u"lblSauPresUnit")

        self.gridSauermann.addWidget(self.lblSauPresUnit, 2, 2, 1, 1)

        self.lblSauHumName = QLabel(self.panelSauermann)
        self.lblSauHumName.setObjectName(u"lblSauHumName")

        self.gridSauermann.addWidget(self.lblSauHumName, 3, 0, 1, 1)

        self.lblSauHumVal = QLabel(self.panelSauermann)
        self.lblSauHumVal.setObjectName(u"lblSauHumVal")
        self.lblSauHumVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridSauermann.addWidget(self.lblSauHumVal, 3, 1, 1, 1)

        self.lblSauHumUnit = QLabel(self.panelSauermann)
        self.lblSauHumUnit.setObjectName(u"lblSauHumUnit")

        self.gridSauermann.addWidget(self.lblSauHumUnit, 3, 2, 1, 1)


        self.laySauermann.addLayout(self.gridSauermann)


        self.topBarLayout_2.addWidget(self.panelSauermann)

        self.panelJulabo = QGroupBox(self.tabDashboard)
        self.panelJulabo.setObjectName(u"panelJulabo")
        self.panelJulabo.setMinimumSize(QSize(240, 150))
        self.layJulabo = QVBoxLayout(self.panelJulabo)
        self.layJulabo.setSpacing(4)
        self.layJulabo.setObjectName(u"layJulabo")
        self.gridJulabo = QGridLayout()
        self.gridJulabo.setObjectName(u"gridJulabo")
        self.gridJulabo.setHorizontalSpacing(8)
        self.gridJulabo.setVerticalSpacing(2)
        self.lblJulTintName = QLabel(self.panelJulabo)
        self.lblJulTintName.setObjectName(u"lblJulTintName")

        self.gridJulabo.addWidget(self.lblJulTintName, 0, 0, 1, 1)

        self.lblJulTintVal = QLabel(self.panelJulabo)
        self.lblJulTintVal.setObjectName(u"lblJulTintVal")
        self.lblJulTintVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridJulabo.addWidget(self.lblJulTintVal, 0, 1, 1, 1)

        self.lblJulTintUnit = QLabel(self.panelJulabo)
        self.lblJulTintUnit.setObjectName(u"lblJulTintUnit")

        self.gridJulabo.addWidget(self.lblJulTintUnit, 0, 2, 1, 1)

        self.lblJulTextName = QLabel(self.panelJulabo)
        self.lblJulTextName.setObjectName(u"lblJulTextName")

        self.gridJulabo.addWidget(self.lblJulTextName, 1, 0, 1, 1)

        self.lblJulTextVal = QLabel(self.panelJulabo)
        self.lblJulTextVal.setObjectName(u"lblJulTextVal")
        self.lblJulTextVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridJulabo.addWidget(self.lblJulTextVal, 1, 1, 1, 1)

        self.lblJulTextUnit = QLabel(self.panelJulabo)
        self.lblJulTextUnit.setObjectName(u"lblJulTextUnit")

        self.gridJulabo.addWidget(self.lblJulTextUnit, 1, 2, 1, 1)

        self.lblJulConsName = QLabel(self.panelJulabo)
        self.lblJulConsName.setObjectName(u"lblJulConsName")

        self.gridJulabo.addWidget(self.lblJulConsName, 2, 0, 1, 1)

        self.lblJulConsVal = QLabel(self.panelJulabo)
        self.lblJulConsVal.setObjectName(u"lblJulConsVal")
        self.lblJulConsVal.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridJulabo.addWidget(self.lblJulConsVal, 2, 1, 1, 1)

        self.lblJulConsUnit = QLabel(self.panelJulabo)
        self.lblJulConsUnit.setObjectName(u"lblJulConsUnit")

        self.gridJulabo.addWidget(self.lblJulConsUnit, 2, 2, 1, 1)


        self.layJulabo.addLayout(self.gridJulabo)


        self.topBarLayout_2.addWidget(self.panelJulabo)

        self.panelIndicateurs = QGroupBox(self.tabDashboard)
        self.panelIndicateurs.setObjectName(u"panelIndicateurs")
        self.panelIndicateurs.setMinimumSize(QSize(320, 150))
        self.layIndicateurs = QVBoxLayout(self.panelIndicateurs)
        self.layIndicateurs.setSpacing(4)
        self.layIndicateurs.setObjectName(u"layIndicateurs")
        self.gridLeds = QGridLayout()
        self.gridLeds.setObjectName(u"gridLeds")
        self.gridLeds.setHorizontalSpacing(10)
        self.gridLeds.setVerticalSpacing(4)
        self.lblLedBroName = QLabel(self.panelIndicateurs)
        self.lblLedBroName.setObjectName(u"lblLedBroName")

        self.gridLeds.addWidget(self.lblLedBroName, 1, 0, 1, 1)

        self.ledBronkhorst = QLabel(self.panelIndicateurs)
        self.ledBronkhorst.setObjectName(u"ledBronkhorst")
        self.ledBronkhorst.setMinimumSize(QSize(18, 18))
        self.ledBronkhorst.setMaximumSize(QSize(18, 18))
        self.ledBronkhorst.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:9px;")

        self.gridLeds.addWidget(self.ledBronkhorst, 1, 1, 1, 1)

        self.lblLedSauName = QLabel(self.panelIndicateurs)
        self.lblLedSauName.setObjectName(u"lblLedSauName")

        self.gridLeds.addWidget(self.lblLedSauName, 0, 0, 1, 1)

        self.ledSauermann = QLabel(self.panelIndicateurs)
        self.ledSauermann.setObjectName(u"ledSauermann")
        self.ledSauermann.setMinimumSize(QSize(18, 18))
        self.ledSauermann.setMaximumSize(QSize(18, 18))
        self.ledSauermann.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:9px;")

        self.gridLeds.addWidget(self.ledSauermann, 0, 1, 1, 1)

        self.lblLedJulName = QLabel(self.panelIndicateurs)
        self.lblLedJulName.setObjectName(u"lblLedJulName")

        self.gridLeds.addWidget(self.lblLedJulName, 2, 0, 1, 1)

        self.ledJulabo = QLabel(self.panelIndicateurs)
        self.ledJulabo.setObjectName(u"ledJulabo")
        self.ledJulabo.setMinimumSize(QSize(18, 18))
        self.ledJulabo.setMaximumSize(QSize(18, 18))
        self.ledJulabo.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:9px;")

        self.gridLeds.addWidget(self.ledJulabo, 2, 1, 1, 1)

        self.lblLedPidName = QLabel(self.panelIndicateurs)
        self.lblLedPidName.setObjectName(u"lblLedPidName")

        self.gridLeds.addWidget(self.lblLedPidName, 3, 0, 1, 1)

        self.ledPid = QLabel(self.panelIndicateurs)
        self.ledPid.setObjectName(u"ledPid")
        self.ledPid.setMinimumSize(QSize(18, 18))
        self.ledPid.setMaximumSize(QSize(18, 18))
        self.ledPid.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:9px;")

        self.gridLeds.addWidget(self.ledPid, 3, 1, 1, 1)


        self.layIndicateurs.addLayout(self.gridLeds)


        self.topBarLayout_2.addWidget(self.panelIndicateurs)

        self.panelButtons = QFrame(self.tabDashboard)
        self.panelButtons.setObjectName(u"panelButtons")
        self.panelButtons.setMinimumSize(QSize(180, 150))
        self.panelButtons.setStyleSheet(u"QFrame { background: transparent; border: none; }")
        self.panelButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.layButtons = QVBoxLayout(self.panelButtons)
        self.layButtons.setSpacing(8)
        self.layButtons.setObjectName(u"layButtons")
        self.layStartStop = QHBoxLayout()
        self.layStartStop.setObjectName(u"layStartStop")
        self.btnStart_2 = QPushButton(self.panelButtons)
        self.btnStart_2.setObjectName(u"btnStart_2")

        self.layStartStop.addWidget(self.btnStart_2)

        self.btnStop_2 = QPushButton(self.panelButtons)
        self.btnStop_2.setObjectName(u"btnStop_2")

        self.layStartStop.addWidget(self.btnStop_2)


        self.layButtons.addLayout(self.layStartStop)

        self.btnStartCsv = QPushButton(self.panelButtons)
        self.btnStartCsv.setObjectName(u"btnStartCsv")

        self.layButtons.addWidget(self.btnStartCsv)

        self.btnStopCsv = QPushButton(self.panelButtons)
        self.btnStopCsv.setObjectName(u"btnStopCsv")

        self.layButtons.addWidget(self.btnStopCsv)


        self.topBarLayout_2.addWidget(self.panelButtons)


        self.layoutDashboard.addLayout(self.topBarLayout_2)

        self.mainAreaLayout = QHBoxLayout()
        self.mainAreaLayout.setSpacing(6)
        self.mainAreaLayout.setObjectName(u"mainAreaLayout")
        self.leftColLayout = QVBoxLayout()
        self.leftColLayout.setSpacing(6)
        self.leftColLayout.setObjectName(u"leftColLayout")
        self.panelVoies = QGroupBox(self.tabDashboard)
        self.panelVoies.setObjectName(u"panelVoies")
        self.panelVoies.setMinimumSize(QSize(250, 200))
        self.panelVoies.setMaximumSize(QSize(340, 16777215))
        self.gridVoies = QGridLayout(self.panelVoies)
        self.gridVoies.setObjectName(u"gridVoies")
        self.gridVoies.setHorizontalSpacing(6)
        self.gridVoies.setVerticalSpacing(10)
        self.lblVoie = QLabel(self.panelVoies)
        self.lblVoie.setObjectName(u"lblVoie")

        self.gridVoies.addWidget(self.lblVoie, 0, 0, 1, 1)

        self.lblHdrScale = QLabel(self.panelVoies)
        self.lblHdrScale.setObjectName(u"lblHdrScale")
        self.lblHdrScale.setStyleSheet(u"font-size:8pt; color:#666;")
        self.lblHdrScale.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridVoies.addWidget(self.lblHdrScale, 0, 1, 1, 1)

        self.lblHdrCurve = QLabel(self.panelVoies)
        self.lblHdrCurve.setObjectName(u"lblHdrCurve")
        self.lblHdrCurve.setStyleSheet(u"font-size:8pt; color:#666;")
        self.lblHdrCurve.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridVoies.addWidget(self.lblHdrCurve, 0, 2, 1, 1)

        self.lblHdrColor = QLabel(self.panelVoies)
        self.lblHdrColor.setObjectName(u"lblHdrColor")

        self.gridVoies.addWidget(self.lblHdrColor, 0, 3, 1, 1)

        self.lblHdrSide = QLabel(self.panelVoies)
        self.lblHdrSide.setObjectName(u"lblHdrSide")
        self.lblHdrSide.setStyleSheet(u"font-size:8pt; color:#666;")
        self.lblHdrSide.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridVoies.addWidget(self.lblHdrSide, 0, 4, 1, 1)

        self.lblV1 = QLabel(self.panelVoies)
        self.lblV1.setObjectName(u"lblV1")
        self.lblV1.setStyleSheet(u"font-weight:bold;")

        self.gridVoies.addWidget(self.lblV1, 1, 0, 1, 1)

        self.chkScaleV1 = QCheckBox(self.panelVoies)
        self.chkScaleV1.setObjectName(u"chkScaleV1")
        self.chkScaleV1.setChecked(True)

        self.gridVoies.addWidget(self.chkScaleV1, 1, 1, 1, 1)

        self.chkCurveV1 = QCheckBox(self.panelVoies)
        self.chkCurveV1.setObjectName(u"chkCurveV1")
        self.chkCurveV1.setChecked(True)

        self.gridVoies.addWidget(self.chkCurveV1, 1, 2, 1, 1)

        self.lblColorV1 = QLabel(self.panelVoies)
        self.lblColorV1.setObjectName(u"lblColorV1")
        self.lblColorV1.setMinimumSize(QSize(40, 18))
        self.lblColorV1.setMaximumSize(QSize(50, 18))
        self.lblColorV1.setStyleSheet(u"background:#E67E22; border:1px solid #555; border-radius:3px;")

        self.gridVoies.addWidget(self.lblColorV1, 1, 3, 1, 1)

        self.comboSideV1 = QComboBox(self.panelVoies)
        self.comboSideV1.addItem("")
        self.comboSideV1.addItem("")
        self.comboSideV1.setObjectName(u"comboSideV1")
        self.comboSideV1.setMaximumSize(QSize(80, 16777215))

        self.gridVoies.addWidget(self.comboSideV1, 1, 4, 1, 1)

        self.lblV2 = QLabel(self.panelVoies)
        self.lblV2.setObjectName(u"lblV2")
        self.lblV2.setStyleSheet(u"font-weight:bold;")

        self.gridVoies.addWidget(self.lblV2, 2, 0, 1, 1)

        self.chkScaleV2 = QCheckBox(self.panelVoies)
        self.chkScaleV2.setObjectName(u"chkScaleV2")
        self.chkScaleV2.setChecked(True)

        self.gridVoies.addWidget(self.chkScaleV2, 2, 1, 1, 1)

        self.chkCurveV2 = QCheckBox(self.panelVoies)
        self.chkCurveV2.setObjectName(u"chkCurveV2")
        self.chkCurveV2.setChecked(True)

        self.gridVoies.addWidget(self.chkCurveV2, 2, 2, 1, 1)

        self.lblColorV2 = QLabel(self.panelVoies)
        self.lblColorV2.setObjectName(u"lblColorV2")
        self.lblColorV2.setMinimumSize(QSize(40, 18))
        self.lblColorV2.setMaximumSize(QSize(50, 18))
        self.lblColorV2.setStyleSheet(u"background:#27AE60; border:1px solid #555; border-radius:3px;")

        self.gridVoies.addWidget(self.lblColorV2, 2, 3, 1, 1)

        self.comboSideV2 = QComboBox(self.panelVoies)
        self.comboSideV2.addItem("")
        self.comboSideV2.addItem("")
        self.comboSideV2.setObjectName(u"comboSideV2")
        self.comboSideV2.setMaximumSize(QSize(80, 16777215))

        self.gridVoies.addWidget(self.comboSideV2, 2, 4, 1, 1)

        self.lblV3 = QLabel(self.panelVoies)
        self.lblV3.setObjectName(u"lblV3")
        self.lblV3.setStyleSheet(u"font-weight:bold;")

        self.gridVoies.addWidget(self.lblV3, 3, 0, 1, 1)

        self.chkScaleV3 = QCheckBox(self.panelVoies)
        self.chkScaleV3.setObjectName(u"chkScaleV3")
        self.chkScaleV3.setChecked(True)

        self.gridVoies.addWidget(self.chkScaleV3, 3, 1, 1, 1)

        self.chkCurveV3 = QCheckBox(self.panelVoies)
        self.chkCurveV3.setObjectName(u"chkCurveV3")
        self.chkCurveV3.setChecked(True)

        self.gridVoies.addWidget(self.chkCurveV3, 3, 2, 1, 1)

        self.lblColorV3 = QLabel(self.panelVoies)
        self.lblColorV3.setObjectName(u"lblColorV3")
        self.lblColorV3.setMinimumSize(QSize(40, 18))
        self.lblColorV3.setMaximumSize(QSize(50, 18))
        self.lblColorV3.setStyleSheet(u"background:#3498DB; border:1px solid #555; border-radius:3px;")

        self.gridVoies.addWidget(self.lblColorV3, 3, 3, 1, 1)

        self.comboSideV3 = QComboBox(self.panelVoies)
        self.comboSideV3.addItem("")
        self.comboSideV3.addItem("")
        self.comboSideV3.setObjectName(u"comboSideV3")
        self.comboSideV3.setMaximumSize(QSize(80, 16777215))

        self.gridVoies.addWidget(self.comboSideV3, 3, 4, 1, 1)

        self.lblV4 = QLabel(self.panelVoies)
        self.lblV4.setObjectName(u"lblV4")
        self.lblV4.setStyleSheet(u"font-weight:bold;")

        self.gridVoies.addWidget(self.lblV4, 4, 0, 1, 1)

        self.chkScaleV4 = QCheckBox(self.panelVoies)
        self.chkScaleV4.setObjectName(u"chkScaleV4")
        self.chkScaleV4.setChecked(True)

        self.gridVoies.addWidget(self.chkScaleV4, 4, 1, 1, 1)

        self.chkCurveV4 = QCheckBox(self.panelVoies)
        self.chkCurveV4.setObjectName(u"chkCurveV4")
        self.chkCurveV4.setChecked(True)

        self.gridVoies.addWidget(self.chkCurveV4, 4, 2, 1, 1)

        self.lblColorV4 = QLabel(self.panelVoies)
        self.lblColorV4.setObjectName(u"lblColorV4")
        self.lblColorV4.setMinimumSize(QSize(40, 18))
        self.lblColorV4.setMaximumSize(QSize(50, 18))
        self.lblColorV4.setStyleSheet(u"background:#E74C3C; border:1px solid #555; border-radius:3px;")

        self.gridVoies.addWidget(self.lblColorV4, 4, 3, 1, 1)

        self.comboSideV4 = QComboBox(self.panelVoies)
        self.comboSideV4.addItem("")
        self.comboSideV4.addItem("")
        self.comboSideV4.setObjectName(u"comboSideV4")
        self.comboSideV4.setMaximumSize(QSize(80, 16777215))

        self.gridVoies.addWidget(self.comboSideV4, 4, 4, 1, 1)

        self.lblVTint = QLabel(self.panelVoies)
        self.lblVTint.setObjectName(u"lblVTint")
        self.lblVTint.setStyleSheet(u"font-weight:bold;")

        self.gridVoies.addWidget(self.lblVTint, 5, 0, 1, 1)

        self.chkScaleTint = QCheckBox(self.panelVoies)
        self.chkScaleTint.setObjectName(u"chkScaleTint")
        self.chkScaleTint.setChecked(True)

        self.gridVoies.addWidget(self.chkScaleTint, 5, 1, 1, 1)

        self.chkCurveTint = QCheckBox(self.panelVoies)
        self.chkCurveTint.setObjectName(u"chkCurveTint")
        self.chkCurveTint.setChecked(True)

        self.gridVoies.addWidget(self.chkCurveTint, 5, 2, 1, 1)

        self.lblColorTint = QLabel(self.panelVoies)
        self.lblColorTint.setObjectName(u"lblColorTint")
        self.lblColorTint.setMinimumSize(QSize(40, 18))
        self.lblColorTint.setMaximumSize(QSize(50, 18))
        self.lblColorTint.setStyleSheet(u"background:#9B59B6; border:1px solid #555; border-radius:3px;")

        self.gridVoies.addWidget(self.lblColorTint, 5, 3, 1, 1)

        self.comboSideTint = QComboBox(self.panelVoies)
        self.comboSideTint.addItem("")
        self.comboSideTint.addItem("")
        self.comboSideTint.setObjectName(u"comboSideTint")
        self.comboSideTint.setMaximumSize(QSize(80, 16777215))

        self.gridVoies.addWidget(self.comboSideTint, 5, 4, 1, 1)

        self.lblVText = QLabel(self.panelVoies)
        self.lblVText.setObjectName(u"lblVText")
        self.lblVText.setStyleSheet(u"font-weight:bold;")

        self.gridVoies.addWidget(self.lblVText, 6, 0, 1, 1)

        self.chkScaleText = QCheckBox(self.panelVoies)
        self.chkScaleText.setObjectName(u"chkScaleText")
        self.chkScaleText.setChecked(True)

        self.gridVoies.addWidget(self.chkScaleText, 6, 1, 1, 1)

        self.chkCurveText = QCheckBox(self.panelVoies)
        self.chkCurveText.setObjectName(u"chkCurveText")
        self.chkCurveText.setChecked(True)

        self.gridVoies.addWidget(self.chkCurveText, 6, 2, 1, 1)

        self.lblColorText = QLabel(self.panelVoies)
        self.lblColorText.setObjectName(u"lblColorText")
        self.lblColorText.setMinimumSize(QSize(40, 18))
        self.lblColorText.setMaximumSize(QSize(50, 18))
        self.lblColorText.setStyleSheet(u"background:#16A085; border:1px solid #555; border-radius:3px;")

        self.gridVoies.addWidget(self.lblColorText, 6, 3, 1, 1)

        self.comboSideText = QComboBox(self.panelVoies)
        self.comboSideText.addItem("")
        self.comboSideText.addItem("")
        self.comboSideText.setObjectName(u"comboSideText")
        self.comboSideText.setMaximumSize(QSize(80, 16777215))

        self.gridVoies.addWidget(self.comboSideText, 6, 4, 1, 1)

        self.spacerVoies = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridVoies.addItem(self.spacerVoies, 7, 0, 1, 5)


        self.leftColLayout.addWidget(self.panelVoies)

        self.panelAnalyseurs = QGroupBox(self.tabDashboard)
        self.panelAnalyseurs.setObjectName(u"panelAnalyseurs")
        self.panelAnalyseurs.setMinimumSize(QSize(180, 200))
        self.panelAnalyseurs.setMaximumSize(QSize(220, 16777215))
        self.layAnalyseurs = QVBoxLayout(self.panelAnalyseurs)
        self.layAnalyseurs.setObjectName(u"layAnalyseurs")
        self.spacerAnalyseurs = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layAnalyseurs.addItem(self.spacerAnalyseurs)


        self.leftColLayout.addWidget(self.panelAnalyseurs)


        self.mainAreaLayout.addLayout(self.leftColLayout)

        self.panelGraph = QFrame(self.tabDashboard)
        self.panelGraph.setObjectName(u"panelGraph")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panelGraph.sizePolicy().hasHeightForWidth())
        self.panelGraph.setSizePolicy(sizePolicy)
        self.panelGraph.setMinimumSize(QSize(600, 400))
        self.panelGraph.setFrameShape(QFrame.Shape.StyledPanel)
        self.layGraph = QVBoxLayout(self.panelGraph)
        self.layGraph.setObjectName(u"layGraph")
        self.lblDashCross = QLabel(self.panelGraph)
        self.lblDashCross.setObjectName(u"lblDashCross")
        self.lblDashCross.setStyleSheet(u"color:#555; font-size:9pt; padding:2px;")

        self.layGraph.addWidget(self.lblDashCross)

        self.lblGraphPlaceholder = QLabel(self.panelGraph)
        self.lblGraphPlaceholder.setObjectName(u"lblGraphPlaceholder")
        self.lblGraphPlaceholder.setStyleSheet(u"color:#999; font-style:italic; font-size:14pt;")
        self.lblGraphPlaceholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layGraph.addWidget(self.lblGraphPlaceholder)


        self.mainAreaLayout.addWidget(self.panelGraph)

        self.rightColLayout = QVBoxLayout()
        self.rightColLayout.setSpacing(6)
        self.rightColLayout.setObjectName(u"rightColLayout")
        self.panelLog = QGroupBox(self.tabDashboard)
        self.panelLog.setObjectName(u"panelLog")
        self.panelLog.setMinimumSize(QSize(240, 200))
        self.panelLog.setMaximumSize(QSize(320, 16777215))
        self.layLog = QVBoxLayout(self.panelLog)
        self.layLog.setObjectName(u"layLog")
        self.spacerLog = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layLog.addItem(self.spacerLog)


        self.rightColLayout.addWidget(self.panelLog)

        self.panelRdms = QGroupBox(self.tabDashboard)
        self.panelRdms.setObjectName(u"panelRdms")
        self.panelRdms.setMinimumSize(QSize(240, 160))
        self.panelRdms.setMaximumSize(QSize(340, 16777215))
        self.layRdms = QVBoxLayout(self.panelRdms)
        self.layRdms.setSpacing(4)
        self.layRdms.setObjectName(u"layRdms")
        self.lblSectLiq = QLabel(self.panelRdms)
        self.lblSectLiq.setObjectName(u"lblSectLiq")
        self.lblSectLiq.setStyleSheet(u"font-weight:bold; margin-top:4px;")

        self.layRdms.addWidget(self.lblSectLiq)

        self.gridLiq = QGridLayout()
        self.gridLiq.setObjectName(u"gridLiq")
        self.gridLiq.setHorizontalSpacing(12)
        self.gridLiq.setVerticalSpacing(2)
        self.lblRdmNum1 = QLabel(self.panelRdms)
        self.lblRdmNum1.setObjectName(u"lblRdmNum1")
        self.lblRdmNum1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.lblRdmNum1, 0, 0, 1, 1)

        self.lblRdmNum2 = QLabel(self.panelRdms)
        self.lblRdmNum2.setObjectName(u"lblRdmNum2")
        self.lblRdmNum2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.lblRdmNum2, 0, 1, 1, 1)

        self.lblRdmNum3 = QLabel(self.panelRdms)
        self.lblRdmNum3.setObjectName(u"lblRdmNum3")
        self.lblRdmNum3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.lblRdmNum3, 0, 2, 1, 1)

        self.lblRdmNum4 = QLabel(self.panelRdms)
        self.lblRdmNum4.setObjectName(u"lblRdmNum4")
        self.lblRdmNum4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.lblRdmNum4, 0, 3, 1, 1)

        self.ledRdm1 = QLabel(self.panelRdms)
        self.ledRdm1.setObjectName(u"ledRdm1")
        self.ledRdm1.setMinimumSize(QSize(20, 20))
        self.ledRdm1.setMaximumSize(QSize(20, 20))
        self.ledRdm1.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.ledRdm1, 1, 0, 1, 1)

        self.ledRdm2 = QLabel(self.panelRdms)
        self.ledRdm2.setObjectName(u"ledRdm2")
        self.ledRdm2.setMinimumSize(QSize(20, 20))
        self.ledRdm2.setMaximumSize(QSize(20, 20))
        self.ledRdm2.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.ledRdm2, 1, 1, 1, 1)

        self.ledRdm3 = QLabel(self.panelRdms)
        self.ledRdm3.setObjectName(u"ledRdm3")
        self.ledRdm3.setMinimumSize(QSize(20, 20))
        self.ledRdm3.setMaximumSize(QSize(20, 20))
        self.ledRdm3.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.ledRdm3, 1, 2, 1, 1)

        self.ledRdm4 = QLabel(self.panelRdms)
        self.ledRdm4.setObjectName(u"ledRdm4")
        self.ledRdm4.setMinimumSize(QSize(20, 20))
        self.ledRdm4.setMaximumSize(QSize(20, 20))
        self.ledRdm4.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLiq.addWidget(self.ledRdm4, 1, 3, 1, 1)


        self.layRdms.addLayout(self.gridLiq)

        self.lblSectHum = QLabel(self.panelRdms)
        self.lblSectHum.setObjectName(u"lblSectHum")
        self.lblSectHum.setStyleSheet(u"font-weight:bold; margin-top:4px;")

        self.layRdms.addWidget(self.lblSectHum)

        self.gridHum = QGridLayout()
        self.gridHum.setObjectName(u"gridHum")
        self.gridHum.setHorizontalSpacing(12)
        self.gridHum.setVerticalSpacing(2)
        self.lblRdmNum5 = QLabel(self.panelRdms)
        self.lblRdmNum5.setObjectName(u"lblRdmNum5")
        self.lblRdmNum5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.lblRdmNum5, 0, 0, 1, 1)

        self.lblRdmNum6 = QLabel(self.panelRdms)
        self.lblRdmNum6.setObjectName(u"lblRdmNum6")
        self.lblRdmNum6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.lblRdmNum6, 0, 1, 1, 1)

        self.lblRdmNum7 = QLabel(self.panelRdms)
        self.lblRdmNum7.setObjectName(u"lblRdmNum7")
        self.lblRdmNum7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.lblRdmNum7, 0, 2, 1, 1)

        self.lblRdmNum8 = QLabel(self.panelRdms)
        self.lblRdmNum8.setObjectName(u"lblRdmNum8")
        self.lblRdmNum8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.lblRdmNum8, 0, 3, 1, 1)

        self.ledRdm5 = QLabel(self.panelRdms)
        self.ledRdm5.setObjectName(u"ledRdm5")
        self.ledRdm5.setMinimumSize(QSize(20, 20))
        self.ledRdm5.setMaximumSize(QSize(20, 20))
        self.ledRdm5.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.ledRdm5, 1, 0, 1, 1)

        self.ledRdm6 = QLabel(self.panelRdms)
        self.ledRdm6.setObjectName(u"ledRdm6")
        self.ledRdm6.setMinimumSize(QSize(20, 20))
        self.ledRdm6.setMaximumSize(QSize(20, 20))
        self.ledRdm6.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.ledRdm6, 1, 1, 1, 1)

        self.ledRdm7 = QLabel(self.panelRdms)
        self.ledRdm7.setObjectName(u"ledRdm7")
        self.ledRdm7.setMinimumSize(QSize(20, 20))
        self.ledRdm7.setMaximumSize(QSize(20, 20))
        self.ledRdm7.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.ledRdm7, 1, 2, 1, 1)

        self.ledRdm8 = QLabel(self.panelRdms)
        self.ledRdm8.setObjectName(u"ledRdm8")
        self.ledRdm8.setMinimumSize(QSize(20, 20))
        self.ledRdm8.setMaximumSize(QSize(20, 20))
        self.ledRdm8.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridHum.addWidget(self.ledRdm8, 1, 3, 1, 1)


        self.layRdms.addLayout(self.gridHum)

        self.lblSectGaz = QLabel(self.panelRdms)
        self.lblSectGaz.setObjectName(u"lblSectGaz")
        self.lblSectGaz.setStyleSheet(u"font-weight:bold; margin-top:4px;")

        self.layRdms.addWidget(self.lblSectGaz)

        self.gridGaz = QGridLayout()
        self.gridGaz.setObjectName(u"gridGaz")
        self.gridGaz.setHorizontalSpacing(12)
        self.gridGaz.setVerticalSpacing(2)
        self.lblRdmNum9 = QLabel(self.panelRdms)
        self.lblRdmNum9.setObjectName(u"lblRdmNum9")
        self.lblRdmNum9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.lblRdmNum9, 0, 0, 1, 1)

        self.lblRdmNum10 = QLabel(self.panelRdms)
        self.lblRdmNum10.setObjectName(u"lblRdmNum10")
        self.lblRdmNum10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.lblRdmNum10, 0, 1, 1, 1)

        self.lblRdmNum11 = QLabel(self.panelRdms)
        self.lblRdmNum11.setObjectName(u"lblRdmNum11")
        self.lblRdmNum11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.lblRdmNum11, 0, 2, 1, 1)

        self.lblRdmNum12 = QLabel(self.panelRdms)
        self.lblRdmNum12.setObjectName(u"lblRdmNum12")
        self.lblRdmNum12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.lblRdmNum12, 0, 3, 1, 1)

        self.ledRdm9 = QLabel(self.panelRdms)
        self.ledRdm9.setObjectName(u"ledRdm9")
        self.ledRdm9.setMinimumSize(QSize(20, 20))
        self.ledRdm9.setMaximumSize(QSize(20, 20))
        self.ledRdm9.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.ledRdm9, 1, 0, 1, 1)

        self.ledRdm10 = QLabel(self.panelRdms)
        self.ledRdm10.setObjectName(u"ledRdm10")
        self.ledRdm10.setMinimumSize(QSize(20, 20))
        self.ledRdm10.setMaximumSize(QSize(20, 20))
        self.ledRdm10.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.ledRdm10, 1, 1, 1, 1)

        self.ledRdm11 = QLabel(self.panelRdms)
        self.ledRdm11.setObjectName(u"ledRdm11")
        self.ledRdm11.setMinimumSize(QSize(20, 20))
        self.ledRdm11.setMaximumSize(QSize(20, 20))
        self.ledRdm11.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.ledRdm11, 1, 2, 1, 1)

        self.ledRdm12 = QLabel(self.panelRdms)
        self.ledRdm12.setObjectName(u"ledRdm12")
        self.ledRdm12.setMinimumSize(QSize(20, 20))
        self.ledRdm12.setMaximumSize(QSize(20, 20))
        self.ledRdm12.setStyleSheet(u"background:#bbb; border:1px solid #555; border-radius:10px;")
        self.ledRdm12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridGaz.addWidget(self.ledRdm12, 1, 3, 1, 1)


        self.layRdms.addLayout(self.gridGaz)


        self.rightColLayout.addWidget(self.panelRdms)


        self.mainAreaLayout.addLayout(self.rightColLayout)


        self.layoutDashboard.addLayout(self.mainAreaLayout)

        self.tabsMain.addTab(self.tabDashboard, "")
        self.tabSauermann = QWidget()
        self.tabSauermann.setObjectName(u"tabSauermann")
        self.layoutSauermann = QVBoxLayout(self.tabSauermann)
        self.layoutSauermann.setSpacing(4)
        self.layoutSauermann.setObjectName(u"layoutSauermann")
        self.layoutSauermann.setContentsMargins(6, 6, 6, 6)
        self.topBarLayout = QHBoxLayout()
        self.topBarLayout.setObjectName(u"topBarLayout")
        self.lblDate = QLabel(self.tabSauermann)
        self.lblDate.setObjectName(u"lblDate")

        self.topBarLayout.addWidget(self.lblDate)

        self.spacerTopBar = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.topBarLayout.addItem(self.spacerTopBar)

        self.lblAcqLed = QLabel(self.tabSauermann)
        self.lblAcqLed.setObjectName(u"lblAcqLed")
        self.lblAcqLed.setMinimumSize(QSize(18, 18))
        self.lblAcqLed.setMaximumSize(QSize(18, 18))

        self.topBarLayout.addWidget(self.lblAcqLed)

        self.lblAcqStatus = QLabel(self.tabSauermann)
        self.lblAcqStatus.setObjectName(u"lblAcqStatus")

        self.topBarLayout.addWidget(self.lblAcqStatus)

        self.lblRecLed = QLabel(self.tabSauermann)
        self.lblRecLed.setObjectName(u"lblRecLed")
        self.lblRecLed.setMinimumSize(QSize(18, 18))
        self.lblRecLed.setMaximumSize(QSize(18, 18))

        self.topBarLayout.addWidget(self.lblRecLed)

        self.lblRecStatus = QLabel(self.tabSauermann)
        self.lblRecStatus.setObjectName(u"lblRecStatus")

        self.topBarLayout.addWidget(self.lblRecStatus)


        self.layoutSauermann.addLayout(self.topBarLayout)

        self.groupAcq = QGroupBox(self.tabSauermann)
        self.groupAcq.setObjectName(u"groupAcq")
        self.gridAcq = QGridLayout(self.groupAcq)
        self.gridAcq.setObjectName(u"gridAcq")
        self.lblFsLabel = QLabel(self.groupAcq)
        self.lblFsLabel.setObjectName(u"lblFsLabel")

        self.gridAcq.addWidget(self.lblFsLabel, 0, 0, 1, 1)

        self.spinFs = QDoubleSpinBox(self.groupAcq)
        self.spinFs.setObjectName(u"spinFs")
        self.spinFs.setDecimals(1)
        self.spinFs.setMinimum(10.000000000000000)
        self.spinFs.setMaximum(50000.000000000000000)
        self.spinFs.setValue(20.000000000000000)

        self.gridAcq.addWidget(self.spinFs, 0, 1, 1, 1)

        self.comboFsUnit = QComboBox(self.groupAcq)
        self.comboFsUnit.addItem("")
        self.comboFsUnit.setObjectName(u"comboFsUnit")

        self.gridAcq.addWidget(self.comboFsUnit, 0, 2, 1, 1)

        self.lblBlocLabel = QLabel(self.groupAcq)
        self.lblBlocLabel.setObjectName(u"lblBlocLabel")

        self.gridAcq.addWidget(self.lblBlocLabel, 1, 0, 1, 1)

        self.spinBlocSec = QDoubleSpinBox(self.groupAcq)
        self.spinBlocSec.setObjectName(u"spinBlocSec")
        self.spinBlocSec.setDecimals(0)
        self.spinBlocSec.setMinimum(1.000000000000000)
        self.spinBlocSec.setMaximum(6000.000000000000000)
        self.spinBlocSec.setValue(2.000000000000000)

        self.gridAcq.addWidget(self.spinBlocSec, 1, 1, 1, 1)

        self.comboDispUnit = QComboBox(self.groupAcq)
        self.comboDispUnit.addItem("")
        self.comboDispUnit.addItem("")
        self.comboDispUnit.setObjectName(u"comboDispUnit")

        self.gridAcq.addWidget(self.comboDispUnit, 1, 2, 1, 1)

        self.lblModeLabel = QLabel(self.groupAcq)
        self.lblModeLabel.setObjectName(u"lblModeLabel")

        self.gridAcq.addWidget(self.lblModeLabel, 2, 0, 1, 1)

        self.comboGraphMode = QComboBox(self.groupAcq)
        self.comboGraphMode.addItem("")
        self.comboGraphMode.addItem("")
        self.comboGraphMode.setObjectName(u"comboGraphMode")

        self.gridAcq.addWidget(self.comboGraphMode, 2, 1, 1, 1)

        self.lblRollingLabel = QLabel(self.groupAcq)
        self.lblRollingLabel.setObjectName(u"lblRollingLabel")

        self.gridAcq.addWidget(self.lblRollingLabel, 2, 2, 1, 1)

        self.spinRollingSec = QDoubleSpinBox(self.groupAcq)
        self.spinRollingSec.setObjectName(u"spinRollingSec")
        self.spinRollingSec.setDecimals(1)
        self.spinRollingSec.setMinimum(5.000000000000000)
        self.spinRollingSec.setMaximum(86400.000000000000000)
        self.spinRollingSec.setValue(600.000000000000000)

        self.gridAcq.addWidget(self.spinRollingSec, 2, 3, 1, 1)

        self.comboRollingUnit = QComboBox(self.groupAcq)
        self.comboRollingUnit.addItem("")
        self.comboRollingUnit.addItem("")
        self.comboRollingUnit.addItem("")
        self.comboRollingUnit.setObjectName(u"comboRollingUnit")

        self.gridAcq.addWidget(self.comboRollingUnit, 2, 4, 1, 1)


        self.layoutSauermann.addWidget(self.groupAcq)

        self.midLayout = QHBoxLayout()
        self.midLayout.setObjectName(u"midLayout")
        self.sidebarLayout = QVBoxLayout()
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.group0 = QGroupBox(self.tabSauermann)
        self.group0.setObjectName(u"group0")
        self.gridGroup0 = QGridLayout(self.group0)
        self.gridGroup0.setObjectName(u"gridGroup0")
        self.lblName0 = QLabel(self.group0)
        self.lblName0.setObjectName(u"lblName0")

        self.gridGroup0.addWidget(self.lblName0, 0, 0, 1, 1)

        self.lblValue0 = QLabel(self.group0)
        self.lblValue0.setObjectName(u"lblValue0")
        font = QFont()
        font.setBold(True)
        self.lblValue0.setFont(font)

        self.gridGroup0.addWidget(self.lblValue0, 0, 1, 1, 1)

        self.lblUnit0 = QLabel(self.group0)
        self.lblUnit0.setObjectName(u"lblUnit0")

        self.gridGroup0.addWidget(self.lblUnit0, 0, 3, 1, 1)

        self.lblName0_2 = QLabel(self.group0)
        self.lblName0_2.setObjectName(u"lblName0_2")

        self.gridGroup0.addWidget(self.lblName0_2, 1, 0, 1, 2)

        self.lblValueCorr0 = QLabel(self.group0)
        self.lblValueCorr0.setObjectName(u"lblValueCorr0")
        self.lblValueCorr0.setFont(font)

        self.gridGroup0.addWidget(self.lblValueCorr0, 1, 2, 1, 1)

        self.lblUnit0_2 = QLabel(self.group0)
        self.lblUnit0_2.setObjectName(u"lblUnit0_2")

        self.gridGroup0.addWidget(self.lblUnit0_2, 1, 3, 1, 1)

        self.btnColor0 = QPushButton(self.group0)
        self.btnColor0.setObjectName(u"btnColor0")

        self.gridGroup0.addWidget(self.btnColor0, 2, 0, 1, 4)


        self.sidebarLayout.addWidget(self.group0)

        self.group1 = QGroupBox(self.tabSauermann)
        self.group1.setObjectName(u"group1")
        self.gridGroup1 = QGridLayout(self.group1)
        self.gridGroup1.setObjectName(u"gridGroup1")
        self.lblName1 = QLabel(self.group1)
        self.lblName1.setObjectName(u"lblName1")

        self.gridGroup1.addWidget(self.lblName1, 0, 0, 1, 1)

        self.lblValue1 = QLabel(self.group1)
        self.lblValue1.setObjectName(u"lblValue1")
        self.lblValue1.setFont(font)

        self.gridGroup1.addWidget(self.lblValue1, 0, 1, 1, 1)

        self.lblUnit1 = QLabel(self.group1)
        self.lblUnit1.setObjectName(u"lblUnit1")

        self.gridGroup1.addWidget(self.lblUnit1, 0, 3, 1, 1)

        self.lblName1_2 = QLabel(self.group1)
        self.lblName1_2.setObjectName(u"lblName1_2")

        self.gridGroup1.addWidget(self.lblName1_2, 1, 0, 1, 2)

        self.lblValueCorr1 = QLabel(self.group1)
        self.lblValueCorr1.setObjectName(u"lblValueCorr1")
        self.lblValueCorr1.setFont(font)

        self.gridGroup1.addWidget(self.lblValueCorr1, 1, 2, 1, 1)

        self.lblUnit1_2 = QLabel(self.group1)
        self.lblUnit1_2.setObjectName(u"lblUnit1_2")

        self.gridGroup1.addWidget(self.lblUnit1_2, 1, 3, 1, 1)

        self.btnColor1 = QPushButton(self.group1)
        self.btnColor1.setObjectName(u"btnColor1")

        self.gridGroup1.addWidget(self.btnColor1, 2, 0, 1, 4)


        self.sidebarLayout.addWidget(self.group1)

        self.group2 = QGroupBox(self.tabSauermann)
        self.group2.setObjectName(u"group2")
        self.gridGroup2 = QGridLayout(self.group2)
        self.gridGroup2.setObjectName(u"gridGroup2")
        self.lblName2 = QLabel(self.group2)
        self.lblName2.setObjectName(u"lblName2")

        self.gridGroup2.addWidget(self.lblName2, 0, 0, 1, 1)

        self.lblValue2 = QLabel(self.group2)
        self.lblValue2.setObjectName(u"lblValue2")
        self.lblValue2.setFont(font)

        self.gridGroup2.addWidget(self.lblValue2, 0, 1, 1, 1)

        self.lblUnit2 = QLabel(self.group2)
        self.lblUnit2.setObjectName(u"lblUnit2")

        self.gridGroup2.addWidget(self.lblUnit2, 0, 3, 1, 1)

        self.lblName2_2 = QLabel(self.group2)
        self.lblName2_2.setObjectName(u"lblName2_2")

        self.gridGroup2.addWidget(self.lblName2_2, 1, 0, 1, 2)

        self.lblValueCorr2 = QLabel(self.group2)
        self.lblValueCorr2.setObjectName(u"lblValueCorr2")
        self.lblValueCorr2.setFont(font)

        self.gridGroup2.addWidget(self.lblValueCorr2, 1, 2, 1, 1)

        self.lblUnit2_2 = QLabel(self.group2)
        self.lblUnit2_2.setObjectName(u"lblUnit2_2")

        self.gridGroup2.addWidget(self.lblUnit2_2, 1, 3, 1, 1)

        self.btnColor2 = QPushButton(self.group2)
        self.btnColor2.setObjectName(u"btnColor2")

        self.gridGroup2.addWidget(self.btnColor2, 2, 0, 1, 4)


        self.sidebarLayout.addWidget(self.group2)

        self.group3 = QGroupBox(self.tabSauermann)
        self.group3.setObjectName(u"group3")
        self.gridGroup3 = QGridLayout(self.group3)
        self.gridGroup3.setObjectName(u"gridGroup3")
        self.lblName3 = QLabel(self.group3)
        self.lblName3.setObjectName(u"lblName3")

        self.gridGroup3.addWidget(self.lblName3, 0, 0, 1, 1)

        self.lblValue3 = QLabel(self.group3)
        self.lblValue3.setObjectName(u"lblValue3")
        self.lblValue3.setFont(font)

        self.gridGroup3.addWidget(self.lblValue3, 0, 1, 1, 1)

        self.lblUnit3 = QLabel(self.group3)
        self.lblUnit3.setObjectName(u"lblUnit3")

        self.gridGroup3.addWidget(self.lblUnit3, 0, 3, 1, 1)

        self.lblName3_2 = QLabel(self.group3)
        self.lblName3_2.setObjectName(u"lblName3_2")

        self.gridGroup3.addWidget(self.lblName3_2, 1, 0, 1, 2)

        self.lblValueCorr3 = QLabel(self.group3)
        self.lblValueCorr3.setObjectName(u"lblValueCorr3")
        self.lblValueCorr3.setFont(font)

        self.gridGroup3.addWidget(self.lblValueCorr3, 1, 2, 1, 1)

        self.lblUnit3_2 = QLabel(self.group3)
        self.lblUnit3_2.setObjectName(u"lblUnit3_2")

        self.gridGroup3.addWidget(self.lblUnit3_2, 1, 3, 1, 1)

        self.btnColor3 = QPushButton(self.group3)
        self.btnColor3.setObjectName(u"btnColor3")

        self.gridGroup3.addWidget(self.btnColor3, 2, 0, 1, 4)


        self.sidebarLayout.addWidget(self.group3)


        self.midLayout.addLayout(self.sidebarLayout)

        self.groupGraph = QGroupBox(self.tabSauermann)
        self.groupGraph.setObjectName(u"groupGraph")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.groupGraph.sizePolicy().hasHeightForWidth())
        self.groupGraph.setSizePolicy(sizePolicy1)
        self.layoutGroupGraph = QVBoxLayout(self.groupGraph)
        self.layoutGroupGraph.setObjectName(u"layoutGroupGraph")
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.setObjectName(u"toolbarLayout")
        self.btnFollow = QToolButton(self.groupGraph)
        self.btnFollow.setObjectName(u"btnFollow")
        self.btnFollow.setCheckable(True)
        self.btnFollow.setChecked(True)

        self.toolbarLayout.addWidget(self.btnFollow)

        self.spacerToolbar = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarLayout.addItem(self.spacerToolbar)

        self.btnSaveImage = QPushButton(self.groupGraph)
        self.btnSaveImage.setObjectName(u"btnSaveImage")

        self.toolbarLayout.addWidget(self.btnSaveImage)


        self.layoutGroupGraph.addLayout(self.toolbarLayout)

        self.plotContainerMain = QWidget(self.groupGraph)
        self.plotContainerMain.setObjectName(u"plotContainerMain")
        sizePolicy1.setHeightForWidth(self.plotContainerMain.sizePolicy().hasHeightForWidth())
        self.plotContainerMain.setSizePolicy(sizePolicy1)

        self.layoutGroupGraph.addWidget(self.plotContainerMain)


        self.midLayout.addWidget(self.groupGraph)


        self.layoutSauermann.addLayout(self.midLayout)

        self.lblCross = QLabel(self.tabSauermann)
        self.lblCross.setObjectName(u"lblCross")

        self.layoutSauermann.addWidget(self.lblCross)

        self.tabsMain.addTab(self.tabSauermann, "")
        self.tabSettings = QWidget()
        self.tabSettings.setObjectName(u"tabSettings")
        self.layoutReglages = QVBoxLayout(self.tabSettings)
        self.layoutReglages.setObjectName(u"layoutReglages")
        self.layoutReglages.setContentsMargins(8, 8, 8, 8)
        self.scrollReglages = QScrollArea(self.tabSettings)
        self.scrollReglages.setObjectName(u"scrollReglages")
        self.scrollReglages.setWidgetResizable(True)
        self.scrollReglagesContents = QWidget()
        self.scrollReglagesContents.setObjectName(u"scrollReglagesContents")
        self.scrollReglagesContents.setGeometry(QRect(0, 0, 1104, 703))
        self.layoutScrollReglages = QVBoxLayout(self.scrollReglagesContents)
        self.layoutScrollReglages.setObjectName(u"layoutScrollReglages")
        self.groupParamMeta = QGroupBox(self.scrollReglagesContents)
        self.groupParamMeta.setObjectName(u"groupParamMeta")
        self.gridParamMeta = QGridLayout(self.groupParamMeta)
        self.gridParamMeta.setObjectName(u"gridParamMeta")
        self.lblHdrVoie0 = QLabel(self.groupParamMeta)
        self.lblHdrVoie0.setObjectName(u"lblHdrVoie0")

        self.gridParamMeta.addWidget(self.lblHdrVoie0, 0, 0, 1, 1)

        self.lblHdrNom = QLabel(self.groupParamMeta)
        self.lblHdrNom.setObjectName(u"lblHdrNom")

        self.gridParamMeta.addWidget(self.lblHdrNom, 0, 1, 1, 1)

        self.lblHdrUnit = QLabel(self.groupParamMeta)
        self.lblHdrUnit.setObjectName(u"lblHdrUnit")

        self.gridParamMeta.addWidget(self.lblHdrUnit, 0, 2, 1, 1)

        self.lblHdrMin = QLabel(self.groupParamMeta)
        self.lblHdrMin.setObjectName(u"lblHdrMin")

        self.gridParamMeta.addWidget(self.lblHdrMin, 0, 3, 1, 1)

        self.lblHdrMax = QLabel(self.groupParamMeta)
        self.lblHdrMax.setObjectName(u"lblHdrMax")

        self.gridParamMeta.addWidget(self.lblHdrMax, 0, 4, 1, 1)

        self.lblPVoie0 = QLabel(self.groupParamMeta)
        self.lblPVoie0.setObjectName(u"lblPVoie0")

        self.gridParamMeta.addWidget(self.lblPVoie0, 1, 0, 1, 1)

        self.editName0 = QLineEdit(self.groupParamMeta)
        self.editName0.setObjectName(u"editName0")

        self.gridParamMeta.addWidget(self.editName0, 1, 1, 1, 1)

        self.editUnit0 = QLineEdit(self.groupParamMeta)
        self.editUnit0.setObjectName(u"editUnit0")

        self.gridParamMeta.addWidget(self.editUnit0, 1, 2, 1, 1)

        self.spinConvMin0 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMin0.setObjectName(u"spinConvMin0")
        self.spinConvMin0.setDecimals(6)
        self.spinConvMin0.setMinimum(-1000000.000000000000000)
        self.spinConvMin0.setMaximum(1000000.000000000000000)
        self.spinConvMin0.setValue(0.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMin0, 1, 3, 1, 1)

        self.spinConvMax0 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMax0.setObjectName(u"spinConvMax0")
        self.spinConvMax0.setDecimals(6)
        self.spinConvMax0.setMinimum(-1000000.000000000000000)
        self.spinConvMax0.setMaximum(1000000.000000000000000)
        self.spinConvMax0.setValue(3.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMax0, 1, 4, 1, 1)

        self.lblPVoie1 = QLabel(self.groupParamMeta)
        self.lblPVoie1.setObjectName(u"lblPVoie1")

        self.gridParamMeta.addWidget(self.lblPVoie1, 2, 0, 1, 1)

        self.editName1 = QLineEdit(self.groupParamMeta)
        self.editName1.setObjectName(u"editName1")

        self.gridParamMeta.addWidget(self.editName1, 2, 1, 1, 1)

        self.editUnit1 = QLineEdit(self.groupParamMeta)
        self.editUnit1.setObjectName(u"editUnit1")

        self.gridParamMeta.addWidget(self.editUnit1, 2, 2, 1, 1)

        self.spinConvMin1 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMin1.setObjectName(u"spinConvMin1")
        self.spinConvMin1.setDecimals(6)
        self.spinConvMin1.setMinimum(-1000000.000000000000000)
        self.spinConvMin1.setMaximum(1000000.000000000000000)
        self.spinConvMin1.setValue(0.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMin1, 2, 3, 1, 1)

        self.spinConvMax1 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMax1.setObjectName(u"spinConvMax1")
        self.spinConvMax1.setDecimals(6)
        self.spinConvMax1.setMinimum(-1000000.000000000000000)
        self.spinConvMax1.setMaximum(1000000.000000000000000)
        self.spinConvMax1.setValue(50.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMax1, 2, 4, 1, 1)

        self.lblPVoie2 = QLabel(self.groupParamMeta)
        self.lblPVoie2.setObjectName(u"lblPVoie2")

        self.gridParamMeta.addWidget(self.lblPVoie2, 3, 0, 1, 1)

        self.editName2 = QLineEdit(self.groupParamMeta)
        self.editName2.setObjectName(u"editName2")

        self.gridParamMeta.addWidget(self.editName2, 3, 1, 1, 1)

        self.editUnit2 = QLineEdit(self.groupParamMeta)
        self.editUnit2.setObjectName(u"editUnit2")

        self.gridParamMeta.addWidget(self.editUnit2, 3, 2, 1, 1)

        self.spinConvMin2 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMin2.setObjectName(u"spinConvMin2")
        self.spinConvMin2.setDecimals(6)
        self.spinConvMin2.setMinimum(-1000000.000000000000000)
        self.spinConvMin2.setMaximum(1000000.000000000000000)
        self.spinConvMin2.setValue(0.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMin2, 3, 3, 1, 1)

        self.spinConvMax2 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMax2.setObjectName(u"spinConvMax2")
        self.spinConvMax2.setDecimals(6)
        self.spinConvMax2.setMinimum(-1000000.000000000000000)
        self.spinConvMax2.setMaximum(1000000.000000000000000)
        self.spinConvMax2.setValue(100.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMax2, 3, 4, 1, 1)

        self.lblPVoie3 = QLabel(self.groupParamMeta)
        self.lblPVoie3.setObjectName(u"lblPVoie3")

        self.gridParamMeta.addWidget(self.lblPVoie3, 4, 0, 1, 1)

        self.editName3 = QLineEdit(self.groupParamMeta)
        self.editName3.setObjectName(u"editName3")

        self.gridParamMeta.addWidget(self.editName3, 4, 1, 1, 1)

        self.editUnit3 = QLineEdit(self.groupParamMeta)
        self.editUnit3.setObjectName(u"editUnit3")

        self.gridParamMeta.addWidget(self.editUnit3, 4, 2, 1, 1)

        self.spinConvMin3 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMin3.setObjectName(u"spinConvMin3")
        self.spinConvMin3.setDecimals(6)
        self.spinConvMin3.setMinimum(-1000000.000000000000000)
        self.spinConvMin3.setMaximum(1000000.000000000000000)
        self.spinConvMin3.setValue(0.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMin3, 4, 3, 1, 1)

        self.spinConvMax3 = QDoubleSpinBox(self.groupParamMeta)
        self.spinConvMax3.setObjectName(u"spinConvMax3")
        self.spinConvMax3.setDecimals(6)
        self.spinConvMax3.setMinimum(-1000000.000000000000000)
        self.spinConvMax3.setMaximum(1000000.000000000000000)
        self.spinConvMax3.setValue(50.000000000000000)

        self.gridParamMeta.addWidget(self.spinConvMax3, 4, 4, 1, 1)


        self.layoutScrollReglages.addWidget(self.groupParamMeta)

        self.groupYRanges = QGroupBox(self.scrollReglagesContents)
        self.groupYRanges.setObjectName(u"groupYRanges")
        self.gridYRanges = QGridLayout(self.groupYRanges)
        self.gridYRanges.setObjectName(u"gridYRanges")
        self.lblHdrYVoie = QLabel(self.groupYRanges)
        self.lblHdrYVoie.setObjectName(u"lblHdrYVoie")

        self.gridYRanges.addWidget(self.lblHdrYVoie, 0, 0, 1, 1)

        self.lblHdrFixed = QLabel(self.groupYRanges)
        self.lblHdrFixed.setObjectName(u"lblHdrFixed")

        self.gridYRanges.addWidget(self.lblHdrFixed, 0, 1, 1, 1)

        self.lblHdrYmin = QLabel(self.groupYRanges)
        self.lblHdrYmin.setObjectName(u"lblHdrYmin")

        self.gridYRanges.addWidget(self.lblHdrYmin, 0, 2, 1, 1)

        self.lblHdrYmax = QLabel(self.groupYRanges)
        self.lblHdrYmax.setObjectName(u"lblHdrYmax")

        self.gridYRanges.addWidget(self.lblHdrYmax, 0, 3, 1, 1)

        self.lblVoie0 = QLabel(self.groupYRanges)
        self.lblVoie0.setObjectName(u"lblVoie0")

        self.gridYRanges.addWidget(self.lblVoie0, 1, 0, 1, 1)

        self.chkYFix0 = QCheckBox(self.groupYRanges)
        self.chkYFix0.setObjectName(u"chkYFix0")

        self.gridYRanges.addWidget(self.chkYFix0, 1, 1, 1, 1)

        self.spinYMin0 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMin0.setObjectName(u"spinYMin0")
        self.spinYMin0.setDecimals(2)
        self.spinYMin0.setMinimum(-1000000.000000000000000)
        self.spinYMin0.setMaximum(1000000.000000000000000)
        self.spinYMin0.setValue(0.000000000000000)

        self.gridYRanges.addWidget(self.spinYMin0, 1, 2, 1, 1)

        self.spinYMax0 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMax0.setObjectName(u"spinYMax0")
        self.spinYMax0.setDecimals(2)
        self.spinYMax0.setMinimum(-1000000.000000000000000)
        self.spinYMax0.setMaximum(1000000.000000000000000)
        self.spinYMax0.setValue(3.000000000000000)

        self.gridYRanges.addWidget(self.spinYMax0, 1, 3, 1, 1)

        self.lblVoie1 = QLabel(self.groupYRanges)
        self.lblVoie1.setObjectName(u"lblVoie1")

        self.gridYRanges.addWidget(self.lblVoie1, 2, 0, 1, 1)

        self.chkYFix1 = QCheckBox(self.groupYRanges)
        self.chkYFix1.setObjectName(u"chkYFix1")

        self.gridYRanges.addWidget(self.chkYFix1, 2, 1, 1, 1)

        self.spinYMin1 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMin1.setObjectName(u"spinYMin1")
        self.spinYMin1.setDecimals(2)
        self.spinYMin1.setMinimum(-1000000.000000000000000)
        self.spinYMin1.setMaximum(1000000.000000000000000)
        self.spinYMin1.setValue(0.000000000000000)

        self.gridYRanges.addWidget(self.spinYMin1, 2, 2, 1, 1)

        self.spinYMax1 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMax1.setObjectName(u"spinYMax1")
        self.spinYMax1.setDecimals(2)
        self.spinYMax1.setMinimum(-1000000.000000000000000)
        self.spinYMax1.setMaximum(1000000.000000000000000)
        self.spinYMax1.setValue(50.000000000000000)

        self.gridYRanges.addWidget(self.spinYMax1, 2, 3, 1, 1)

        self.lblVoie2 = QLabel(self.groupYRanges)
        self.lblVoie2.setObjectName(u"lblVoie2")

        self.gridYRanges.addWidget(self.lblVoie2, 3, 0, 1, 1)

        self.chkYFix2 = QCheckBox(self.groupYRanges)
        self.chkYFix2.setObjectName(u"chkYFix2")

        self.gridYRanges.addWidget(self.chkYFix2, 3, 1, 1, 1)

        self.spinYMin2 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMin2.setObjectName(u"spinYMin2")
        self.spinYMin2.setDecimals(2)
        self.spinYMin2.setMinimum(-1000000.000000000000000)
        self.spinYMin2.setMaximum(1000000.000000000000000)
        self.spinYMin2.setValue(0.000000000000000)

        self.gridYRanges.addWidget(self.spinYMin2, 3, 2, 1, 1)

        self.spinYMax2 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMax2.setObjectName(u"spinYMax2")
        self.spinYMax2.setDecimals(2)
        self.spinYMax2.setMinimum(-1000000.000000000000000)
        self.spinYMax2.setMaximum(1000000.000000000000000)
        self.spinYMax2.setValue(100.000000000000000)

        self.gridYRanges.addWidget(self.spinYMax2, 3, 3, 1, 1)

        self.lblVoie3 = QLabel(self.groupYRanges)
        self.lblVoie3.setObjectName(u"lblVoie3")

        self.gridYRanges.addWidget(self.lblVoie3, 4, 0, 1, 1)

        self.chkYFix3 = QCheckBox(self.groupYRanges)
        self.chkYFix3.setObjectName(u"chkYFix3")

        self.gridYRanges.addWidget(self.chkYFix3, 4, 1, 1, 1)

        self.spinYMin3 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMin3.setObjectName(u"spinYMin3")
        self.spinYMin3.setDecimals(2)
        self.spinYMin3.setMinimum(-1000000.000000000000000)
        self.spinYMin3.setMaximum(1000000.000000000000000)
        self.spinYMin3.setValue(0.000000000000000)

        self.gridYRanges.addWidget(self.spinYMin3, 4, 2, 1, 1)

        self.spinYMax3 = QDoubleSpinBox(self.groupYRanges)
        self.spinYMax3.setObjectName(u"spinYMax3")
        self.spinYMax3.setDecimals(2)
        self.spinYMax3.setMinimum(-1000000.000000000000000)
        self.spinYMax3.setMaximum(1000000.000000000000000)
        self.spinYMax3.setValue(50.000000000000000)

        self.gridYRanges.addWidget(self.spinYMax3, 4, 3, 1, 1)

        self.lblVoieTint = QLabel(self.groupYRanges)
        self.lblVoieTint.setObjectName(u"lblVoieTint")

        self.gridYRanges.addWidget(self.lblVoieTint, 5, 0, 1, 1)

        self.chkYFixTint = QCheckBox(self.groupYRanges)
        self.chkYFixTint.setObjectName(u"chkYFixTint")

        self.gridYRanges.addWidget(self.chkYFixTint, 5, 1, 1, 1)

        self.spinYMinTint = QDoubleSpinBox(self.groupYRanges)
        self.spinYMinTint.setObjectName(u"spinYMinTint")
        self.spinYMinTint.setDecimals(2)
        self.spinYMinTint.setMinimum(-1000000.000000000000000)
        self.spinYMinTint.setMaximum(1000000.000000000000000)
        self.spinYMinTint.setValue(0.000000000000000)

        self.gridYRanges.addWidget(self.spinYMinTint, 5, 2, 1, 1)

        self.spinYMaxTint = QDoubleSpinBox(self.groupYRanges)
        self.spinYMaxTint.setObjectName(u"spinYMaxTint")
        self.spinYMaxTint.setDecimals(2)
        self.spinYMaxTint.setMinimum(-1000000.000000000000000)
        self.spinYMaxTint.setMaximum(1000000.000000000000000)
        self.spinYMaxTint.setValue(100.000000000000000)

        self.gridYRanges.addWidget(self.spinYMaxTint, 5, 3, 1, 1)

        self.lblVoieText = QLabel(self.groupYRanges)
        self.lblVoieText.setObjectName(u"lblVoieText")

        self.gridYRanges.addWidget(self.lblVoieText, 6, 0, 1, 1)

        self.chkYFixText = QCheckBox(self.groupYRanges)
        self.chkYFixText.setObjectName(u"chkYFixText")

        self.gridYRanges.addWidget(self.chkYFixText, 6, 1, 1, 1)

        self.spinYMinText = QDoubleSpinBox(self.groupYRanges)
        self.spinYMinText.setObjectName(u"spinYMinText")
        self.spinYMinText.setDecimals(2)
        self.spinYMinText.setMinimum(-1000000.000000000000000)
        self.spinYMinText.setMaximum(1000000.000000000000000)
        self.spinYMinText.setValue(0.000000000000000)

        self.gridYRanges.addWidget(self.spinYMinText, 6, 2, 1, 1)

        self.spinYMaxText = QDoubleSpinBox(self.groupYRanges)
        self.spinYMaxText.setObjectName(u"spinYMaxText")
        self.spinYMaxText.setDecimals(2)
        self.spinYMaxText.setMinimum(-1000000.000000000000000)
        self.spinYMaxText.setMaximum(1000000.000000000000000)
        self.spinYMaxText.setValue(100.000000000000000)

        self.gridYRanges.addWidget(self.spinYMaxText, 6, 3, 1, 1)


        self.layoutScrollReglages.addWidget(self.groupYRanges)

        self.groupCorrections = QGroupBox(self.scrollReglagesContents)
        self.groupCorrections.setObjectName(u"groupCorrections")
        self.gridCorrections = QGridLayout(self.groupCorrections)
        self.gridCorrections.setObjectName(u"gridCorrections")
        self.lblHdrCVoie = QLabel(self.groupCorrections)
        self.lblHdrCVoie.setObjectName(u"lblHdrCVoie")

        self.gridCorrections.addWidget(self.lblHdrCVoie, 0, 0, 1, 1)

        self.lblHdrCMode = QLabel(self.groupCorrections)
        self.lblHdrCMode.setObjectName(u"lblHdrCMode")

        self.gridCorrections.addWidget(self.lblHdrCMode, 0, 1, 1, 1)

        self.lblHdrCa = QLabel(self.groupCorrections)
        self.lblHdrCa.setObjectName(u"lblHdrCa")

        self.gridCorrections.addWidget(self.lblHdrCa, 0, 2, 1, 1)

        self.lblHdrCb = QLabel(self.groupCorrections)
        self.lblHdrCb.setObjectName(u"lblHdrCb")

        self.gridCorrections.addWidget(self.lblHdrCb, 0, 3, 1, 1)

        self.lblHdrCc = QLabel(self.groupCorrections)
        self.lblHdrCc.setObjectName(u"lblHdrCc")

        self.gridCorrections.addWidget(self.lblHdrCc, 0, 4, 1, 1)

        self.lblHdrCd = QLabel(self.groupCorrections)
        self.lblHdrCd.setObjectName(u"lblHdrCd")

        self.gridCorrections.addWidget(self.lblHdrCd, 0, 5, 1, 1)

        self.lblCVoie0 = QLabel(self.groupCorrections)
        self.lblCVoie0.setObjectName(u"lblCVoie0")

        self.gridCorrections.addWidget(self.lblCVoie0, 1, 0, 1, 1)

        self.comboCorr0 = QComboBox(self.groupCorrections)
        self.comboCorr0.addItem("")
        self.comboCorr0.addItem("")
        self.comboCorr0.addItem("")
        self.comboCorr0.addItem("")
        self.comboCorr0.setObjectName(u"comboCorr0")

        self.gridCorrections.addWidget(self.comboCorr0, 1, 1, 1, 1)

        self.spinCorrA0 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrA0.setObjectName(u"spinCorrA0")
        self.spinCorrA0.setDecimals(6)
        self.spinCorrA0.setMinimum(-1000000.000000000000000)
        self.spinCorrA0.setMaximum(1000000.000000000000000)
        self.spinCorrA0.setValue(1.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrA0, 1, 2, 1, 1)

        self.spinCorrB0 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrB0.setObjectName(u"spinCorrB0")
        self.spinCorrB0.setDecimals(6)
        self.spinCorrB0.setMinimum(-1000000.000000000000000)
        self.spinCorrB0.setMaximum(1000000.000000000000000)
        self.spinCorrB0.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrB0, 1, 3, 1, 1)

        self.spinCorrC0 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrC0.setObjectName(u"spinCorrC0")
        self.spinCorrC0.setDecimals(6)
        self.spinCorrC0.setMinimum(-1000000.000000000000000)
        self.spinCorrC0.setMaximum(1000000.000000000000000)
        self.spinCorrC0.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrC0, 1, 4, 1, 1)

        self.spinCorrD0 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrD0.setObjectName(u"spinCorrD0")
        self.spinCorrD0.setDecimals(6)
        self.spinCorrD0.setMinimum(-1000000.000000000000000)
        self.spinCorrD0.setMaximum(1000000.000000000000000)
        self.spinCorrD0.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrD0, 1, 5, 1, 1)

        self.lblCVoie1 = QLabel(self.groupCorrections)
        self.lblCVoie1.setObjectName(u"lblCVoie1")

        self.gridCorrections.addWidget(self.lblCVoie1, 2, 0, 1, 1)

        self.comboCorr1 = QComboBox(self.groupCorrections)
        self.comboCorr1.addItem("")
        self.comboCorr1.addItem("")
        self.comboCorr1.addItem("")
        self.comboCorr1.addItem("")
        self.comboCorr1.setObjectName(u"comboCorr1")

        self.gridCorrections.addWidget(self.comboCorr1, 2, 1, 1, 1)

        self.spinCorrA1 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrA1.setObjectName(u"spinCorrA1")
        self.spinCorrA1.setDecimals(6)
        self.spinCorrA1.setMinimum(-1000000.000000000000000)
        self.spinCorrA1.setMaximum(1000000.000000000000000)
        self.spinCorrA1.setValue(1.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrA1, 2, 2, 1, 1)

        self.spinCorrB1 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrB1.setObjectName(u"spinCorrB1")
        self.spinCorrB1.setDecimals(6)
        self.spinCorrB1.setMinimum(-1000000.000000000000000)
        self.spinCorrB1.setMaximum(1000000.000000000000000)
        self.spinCorrB1.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrB1, 2, 3, 1, 1)

        self.spinCorrC1 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrC1.setObjectName(u"spinCorrC1")
        self.spinCorrC1.setDecimals(6)
        self.spinCorrC1.setMinimum(-1000000.000000000000000)
        self.spinCorrC1.setMaximum(1000000.000000000000000)
        self.spinCorrC1.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrC1, 2, 4, 1, 1)

        self.spinCorrD1 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrD1.setObjectName(u"spinCorrD1")
        self.spinCorrD1.setDecimals(6)
        self.spinCorrD1.setMinimum(-1000000.000000000000000)
        self.spinCorrD1.setMaximum(1000000.000000000000000)
        self.spinCorrD1.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrD1, 2, 5, 1, 1)

        self.lblCVoie2 = QLabel(self.groupCorrections)
        self.lblCVoie2.setObjectName(u"lblCVoie2")

        self.gridCorrections.addWidget(self.lblCVoie2, 3, 0, 1, 1)

        self.comboCorr2 = QComboBox(self.groupCorrections)
        self.comboCorr2.addItem("")
        self.comboCorr2.addItem("")
        self.comboCorr2.addItem("")
        self.comboCorr2.addItem("")
        self.comboCorr2.setObjectName(u"comboCorr2")

        self.gridCorrections.addWidget(self.comboCorr2, 3, 1, 1, 1)

        self.spinCorrA2 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrA2.setObjectName(u"spinCorrA2")
        self.spinCorrA2.setDecimals(6)
        self.spinCorrA2.setMinimum(-1000000.000000000000000)
        self.spinCorrA2.setMaximum(1000000.000000000000000)
        self.spinCorrA2.setValue(1.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrA2, 3, 2, 1, 1)

        self.spinCorrB2 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrB2.setObjectName(u"spinCorrB2")
        self.spinCorrB2.setDecimals(6)
        self.spinCorrB2.setMinimum(-1000000.000000000000000)
        self.spinCorrB2.setMaximum(1000000.000000000000000)
        self.spinCorrB2.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrB2, 3, 3, 1, 1)

        self.spinCorrC2 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrC2.setObjectName(u"spinCorrC2")
        self.spinCorrC2.setDecimals(6)
        self.spinCorrC2.setMinimum(-1000000.000000000000000)
        self.spinCorrC2.setMaximum(1000000.000000000000000)
        self.spinCorrC2.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrC2, 3, 4, 1, 1)

        self.spinCorrD2 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrD2.setObjectName(u"spinCorrD2")
        self.spinCorrD2.setDecimals(6)
        self.spinCorrD2.setMinimum(-1000000.000000000000000)
        self.spinCorrD2.setMaximum(1000000.000000000000000)
        self.spinCorrD2.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrD2, 3, 5, 1, 1)

        self.lblCVoie3 = QLabel(self.groupCorrections)
        self.lblCVoie3.setObjectName(u"lblCVoie3")

        self.gridCorrections.addWidget(self.lblCVoie3, 4, 0, 1, 1)

        self.comboCorr3 = QComboBox(self.groupCorrections)
        self.comboCorr3.addItem("")
        self.comboCorr3.addItem("")
        self.comboCorr3.addItem("")
        self.comboCorr3.addItem("")
        self.comboCorr3.setObjectName(u"comboCorr3")

        self.gridCorrections.addWidget(self.comboCorr3, 4, 1, 1, 1)

        self.spinCorrA3 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrA3.setObjectName(u"spinCorrA3")
        self.spinCorrA3.setDecimals(6)
        self.spinCorrA3.setMinimum(-1000000.000000000000000)
        self.spinCorrA3.setMaximum(1000000.000000000000000)
        self.spinCorrA3.setValue(1.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrA3, 4, 2, 1, 1)

        self.spinCorrB3 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrB3.setObjectName(u"spinCorrB3")
        self.spinCorrB3.setDecimals(6)
        self.spinCorrB3.setMinimum(-1000000.000000000000000)
        self.spinCorrB3.setMaximum(1000000.000000000000000)
        self.spinCorrB3.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrB3, 4, 3, 1, 1)

        self.spinCorrC3 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrC3.setObjectName(u"spinCorrC3")
        self.spinCorrC3.setDecimals(6)
        self.spinCorrC3.setMinimum(-1000000.000000000000000)
        self.spinCorrC3.setMaximum(1000000.000000000000000)
        self.spinCorrC3.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrC3, 4, 4, 1, 1)

        self.spinCorrD3 = QDoubleSpinBox(self.groupCorrections)
        self.spinCorrD3.setObjectName(u"spinCorrD3")
        self.spinCorrD3.setDecimals(6)
        self.spinCorrD3.setMinimum(-1000000.000000000000000)
        self.spinCorrD3.setMaximum(1000000.000000000000000)
        self.spinCorrD3.setValue(0.000000000000000)

        self.gridCorrections.addWidget(self.spinCorrD3, 4, 5, 1, 1)


        self.layoutScrollReglages.addWidget(self.groupCorrections)

        self.layoutApplySettings = QHBoxLayout()
        self.layoutApplySettings.setObjectName(u"layoutApplySettings")
        self.btnApplySettings = QPushButton(self.scrollReglagesContents)
        self.btnApplySettings.setObjectName(u"btnApplySettings")

        self.layoutApplySettings.addWidget(self.btnApplySettings)

        self.spacerApplySettings = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutApplySettings.addItem(self.spacerApplySettings)


        self.layoutScrollReglages.addLayout(self.layoutApplySettings)

        self.scrollReglages.setWidget(self.scrollReglagesContents)

        self.layoutReglages.addWidget(self.scrollReglages)

        self.tabsMain.addTab(self.tabSettings, "")
        self.tabBronkhorst = QWidget()
        self.tabBronkhorst.setObjectName(u"tabBronkhorst")
        self.layoutBronkhorst = QVBoxLayout(self.tabBronkhorst)
        self.layoutBronkhorst.setSpacing(6)
        self.layoutBronkhorst.setObjectName(u"layoutBronkhorst")
        self.layoutBronkhorst.setContentsMargins(8, 8, 8, 8)
        self.bronkTopRow = QHBoxLayout()
        self.bronkTopRow.setObjectName(u"bronkTopRow")
        self.lblPortBronk = QLabel(self.tabBronkhorst)
        self.lblPortBronk.setObjectName(u"lblPortBronk")

        self.bronkTopRow.addWidget(self.lblPortBronk)

        self.input_port = QLineEdit(self.tabBronkhorst)
        self.input_port.setObjectName(u"input_port")
        self.input_port.setMaximumSize(QSize(90, 16777215))

        self.bronkTopRow.addWidget(self.input_port)

        self.btn_scan = QPushButton(self.tabBronkhorst)
        self.btn_scan.setObjectName(u"btn_scan")

        self.bronkTopRow.addWidget(self.btn_scan)

        self.spacerBronkTop = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bronkTopRow.addItem(self.spacerBronkTop)

        self.lbl_status = QLabel(self.tabBronkhorst)
        self.lbl_status.setObjectName(u"lbl_status")

        self.bronkTopRow.addWidget(self.lbl_status)

        self.btn_selection = QPushButton(self.tabBronkhorst)
        self.btn_selection.setObjectName(u"btn_selection")

        self.bronkTopRow.addWidget(self.btn_selection)


        self.layoutBronkhorst.addLayout(self.bronkTopRow)

        self.bronkOptsRow = QHBoxLayout()
        self.bronkOptsRow.setObjectName(u"bronkOptsRow")
        self.lblWindowBronkLabel = QLabel(self.tabBronkhorst)
        self.lblWindowBronkLabel.setObjectName(u"lblWindowBronkLabel")

        self.bronkOptsRow.addWidget(self.lblWindowBronkLabel)

        self.spin_window = QSpinBox(self.tabBronkhorst)
        self.spin_window.setObjectName(u"spin_window")
        self.spin_window.setMaximumSize(QSize(80, 16777215))
        self.spin_window.setMinimum(10)
        self.spin_window.setMaximum(600)
        self.spin_window.setValue(60)

        self.bronkOptsRow.addWidget(self.spin_window)

        self.spacerBronkOpts = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.bronkOptsRow.addItem(self.spacerBronkOpts)


        self.layoutBronkhorst.addLayout(self.bronkOptsRow)

        self.progress_bar = QProgressBar(self.tabBronkhorst)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMaximumSize(QSize(16777215, 8))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.layoutBronkhorst.addWidget(self.progress_bar)

        self.scrollBronk = QScrollArea(self.tabBronkhorst)
        self.scrollBronk.setObjectName(u"scrollBronk")
        self.scrollBronk.setWidgetResizable(True)
        self.scrollBronkContents = QWidget()
        self.scrollBronkContents.setObjectName(u"scrollBronkContents")
        self.scrollBronkContents.setGeometry(QRect(0, 0, 1104, 621))
        self.tiles_layout = QVBoxLayout(self.scrollBronkContents)
        self.tiles_layout.setObjectName(u"tiles_layout")
        self.scrollBronk.setWidget(self.scrollBronkContents)

        self.layoutBronkhorst.addWidget(self.scrollBronk)

        self.tabsMain.addTab(self.tabBronkhorst, "")
        self.tabJulabo = QWidget()
        self.tabJulabo.setObjectName(u"tabJulabo")
        self.layoutJulabo = QVBoxLayout(self.tabJulabo)
        self.layoutJulabo.setSpacing(6)
        self.layoutJulabo.setObjectName(u"layoutJulabo")
        self.layoutJulabo.setContentsMargins(8, 8, 8, 8)
        self.connRow = QHBoxLayout()
        self.connRow.setObjectName(u"connRow")
        self.lblConnLed = QLabel(self.tabJulabo)
        self.lblConnLed.setObjectName(u"lblConnLed")
        self.lblConnLed.setMinimumSize(QSize(18, 18))
        self.lblConnLed.setMaximumSize(QSize(18, 18))

        self.connRow.addWidget(self.lblConnLed)

        self.lblConnStatus = QLabel(self.tabJulabo)
        self.lblConnStatus.setObjectName(u"lblConnStatus")

        self.connRow.addWidget(self.lblConnStatus)

        self.spacerConn = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.connRow.addItem(self.spacerConn)

        self.lblPortLabel = QLabel(self.tabJulabo)
        self.lblPortLabel.setObjectName(u"lblPortLabel")

        self.connRow.addWidget(self.lblPortLabel)

        self.linePort = QLineEdit(self.tabJulabo)
        self.linePort.setObjectName(u"linePort")
        self.linePort.setMaximumSize(QSize(120, 16777215))

        self.connRow.addWidget(self.linePort)

        self.btnConnect = QPushButton(self.tabJulabo)
        self.btnConnect.setObjectName(u"btnConnect")
        self.btnConnect.setMaximumSize(QSize(100, 16777215))

        self.connRow.addWidget(self.btnConnect)

        self.btnDisconnect = QPushButton(self.tabJulabo)
        self.btnDisconnect.setObjectName(u"btnDisconnect")
        self.btnDisconnect.setEnabled(False)
        self.btnDisconnect.setMaximumSize(QSize(110, 16777215))

        self.connRow.addWidget(self.btnDisconnect)


        self.layoutJulabo.addLayout(self.connRow)

        self.midRowJulabo = QHBoxLayout()
        self.midRowJulabo.setObjectName(u"midRowJulabo")
        self.grpVal = QGroupBox(self.tabJulabo)
        self.grpVal.setObjectName(u"grpVal")
        self.gridVal = QGridLayout(self.grpVal)
        self.gridVal.setObjectName(u"gridVal")
        self.lblTIntLabel = QLabel(self.grpVal)
        self.lblTIntLabel.setObjectName(u"lblTIntLabel")
        self.lblTIntLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblTIntLabel, 0, 0, 1, 1)

        self.lblTInt = QLabel(self.grpVal)
        self.lblTInt.setObjectName(u"lblTInt")
        self.lblTInt.setMinimumSize(QSize(90, 0))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.lblTInt.setFont(font1)
        self.lblTInt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblTInt, 0, 1, 1, 1)

        self.lblTIntUnit = QLabel(self.grpVal)
        self.lblTIntUnit.setObjectName(u"lblTIntUnit")

        self.gridVal.addWidget(self.lblTIntUnit, 0, 2, 1, 1)

        self.lblTExtLabel = QLabel(self.grpVal)
        self.lblTExtLabel.setObjectName(u"lblTExtLabel")
        self.lblTExtLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblTExtLabel, 0, 4, 1, 1)

        self.lblTExt = QLabel(self.grpVal)
        self.lblTExt.setObjectName(u"lblTExt")
        self.lblTExt.setMinimumSize(QSize(90, 0))
        self.lblTExt.setFont(font1)
        self.lblTExt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblTExt, 0, 5, 1, 1)

        self.lblTExtUnit = QLabel(self.grpVal)
        self.lblTExtUnit.setObjectName(u"lblTExtUnit")

        self.gridVal.addWidget(self.lblTExtUnit, 0, 6, 1, 1)

        self.lblPressureLabel = QLabel(self.grpVal)
        self.lblPressureLabel.setObjectName(u"lblPressureLabel")
        self.lblPressureLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblPressureLabel, 1, 0, 1, 1)

        self.lblPressure = QLabel(self.grpVal)
        self.lblPressure.setObjectName(u"lblPressure")
        self.lblPressure.setFont(font1)
        self.lblPressure.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblPressure, 1, 1, 1, 1)

        self.lblPressureUnit = QLabel(self.grpVal)
        self.lblPressureUnit.setObjectName(u"lblPressureUnit")

        self.gridVal.addWidget(self.lblPressureUnit, 1, 2, 1, 1)

        self.lblLevelLabel = QLabel(self.grpVal)
        self.lblLevelLabel.setObjectName(u"lblLevelLabel")
        self.lblLevelLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblLevelLabel, 1, 4, 1, 1)

        self.lblLevel = QLabel(self.grpVal)
        self.lblLevel.setObjectName(u"lblLevel")
        self.lblLevel.setFont(font1)
        self.lblLevel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblLevel, 1, 5, 1, 1)

        self.lblLevelUnit = QLabel(self.grpVal)
        self.lblLevelUnit.setObjectName(u"lblLevelUnit")

        self.gridVal.addWidget(self.lblLevelUnit, 1, 6, 1, 1)

        self.lblPumpLabel = QLabel(self.grpVal)
        self.lblPumpLabel.setObjectName(u"lblPumpLabel")
        self.lblPumpLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblPumpLabel, 2, 0, 1, 1)

        self.lblPumpSpeed = QLabel(self.grpVal)
        self.lblPumpSpeed.setObjectName(u"lblPumpSpeed")
        self.lblPumpSpeed.setFont(font1)
        self.lblPumpSpeed.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblPumpSpeed, 2, 1, 1, 1)

        self.lblPumpUnit = QLabel(self.grpVal)
        self.lblPumpUnit.setObjectName(u"lblPumpUnit")

        self.gridVal.addWidget(self.lblPumpUnit, 2, 2, 1, 1)

        self.lblSetpointLabel = QLabel(self.grpVal)
        self.lblSetpointLabel.setObjectName(u"lblSetpointLabel")
        self.lblSetpointLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblSetpointLabel, 2, 4, 1, 1)

        self.lblSetpoint = QLabel(self.grpVal)
        self.lblSetpoint.setObjectName(u"lblSetpoint")
        self.lblSetpoint.setFont(font1)
        self.lblSetpoint.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridVal.addWidget(self.lblSetpoint, 2, 5, 1, 1)

        self.lblSetpointUnit = QLabel(self.grpVal)
        self.lblSetpointUnit.setObjectName(u"lblSetpointUnit")

        self.gridVal.addWidget(self.lblSetpointUnit, 2, 6, 1, 1)


        self.midRowJulabo.addWidget(self.grpVal)

        self.grpCtrl = QGroupBox(self.tabJulabo)
        self.grpCtrl.setObjectName(u"grpCtrl")
        self.grpCtrl.setMinimumSize(QSize(380, 0))
        self.gridCtrl = QGridLayout(self.grpCtrl)
        self.gridCtrl.setObjectName(u"gridCtrl")
        self.lblNewSp = QLabel(self.grpCtrl)
        self.lblNewSp.setObjectName(u"lblNewSp")

        self.gridCtrl.addWidget(self.lblNewSp, 0, 0, 1, 1)

        self.spinSetpoint = QDoubleSpinBox(self.grpCtrl)
        self.spinSetpoint.setObjectName(u"spinSetpoint")
        self.spinSetpoint.setMinimum(-150.000000000000000)
        self.spinSetpoint.setMaximum(400.000000000000000)
        self.spinSetpoint.setSingleStep(0.500000000000000)
        self.spinSetpoint.setValue(20.000000000000000)

        self.gridCtrl.addWidget(self.spinSetpoint, 0, 1, 1, 1)

        self.btnApplySp = QPushButton(self.grpCtrl)
        self.btnApplySp.setObjectName(u"btnApplySp")
        self.btnApplySp.setEnabled(False)

        self.gridCtrl.addWidget(self.btnApplySp, 0, 2, 1, 1)

        self.lblWindowJLabel = QLabel(self.grpCtrl)
        self.lblWindowJLabel.setObjectName(u"lblWindowJLabel")

        self.gridCtrl.addWidget(self.lblWindowJLabel, 1, 0, 1, 1)

        self.spinWindow = QSpinBox(self.grpCtrl)
        self.spinWindow.setObjectName(u"spinWindow")
        self.spinWindow.setMinimum(1)
        self.spinWindow.setMaximum(1440)
        self.spinWindow.setValue(30)

        self.gridCtrl.addWidget(self.spinWindow, 1, 1, 1, 1)

        self.btnStart = QPushButton(self.grpCtrl)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setEnabled(False)

        self.gridCtrl.addWidget(self.btnStart, 1, 2, 1, 1)

        self.btnStop = QPushButton(self.grpCtrl)
        self.btnStop.setObjectName(u"btnStop")
        self.btnStop.setEnabled(False)

        self.gridCtrl.addWidget(self.btnStop, 1, 3, 1, 1)


        self.midRowJulabo.addWidget(self.grpCtrl)


        self.layoutJulabo.addLayout(self.midRowJulabo)

        self.grpPlots = QGroupBox(self.tabJulabo)
        self.grpPlots.setObjectName(u"grpPlots")
        sizePolicy1.setHeightForWidth(self.grpPlots.sizePolicy().hasHeightForWidth())
        self.grpPlots.setSizePolicy(sizePolicy1)
        self.layoutGrpPlots = QHBoxLayout(self.grpPlots)
        self.layoutGrpPlots.setObjectName(u"layoutGrpPlots")
        self.plotContainer = QWidget(self.grpPlots)
        self.plotContainer.setObjectName(u"plotContainer")
        sizePolicy1.setHeightForWidth(self.plotContainer.sizePolicy().hasHeightForWidth())
        self.plotContainer.setSizePolicy(sizePolicy1)
        self.plotContainer.setMinimumSize(QSize(0, 280))

        self.layoutGrpPlots.addWidget(self.plotContainer)


        self.layoutJulabo.addWidget(self.grpPlots)

        self.tabsMain.addTab(self.tabJulabo, "")
        self.tabPID = QWidget()
        self.tabPID.setObjectName(u"tabPID")
        self.layoutTabPID = QVBoxLayout(self.tabPID)
        self.layoutTabPID.setObjectName(u"layoutTabPID")
        self.groupPid = QGroupBox(self.tabPID)
        self.groupPid.setObjectName(u"groupPid")
        self.layoutGroupPid = QVBoxLayout(self.groupPid)
        self.layoutGroupPid.setSpacing(8)
        self.layoutGroupPid.setObjectName(u"layoutGroupPid")
        self.layoutGroupPid.setContentsMargins(10, 16, 10, 10)
        self.layoutPidStatus = QHBoxLayout()
        self.layoutPidStatus.setSpacing(6)
        self.layoutPidStatus.setObjectName(u"layoutPidStatus")
        self.lblPidLed = QLabel(self.groupPid)
        self.lblPidLed.setObjectName(u"lblPidLed")
        self.lblPidLed.setMinimumSize(QSize(18, 18))
        self.lblPidLed.setMaximumSize(QSize(18, 18))
        self.lblPidLed.setStyleSheet(u"border:1px solid #888; border-radius:6px; background:#bbb;")

        self.layoutPidStatus.addWidget(self.lblPidLed)

        self.lblPidStatus = QLabel(self.groupPid)
        self.lblPidStatus.setObjectName(u"lblPidStatus")

        self.layoutPidStatus.addWidget(self.lblPidStatus)

        self.spacerPidStatus = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutPidStatus.addItem(self.spacerPidStatus)

        self.chkPidActive = QCheckBox(self.groupPid)
        self.chkPidActive.setObjectName(u"chkPidActive")

        self.layoutPidStatus.addWidget(self.chkPidActive)


        self.layoutGroupPid.addLayout(self.layoutPidStatus)

        self.gridPidParams = QGridLayout()
        self.gridPidParams.setSpacing(6)
        self.gridPidParams.setObjectName(u"gridPidParams")
        self.lblPidConsigne = QLabel(self.groupPid)
        self.lblPidConsigne.setObjectName(u"lblPidConsigne")

        self.gridPidParams.addWidget(self.lblPidConsigne, 0, 0, 1, 1)

        self.spinPidConsigne = QDoubleSpinBox(self.groupPid)
        self.spinPidConsigne.setObjectName(u"spinPidConsigne")
        self.spinPidConsigne.setDecimals(1)
        self.spinPidConsigne.setMinimum(0.000000000000000)
        self.spinPidConsigne.setMaximum(100.000000000000000)
        self.spinPidConsigne.setSingleStep(0.500000000000000)
        self.spinPidConsigne.setValue(50.000000000000000)

        self.gridPidParams.addWidget(self.spinPidConsigne, 0, 1, 1, 1)

        self.lblPidConsUnit = QLabel(self.groupPid)
        self.lblPidConsUnit.setObjectName(u"lblPidConsUnit")

        self.gridPidParams.addWidget(self.lblPidConsUnit, 0, 2, 1, 1)

        self.lblPidKp = QLabel(self.groupPid)
        self.lblPidKp.setObjectName(u"lblPidKp")

        self.gridPidParams.addWidget(self.lblPidKp, 1, 0, 1, 1)

        self.spinPidKp = QDoubleSpinBox(self.groupPid)
        self.spinPidKp.setObjectName(u"spinPidKp")
        self.spinPidKp.setDecimals(4)
        self.spinPidKp.setMinimum(0.000000000000000)
        self.spinPidKp.setMaximum(1000.000000000000000)
        self.spinPidKp.setSingleStep(0.010000000000000)
        self.spinPidKp.setValue(0.400000000000000)

        self.gridPidParams.addWidget(self.spinPidKp, 1, 1, 1, 1)

        self.lblPidKi = QLabel(self.groupPid)
        self.lblPidKi.setObjectName(u"lblPidKi")

        self.gridPidParams.addWidget(self.lblPidKi, 2, 0, 1, 1)

        self.spinPidKi = QDoubleSpinBox(self.groupPid)
        self.spinPidKi.setObjectName(u"spinPidKi")
        self.spinPidKi.setDecimals(6)
        self.spinPidKi.setMinimum(0.000000000000000)
        self.spinPidKi.setMaximum(100.000000000000000)
        self.spinPidKi.setSingleStep(0.000100000000000)
        self.spinPidKi.setValue(0.002000000000000)

        self.gridPidParams.addWidget(self.spinPidKi, 2, 1, 1, 1)

        self.lblPidKd = QLabel(self.groupPid)
        self.lblPidKd.setObjectName(u"lblPidKd")

        self.gridPidParams.addWidget(self.lblPidKd, 3, 0, 1, 1)

        self.spinPidKd = QDoubleSpinBox(self.groupPid)
        self.spinPidKd.setObjectName(u"spinPidKd")
        self.spinPidKd.setDecimals(4)
        self.spinPidKd.setMinimum(0.000000000000000)
        self.spinPidKd.setMaximum(100.000000000000000)
        self.spinPidKd.setSingleStep(0.001000000000000)
        self.spinPidKd.setValue(0.000000000000000)

        self.gridPidParams.addWidget(self.spinPidKd, 3, 1, 1, 1)

        self.lblPidAddr = QLabel(self.groupPid)
        self.lblPidAddr.setObjectName(u"lblPidAddr")

        self.gridPidParams.addWidget(self.lblPidAddr, 4, 0, 1, 1)

        self.spinPidAddr = QSpinBox(self.groupPid)
        self.spinPidAddr.setObjectName(u"spinPidAddr")
        self.spinPidAddr.setMinimum(1)
        self.spinPidAddr.setMaximum(128)
        self.spinPidAddr.setValue(7)

        self.gridPidParams.addWidget(self.spinPidAddr, 4, 1, 1, 1)

        self.lblPidLoop = QLabel(self.groupPid)
        self.lblPidLoop.setObjectName(u"lblPidLoop")

        self.gridPidParams.addWidget(self.lblPidLoop, 5, 0, 1, 1)

        self.spinPidLoop = QDoubleSpinBox(self.groupPid)
        self.spinPidLoop.setObjectName(u"spinPidLoop")
        self.spinPidLoop.setDecimals(1)
        self.spinPidLoop.setMinimum(0.500000000000000)
        self.spinPidLoop.setMaximum(60.000000000000000)
        self.spinPidLoop.setSingleStep(0.500000000000000)
        self.spinPidLoop.setValue(1.000000000000000)

        self.gridPidParams.addWidget(self.spinPidLoop, 5, 1, 1, 1)

        self.lblPidLoopUnit = QLabel(self.groupPid)
        self.lblPidLoopUnit.setObjectName(u"lblPidLoopUnit")

        self.gridPidParams.addWidget(self.lblPidLoopUnit, 5, 2, 1, 1)

        self.lblPidVoie = QLabel(self.groupPid)
        self.lblPidVoie.setObjectName(u"lblPidVoie")

        self.gridPidParams.addWidget(self.lblPidVoie, 6, 0, 1, 1)

        self.comboPidVoie = QComboBox(self.groupPid)
        self.comboPidVoie.addItem("")
        self.comboPidVoie.addItem("")
        self.comboPidVoie.addItem("")
        self.comboPidVoie.addItem("")
        self.comboPidVoie.setObjectName(u"comboPidVoie")

        self.gridPidParams.addWidget(self.comboPidVoie, 6, 1, 1, 2)


        self.layoutGroupPid.addLayout(self.gridPidParams)

        self.linePidSep = QFrame(self.groupPid)
        self.linePidSep.setObjectName(u"linePidSep")
        self.linePidSep.setFrameShape(QFrame.Shape.HLine)
        self.linePidSep.setFrameShadow(QFrame.Shadow.Sunken)

        self.layoutGroupPid.addWidget(self.linePidSep)

        self.layoutPidBtns = QHBoxLayout()
        self.layoutPidBtns.setSpacing(6)
        self.layoutPidBtns.setObjectName(u"layoutPidBtns")
        self.spacerPidBtns = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutPidBtns.addItem(self.spacerPidBtns)


        self.layoutGroupPid.addLayout(self.layoutPidBtns)


        self.layoutTabPID.addWidget(self.groupPid)

        self.groupPidHelp = QGroupBox(self.tabPID)
        self.groupPidHelp.setObjectName(u"groupPidHelp")
        self.layPidHelp = QVBoxLayout(self.groupPidHelp)
        self.layPidHelp.setObjectName(u"layPidHelp")
        self.lblPidHelp = QLabel(self.groupPidHelp)
        self.lblPidHelp.setObjectName(u"lblPidHelp")
        self.lblPidHelp.setStyleSheet(u"color:#333;")
        self.lblPidHelp.setTextFormat(Qt.TextFormat.RichText)
        self.lblPidHelp.setWordWrap(True)

        self.layPidHelp.addWidget(self.lblPidHelp)

        self.lblPidSchemaCap = QLabel(self.groupPidHelp)
        self.lblPidSchemaCap.setObjectName(u"lblPidSchemaCap")
        self.lblPidSchemaCap.setStyleSheet(u"font-weight:bold; margin-top:6px;")

        self.layPidHelp.addWidget(self.lblPidSchemaCap)

        self.lblPidSchema = QLabel(self.groupPidHelp)
        self.lblPidSchema.setObjectName(u"lblPidSchema")
        self.lblPidSchema.setMinimumSize(QSize(600, 144))
        self.lblPidSchema.setMaximumSize(QSize(600, 144))
        self.lblPidSchema.setPixmap(QPixmap(u"schema_pid_boucle.png"))
        self.lblPidSchema.setScaledContents(True)

        self.layPidHelp.addWidget(self.lblPidSchema)


        self.layoutTabPID.addWidget(self.groupPidHelp)

        self.spacerTabPID = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutTabPID.addItem(self.spacerTabPID)

        self.tabsMain.addTab(self.tabPID, "")

        self.rootLayout.addWidget(self.tabsMain)

        PolarisMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(PolarisMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        PolarisMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PolarisMainWindow)

        self.tabsMain.setCurrentIndex(0)
        self.comboSideV1.setCurrentIndex(0)
        self.comboSideV2.setCurrentIndex(0)
        self.comboSideV3.setCurrentIndex(0)
        self.comboSideV4.setCurrentIndex(0)
        self.comboSideTint.setCurrentIndex(1)
        self.comboSideText.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(PolarisMainWindow)
    # setupUi

    def retranslateUi(self, PolarisMainWindow):
        PolarisMainWindow.setWindowTitle(QCoreApplication.translate("PolarisMainWindow", u"POLARIS", None))
        self.panelSauermann.setTitle(QCoreApplication.translate("PolarisMainWindow", u"SAUERMANN", None))
        self.lblSauTempName.setText(QCoreApplication.translate("PolarisMainWindow", u"Vitesse", None))
        self.lblSauTempVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblSauTempUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"m/s", None))
        self.lblSauVitName.setText(QCoreApplication.translate("PolarisMainWindow", u"Temp\u00e9rature", None))
        self.lblSauVitVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblSauVitUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.lblSauPresName.setText(QCoreApplication.translate("PolarisMainWindow", u"Humidit\u00e9", None))
        self.lblSauPresVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblSauPresUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"%", None))
        self.lblSauHumName.setText(QCoreApplication.translate("PolarisMainWindow", u"Pression", None))
        self.lblSauHumVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblSauHumUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"Pa", None))
        self.panelJulabo.setTitle(QCoreApplication.translate("PolarisMainWindow", u"JULABO", None))
        self.lblJulTintName.setText(QCoreApplication.translate("PolarisMainWindow", u"Tint :", None))
        self.lblJulTintVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblJulTintUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.lblJulTextName.setText(QCoreApplication.translate("PolarisMainWindow", u"Text :", None))
        self.lblJulTextVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblJulTextUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.lblJulConsName.setText(QCoreApplication.translate("PolarisMainWindow", u"Consigne T :", None))
        self.lblJulConsVal.setText(QCoreApplication.translate("PolarisMainWindow", u"--", None))
        self.lblJulConsUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.panelIndicateurs.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Status de communication", None))
        self.lblLedBroName.setText(QCoreApplication.translate("PolarisMainWindow", u"BRONKHORST", None))
        self.ledBronkhorst.setText("")
        self.lblLedSauName.setText(QCoreApplication.translate("PolarisMainWindow", u"SAUERMANN", None))
        self.ledSauermann.setText("")
        self.lblLedJulName.setText(QCoreApplication.translate("PolarisMainWindow", u"JULABO", None))
        self.ledJulabo.setText("")
        self.lblLedPidName.setText(QCoreApplication.translate("PolarisMainWindow", u"PID", None))
        self.ledPid.setText("")
        self.btnStart_2.setText(QCoreApplication.translate("PolarisMainWindow", u"Start", None))
        self.btnStop_2.setText(QCoreApplication.translate("PolarisMainWindow", u"Stop", None))
        self.btnStartCsv.setText(QCoreApplication.translate("PolarisMainWindow", u"Start CSV", None))
        self.btnStopCsv.setText(QCoreApplication.translate("PolarisMainWindow", u"Stop CSV", None))
        self.panelVoies.setTitle("")
        self.lblVoie.setText("")
        self.lblHdrScale.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00c9ch.", None))
        self.lblHdrCurve.setText(QCoreApplication.translate("PolarisMainWindow", u"Courbe", None))
        self.lblHdrColor.setText("")
        self.lblHdrSide.setText(QCoreApplication.translate("PolarisMainWindow", u"C\u00f4t\u00e9", None))
        self.lblV1.setText(QCoreApplication.translate("PolarisMainWindow", u"V1", None))
        self.chkScaleV1.setText("")
        self.chkCurveV1.setText("")
        self.lblColorV1.setText("")
        self.comboSideV1.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Gauche", None))
        self.comboSideV1.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Droite", None))

#if QT_CONFIG(tooltip)
        self.comboSideV1.setToolTip(QCoreApplication.translate("PolarisMainWindow", u"Place l'\u00e9chelle (axe Y) de cette courbe \u00e0 gauche ou \u00e0 droite", None))
#endif // QT_CONFIG(tooltip)
        self.lblV2.setText(QCoreApplication.translate("PolarisMainWindow", u"V2", None))
        self.chkScaleV2.setText("")
        self.chkCurveV2.setText("")
        self.lblColorV2.setText("")
        self.comboSideV2.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Gauche", None))
        self.comboSideV2.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Droite", None))

#if QT_CONFIG(tooltip)
        self.comboSideV2.setToolTip(QCoreApplication.translate("PolarisMainWindow", u"Place l'\u00e9chelle (axe Y) de cette courbe \u00e0 gauche ou \u00e0 droite", None))
#endif // QT_CONFIG(tooltip)
        self.lblV3.setText(QCoreApplication.translate("PolarisMainWindow", u"V3", None))
        self.chkScaleV3.setText("")
        self.chkCurveV3.setText("")
        self.lblColorV3.setText("")
        self.comboSideV3.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Gauche", None))
        self.comboSideV3.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Droite", None))

#if QT_CONFIG(tooltip)
        self.comboSideV3.setToolTip(QCoreApplication.translate("PolarisMainWindow", u"Place l'\u00e9chelle (axe Y) de cette courbe \u00e0 gauche ou \u00e0 droite", None))
#endif // QT_CONFIG(tooltip)
        self.lblV4.setText(QCoreApplication.translate("PolarisMainWindow", u"V4", None))
        self.chkScaleV4.setText("")
        self.chkCurveV4.setText("")
        self.lblColorV4.setText("")
        self.comboSideV4.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Gauche", None))
        self.comboSideV4.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Droite", None))

#if QT_CONFIG(tooltip)
        self.comboSideV4.setToolTip(QCoreApplication.translate("PolarisMainWindow", u"Place l'\u00e9chelle (axe Y) de cette courbe \u00e0 gauche ou \u00e0 droite", None))
#endif // QT_CONFIG(tooltip)
        self.lblVTint.setText(QCoreApplication.translate("PolarisMainWindow", u"T\u00b0 int", None))
        self.chkScaleTint.setText("")
        self.chkCurveTint.setText("")
        self.lblColorTint.setText("")
        self.comboSideTint.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Gauche", None))
        self.comboSideTint.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Droite", None))

#if QT_CONFIG(tooltip)
        self.comboSideTint.setToolTip(QCoreApplication.translate("PolarisMainWindow", u"Place l'\u00e9chelle (axe Y) de cette courbe \u00e0 gauche ou \u00e0 droite", None))
#endif // QT_CONFIG(tooltip)
        self.lblVText.setText(QCoreApplication.translate("PolarisMainWindow", u"T\u00b0 ext", None))
        self.chkScaleText.setText("")
        self.chkCurveText.setText("")
        self.lblColorText.setText("")
        self.comboSideText.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Gauche", None))
        self.comboSideText.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Droite", None))

#if QT_CONFIG(tooltip)
        self.comboSideText.setToolTip(QCoreApplication.translate("PolarisMainWindow", u"Place l'\u00e9chelle (axe Y) de cette courbe \u00e0 gauche ou \u00e0 droite", None))
#endif // QT_CONFIG(tooltip)
        self.panelAnalyseurs.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Analyseurs", None))
        self.lblDashCross.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblGraphPlaceholder.setText(QCoreApplication.translate("PolarisMainWindow", u"[ Zone graphique ]", None))
        self.panelLog.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Log et alarmes", None))
        self.panelRdms.setTitle(QCoreApplication.translate("PolarisMainWindow", u"LEDs RDMs", None))
        self.lblSectLiq.setText(QCoreApplication.translate("PolarisMainWindow", u"Polluants liquides", None))
        self.lblRdmNum1.setText("")
        self.lblRdmNum2.setText("")
        self.lblRdmNum3.setText("")
        self.lblRdmNum4.setText("")
        self.ledRdm1.setText("")
        self.ledRdm2.setText("")
        self.ledRdm3.setText("")
        self.ledRdm4.setText("")
        self.lblSectHum.setText(QCoreApplication.translate("PolarisMainWindow", u"Air humide", None))
        self.lblRdmNum5.setText("")
        self.lblRdmNum6.setText("")
        self.lblRdmNum7.setText("")
        self.lblRdmNum8.setText("")
        self.ledRdm5.setText("")
        self.ledRdm6.setText("")
        self.ledRdm7.setText("")
        self.ledRdm8.setText("")
        self.lblSectGaz.setText(QCoreApplication.translate("PolarisMainWindow", u"Polluants gazeux", None))
        self.lblRdmNum9.setText("")
        self.lblRdmNum10.setText("")
        self.lblRdmNum11.setText("")
        self.lblRdmNum12.setText("")
        self.ledRdm9.setText("")
        self.ledRdm10.setText("")
        self.ledRdm11.setText("")
        self.ledRdm12.setText("")
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.tabDashboard), QCoreApplication.translate("PolarisMainWindow", u"\U0001f5c2  Dashboard", None))
        self.lblDate.setText(QCoreApplication.translate("PolarisMainWindow", u"--/-- --:--:--", None))
        self.lblAcqLed.setStyleSheet(QCoreApplication.translate("PolarisMainWindow", u"border:1px solid #888; border-radius:6px; background:#bbb;", None))
        self.lblAcqLed.setText("")
        self.lblAcqStatus.setText(QCoreApplication.translate("PolarisMainWindow", u"Acquisition", None))
        self.lblRecLed.setStyleSheet(QCoreApplication.translate("PolarisMainWindow", u"border:1px solid #888; border-radius:6px; background:#bbb;", None))
        self.lblRecLed.setText("")
        self.lblRecStatus.setText(QCoreApplication.translate("PolarisMainWindow", u"Enregistrement : inactif", None))
        self.groupAcq.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Param\u00e8tres de graph", None))
        self.lblFsLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Fr\u00e9quence d'\u00e9chantillonnage :", None))
        self.comboFsUnit.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"mesures/s", None))

        self.lblBlocLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Points affich\u00e9s :", None))
        self.comboDispUnit.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"par seconde", None))
        self.comboDispUnit.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"par minute", None))

        self.lblModeLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Mode du graph :", None))
        self.comboGraphMode.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"fixe", None))
        self.comboGraphMode.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"glissant", None))

        self.lblRollingLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Fen\u00eatre glissante :", None))
        self.comboRollingUnit.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"secondes", None))
        self.comboRollingUnit.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"minutes", None))
        self.comboRollingUnit.setItemText(2, QCoreApplication.translate("PolarisMainWindow", u"heures", None))

        self.group0.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Voie 0", None))
        self.lblName0.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 0 :", None))
        self.lblValue0.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit0.setText("")
        self.lblName0_2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 0 corrig\u00e9 :", None))
        self.lblValueCorr0.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit0_2.setText("")
        self.btnColor0.setText("")
        self.group1.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Voie 1", None))
        self.lblName1.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 1 :", None))
        self.lblValue1.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit1.setText("")
        self.lblName1_2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 1 corrig\u00e9 :", None))
        self.lblValueCorr1.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit1_2.setText("")
        self.btnColor1.setText("")
        self.group2.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Voie 2", None))
        self.lblName2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 2 :", None))
        self.lblValue2.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit2.setText("")
        self.lblName2_2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 2 corrig\u00e9 :", None))
        self.lblValueCorr2.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit2_2.setText("")
        self.btnColor2.setText("")
        self.group3.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Voie 3", None))
        self.lblName3.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 3 :", None))
        self.lblValue3.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit3.setText("")
        self.lblName3_2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 3 corrig\u00e9 :", None))
        self.lblValueCorr3.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblUnit3_2.setText("")
        self.btnColor3.setText("")
        self.groupGraph.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Graphique (4 axes Y ind\u00e9pendants)", None))
        self.btnFollow.setStyleSheet(QCoreApplication.translate("PolarisMainWindow", u"QToolButton{background-color:rgb(220,220,220);}QToolButton:checked{background-color:rgb(100,180,255);border:2px solid rgb(0,120,200);}", None))
        self.btnFollow.setText(QCoreApplication.translate("PolarisMainWindow", u"auto", None))
        self.btnSaveImage.setText(QCoreApplication.translate("PolarisMainWindow", u"Enregistrer le graphe (PNG)", None))
        self.lblCross.setStyleSheet(QCoreApplication.translate("PolarisMainWindow", u"color:#555; font-size:9pt; padding:2px;", None))
        self.lblCross.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.tabSauermann), QCoreApplication.translate("PolarisMainWindow", u"\U0001f4c8  Sauermann", None))
        self.groupParamMeta.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Param\u00e8tres des voies", None))
        self.lblHdrVoie0.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Voie</b>", None))
        self.lblHdrNom.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Nom</b>", None))
        self.lblHdrUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Unit\u00e9</b>", None))
        self.lblHdrMin.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Conv. min</b>", None))
        self.lblHdrMax.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Conv. max</b>", None))
        self.lblPVoie0.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 0", None))
        self.editName0.setText(QCoreApplication.translate("PolarisMainWindow", u"Vitesse", None))
        self.editUnit0.setText(QCoreApplication.translate("PolarisMainWindow", u"m/s", None))
        self.lblPVoie1.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 1", None))
        self.editName1.setText(QCoreApplication.translate("PolarisMainWindow", u"Temp\u00e9rature", None))
        self.editUnit1.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.lblPVoie2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 2", None))
        self.editName2.setText(QCoreApplication.translate("PolarisMainWindow", u"Humidit\u00e9", None))
        self.editUnit2.setText(QCoreApplication.translate("PolarisMainWindow", u"%RH", None))
        self.lblPVoie3.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 3", None))
        self.editName3.setText(QCoreApplication.translate("PolarisMainWindow", u"Pression", None))
        self.editUnit3.setText(QCoreApplication.translate("PolarisMainWindow", u"Pa", None))
        self.groupYRanges.setTitle(QCoreApplication.translate("PolarisMainWindow", u"R\u00e9glages Y", None))
        self.lblHdrYVoie.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Voie</b>", None))
        self.lblHdrFixed.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Plage fixe</b>", None))
        self.lblHdrYmin.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Ymin</b>", None))
        self.lblHdrYmax.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Ymax</b>", None))
        self.lblVoie0.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 0", None))
        self.chkYFix0.setText(QCoreApplication.translate("PolarisMainWindow", u"Fixe", None))
        self.lblVoie1.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 1", None))
        self.chkYFix1.setText(QCoreApplication.translate("PolarisMainWindow", u"Fixe", None))
        self.lblVoie2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 2", None))
        self.chkYFix2.setText(QCoreApplication.translate("PolarisMainWindow", u"Fixe", None))
        self.lblVoie3.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 3", None))
        self.chkYFix3.setText(QCoreApplication.translate("PolarisMainWindow", u"Fixe", None))
        self.lblVoieTint.setText(QCoreApplication.translate("PolarisMainWindow", u"T\u00b0 int (Julabo)", None))
        self.chkYFixTint.setText(QCoreApplication.translate("PolarisMainWindow", u"Fixe", None))
        self.lblVoieText.setText(QCoreApplication.translate("PolarisMainWindow", u"T\u00b0 ext (Julabo)", None))
        self.chkYFixText.setText(QCoreApplication.translate("PolarisMainWindow", u"Fixe", None))
        self.groupCorrections.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Corrections par voie", None))
        self.lblHdrCVoie.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Voie</b>", None))
        self.lblHdrCMode.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Mode</b>", None))
        self.lblHdrCa.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>a</b>", None))
        self.lblHdrCb.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>b</b>", None))
        self.lblHdrCc.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>c</b>", None))
        self.lblHdrCd.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>d</b>", None))
        self.lblCVoie0.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 0", None))
        self.comboCorr0.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Aucune", None))
        self.comboCorr0.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Lin\u00e9aire (ax + b)", None))
        self.comboCorr0.setItemText(2, QCoreApplication.translate("PolarisMainWindow", u"Quadratique (ax\u00b2 + bx + c)", None))
        self.comboCorr0.setItemText(3, QCoreApplication.translate("PolarisMainWindow", u"Cubique (ax\u00b3 + bx\u00b2 + cx + d)", None))

        self.lblCVoie1.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 1", None))
        self.comboCorr1.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Aucune", None))
        self.comboCorr1.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Lin\u00e9aire (ax + b)", None))
        self.comboCorr1.setItemText(2, QCoreApplication.translate("PolarisMainWindow", u"Quadratique (ax\u00b2 + bx + c)", None))
        self.comboCorr1.setItemText(3, QCoreApplication.translate("PolarisMainWindow", u"Cubique (ax\u00b3 + bx\u00b2 + cx + d)", None))

        self.lblCVoie2.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 2", None))
        self.comboCorr2.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Aucune", None))
        self.comboCorr2.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Lin\u00e9aire (ax + b)", None))
        self.comboCorr2.setItemText(2, QCoreApplication.translate("PolarisMainWindow", u"Quadratique (ax\u00b2 + bx + c)", None))
        self.comboCorr2.setItemText(3, QCoreApplication.translate("PolarisMainWindow", u"Cubique (ax\u00b3 + bx\u00b2 + cx + d)", None))

        self.lblCVoie3.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie 3", None))
        self.comboCorr3.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"Aucune", None))
        self.comboCorr3.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"Lin\u00e9aire (ax + b)", None))
        self.comboCorr3.setItemText(2, QCoreApplication.translate("PolarisMainWindow", u"Quadratique (ax\u00b2 + bx + c)", None))
        self.comboCorr3.setItemText(3, QCoreApplication.translate("PolarisMainWindow", u"Cubique (ax\u00b3 + bx\u00b2 + cx + d)", None))

        self.btnApplySettings.setText(QCoreApplication.translate("PolarisMainWindow", u"Appliquer les r\u00e9glages", None))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.tabSettings), QCoreApplication.translate("PolarisMainWindow", u"\u2699  R\u00e9glages ", None))
        self.lblPortBronk.setText(QCoreApplication.translate("PolarisMainWindow", u"Port COM :", None))
        self.input_port.setText(QCoreApplication.translate("PolarisMainWindow", u"COM5", None))
        self.btn_scan.setText(QCoreApplication.translate("PolarisMainWindow", u"Connecter", None))
        self.lbl_status.setText(QCoreApplication.translate("PolarisMainWindow", u"En attente\u2026", None))
        self.btn_selection.setText(QCoreApplication.translate("PolarisMainWindow", u"S\u00e9l\u00e9ction", None))
        self.lblWindowBronkLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Fen\u00eatre graphique :", None))
        self.spin_window.setSuffix(QCoreApplication.translate("PolarisMainWindow", u" s", None))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.tabBronkhorst), QCoreApplication.translate("PolarisMainWindow", u"\U0001f4a8  Bronkhorst", None))
        self.lblConnLed.setStyleSheet(QCoreApplication.translate("PolarisMainWindow", u"border:1px solid #888; border-radius:6px; background:#bbb;", None))
        self.lblConnLed.setText("")
        self.lblConnStatus.setText(QCoreApplication.translate("PolarisMainWindow", u"D\u00e9connect\u00e9", None))
        self.lblPortLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Port :", None))
        self.linePort.setText(QCoreApplication.translate("PolarisMainWindow", u"COM8", None))
        self.btnConnect.setText(QCoreApplication.translate("PolarisMainWindow", u"Connecter", None))
        self.btnDisconnect.setText(QCoreApplication.translate("PolarisMainWindow", u"D\u00e9connecter", None))
        self.grpVal.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Mesures", None))
        self.lblTIntLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"T\u00b0 interne :", None))
        self.lblTInt.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblTIntUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.lblTExtLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"T\u00b0 externe :", None))
        self.lblTExt.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblTExtUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.lblPressureLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Puissance :", None))
        self.lblPressure.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblPressureUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"%", None))
        self.lblLevelLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Niveau fluide :", None))
        self.lblLevel.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblLevelUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"%", None))
        self.lblPumpLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Pompe :", None))
        self.lblPumpSpeed.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblPumpUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"%", None))
        self.lblSetpointLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Setpoint :", None))
        self.lblSetpoint.setText(QCoreApplication.translate("PolarisMainWindow", u"\u2014", None))
        self.lblSetpointUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"\u00b0C", None))
        self.grpCtrl.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Contr\u00f4le setpoint", None))
        self.lblNewSp.setText(QCoreApplication.translate("PolarisMainWindow", u"Nouveau setpoint (\u00b0C) :", None))
        self.btnApplySp.setText(QCoreApplication.translate("PolarisMainWindow", u"Appliquer", None))
        self.lblWindowJLabel.setText(QCoreApplication.translate("PolarisMainWindow", u"Fen\u00eatre historique (min) :", None))
        self.btnStart.setText(QCoreApplication.translate("PolarisMainWindow", u"START", None))
        self.btnStop.setText(QCoreApplication.translate("PolarisMainWindow", u"STOP", None))
        self.grpPlots.setTitle(QCoreApplication.translate("PolarisMainWindow", u"Graphique", None))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.tabJulabo), QCoreApplication.translate("PolarisMainWindow", u"\U0001f321  JULABO", None))
        self.groupPid.setTitle(QCoreApplication.translate("PolarisMainWindow", u"R\u00e9gulation PID", None))
        self.lblPidLed.setText("")
        self.lblPidStatus.setText(QCoreApplication.translate("PolarisMainWindow", u"Inactif", None))
        self.chkPidActive.setText(QCoreApplication.translate("PolarisMainWindow", u"Activer / D\u00e9sactiver", None))
        self.lblPidConsigne.setText(QCoreApplication.translate("PolarisMainWindow", u"Consigne HR :", None))
        self.lblPidConsUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"%HR", None))
        self.lblPidKp.setText(QCoreApplication.translate("PolarisMainWindow", u"P :", None))
        self.lblPidKi.setText(QCoreApplication.translate("PolarisMainWindow", u"I :", None))
        self.lblPidKd.setText(QCoreApplication.translate("PolarisMainWindow", u"D :", None))
        self.lblPidAddr.setText(QCoreApplication.translate("PolarisMainWindow", u"Adresse RDM :", None))
        self.lblPidLoop.setText(QCoreApplication.translate("PolarisMainWindow", u"Temps boucle :", None))
        self.lblPidLoopUnit.setText(QCoreApplication.translate("PolarisMainWindow", u"s", None))
        self.lblPidVoie.setText(QCoreApplication.translate("PolarisMainWindow", u"Voie HR :", None))
        self.comboPidVoie.setItemText(0, QCoreApplication.translate("PolarisMainWindow", u"V1", None))
        self.comboPidVoie.setItemText(1, QCoreApplication.translate("PolarisMainWindow", u"V2", None))
        self.comboPidVoie.setItemText(2, QCoreApplication.translate("PolarisMainWindow", u"V3", None))
        self.comboPidVoie.setItemText(3, QCoreApplication.translate("PolarisMainWindow", u"V4", None))

        self.groupPidHelp.setTitle(QCoreApplication.translate("PolarisMainWindow", u"\u00c0 quoi sert le PID ?", None))
        self.lblPidHelp.setText(QCoreApplication.translate("PolarisMainWindow", u"<b>Qu'est-ce que le PID ?</b> Un r\u00e9gulateur <b>PID</b> est un automate qui compare en permanence une <b>mesure</b> \u00e0 une <b>consigne</b> (la valeur vis\u00e9e) et ajuste tout seul une <b>commande</b> pour annuler l'\u00e9cart. Ici, il maintient l'<b>humidit\u00e9</b> \u00e0 la cible en r\u00e9glant le <b>d\u00e9bit</b> d'un d\u00e9bitm\u00e8tre.<br><br><b>Les trois actions :</b> <b>P</b> (proportionnel) r\u00e9agit \u00e0 l'erreur actuelle ; <b>I</b> (int\u00e9gral) rattrape l'erreur accumul\u00e9e pour supprimer l'\u00e9cart r\u00e9siduel ; <b>D</b> (d\u00e9riv\u00e9) anticipe en r\u00e9agissant \u00e0 la vitesse de variation pour limiter les oscillations.<br><br><b>R\u00e9glages par d\u00e9faut :</b> Kp = 0,4 ; Ki = 0,002 ; Kd = 0 ; consigne = 50 % ; p\u00e9riode = 1 s. Valeurs de d\u00e9part prudentes, \u00e0 affiner selon la r\u00e9activit\u00e9 observ\u00e9e.<br><br><b>Adresse 7</b> = le d\u00e9bitm\u00e8tre (RDM) command\u00e9 par le PID, \u00e0 l'adresse 7 sur le bus \u2014 c'est la <i>sortie<"
                        "/i> de la r\u00e9gulation.<br><b>Voie V3</b> = la voie analogique qui <i>mesure</i> l'humidit\u00e9, utilis\u00e9e comme <i>entr\u00e9e</i> du PID.", None))
        self.lblPidSchemaCap.setText(QCoreApplication.translate("PolarisMainWindow", u"Sch\u00e9ma d'une boucle ferm\u00e9e :", None))
        self.tabsMain.setTabText(self.tabsMain.indexOf(self.tabPID), QCoreApplication.translate("PolarisMainWindow", u"PID", None))
    # retranslateUi

