#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: plot_default.py               #
# Version: 0.0.1                      #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/8             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/19      #
# ################################### #

from random import randint
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)
from pyqtgraph import PlotWidget 

from lib import *


class PlotDefault(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_layout()
        self.init_control_panel()
        self.maxn = 10
        self.type = None

    def update(self, **kwargs):
        print(kwargs)

    def init_ui(self):
        # plotting
        self.plot_w = PlotWidget()
        self.plot_w.setBackground('w')
        self.plot_w.showGrid(x=True, y=True)
        self.plot_w.setTitle('Default')
        # control panel 1
        self.control_1_title = QLabel('Plot Control Panel')
        self.control_1_list = QListWidget()
        # control panel 2
        self.control_2_title = QLabel('Number Control Panel')
        self.control_2_list = QListWidget()
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
        # control panel 1
        self.control_1_list.addItems([
            'plain plot',
            'scatter plot',
            'line plot'
        ])
        self.control_1_list.currentTextChanged.connect(self._handle_control_plot_1_clicked)
        # control panel 2
        self.control_2_list.addItems([
            '10',
            '100',
            '1000'
        ])
        self.control_2_list.currentTextChanged.connect(self._handle_control_plot_2_clicked)
        #
        self.control_plot.clicked.connect(self._handle_control_plot_clicked)
        self.control_autorange.clicked.connect(self._handle_control_autorange_clicked)

    def _handle_control_autorange_clicked(self):
        self.plot_w.autoRange()

    def _handle_control_plot_clicked(self):
        self.plot_w.clear()
        if self.type == 'plain plot':
            self._display_plain_plot()
        elif self.type == 'scatter plot':
            self._display_scatter_plot()
        elif self.type == 'line plot':
            self._display_line_plot()
        self.plot_w.autoRange()

    def _handle_control_plot_1_clicked(self):
        self.type = self.control_1_list.currentItem().text()
        print(f'selected type = {self.type}')

    def _handle_control_plot_2_clicked(self):
        self.maxn = int(self.control_2_list.currentItem().text())
        print(f'selected maxn = {self.maxn}')

    def _display_plain_plot(self):
        print('Display default plot')
        self.plot_w.setTitle('Default')

    def _display_scatter_plot(self):
        print('Display random scatter plot')
        self.plot_w.setTitle('Random Scatter Plot')
        scatter = pg.ScatterPlotItem(symbol='o', size=2)
        self.plot_w.addItem(scatter)
        n = 1000
        x = [randint(0, self.maxn) for _ in range(n)]
        y = [randint(0, self.maxn) for _ in range(n)]
        pens = [pg.mkPen(width=5, color=pg.intColor(randint(0, 1000))) for _ in range(n)]
        scatter.setData(x, y, pen=pens)

    def _display_line_plot(self):
        print('Display random line plot')
        self.plot_w.setTitle('Random Line Plot')
        for _ in range(5):
            pen = pg.mkPen(width=2, color=pg.intColor(randint(0, 1000)))
            n = 20
            x = [i for i in range(n)]
            y = [randint(0, self.maxn) for _ in range(n)]
            self.plot_w.plot(x, y, pen=pen, symbol='+')