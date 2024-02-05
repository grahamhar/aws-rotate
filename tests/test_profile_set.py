import os

from aws_rotate import get_current_aws_profile


def test_with_no_env_var():
    """
    With no environment variable set it should return default
    """
    assert get_current_aws_profile() == 'default'


def test_with_env_var():
    """
    With environment variable set it should return the value of the env var
    """
    os.environ['AWS_PROFILE'] = 'test_profile_for_pytest'
    assert get_current_aws_profile() == 'test_profile_for_pytest'
