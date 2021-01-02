# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 21:42:34 2021

@author: bjusp
"""

#!/usr/bin/env python3
import sys
import csv
import os

def process_csv(csv_file):
    """Turn the contents of the CSV file into a list of lists"""
    print("Processing {}".format(csv_file))
    with open(csv_file,"r") as datafile:
        data = list(csv.reader(datafile))
    return data
