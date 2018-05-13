# -*- coding: utf-8 -*-

import os
from bossfight.client.config import Config, DEFAULT_CONFIG

class TestConfig:

    def test_config_singleton(self, tmpdir, monkeypatch):
        monkeypatch.setattr(Config, 'path', os.path.join(tmpdir, 'test_config.json'))
        config_instance = Config()
        assert config_instance.__dict__ == DEFAULT_CONFIG
        config_instance.fullscreen = True
        assert config_instance.__dict__ != DEFAULT_CONFIG
        other_config_instance = Config()
        assert config_instance.__dict__ == other_config_instance.__dict__
        other_config_instance.screen_resolution['width'] = 920
        assert config_instance.__dict__ == other_config_instance.__dict__
        assert config_instance.screen_resolution['height'] == 600

    def test_config_persistence(self, tmpdir, monkeypatch):
        monkeypatch.setattr(Config, 'path', os.path.join(tmpdir, 'test_config.json'))
        config = Config()
        config.fullscreen = True
        config.load()
        assert config.fullscreen is False
        config.fullscreen = True
        config.save()
        other_config = Config()
        assert other_config.fullscreen is True
        config.set_default()
        assert config.__dict__ == DEFAULT_CONFIG
        config.load()
        assert config.__dict__ != DEFAULT_CONFIG
        