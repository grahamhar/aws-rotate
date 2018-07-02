import pytest
from configparser import ConfigParser
from unittest.mock import patch
from aws_rotate import open_aws_credentials, ConfigException

@patch('aws_rotate.ConfigParser', spec=ConfigParser)
def test_is_called_with_default_filename(mock_config):
    """
    Configparser should be called with the correct filename
    """
    mock_config.return_value.read.return_value = ['/test_credentials']
    open_aws_credentials(credentials_file='/test_credentials')
    mock_config().read.assert_called_with('/test_credentials')

@patch('aws_rotate.ConfigParser')
def test_an_exception_is_raised_no_file(mock_config):
    """
    It should raise an exception if the AWS credentials file is not opened
    """
    with pytest.raises(ConfigException):
        open_aws_credentials(credentials_file='/test_credentials')
