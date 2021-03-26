#!/usr/bin/env python3

import os
import progressbar import progressbar
from rules import *


def check_model(model_dir_path):
    assert os.path.exists(model_dir_path)
    assert os.path.isdir(model_dir_path)


def check(args):
    assert args.subparser_name == 'check'
    assert os.path.exists(args.model_dir)
    assert os.path.isdir(args.model_dir)

