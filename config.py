import os
import sys


def add_parent_to_path():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    sys.path.append(PARENT_DIR)
