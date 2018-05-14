# -*- coding: utf-8 -*-

import os
from bossfight.client.config import Config

class TestConfig:

    def test_config_singleton(self, tmpdir, monkeypatch):
        monkeypatch.setattr(Config, 'path', os.path.join(tmpdir, 'test_config.json'))
        config_instance = Config()
        assert config_instance.__dict__ == Config.get_default()
        config_instance.screen_mode['fullscreen'] = not config_instance.screen_mode['fullscreen']
        assert config_instance.__dict__ != Config.get_default()
        other_config_instance = Config()
        assert config_instance.__dict__ == other_config_instance.__dict__
        other_config_instance.screen_mode['height'] += 100
        assert config_instance.__dict__ == other_config_instance.__dict__
        other_config_instance.revert_to_default()
        assert config_instance.screen_mode['height'] == \
            Config.get_default()['screen_mode']['height']

    def test_config_persistence(self, tmpdir, monkeypatch):
        monkeypatch.setattr(Config, 'path', os.path.join(tmpdir, 'test_config.json'))
        config = Config()
        config.screen_mode['fullscreen'] = not config.screen_mode['fullscreen']
        config.load()
        assert config.screen_mode['fullscreen'] is Config.get_default()['screen_mode']['fullscreen']
        config.screen_mode['fullscreen'] = not config.screen_mode['fullscreen']
        config.save()
        other_config = Config()
        assert other_config.screen_mode['fullscreen'] is config.screen_mode['fullscreen']
        config.revert_to_default()
        assert config.__dict__ == Config.get_default()
        config.load()
        assert config.__dict__ != Config.get_default()
        