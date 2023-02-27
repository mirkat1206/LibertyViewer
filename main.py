#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: main.py                       #
# Version: 0.0.1                      #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/5             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/8       #
# ################################### #

import sys
from PyQt5.QtWidgets import QApplication

from gui.maingui import MainWindow


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())