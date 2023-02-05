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

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QFileDialog,
    QAction,
)

from liberty import Liberty

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_menu()

    def init_ui(self):
        self.setWindowTitle('LibertyViewer')
    
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

    def _open_directory_dialog(self):
        dirpath = QFileDialog.getExistingDirectory(
            self,
            caption='Open Directory',
        )
        if dirpath:
            print(f'Loading directory: {dirpath}')

    def _open_file_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            caption='Open File',
            filter='JSON Files (*.json)'
        )
        if filepath:
            print(f'Loading file: {filepath}')
            self.lib = Liberty(filepath=filepath)