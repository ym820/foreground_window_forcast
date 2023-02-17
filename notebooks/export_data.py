import sqlite3 as sql
import os
import csv
from sqlite3 import Error

def get_input_output_folder(dafault_path = True):
    if default_path:
        os.chdir("../../../data/raw/outputs/")
        input_folder = os.fspath(os.getcwd())
        os.chdir("../../processed/")
        output_folder = os.fspath(os.getcwd())