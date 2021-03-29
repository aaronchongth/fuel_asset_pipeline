#!/usr/bin/env python3

import os
import zipfile
import subprocess
from utils import check_dirs
from progressbar import progressbar


def generate_thumbnails(args):
    assert args.subparser_name == 'generate_thumbnails'
    if not check_dirs([args.dir, args.output_dir]):
        return

    host_dir = os.path.abspath(args.dir)
    models_dir = os.listdir(host_dir)
    output_dir = os.path.abspath(args.output_dir)
    tmp_zips_dir = os.path.join(output_dir, 'zips')
    os.mkdir(tmp_zips_dir)

    os.environ['GAZEBO_MODEL_PATH'] = os.path.abspath(host_dir)

    success = 0
    has_errors = {}
    for i in progressbar(range(len(models_dir))):
        model_dir = models_dir[i]
        model_dir_path = os.path.join(host_dir, model_dir)
        sdf_path = os.path.join(model_dir_path, 'model.sdf')
        
        # Generate
        process = subprocess.Popen(
            ['gzprop', sdf_path],
            stdout=subprocess.PIPE,
            cwd=tmp_zips_dir)
        output, gzprop_error = process.communicate()

        if gzprop_error is not None:
            has_errors.add(model_dir)
            continue

        # Unzip
        zip_file = os.listdir(tmp_zips_dir)[0]
        zip_path = os.path.join(tmp_zips_dir, zip_file)

        model_name = zip_file[:-4]
        output_path = os.path.join(output_dir, model_name)
        os.mkdir(output_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
        os.remove(zip_path)

        # Rename
        os.rename(
            os.path.join(output_path, 'meta'),
            os.path.join(output_path, 'thumbnails'))

        success += 1

    print('Success: {} out of {} models.'.format(success, len(models_dir)))
    print('Has errors: {}'.format(has_errors))
