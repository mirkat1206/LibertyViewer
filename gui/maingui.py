#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: maingui.py                    #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/5             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/19      #
# ################################### #

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QLabel, QTabWidget, QPushButton,
    QListWidget, QListWidgetItem,
    QHBoxLayout, QVBoxLayout,
    QFileDialog, QAction
)
from PyQt5.QtGui import QIcon

from lib import *
from plotting import *


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
        self.init_buttons()
        self.libdir = None
        self.selected_corners = []
        self.selected_cellnames = []

    def init_ui(self):
        self.setWindowTitle('LibertyViewer')
        self.setWindowIcon(QIcon('./image/taiwan_black_bear.png'))
        self.resize(1200, 600)
        # corners
        self.corners_title = QLabel('Corners')
        self.corners_tabs = QTabWidget()
        self.corners_list = QListWidget()
        self.corners_select = QPushButton('Select')
        self.corners_select_all = QPushButton('Select All')
        self.corners_clear_all = QPushButton('Clear All')
        # cells
        self.cells_title = QLabel('Cells')
        self.cells_list = QListWidget()
        self.cells_select = QPushButton('Select')
        self.cells_select_all = QPushButton('Select All')
        self.cells_clear_all = QPushButton('Clear All')
        # plotting
        self.plot_w = PlotDefault()
        # self.plot_w = PlotCellTiming()
        
    def init_layout(self):
        # corners
        corners_v = QVBoxLayout()
        corners_v.setContentsMargins(0, 0, 0, 0)
        corners_v.addWidget(self.corners_title)
        self.corners_title.setStyleSheet('font: bold')
        corners_v.addWidget(self.corners_tabs)
        self.corners_tabs.setTabPosition(QTabWidget.North)
        self.corners_tabs.setMovable(False)
        corners_v.addWidget(self.corners_select)
        corners_v.addWidget(self.corners_select_all)
        corners_v.addWidget(self.corners_clear_all)
        corners_v_w = QWidget()
        corners_v_w.setLayout(corners_v)
        corners_v_w.setFixedWidth(260)

        # cells
        cells_v = QVBoxLayout()
        cells_v.setContentsMargins(0, 0, 0, 0)
        cells_v.addWidget(self.cells_title)
        self.cells_title.setStyleSheet('font: bold')
        cells_v.addWidget(self.cells_list)
        cells_v.addWidget(self.cells_select)
        cells_v.addWidget(self.cells_select_all)
        cells_v.addWidget(self.cells_clear_all)
        cells_v_w = QWidget()
        cells_v_w.setLayout(cells_v)
        cells_v_w.setFixedWidth(180)

        # horizontal layout
        ui_h = QHBoxLayout()
        ui_h.addWidget(corners_v_w)
        ui_h.addWidget(cells_v_w)
        ui_h.addWidget(self.plot_w)

        # vertical layout
        ui_v = QVBoxLayout()
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
        plottiming_action = QAction('Timing', self)
        # plottiming_action.triggered.connect(self._plot_update)
        plot_menu.addAction(plottiming_action)

        # 'Help'
        help_menu = menu.addMenu('&Help')

    def init_buttons(self):
        # corners
        self.corners_select.clicked.connect(self._handle_corners_select_clicked)
        self.corners_select_all.clicked.connect(self._handle_corners_select_all_clicked)
        self.corners_clear_all.clicked.connect(self._handle_corners_clear_all_clicked)
        # cells
        self.cells_select.clicked.connect(self._handle_cells_select_clicked)
        self.cells_select_all.clicked.connect(self._handle_cells_select_all_clicked)
        self.cells_clear_all.clicked.connect(self._handle_cells_clear_all_clicked)
        #
        self.corners_select.clicked.connect(self._plot_update)
        self.corners_select_all.clicked.connect(self._plot_update)
        self.corners_clear_all.clicked.connect(self._plot_update)
        self.cells_select.clicked.connect(self._plot_update)
        self.cells_select_all.clicked.connect(self._plot_update)
        self.cells_clear_all.clicked.connect(self._plot_update)

    def _plot_update(self):
        self.plot_w.update()

    def _handle_select_clicked(self, the_list):
        selected = []
        for i in range(the_list.count()):
            if the_list.item(i).checkState() == Qt.Checked:
                selected.append(the_list.item(i).text())
        return selected

    def _handle_corners_select_clicked(self):
        self.selected_corners = self._handle_select_clicked(self.corners_tabs.currentWidget())
        print(f'{len(self.selected_corners)} corners selected: \n{self.selected_corners}')

    def _handle_cells_select_clicked(self):
        self.selected_cellnames = self._handle_select_clicked(self.cells_list)
        print(f'{len(self.selected_cellnames)} cells selected: \n{self.selected_cellnames}')

    def _handle_select_all_clicked(self, the_list):
        selected = []
        for i in range(the_list.count()):
            the_list.item(i).setCheckState(Qt.Checked)
            selected.append(the_list.item(i).text())
        return selected

    def _handle_corners_select_all_clicked(self):
        self.selected_corners = self._handle_select_all_clicked(self.corners_tabs.currentWidget())
        print(f'{len(self.selected_corners)} corners selected: \n{self.selected_corners}')

    def _handle_cells_select_all_clicked(self):
        self.selected_cellnames = self._handle_select_all_clicked(self.cells_list)
        print(f'{len(self.selected_cellnames)} cells selected: \n{self.selected_cellnames}')

    def _handle_clear_all_clicked(self, the_list):
        selected = []
        for i in range(the_list.count()):
            the_list.item(i).setCheckState(Qt.Unchecked)
        return selected

    def _handle_corners_clear_all_clicked(self):
        self.selected_corners = self._handle_clear_all_clicked(self.corners_tabs.currentWidget())
        print(f'{len( self.selected_corners)} corners selected: \n{self.selected_corners}')

    def _handle_cells_clear_all_clicked(self):
        self.selected_cellnames = self._handle_clear_all_clicked(self.cells_list)
        print(f'{len(self.selected_cellnames)} cells selected: \n{self.selected_cellnames}')

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
            self.setWindowTitle(f'LibertyViewer : {dirpath}')
            self.libdir = LibertyDir(dirpath)
            if dirpath == '.':
                self.libdir.update()
            self._create_corners_tabs()
            # reset
            self.cells_list.clear()
            self._handle_corners_tabs_clicked(0)

    def _open_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption='Open File',
            filter='JSON Files (*.json)'
        )
        if filepath:
            print(f'Loading file: {filepath}')
            # update
            self.setWindowTitle(f'LibertyViewer : {filepath}')
            self.lib = Liberty(filepath=filepath)
            self._create_checkbox_list(self.cells_list, self.lib.list_cells())
            # reset
            self.corners_tabs.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())            