#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: plot_default.py               #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/8             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/8       #
# ################################### #

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QLabel, QTabWidget, QPushButton,
    QListWidget, QListWidgetItem,
    QHBoxLayout, QVBoxLayout,
    QFileDialog, QAction,
)
from pyqtgraph import PlotWidget, plot

from lib import *

class PlotDefault(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_layout()
    
    def init_ui(self):
        self.plotting = PlotWidget()
        self.plotting.setBackground('w')
        self.plotting.showGrid(x=True, y=True)
        self.plotting.setTitle('Default')

    def init_layout(self):
        layout_h = QHBoxLayout()
        layout_h.addWidget(self.plotting)
        self.setLayout(layout_h)