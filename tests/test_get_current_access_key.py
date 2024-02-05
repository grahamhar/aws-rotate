import configparser

import pytest

from aws_rotate import get_current_access_key_from_config


def test_key_returned():
    """
    When the profile exists and there is an access key defined it is returned
    """
    config = configparser.ConfigParser()
    config['default'] = {'aws_access_key_id': 'FAKEKEY'}
    assert 'FAKEKEY' == get_current_access_key_from_config(config, 'default')


def test_profile_not_found():
    """
    When the profile doesn't exist an exception is raised
    """
    with pytest.raises(KeyError):
        get_current_access_key_from_config(configparser.ConfigParser(), 'default')


def test_key_not_found():
    """
    When the profile exists but the key doesn't an exception is raised
    """
    config = configparser.ConfigParser()
    config['default'] = {'not_the_key': 'FAKEKEY'}
    with pytest.raises(KeyError):
        get_current_access_key_from_config(config, 'default')
