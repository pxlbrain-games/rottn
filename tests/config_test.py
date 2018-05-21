# -*- coding: utf-8 -*-

import os
import bossfight.client.config as config
#from bossfight.client.config import config

class Testconfig:

    def test_config_persistence(self, tmpdir, monkeypatch):
        config.CONFIG_PATH = os.path.join(str(tmpdir), 'test_config.json')
        config.revert_to_default()
        config.save()
        assert config.get.__dict__ == config._DEFAULT_CONFIG
        config.get.screen_mode['fullscreen'] = not config.get.screen_mode['fullscreen']
        config.load()
        assert config.get.screen_mode['fullscreen'] is config.get_default()['screen_mode']['fullscreen']
        config.get.screen_mode['fullscreen'] = not config.get.screen_mode['fullscreen']
        config.save()
        assert config.get.screen_mode['fullscreen'] is not config.get_default()['screen_mode']['fullscreen']
        config.revert_to_default()
        assert config.get.__dict__ == config.get_default()
        config.load()
        assert config.__dict__ != config.get_default()
