#!/usr/bin/env python3

import os
import argparse

from copy_with_ref import copy_with_ref
from check import check
from check_all import check_all


# Init overall parser
parser = argparse.ArgumentParser(
    prog='fuel_asset_pipeline',
    description="Scripts to help check and prepare assets to be uploaded onto Ignition Fuel"
)
subparsers = parser.add_subparsers(dest='subparser_name')

# Copy with reference call
parser_copy_with_ref = subparsers.add_parser('copy_with_ref')
parser_copy_with_ref.add_argument('--source', '-s', type=str)
parser_copy_with_ref.add_argument('--dest', '-d', type=str)
parser_copy_with_ref.add_argument('--ref', '-r', type=str)
parser_copy_with_ref.add_argument('--folders-only', '-f', action='store_true')
parser_copy_with_ref.add_argument('--ignore', '-i', type=str)

# Check a single model
parser_check = subparsers.add_parser('check')
parser_check.add_argument('--model-dir', '-m', type=str)

# Check all models in directory
parser_check_all = subparsers.add_parser('check_all')
parser_check_all.add_argument('--dir', '-d', type=str)


def main():
    args = parser.parse_args()

    if args.subparser_name == 'copy_with_ref':
        copy_with_ref(args)
    else:
        print('all done!')


if __name__ == '__main__':
    main()
