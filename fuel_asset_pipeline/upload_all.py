#!/usr/bin/env python3

import os
from utils import check_dir
from upload import upload_model
from progressbar import progressbar


def upload_all(args):
    assert args.subparser_name == 'upload_all'
    if not check_dir(args.dir):
        return

    host_dir = os.path.abspath(args.dir)
    models_dir = os.listdir(host_dir)

    success = 0
    failed = []
    for i in progressbar(range(len(models_dir))):
        model_dir = models_dir[i]
        model_dir_path = os.path.join(host_dir, model_dir)

        if upload_model(model_dir_path, args.token, args.owner, args.url):
            success += 1
        else:
            failed.append(model_dir)
    
    print('Completed: uploaded {} out of {} models.'
        .format(success, len(models_dir)))
    print('Failed: {}'.format(failed))
