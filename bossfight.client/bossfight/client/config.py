# -*- coding: utf-8 -*-

import sys
import os
import json
import appdirs

DEFAULT_CONFIG = {
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

    def __init__(self):
        self.__dict__ = Config._singleton_state
        if os.path.exists(Config.path):
            self.load()
            for key in DEFAULT_CONFIG.keys():
                if key not in self.__dict__.keys():
                    self.__dict__[key] = DEFAULT_CONFIG[key]
        else:
            self.set_default()
            self.save()

    def set_default(self):
        '''
        Reverts config data to the default configuration defined in *DEFAULT_CONFIG*.
        '''
        self.__dict__.update(
            # JSON serialization + deserialization for deep copy
            json.loads(json.dumps(DEFAULT_CONFIG))
        ) 

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
