# -*- coding: utf-8 -*-

"""
A threaded GUI Monitor with Python and PyQt4 plots live data using PythonQwt

Code modified from mba7 (monta.bha@gmail.com)

License: this code is in the public domain

Author:   Cheng Tianshi
Email:    chengts95@163.com

Last modified: 2016.7.28

"""

import random
import sys
import queue
import serial
import glob
import os
import csv
import time

import qwt as Qwt
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from DHT_monitor_thread import ComMonitorThread
from DHT_globals import *


class PlottingDataMonitor(QMainWindow):

    def __init__(self, parent=None):

        super(PlottingDataMonitor, self).__init__(parent)

        self.setWindowIcon(QIcon('seu.ico'))

        self.setWindowTitle('DHT11 Real-time Monitor')
        self.resize(800, 600)

        self.port = ""
        self.baudrate = 9600
        self.monitor_active = False  # on/off monitor state
        self.com_monitor = None  # monitor reception thread
        self.com_data_q = None
        self.com_error_q = None

        self.livefeed = LiveDataFeed()
        self.timer = QTimer()

        self.g_samples = [[], [], []]
        self.curve = [None] * 3
        self.gcurveOn = [1] * 3  # by default all curve are plotted

        self.csvdata = []

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()

        # Activate start-stop button connections
        self.connect(self.button_Connect, SIGNAL("clicked()"),
                     self.OnStart)
        self.connect(self.button_Disconnect, SIGNAL("clicked()"),
                     self.OnStop)

    def create_com_box(self):
        """
        Purpose:   create the serial com groupbox
        Return:    return a layout of the serial com
        """
        self.com_box = QGroupBox("COM Configuration")

        #  Grid Layout
        com_layout = QGridLayout()

        self.radio9600 = QRadioButton("9600")
        self.radio9600.setChecked(1)
        self.radio19200 = QRadioButton("19200")
        self.Com_ComboBox = QComboBox()

        com_layout.addWidget(self.Com_ComboBox, 0, 0, 1, 2)
        com_layout.addWidget(self.radio9600, 1, 0)
        com_layout.addWidget(self.radio19200, 1, 1)
        self.fill_ports_combobox()

        self.button_Connect = QPushButton("Start")
        self.button_Disconnect = QPushButton("Stop")
        self.button_Disconnect.setEnabled(False)

        com_layout.addWidget(self.button_Connect, 0, 2)
        com_layout.addWidget(self.button_Disconnect, 1, 2)

        return com_layout

    def create_plot(self):
        """
        Purpose:   create the pyqwt plot
        Return:    return a list containing the plot and the list of the curves
        """
        plot = Qwt.QwtPlot(self)
        plot.setCanvasBackground(Qt.black)

        plot.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time')
        plot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 10, 1)

        plot.setAxisTitle(Qwt.QwtPlot.yLeft, 'Temperature')
        plot.setAxisScale(
            Qwt.QwtPlot.yLeft, LeftYMIN, LeftYMAX, (LeftYMAX - LeftYMIN) / 5)

        plot.setAxisTitle(Qwt.QwtPlot.yRight, 'Humidity')
        plot.setAxisScale(
            Qwt.QwtPlot.yRight, RightYMIN, RightYMAX, (RightYMAX - RightYMIN) / 5)
        plot.replot()

        curve = [None] * 3
        pen = [QPen(QColor('red')), QPen(
            QColor('green')), QPen(QColor('blue'))]

        for i in range(3):
            curve[i] = Qwt.QwtPlotCurve('')
            curve[i].setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
            pen[i].setWidth(2)
            curve[i].setPen(pen[i])
            curve[i].attach(plot)

        return plot, curve

    def create_tableview(self):
        """
        Purpose:   create the table
        Return:    return a table containing the list of the data
        """
        self.RowCount = 5
        self.currecordid = 0

        table = QTableWidget()
        table.setRowCount(self.RowCount)
        table.setColumnCount(4)

        table.setHorizontalHeaderLabels(['Time', 'T', 'H', 'HI'])
        table.horizontalHeader().setStretchLastSection(True)
        table.setColumnWidth(0, 80)
        table.setColumnWidth(1, 75)
        table.setColumnWidth(2, 75)
        for x in range(table.columnCount()):
            headItem = table.horizontalHeaderItem(x)
            headItem.setTextColor(QColor(200, 111, 30))

        return table

    def create_status_bar(self):
        self.status_text = QLabel('Monitor idle')
        self.statusBar().addWidget(self.status_text, 1)

    def create_checkbox(self, label, color, connect_fn, connect_param):
        """
        Purpose:    create a personalized checkbox
        Input:      the label, color, activated function and the transmitted parameter
        Return:     return a checkbox widget
        """
        checkBox = QCheckBox(label)
        checkBox.setChecked(1)
        checkBox.setFont(QFont("Arial", pointSize=9, weight=QFont.Bold))
        green = QPalette()
        green.setColor(QPalette.Foreground, color)
        checkBox.setPalette(green)
        self.connect(
            checkBox, SIGNAL("clicked()"), partial(connect_fn, connect_param))
        return checkBox

    def create_main_frame(self):
        """
        Purpose:    create the main frame Qt widget
        """
        # Serial communication combo box
        portname_layout = self.create_com_box()
        self.com_box.setLayout(portname_layout)

        # Create the plot and curves
        self.plot, self.curve = self.create_plot()

        # Create the tableview
        self.table = self.create_tableview()

        # Create the configuration horizontal panel
        self.max_spin = QSpinBox()
        self.max_spin.setMaximum(1000)
        self.max_spin.setValue(savedsamples)
        spins_hbox = QHBoxLayout()
        spins_hbox.addWidget(QLabel('Save every'))
        spins_hbox.addWidget(self.max_spin)
        spins_hbox.addWidget(QLabel('Samples'))

        # spins_hbox.addStretch(1)

        self.gCheckBox = [self.create_checkbox("Temperature(t)", Qt.red, self.activate_curve, 0),
                          self.create_checkbox(
                              "Humidity(h)", Qt.green, self.activate_curve, 1),
                          self.create_checkbox(
                              "Heat Index(a)", Qt.blue, self.activate_curve, 2)
                          ]

        self.button_clear = QPushButton("Clear screen")

        self.connect(self.button_clear, SIGNAL("clicked()"), self.clear_screen)

        # Place the horizontal panel widget
        # GridLayout
        plot_layout = QGridLayout()
       # void QGridLayout::addWidget
       # (QWidget * widget, int fromRow, int fromColumn,
       # int rowSpan, int columnSpan, Qt::Alignment alignment = 0)
        plot_layout.addWidget(self.plot, 0, 0, 9, 6)

        plot_layout.addWidget(self.table, 4, 6, 3, 3)

        plot_layout.addWidget(self.gCheckBox[0], 0, 6)
        plot_layout.addWidget(self.gCheckBox[1], 1, 6)
        plot_layout.addWidget(self.gCheckBox[2], 2, 6)

        plot_layout.addWidget(self.button_clear, 3, 6, 1, 2)

        plot_layout.addLayout(spins_hbox, 3, 8)

        plot_groupbox = QGroupBox('DHT11')
        plot_groupbox.setLayout(plot_layout)

        # Place the main frame and layout
        #  main_layout： QVBoxLayout
        #    self.com_box：self.com_box.setLayout(portname_layout)
        #    plot_groupbox： plot_groupbox.setLayout(plot_layout)
        #
        self.main_frame = QWidget()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.com_box)
        main_layout.addWidget(plot_groupbox)

        main_layout.addStretch(1)
        self.main_frame.setLayout(main_layout)

        self.setCentralWidget(self.main_frame)

    def clear_screen(self):
        g_samples[0] = []

    def activate_curve(self, axe):
        if self.gCheckBox[axe].isChecked():
            self.gcurveOn[axe] = 1
        else:
            self.gcurveOn[axe] = 0

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        selectport_action = self.create_action("Select COM &Port...",
                                               shortcut="Ctrl+P", slot=self.on_select_port, tip="Select a COM port")
        self.start_action = self.create_action("&Start monitor",
                                               shortcut="Ctrl+M", slot=self.OnStart, tip="Start the data monitor")
        self.stop_action = self.create_action("&Stop monitor",
                                              shortcut="Ctrl+T", slot=self.OnStop, tip="Stop the data monitor")
        exit_action = self.create_action("E&xit", slot=self.close,
                                         shortcut="Ctrl+X", tip="Exit the application")

        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(False)

        self.add_actions(self.file_menu,
                         (selectport_action, self.start_action, self.stop_action,
                          None, exit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About",
                                          shortcut='F1', slot=self.on_about,
                                          tip='About the monitor')

        self.add_actions(self.help_menu, (about_action,))

    def set_actions_enable_state(self):
        if self.portname.text() == '':
            start_enable = stop_enable = False
        else:
            start_enable = not self.monitor_active
            stop_enable = self.monitor_active

        self.start_action.setEnabled(start_enable)
        self.stop_action.setEnabled(stop_enable)

    def on_about(self):
        msg = __doc__
        QMessageBox.about(self, "About the demo", msg.strip())

    def on_select_port(self):

        ports = enumerate_serial_ports()

        if len(ports) == 0:
            QMessageBox.critical(self, 'No ports',
                                 'No serial ports found')
            return

        item, ok = QInputDialog.getItem(self, 'Select a port',
                                        'Serial port:', ports, 0, False)

        if ok and not (item==''):
            self.portname.setText(item)
            self.set_actions_enable_state()

    def fill_ports_combobox(self):
        """
          Purpose: rescan the serial port com and update the combobox
        """
        vNbCombo = ""
        self.Com_ComboBox.clear()
        self.AvailablePorts = enumerate_serial_ports()
        for value in self.AvailablePorts:
            self.Com_ComboBox.addItem(value)
            vNbCombo += value + " - "
        vNbCombo = vNbCombo[:-3]

        debug(("--> Les ports series disponibles sont: %s " % (vNbCombo)))

    def OnStart(self):
        """
          Start the monitor: com_monitor thread and the update timer
        """
        if self.radio19200.isChecked():
            self.baudrate = 19200
            print("--> baudrate is 19200 bps")
        if self.radio9600.isChecked():
            self.baudrate = 9600
            print("--> baudrate is 9600 bps")

        vNbCombo = self.Com_ComboBox.currentIndex()
        self.port = self.AvailablePorts[vNbCombo]

        self.button_Connect.setEnabled(False)
        self.button_Disconnect.setEnabled(True)
        self.Com_ComboBox.setEnabled(False)

        self.data_q = queue.Queue()
        self.error_q = queue.Queue()
        self.com_monitor = ComMonitorThread(
            self.data_q,
            self.error_q,
            self.port,
            self.baudrate)

        self.com_monitor.start()

        com_error = get_item_from_queue(self.error_q)
        if com_error is not None:
            QMessageBox.critical(self, 'ComMonitorThread error',
                                 com_error)
            self.com_monitor = None

        self.monitor_active = True

        self.connect(self.timer, SIGNAL('timeout()'), self.on_timer)

        update_interval = 2000
        if update_interval > 0:
            self.timer.start(update_interval)

        self.status_text.setText('Monitor running')

        debug('--> Monitor running')

    def OnStop(self):
        """
          Stop the monitor
        """
        if self.com_monitor is not None:
            self.com_monitor.join(1000)
            self.com_monitor = None

        self.monitor_active = False
        self.button_Connect.setEnabled(True)
        self.button_Disconnect.setEnabled(False)
        self.Com_ComboBox.setEnabled(True)
        self.timer.stop()
        self.status_text.setText('Monitor idle')
        debug('--> Monitor idle')

    def on_timer(self):
        """
          Executed periodically when the monitor update timer
            is fired.
        """
        self.read_serial_data()
        self.update_monitor()

    def update_monitor(self):
        """
            Updates the state of the monitor window with new
            data. The livefeed is used to find out whether new
            data was received since the last update. If not,
            nothing is updated.
        """
        if self.livefeed.has_new_data:

            data = self.livefeed.read_data()

            if self.currecordid == self.RowCount:
                self.currecordid = self.RowCount - 1
                for i in range(1, self.table.rowCount()):
                    for j in range(self.table.columnCount()):
                        cnt = self.table.item(i, j)
                        newItem = QTableWidgetItem(cnt)
                        self.table.setItem(i - 1, j, newItem)

            x = time.localtime(data['timestamp'])
            cnt = time.strftime('%H:%M:%S', x)

            tableItem = QTableWidgetItem(cnt)
            tableItem.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.table.setItem(self.currecordid, 0, tableItem)

            cnt = str('%.2f  ' % data['t'])
            tableItem = QTableWidgetItem(cnt)
            tableItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(self.currecordid, 1, tableItem)

            cnt = str('%.2f  ' % data['h'])
            tableItem = QTableWidgetItem(cnt)
            tableItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(self.currecordid, 2, tableItem)

            cnt = str('%.2f  ' % data['d'])
            tableItem = QTableWidgetItem(cnt)
            tableItem.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(self.currecordid, 3, tableItem)

            self.currecordid += 1

            # save data 
            self.csvdata.append(
                [data['timestamp'], data['t'], data['h'], data['d']])
            print(len(self.csvdata))
            if len(self.csvdata) > self.max_spin.value():
                f = open(time.strftime("%H%M%S") + ".csv", 'wt')
                print(time.strftime("%H%M%S") + ".csv")
                try:
                    writer = csv.writer(f)
                    for i in range(self.max_spin.value()):
                        writer.writerow(self.csvdata[i])
                    print('transfert data to csv after set samples')
                finally:
                    f.close()
                self.csvdata = []

            self.g_samples[0].append(
                (data['timestamp'], data['t']))
            if len(self.g_samples[0]) > 100:
                self.g_samples[0].pop(0)

            self.g_samples[1].append(
                (data['timestamp'], data['h']))
            if len(self.g_samples[1]) > 100:
                self.g_samples[1].pop(0)

            self.g_samples[2].append(
                (data['timestamp'], data['d']))
            if len(self.g_samples[2]) > 100:
                self.g_samples[2].pop(0)

            tdata = [s[0] for s in self.g_samples[2]]

            for i in range(3):
                data[i] = [s[1] for s in self.g_samples[i]]
                if self.gcurveOn[i]:
                    self.curve[i].setData(tdata, data[i])

            """
            debug("tdata", data[0])
            debug("hdata", data[1])
            debug("ddata", data[2])
            """

            self.plot.setAxisScale(
                Qwt.QwtPlot.xBottom, tdata[0], max(5, tdata[-1]))
            self.plot.replot()

    def read_serial_data(self):
        """ Called periodically by the update timer to read data
            from the serial port.
        """
        qdata = list(get_all_from_queue(self.data_q))
        # get just the most recent data, others are lost
        # print "qdata" , qdata
        if len(qdata) > 0:
            data = dict(timestamp=qdata[-1][1],
                        t=qdata[-1][0][0],
                        h=qdata[-1][0][1],
                        d=qdata[-1][0][2]
                        )
            self.livefeed.add_data(data)

    # The following two methods are utilities for simpler creation
    # and assignment of actions
    #
    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QApplication(sys.argv)
    form = PlottingDataMonitor()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
