#!/usr/bin/env python3

import os
import difflib
from check import ModelChecker
from progressbar import progressbar


def check_all(args):
    assert args.subparser_name == 'check_all'
    assert os.path.exists(args.dir)
    assert os.path.isdir(args.dir)

    host_dir = os.path.abspath(args.dir)
    models_dir = os.listdir(host_dir)

    success = 0
    failed = []
    for i in progressbar(range(len(models_dir))):
        model_dir = models_dir[i]
        model_dir_path = os.path.join(host_dir, model_dir)
        checker = ModelChecker(model_dir_path)
        if checker.check():
            success += 1
        else:
            failed.append(model_dir)
    
    print('Success: {} out of {} models.'.format(success, len(models_dir)))
    print('Failed: {}'.format(failed))
