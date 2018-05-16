# -*- coding: utf-8 -*-

import netifaces

_RUNNING_PROCESSES = {}

class GameServiceManager:
    def __init__(self):
        pass

    @staticmethod
    def get_available_ip_addresses():
        '''
        Returns a list of all available IP addresses that the server can be bound to.
        Keep in mind that `127.0.0.1` is only suitable for local servers.
        '''
        addresses = []
        for interface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    addresses.append(link['addr'])
        return addresses