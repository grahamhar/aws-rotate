from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from botocore.exceptions import ClientError

from aws_rotate import create_new_access_key


@patch('boto3.client')
def test_returns_new_keys(mock_iam):
    """
    The new keys should be returned
    """
    mock_iam.return_value.create_access_key.return_value = {
        'AccessKey': {
            'UserName': 'foo.bar',
            'AccessKeyId': 'MYACCESSKEYID',
            'Status': 'Active',
            'SecretAccessKey': 'NOTONEOFTHESE',
            'CreateDate': datetime(2015, 1, 1),
        }
    }
    assert create_new_access_key() == {
        'AccessKeyId': 'MYACCESSKEYID',
        'SecretAccessKey': 'NOTONEOFTHESE',
    }


@patch('boto3.client')
def test_an_exception_is_raised_too_many_keys(mock_iam):
    """
    It should raise an exception if the AWS client raises an exception
    """
    mock_iam.side_effect = ClientError(
        error_response={'Error': {'Code': 'LimitExceededException'}},
        operation_name='CreateAccessKey',
    )
    with pytest.raises(ClientError):
        create_new_access_key()
