#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ################################### #
# File: libertydir.py                 #
# Version: 0.0.1                      #
# @author: Shiuan-Yun Ding            #
# @email: mirkat.ding@gmail.com       #
# @date created: 2023/2/6             #
# @last modified by: Shiuan-Yun Ding  #
# @last modified date: 2023/2/19      #
# ################################### #

import os
import glob

from lib import *


class LibertyDir():
    def __init__(self, dirpath='.', corners_filters=['pg', 'dlvl', 'ulvl']):
        self.dirpath = dirpath
        self.corners = []
        self.corners_filters = corners_filters
        self.corners_by_groups = {}
        self.cells_by_groups = {}

        if self.dirpath != '.':
            self.update()
    
    def update(self):
        filepaths = glob.glob(self.dirpath + '/*.json')
        corners = [os.path.basename(fp) for fp in filepaths]
        corners = [fn[:fn.find('.')] for fn in corners]
        self.corners = corners
        self.corners.sort()
        #
        is_selected = []
        for filtre in self.corners_filters:
            corners = [corner for corner in self.corners if corner.find(filtre) != -1]
            if len(corners):
                self.corners_by_groups[filtre] = corners
                is_selected.extend(corners)
        self.corners_by_groups['base'] = [corner for corner in self.corners if corner not in is_selected]
        #
        for filtre, corners_by_group in self.corners_by_groups.items():
            lib = Liberty(filepath=f'{self.dirpath}/{corners_by_group[0]}.json')
            self.cells_by_groups[filtre] = lib.list_cells()
        self.check_cells_consistency()

    def get_lib(self, corner_name):
        return Liberty(filepath=(self.dirpath + '/' + corner_name + '.json'))

    def check_cells_consistency(self):
        for filtre, corners_by_group in self.corners_by_groups.items():
            golden_cells = self.cells_by_groups[filtre]
            for i in range(len(corners_by_group)):
                lib = Liberty(filepath=f'{self.dirpath}/{corners_by_group[i]}.json')
                cells = lib.list_cells()
                if golden_cells != cells:
                    raise AssertionError(f'Error: cells consistency check fails '
                                         f'at corner \"{corners_by_group[i]}\" of group \"{filtre}\"')
        print('Cell consistency check Passed!')