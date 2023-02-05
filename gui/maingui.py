#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: maingui.py                    #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/5             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/5       #
# ################################### #

import os
import sys
import glob
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, 
    QWidget, QLabel, QPushButton,
    QListWidget, QListWidgetItem,
    QHBoxLayout, QVBoxLayout,
    QFileDialog, QAction,
)
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

from liberty import Liberty


class ListWidgetItemWithCheckbox(QListWidgetItem):
    def __init__(self, text='unkown'):
        super().__init__()
        self.setText(text)
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        self.setCheckState(Qt.Unchecked)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_menu()
        self.init_plotting()

    def init_ui(self):
        self.setWindowTitle('LibertyViewer')
        self.filepath_label = QLabel('Current filepath : None', self)
        self.dirpath_label = QLabel('Current dirpath : None', self)
        self.cells_list = QListWidget(self)
        self.cells_button = QPushButton('Update Cells')
        self.corners_list = QListWidget(self)
        self.corners_button = QPushButton('Update Corners')
        self.plotting = pg.PlotWidget()
        
        # buttons
        
        # cells
        cells_v = QVBoxLayout()
        cells_v.addWidget(self.cells_list)
        cells_v.addWidget(self.cells_button)

        # corners
        corners_v = QVBoxLayout()
        corners_v.addWidget(self.corners_list)
        corners_v.addWidget(self.corners_button)

        # plotting
        plot_v = QVBoxLayout()
        plot_v.addWidget(self.plotting)

        # horizontal layout
        ui_h = QHBoxLayout()
        ui_h.addLayout(cells_v)
        ui_h.addLayout(plot_v)
        ui_h.addLayout(corners_v)

        # vertical layout
        ui_v = QVBoxLayout()
        ui_v.addWidget(self.filepath_label)
        ui_v.addWidget(self.dirpath_label)
        ui_v.addLayout(ui_h)

        #
        widget = QWidget()
        widget.setLayout(ui_v)
        self.setCentralWidget(widget)
    
    def init_menu(self):
        menu = self.menuBar()

        # 'File'
        file_menu = menu.addMenu('&File')
        openfile_action = QAction('Open File', self)
        openfile_action.triggered.connect(self._open_file_dialog)
        file_menu.addAction(openfile_action)
        opendirectory_action = QAction('Open Directory', self)
        opendirectory_action.triggered.connect(self._open_directory_dialog)
        file_menu.addAction(opendirectory_action)

        # 'Plot'
        plot_menu = menu.addMenu('&Plot')

        # 'Help'
        help_menu = menu.addMenu('&Help')

    def init_plotting(self):
        self.plotting.setBackground('w')
        self.plotting.showGrid(x=True, y=True)

    def _create_checkbox_list(self, the_list, item_names):
        for name in item_names:
            item = ListWidgetItemWithCheckbox(name)
            the_list.addItem(item)

    def _open_directory_dialog(self):
        dirpath = QFileDialog.getExistingDirectory(
            self,
            caption='Open Directory',
        )
        if dirpath:
            print(f'Loading directory: {dirpath}')
            # update
            self.dirpath_label.setText(f'Current dirpath : {dirpath}')
            corners = [os.path.basename(fp) for fp in glob.glob(dirpath + '/*.json')]
            corners = [fn[:fn.find('.')] for fn in corners]
            self._create_checkbox_list(self.corners_list, corners)

    def _open_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption='Open File',
            filter='JSON Files (*.json)'
        )
        if filepath:
            print(f'Loading file: {filepath}')
            self.lib = Liberty(filepath=filepath)
            # update
            self.filepath_label.setText(f'Current filepath : {filepath}')
            self._create_checkbox_list(self.cells_list, self.lib.list_cells())