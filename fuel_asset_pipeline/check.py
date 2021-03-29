#!/usr/bin/env python3

import os
import difflib
import xml.etree.ElementTree as ET
from progressbar import progressbar


class ModelChecker:
    def __init__(self, model_dir_path):
        self.model_dir_path = model_dir_path
        self.model_dir_name = None
        self.config_path = None
        self.config_tree = None
        self.config_root = None
        self.sdf_names = []
        self.sdf_paths = []
        self.model_sdf_roots = []
        self.model_tags = []
        self.uris = []

        # Each one of these rules should only return False if it is necessary
        # for the other tests, e.g. file existence, valid xml, etc
        self.rules = [
            self.model_dir_is_valid,
            self.config_exists,
            self.recommended_sdf_exists,
            self.file_and_folder_names_have_no_spaces,
            self.config_xml_is_valid,
            self.sdfs_exist,
            self.sdfs_xml_is_valid,
            self.config_model_name_is_valid,
            self.sdfs_model_name_is_valid,
            self.sdfs_uri_is_local,
            self.sdfs_uri_exists,
        ]

    def model_dir_is_valid(self):
        if not os.path.exists(self.model_dir_path):
            print('Error: {} does not exist.'.format(self.model_dir_path))
            return False
        
        if not os.path.isdir(self.model_dir_path):
            print('Error: {} is not a directory.'.format(self.model_dir_path))
            return False
        
        self.model_dir_name = os.path.basename(self.model_dir_path)
        return True

    def config_exists(self):
        self.config_path = os.path.join(self.model_dir_path, 'model.config')
        if not os.path.exists(self.config_path):
            print('Error: model.config missing in {}.'
                .format(self.model_dir_path))
            return False
        return True

    def recommended_sdf_exists(self):
        rec_sdf_path = os.path.join(self.model_dir_path, 'model.sdf')
        if not os.path.exists(rec_sdf_path):
            print('Warning: recommended sdf file name model.sdf missing in {}.'
                .format(self.model_dir_path))
        return True

    def file_and_folder_names_have_no_spaces(self):
        def check_recurse(path):
            space_char = ' '
            if space_char in path:
                print('Warning: found white space in name, {}'.format(path))
            
            if not os.path.isdir(path):
                return
            children = os.listdir(path)
            for child in children:
                check_recurse(os.path.join(path, child))
        
        check_recurse(self.model_dir_path)
        return True

    def config_xml_is_valid(self):
        try:
            self.config_tree = ET.parse(self.config_path)
            self.config_root = self.config_tree.getroot()
        except:
            print('Error: XML is not valid, {}'.format(self.config_path))
            return False
        return True

    def sdfs_exist(self):
        self.sdf_names = [
            sdf_tag.text for sdf_tag in self.config_root.findall('sdf')]
        if len(self.sdf_names) == 0:
            print('Error: could not find any sdf tags in model.config, {}'
                .format(self.config_path))
            return False

        success = True
        for sdf_name in self.sdf_names:
            sdf_path = os.path.join(self.model_dir_path, sdf_name)
            if not os.path.exists(sdf_path):
                print('Error: missing sdf file, {}'.format(sdf_path))
                success = False
            else:
                self.sdf_paths.append(sdf_path)
        return success

    def sdfs_xml_is_valid(self):
        success = True
        for sdf_path in self.sdf_paths:
            try:
                sdf_tree = ET.parse(sdf_path)
                self.model_sdf_roots.append(sdf_tree.getroot())
            except:
                print('Error: XML is not valid, {}'.format(sdf_path))
                success = False
        return success

    def config_model_name_is_valid(self):
        names = self.config_root.findall('name')
        if len(names) != 1:
            print('Error: found more than 1 name tag, {}'
                .format(self.config_path))
            return False
        if names[0].text != self.model_dir_name:
            print('Error: config model name is not the same as model directory name'
                .format(self.config_path))
            return False
        return True

    def sdfs_model_name_is_valid(self):
        assert len(self.sdf_paths) == len(self.model_sdf_roots)
        success = True
        for i in range(len(self.sdf_paths)):
            sdf_path = self.sdf_paths[i]
            root = self.model_sdf_roots[i]

            model_tags = root.findall('model')
            if len(model_tags) != 1:
                print('Error: number of model tags is not 1, {}'
                    .format(sdf_path))
                success = False
                continue
            model_tag = model_tags[0]
            self.model_tags.append(model_tag)

            model_name = model_tag.get('name')
            if model_name != self.model_dir_name:
                print(
                    'Error: sdf model name [{}] is not the same as model ' +
                    'directory name [{}], {}'
                    .format(model_name, self.model_dir_name, self.sdf_path))
                success = False
                continue
        return success

    def sdfs_uri_is_local(self):
        success = True
        for m in self.model_tags:
            for uri in m.iter('uri'):
                uri_text = uri.text
                if uri_text[:8] != 'model://':
                    print('Error: sdf uri not getting from model, {}'
                        .format(self.sdf_path))
                    success = False
                    continue
                uri_model_name = uri_text[8:].split('/')[0]
                if uri_model_name != self.model_dir_name:
                    print('Error: uri is linking to a different model, {}'
                        .format(uri_model_name))
                    success = False
                    continue
                self.uris.append(uri_text)
        return success

    def sdfs_uri_exists(self):
        success = True
        for u in self.uris:
            uri_model_name = u[8:].split('/')[0]
            uri_path = u[(9+len(uri_model_name)):]
            uri_abs_path = os.path.join(self.model_dir_path, uri_path)
            if not os.path.exists(uri_abs_path):
                print('Error: uri linked item does not exist, {}'
                    .format(uri_abs_path))
                success = False
        return success

    def check(self):
        for i in range(len(self.rules)):
            rule = self.rules[i]
            if not rule():
                print('Failed: {} out of {} checks passed.'
                    .format(i, len(self.rules)))
                return False
        print('Success [{}]: {} out of {} checks passed.'
            .format(self.model_dir_name, len(self.rules), len(self.rules)))
        return True


def check(args):
    assert args.subparser_name == 'check'
    assert os.path.exists(args.model_dir)
    assert os.path.isdir(args.model_dir)
    model_dir_path = os.path.abspath(args.model_dir)
    model_checker = ModelChecker(model_dir_path)
    model_checker.check()
