#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: plot_cell_timing.py           #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/13            #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/22      #
# ################################### #

import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from pyqtgraph import PlotWidget 

from lib import *


class PlotCellTiming(QWidget):
    def __init__(self, libdir=LibertyDir()):
        super().__init__()
        self.init_ui()
        self.init_layout()
        self.init_control_panel()

        self.lib = Liberty()
        self.libdir = LibertyDir()
        self.cell = Cell()
        self.output_pin = Pin()

    def update(self, **kwargs):
        corners = kwargs['corners']
        cellnames = kwargs['cellnames']

        if len(corners) > 1:
            print('\nWarning: only timing plot of ONE cell in ONE corner is supported')
            print(f'{len(corners)} corners are selected. Only corner {corners[0]} will be plotted\n')
        if len(corners) < 1:
            print('\nWarning: only timing plot of ONE cell in ONE corner is supported')
            print('No corner is selected\n')

        if len(cellnames) > 1:
            print('\nWarning: only timing plot of ONE cell in ONE corner is supported')
            print(f'{len(cellnames)} cells are selected. Only corner {cellnames[0]} will be plotted\n')
        if len(cellnames) < 1:
            print('\nWarning: only timing plot of ONE cell in ONE corner is supported')
            print('No cell is selected\n')

        self.corner = corners[0]
        self.cellname = cellnames[0]
        self.libdir = kwargs['libdir']
        self.lib = self.libdir.get_lib(self.corner)
        self.cell = self.lib.get_cell(self.cellname)
        try:
            self.output_pin = self.cell.get_output_pins()[self.cell.list_output_pins()[0]]
        except Exception as e:
            print(f'Error: {e}')
            return

        self.control_1_list.clear()
        self.control_2_list.clear()
        self.control_3_list.clear()
        # control panel 1
        try:
            self.timings = self.output_pin.get_attribute('timing')
            for i in range(len(self.timings)):
                new_item = self.timings[i]['related_pin']
                if 'when' in self.timings[i]:
                    new_item += ' (' + self.timings[i]['when'] + ')'
                if 'timing_sense' in self.timings[i]:
                    new_item += ' (' + self.timings[i]['timing_sense'] + ')'
                print(new_item)
                print()
                self.control_1_list.addItem(new_item)
        except Exception as e:
            print(f'Error: {e}')
            return
        # control panel 2
        self.control_2_list.addItems([
            'cell_rise',
            'cell_fall',
            'rise_transition',
            'fall_transition'
        ])
        # control panel 3
        lu_table_key = list(self.timings[0]['cell_rise'].keys())[0]
        self.variable_1 = self.lib.get_attribute('lu_table_template')[lu_table_key]['variable_1']
        self.variable_2 = self.lib.get_attribute('lu_table_template')[lu_table_key]['variable_2']
        self.control_3_list.addItems([
            self.variable_1,
            self.variable_2
        ])


    def init_ui(self):
        # plotting
        self.plot_w = PlotWidget()
        self.plot_w.setBackground('w')
        self.plot_w.showGrid(x=True, y=True)
        self.plot_w.setTitle('Default')
        # control panel 1
        self.control_1_title = QLabel('Related Pin')
        self.control_1_list = QListWidget()
        # control panel 2
        self.control_2_title = QLabel('Timing Type')
        self.control_2_list = QListWidget()
        # control panel 3
        self.control_3_title = QLabel('Plot Setting')
        self.control_3_list = QListWidget()
        #
        self.control_plot = QPushButton('Plot')
        self.control_autorange = QPushButton('Auto Range')

    def init_layout(self):
        # control panel
        control_v = QVBoxLayout()
        control_v.setContentsMargins(0, 0, 0, 0)
        # control panel 1
        control_v.addWidget(self.control_1_title)
        self.control_1_title.setStyleSheet('font: bold')
        control_v.addWidget(self.control_1_list)
        # control panel 2
        control_v.addWidget(self.control_2_title)
        self.control_2_title.setStyleSheet('font: bold')
        control_v.addWidget(self.control_2_list)
        # control panel 3
        control_v.addWidget(self.control_3_title)
        self.control_3_title.setStyleSheet('font: bold')
        control_v.addWidget(self.control_3_list)
        #
        control_v.addWidget(self.control_plot)
        control_v.addWidget(self.control_autorange)
        #
        control_v_w = QWidget()
        control_v_w.setLayout(control_v)
        control_v_w.setFixedWidth(180)

        #
        layout_h = QHBoxLayout()
        layout_h.addWidget(self.plot_w)
        layout_h.addWidget(control_v_w)
        self.setLayout(layout_h)

    def init_control_panel(self):
        self.control_plot.clicked.connect(self._handle_control_plot_clicked)
        self.control_autorange.clicked.connect(self._handle_control_autorange_clicked)

    def _handle_control_autorange_clicked(self):
        self.plot_w.autoRange()

    def _handle_control_plot_clicked(self):
        related_pin = self.control_1_list.currentItem().text()
        related_pin_idx = self.control_1_list.currentRow()
        timing_type = self.control_2_list.currentItem().text()
        x_name = self.control_3_list.currentItem().text()
        flag_use_variable_1 = self.control_3_list.currentRow()
        lu_table_key = list(self.timings[0][timing_type].keys())[0]
        now_timing = self.timings[related_pin_idx][timing_type][lu_table_key]

        if x_name == self.variable_1:
            x_values = now_timing['index_1']
            z_values = now_timing['index_2']
        elif x_name == self.variable_2:
            x_values = now_timing['index_2']
            z_values = now_timing['index_1']
        x_values = x_values.split(',')
        x_values = [float(x) for x in x_values]
        z_values = z_values.split(',')
        z_values = [float(x) for x in z_values]
        values = now_timing['values']
        values = values.split(',')
        values = [float(v) for v in values]

        self.plot_w.clear()
        print(x_values, values, x_name, flag_use_variable_1, related_pin)
        self._display_line_plot(
            x_values=x_values,
            z_values=z_values,
            values=values,
            x_name=x_name,
            flag_use_variable_1=(flag_use_variable_1 == 0),
            related_pin=related_pin
        )
        self.plot_w.autoRange()

    def _display_line_plot(self, x_values, z_values, values, x_name, flag_use_variable_1, related_pin):
        print(f'Displaying delay line plot of cell {self.cellname} with related pin {related_pin} at corner {self.corner}')
        self.plot_w.setTitle(f'{self.cellname} ({self.corner})')
        colors = ['red', 'gold', 'green', 'lime', 'purple', 'cyan', 'fuchsia', 'blue', 'black']
        for i in range(len(z_values)): # use variable_2 as z-axis (different lines)
            pen = pg.mkPen(width=2, color=colors[i % len(colors)])

            if flag_use_variable_1:  # use variable_1 as x_axis, delays as y_axis
                y_values = [values[i + k * len(z_values)] for k in range(len(z_values))]
            else: # use variable_2 as x_axis, delays as y_axis
                y_values = [values[i * len(z_values) + k] for k in range(len(z_values))]
            
            self.plot_w.setLabel('left', 'Delay')
            self.plot_w.setLabel('bottom', x_name)
            self.plot_w.addLegend()
            self.plot_w.plot(x_values, y_values, pen=pen, symbol='+', name=z_values[i])