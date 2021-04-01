#!/usr/bin/env python3

import os
import argparse

from generate_thumbnails import generate_thumbnails
from copy_with_ref import copy_with_ref
from upload_all import upload_all
from check_all import check_all
from upload import upload
from check import check


# Init overall parser
parser = argparse.ArgumentParser(
    prog='fuel_asset_pipeline',
    description="Scripts to help check and prepare assets to be uploaded onto Ignition Fuel"
)
subparsers = parser.add_subparsers(dest='subparser_name')

# Copy with reference call
parser_copy_with_ref = subparsers.add_parser('copy_with_ref')
parser_copy_with_ref.add_argument('--source', '-s', type=str, required=True)
parser_copy_with_ref.add_argument('--dest', '-d', type=str, required=True)
parser_copy_with_ref.add_argument('--ref', '-r', type=str, required=True)
parser_copy_with_ref.add_argument(
    '--folders-only', '-f', action='store_true', required=True)
parser_copy_with_ref.add_argument('--ignore', '-i', type=str, required=True)

# Check a single model
parser_check = subparsers.add_parser('check')
parser_check.add_argument('--model-dir', '-m', type=str, required=True)

# Check all models in directory
parser_check_all = subparsers.add_parser('check_all')
parser_check_all.add_argument('--dir', '-d', type=str, required=True)

# Generate thumbnails
parser_generate_thumbnails = subparsers.add_parser('generate_thumbnails')
parser_generate_thumbnails.add_argument('--dir', '-d', type=str, required=True)
parser_generate_thumbnails.add_argument(
    '--output-dir', '-o', type=str, required=True)

# Upload a single model
parser_upload = subparsers.add_parser('upload')
parser_upload.add_argument('--model-dir', '-m', type=str, required=True)
parser_upload.add_argument('--token', '-t', type=str, required=True)
parser_upload.add_argument('--owner', '-o', type=str)
parser_upload.add_argument('--url', '-u', type=str,
    default='https://fuel.ignitionrobotics.org')

# Upload all models in directory
parser_upload_all = subparsers.add_parser('upload_all')
parser_upload_all.add_argument('--dir', '-d', type=str, required=True)
parser_upload_all.add_argument('--token', '-t', type=str, required=True)
parser_upload_all.add_argument('--owner', '-o', type=str)
parser_upload_all.add_argument('--url', '-u', type=str,
    default='https://fuel.ignitionrobotics.org')

def main():
    args = parser.parse_args()

    if args.subparser_name == 'copy_with_ref':
        copy_with_ref(args)
    elif args.subparser_name == 'check':
        check(args)
    elif args.subparser_name == 'check_all':
        check_all(args)
    elif args.subparser_name == 'generate_thumbnails':
        generate_thumbnails(args)
    elif args.subparser_name == 'upload':
        upload(args)
    elif args.subparser_name == 'upload_all':
        upload_all(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
