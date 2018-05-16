# -*- coding: utf-8 -*-
'''
Module that manages access to the clients configuration. Contains the *Config* class,
which acts as an interface to a singleton config data state in memory and deals with
saving/loading the client config on/from disk.
'''

import sys
import os
import json
import appdirs

_DEFAULT_CONFIG = {
    'screen_mode': {
        'width': 854,
        'height': 480,
        'fullscreen': False
    },
    'local_server_exec': [sys.executable, '-m', 'bossfight.server']
}

CONFIG_PATH = os.path.join(
    appdirs.AppDirs(appname='bossfight', appauthor='ePyCom').user_config_dir,
    'client_config.json'
    )
_SINGLETON_STATE = {}
_CONFIG_INITIALIZED = False

class Config:
    '''
    Singleton class that stores all the client configuration info.
    You can create as many instances as you like, they all will refer to the same config data.
    '''

    def __init__(self):
        global _SINGLETON_STATE, _CONFIG_INITIALIZED, CONFIG_PATH, _DEFAULT_CONFIG
        self.__dict__ = _SINGLETON_STATE
        if not _CONFIG_INITIALIZED:
            if os.path.exists(CONFIG_PATH):
                self.load()
                # If config keys have been added or changed:
                for key in _DEFAULT_CONFIG:
                    if key not in self.__dict__:
                        self.__dict__[key] = Config.get_default()[key]
            else:
                self.revert_to_default()
                self.save()
            _CONFIG_INITIALIZED = True

    def revert_to_default(self):
        '''
        Reverts config data to the default configuration defined in *DEFAULT_CONFIG*.
        '''
        self.__dict__.update(Config.get_default())

    @staticmethod
    def get_default():
        '''
        Returns a deep copy of the default configuration dictionary.
        '''
        global _DEFAULT_CONFIG
        return json.loads(json.dumps(_DEFAULT_CONFIG))

    def save(self):
        '''
        Saves the client configuration data in a json file in the application data directory.

        Windows 7+: `C:\\Users\\{username}\\AppData\\Local\\ePyCom\\bossfight\\client_config.json`
        '''
        global CONFIG_PATH
        if not os.path.exists(os.path.dirname(CONFIG_PATH)):
            os.makedirs(os.path.dirname(CONFIG_PATH))
        with open(CONFIG_PATH, mode='w') as file:
            json.dump(self.__dict__, file, indent=4)

    def load(self):
        '''
        Loads the client configuration data from a json file in the application data directory.

        Windows 7+: `C:\\Users\\{username}\\AppData\\Local\\ePyCom\\bossfight\\client_config.json`
        '''
        global CONFIG_PATH
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, mode='r') as file:
                self.__dict__.update(json.load(file))
