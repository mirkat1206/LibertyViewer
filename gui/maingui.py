#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: maingui.py                    #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/5             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/6       #
# ################################### #

import os
import sys
import glob
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QLabel, QTabWidget, QPushButton,
    QListWidget, QListWidgetItem,
    QHBoxLayout, QVBoxLayout,
    QFileDialog, QAction,
)
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot

from liberty import Liberty
from libertydir import LibertyDir


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
        self.init_layout()
        self.init_menu()
        self.init_plotting()

    def init_ui(self):
        self.setWindowTitle('LibertyViewer')
        self.resize(1200, 600)
        self.corners_filters=['pg', 'dlvl', 'ulvl']
        #
        self.filepath_label = QLabel('Current filepath : None', self)
        self.dirpath_label = QLabel('Current dirpath : None', self)
        #
        self.cells_list = QListWidget(self)
        self.cells_button = QPushButton('Select Cells')
        #
        self.corners_tabs = QTabWidget(self)
        self.corners_list = QListWidget(self)
        self.corners_button = QPushButton('Select Corners')
        #
        self.plotting = pg.PlotWidget(self)
        
    def init_layout(self):
        # corners
        corners_v = QVBoxLayout()
        corners_v.addWidget(self.corners_tabs)
        self.corners_tabs.setTabPosition(QTabWidget.North)
        self.corners_tabs.setMovable(False)
        corners_v.addWidget(self.corners_button)
        corners_v_w = QWidget()
        corners_v_w.setLayout(corners_v)
        corners_v_w.setFixedWidth(260)

        # cells
        cells_v = QVBoxLayout()
        cells_v.addWidget(self.cells_list)
        cells_v.addWidget(self.cells_button)
        cells_v_w = QWidget()
        cells_v_w.setLayout(cells_v)
        cells_v_w.setFixedWidth(200)

        # plotting
        plot_v = QVBoxLayout()
        plot_v.addWidget(self.plotting)

        # horizontal layout
        ui_h = QHBoxLayout()
        ui_h.addWidget(corners_v_w)
        ui_h.addWidget(cells_v_w)
        ui_h.addLayout(plot_v)

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

        # 'Setting'
        setting_menu = menu.addMenu('&Setting')

        # 'Plot'
        plot_menu = menu.addMenu('&Plot')

        # 'Help'
        help_menu = menu.addMenu('&Help')

    def init_plotting(self):
        self.plotting.setBackground('w')
        self.plotting.showGrid(x=True, y=True)

    def _create_checkbox_list(self, the_list, item_names):
        the_list.clear()
        for name in item_names:
            item = ListWidgetItemWithCheckbox(name)
            the_list.addItem(item)

    def _create_corners_tabs(self):
        self.corners_tabs.clear()
        for k, v in self.libdir.corners_by_groups.items():
            corners_list = QListWidget(self)
            self._create_checkbox_list(corners_list, v)
            self.corners_tabs.addTab(corners_list, k)
        self.corners_tabs.tabBarClicked.connect(self._handle_corners_tabs_clicked)

    def _handle_corners_tabs_clicked(self, index):
        filtre = self.corners_tabs.tabText(index)
        self._create_checkbox_list(self.cells_list, self.libdir.cells_by_groups[filtre])

    def _open_directory_dialog(self):
        dirpath = QFileDialog.getExistingDirectory(
            self,
            caption='Open Directory',
        )
        if dirpath:
            print(f'Loading directory: {dirpath}')
            # update
            self.dirpath_label.setText(f'Current dirpath : {dirpath}')
            self.libdir = LibertyDir(dirpath)
            self._create_corners_tabs()
            # reset
            self.filepath_label.setText('Current filepath : None')
            self.cells_list.clear()

    def _open_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption='Open File',
            filter='JSON Files (*.json)'
        )
        if filepath:
            print(f'Loading file: {filepath}')
            # update
            self.lib = Liberty(filepath=filepath)
            self.filepath_label.setText(f'Current filepath : {filepath}')
            self._create_checkbox_list(self.cells_list, self.lib.list_cells())
            # reset
            self.dirpath_label.setText('Current dirpath : None')
            self.corners_tabs.clear()