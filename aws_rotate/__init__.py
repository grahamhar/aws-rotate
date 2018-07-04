"""
Make rotating AWS Access Keys easier.
"""
import os
from configparser import ConfigParser
from shutil import copyfile

import boto3


class ConfigException(Exception):
    pass


def get_current_aws_profile():
    return os.getenv('AWS_PROFILE', os.getenv('AWS_DEFAULT_PROFILE', 'default'))


def get_aws_credentials_file():
    return os.path.expanduser(os.getenv('AWS_SHARED_CREDENTIALS_FILE', '~/.aws/credentials'))


def open_aws_credentials(credentials_file):
    """
    Return the AWS credentials file as a config object
    """
    aws_credentials = ConfigParser()
    print('Using {}'.format(credentials_file))
    files_read = aws_credentials.read(credentials_file)
    if credentials_file not in files_read:
        print('Credentials file at {} not read'.format(credentials_file))
        raise ConfigException('Unable to read AWS credentials file')
    return aws_credentials


def write_aws_credentials(aws_credentials, credentials_file):
    """
    Write the AWS credentials config to file as an ini file
    """
    with open(credentials_file, 'w') as aws_credentials_file:
        aws_credentials.write(aws_credentials_file)
        print('Written credentials out to {}'.format(credentials_file))
    return True


def backup_aws_credentials(credentials_file):
    """
    Backup the current AWS credentials file with a .bkp extension
    """
    copyfile(credentials_file, '{}.bkp'.format(credentials_file))
    print('Created backup file {}.bkp'.format(credentials_file))


def get_current_access_key_from_config(aws_credentials, profile):
    """
    Get the current Access key so we know which to delete
    """
    return aws_credentials[profile]['aws_access_key_id']


def create_new_access_key():
    """
    Create a new pair of AWS credentials
    """
    iam_client = boto3.client('iam')
    new_access_keys = iam_client.create_access_key()['AccessKey']
    return {'AccessKeyId': new_access_keys['AccessKeyId'], 'SecretAccessKey': new_access_keys['SecretAccessKey']}


def delete_old_access_key(key_to_delete):
    """
    Delete the old access key
    """
    iam_client = boto3.client('iam')
    iam_client.delete_access_key(AccessKeyId=key_to_delete)
    print('Old access key deleted from IAM')
    return True


def run():
    """
    Execute the rotation of AWS keys
    """
    aws_profile = get_current_aws_profile()
    aws_credentials_file = get_aws_credentials_file()
    backup_aws_credentials(aws_credentials_file)
    aws_credentials = open_aws_credentials(aws_credentials_file)
    current_access_key = get_current_access_key_from_config(aws_credentials, aws_profile)
    new_access_key = create_new_access_key()
    aws_credentials.set(aws_profile, 'aws_access_key_id', new_access_key['AccessKeyId'])
    aws_credentials.set(aws_profile, 'aws_secret_access_key', new_access_key['SecretAccessKey'])
    write_aws_credentials(aws_credentials, aws_credentials_file)
    delete_old_access_key(current_access_key)


if __name__ == '__main__':
    run()
