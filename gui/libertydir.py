#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: libertydir.py                 #
# Version: 1.0                        #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/6             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/6       #
# ################################### #

import os
import glob

from liberty import Liberty


class LibertyDir():
    def __init__(self, dirpath, corners_filters=['pg', 'dlvl', 'ulvl']):
        self.dirpath = dirpath
        self.filepaths = glob.glob(dirpath + '/*.json')
        self.corners = []
        self.corners_filters = corners_filters
        self.corners_groups = {}
        #
        corners = [os.path.basename(fp) for fp in self.filepaths]
        corners = [fn[:fn.find('.')] for fn in corners]
        self.corners = corners
        #
        self.filepaths.sort()
        self.corners.sort()
        #
        is_selected = []
        for filtre in self.corners_filters:
            corners = [corner for corner in self.corners if corner.find(filtre) != -1]
            if len(corners):
                self.corners_groups[filtre] = corners
                is_selected.extend(corners)
        self.corners_groups['base'] = [corner for corner in self.corners if corner not in is_selected]