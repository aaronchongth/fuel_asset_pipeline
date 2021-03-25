import os
import shutil

def copy_with_ref(args):
    assert args.subparser_name == 'copy_with_ref'
    assert os.path.exists(args.ref)
    assert os.path.isdir(args.ref)
    assert os.path.exists(args.source)
    assert os.path.isdir(args.source)
    assert os.path.exists(args.dest)
    assert os.path.isdir(args.dest)

    ref = os.path.abspath(args.ref)
    source = os.path.abspath(args.source)
    dest = os.path.abspath(args.dest)
    folders_only = args.folders_only

    if folders_only:
        print('Copying folders only')
    else:
        print('Copying everything')
    print('  ref : {}'.format(ref))
    print('  from: {}'.format(source))
    print('  to  : {}'.format(dest))

    ref_dirs = os.listdir(ref)

    # Checking loop
    failed = False
    for dir in ref_dirs:
        ref_dir_path = os.path.join(ref, dir)
        if folders_only and not os.path.isdir(ref_dir_path):
            continue

        source_dir_path = os.path.join(source, dir)
        dest_dir_path = os.path.join(dest, dir)

        if not os.path.exists(source_dir_path) or \
                not os.path.isdir(source_dir_path):
            print('Error: missing in source [{}]'.format(source_dir_path))
            failed = True
            continue

        if os.path.exists(dest_dir_path):
            print('Error: destination [{}] already exists'
                .format(dest_dir_path))
            failed = True
            continue
    if failed:
        print('There were failures during initial checks, no copying was done.')
        return
    print('Initial checks passed, copying...')

    # Copying
    for dir in ref_dirs:
        ref_dir_path = os.path.join(ref, dir)
        source_dir_path = os.path.join(source, dir)
        dest_dir_path = os.path.join(dest, dir)



