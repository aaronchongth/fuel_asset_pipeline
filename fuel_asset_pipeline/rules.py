#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
import difflib
from abc import ABC, abstractmethod

#===============================================================================
def get_sdf_paths_from_dir_config(dir):
    config_path = os.path.join(dir, 'model.config')
    assert os.path.exists(config_path)
    config_tree = None
    try:
        config_tree = ET.parse(config_path)
    except:
        print('Error: {} is not valid XML.'.format(config_path))
        return []

    config_root = config_tree.getroot()
    config_models = config_root.findall('model')
    if len(config_models) != 1:
        print('Error: More than 1 model defined in model.config for {}.'
            .format(dir))
        return []

    sdf_tags = config_models[0].findall('sdf')
    sdf_paths = []
    for tag in sdf_tags:
        sdf_file = tag.text
        sdf_path = os.path.join(dir, sdf_file)
        if not os.path.exists(sdf_path):
            print('Error: missing sdf {}'.format(sdf_path))
            return []
        sdf_paths.append(sdf_path)
    return sdf_paths

#===============================================================================
class Rule(ABC):

    def __init__(self, rule_name):
        super().__init__()
        self.rule_name = rule_name

    def name(self):
        return self.rule_name
        
    @abstractmethod
    def is_valid(self):
        pass

#===============================================================================
class BaseFilesExist(Rule):

    def __init__(self, dir):
        super().__init__('base_files_exist')
        self.dir = dir
        self.success = True

    def is_valid(self):
        config_path = os.path.join(self.dir, 'model.config')
        if not os.path.exists(config_path):
            print('Error: missing model.config in {}'.format(self.dir))
            self.success = False

        recommended_sdf_path = os.path.join(self.dir, 'model.sdf')
        if not os.path.exists(recommended_sdf_path):
            print('Warning: missing recommended model.sdf in {}'
                .format(self.dir))

        sdf_paths = get_sdf_paths_from_dir_config(self.dir)
        if len(sdf_paths) == 0:
            self.success = False

        return self.success


#===============================================================================
class ValidXml(Rule):

    def __init__(self, dir):
        super().__init__('valid_xml')
        self.dir = dir
        self.success = True

    def is_valid(self):
        if not BaseFilesExist(self.dir).is_valid():
            print('Error: ValidXml failed, due to failed BaseFilesExists, {}.'
                .format(self.dir))
            return False

        config_path = os.path.join(self.dir, 'model.config')
        sdf_paths = get_sdf_paths_from_dir_config(self.dir)

        try:
            ET.parse(config_path)
        except:
            print('Error: Failed to parse XML, {}.'.format(config_path))
            self.success = False

        for path in sdf_paths:
            try:
                ET.parse(path)
            except:
                print('Error: Failed to parse XML, {}.'.format(path))
                self.success = False

        return self.success

#===============================================================================
class NamingConvention(Rule):

    def __init__(self, dir):
        super().__init__('naming_convention')
        self.dir = dir
        self.success = True

    def is_valid(self):
        if not ValidXml(self.dir).is_valid():
            print('Error: NamingConvention failed, due to failed ValidXml, {}'
                .format(self.dir))
            return False

        config_path = os.path.join(dir, 'model.config')
        config_tree = None
        try:
            config_tree = ET.parse(config_path)
        except:
            print('Error: {} is not valid XML.'.format(config_path))
            return []

        config_root = config_tree.getroot()
        config_models = config_root.findall('model')
        if len(config_models) != 1:
            print('Error: More than 1 model defined in model.config for {}.'
                .format(dir))
            return []
        
        dir_name = os.path.dirname(self.dir)
        # Check that dir, config, sdf is the same
        # Check that there are no spaces
        # Check that they are UpperCamelCase

