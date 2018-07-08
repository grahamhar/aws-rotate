import os
from aws_rotate import get_aws_credentials_file
from unittest.mock import patch

@patch('aws_rotate.os.path.expanduser')
def test_with_no_credentials_env_var(mock_expand):
    """
    With no environment variable set it should return default
    """
    get_aws_credentials_file()
    mock_expand.assert_called_with('~/.aws/credentials')


def test_with_credentials_env_var():
    """
    With environment variable set it should return the value of the env var
    """
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = 'test_credentials_file_for_pytest'
    assert get_aws_credentials_file() == 'test_credentials_file_for_pytest'
