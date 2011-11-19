import sys
import os

here_folder = os.path.dirname(os.path.abspath(__file__))

def monkey_patch():
    sys.path.insert(0, os.path.join(here_folder, "fake_openerp"))

