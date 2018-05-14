# -*- coding: utf-8 -*-

import sys
import os
import json
import appdirs

_DEFAULT_CONFIG = {
    'screen_mode': {
        'width': 800,
        'height': 600,
        'fullscreen': False
    },
    'local_server_exec': [sys.executable, '-m', 'bossfight.server']
}



class Config:
    '''
    Singleton class that stores all the client configuration info.
    (You can create as many instances as you like, the all will refer to the same config data.)
    '''
    path = os.path.join(
        appdirs.AppDirs(appname='bossfight', appauthor='ePyCom').user_config_dir,
        'client_config.json')
    _singleton_state = {}
    _initialized = False

    def __init__(self):
        self.__dict__ = Config._singleton_state
        if not Config._initialized:
            if os.path.exists(Config.path):
                self.load()
                # If config keys have been added or changed:
                for key in _DEFAULT_CONFIG:
                    if key not in self.__dict__:
                        self.__dict__[key] = Config.get_default()[key]
            else:
                self.revert_to_default()
                self.save()
            Config._initialized = True

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
        return json.loads(json.dumps(_DEFAULT_CONFIG))

    def save(self):
        '''
        Saves the client configuration data in a json file in the application data directory.

        Windows 7+: `C:\\Users\\{username}\\AppData\\Local\\ePyCom\\bossfight\\client_config.json`
        '''
        if not os.path.exists(os.path.dirname(Config.path)):
            os.makedirs(os.path.dirname(Config.path))
        with open(Config.path, mode='w') as file:
            json.dump(self.__dict__, file, indent=4)

    def load(self):
        '''
        Loads the client configuration data from a json file in the application data directory.

        Windows 7+: `C:\\Users\\{username}\\AppData\\Local\\ePyCom\\bossfight\\client_config.json`
        '''
        if os.path.exists(Config.path):
            with open(Config.path, mode='r') as file:
                self.__dict__.update(json.load(file))
