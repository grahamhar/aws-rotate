import pytest
from unittest.mock import patch, Mock
from aws_rotate import delete_old_access_key
from botocore.exceptions import ClientError

@patch('boto3.client')
def test_returns_new_keys(mock_iam):
    """
    None should be returned if the delete is successful
    """
    mock_iam.return_value.create_access_keys.return_value = None
    assert delete_old_access_key('AFAKEKEY') == True

@patch('boto3.client')
def test_an_exception_is_raised_key_not_found(mock_iam):
    """
    It should raise an exception if the AWS client raises an exception
    """
    mock_iam.side_effect = ClientError(error_response={'Error': {'Code': 'NoSuchEntity'}}, operation_name='DeleteAccessKey')
    with pytest.raises(ClientError):
        delete_old_access_key('AFAKEKEY')
