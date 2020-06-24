# -*- coding: utf-8 -*-
import yaml, sys
import os.path

class Deck():

    def __init__(self, inputhpath):
        if not os.path.exists(inputhpath):
            print("File " + inputhpath)
            sys.exit(1)
        else:
            with open(inputhpath,'r') as f:
                ## Container of the tags parsed from the yaml file
                self.doc = yaml.load(f, Loader=yaml.BaseLoader)
        self.create_folder_structure()

    def create_folder_structure(self):
        plot_dir = "./output/"
        check_folder = os.path.isdir(plot_dir)
        if not check_folder:
              os.makedirs(plot_dir)
