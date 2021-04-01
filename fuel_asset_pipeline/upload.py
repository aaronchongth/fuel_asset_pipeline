#!/usr/bin/env python3

import os
import subprocess
from utils import check_dir


def upload_model(model_dir, token, 
    owner=None,
    url='https://fuel.ignitionrobotics.org'):
    if not check_dir(model_dir):
        return False

    model_dir = os.path.abspath(model_dir)

    env_var = {
        'IGN_CONFIG_PATH': os.environ['IGN_CONFIG_PATH'],
        'LD_LIBRARY_PATH': os.environ['LD_LIBRARY_PATH'],
    }

    command = [
        'ign fuel upload' +
        ' -m {}'.format(model_dir) +
        ' --header "Private-Token: {}"'.format(token) +
        ' --url {}'.format(url)]
    if owner is not None:
        new_command = command[0] + ' --owner {}'.format(owner)
        command = [new_command]

    # TODO(AA): Checks before uploading
    # TODO(AA): Check fuel for existing models, don't upload in that case
    process = subprocess.Popen(
        command,
        env=env_var,
        stdout=subprocess.PIPE,
        shell=True)
    outs, errs = process.communicate()

    if errs is not None:
        return False
    return True


def upload(args):
    assert args.subparser_name == 'upload'
    upload_model(
        args.model_dir, args.token, args.owner, args.url)
