from configparser import ConfigParser
from unittest.mock import Mock, mock_open, patch

import pytest

from aws_rotate import (
    ConfigException,
    backup_aws_credentials,
    open_aws_credentials,
    write_aws_credentials,
)


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


def test_the_credentials_file_is_writen():
    """
    The correct credentials are writen to the correct file
    """
    with patch('builtins.open', mock_open()) as mock_file:
        credentials_mock = Mock()
        write_aws_credentials(credentials_mock, '/a/test/file')
        mock_file.assert_called_with('/a/test/file', 'w')
        credentials_mock.write.assert_called_once()


@patch('aws_rotate.copyfile')
def test_file_is_backed_up(mock_copy):
    """
    Test the file is backed up to the default location
    """
    backup_aws_credentials('/test/location')
    mock_copy.assert_called_with('/test/location', '/test/location.bkp')
