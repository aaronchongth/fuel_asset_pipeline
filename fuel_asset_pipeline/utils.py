#!/usr/bin/env python3

import os


def check_path(path):
    if path is None:
        return False
    if not os.path.exists(path):
        print('Error: path {} does not exist.'.format(path))
        return False
    return True


def check_paths(paths):
    success = True
    for p in paths:
        if not check_path(p):
            success = False
    return success


def check_dir(dir):
    if dir is None:
        return False
    if not os.path.exists(dir):
        print('Error: path {} does not exist.'.format(dir))
        return False
    if not os.path.isdir(dir):
        print('Error: path {} is not directory.'.format(dir))
        return False
    return True


def check_dirs(dirs):
    success = True
    for d in dirs:
        if not check_dir(d):
            success = False
    return success
