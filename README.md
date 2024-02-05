# aws-rotate

![aws-rotate](https://github.com/grahamhar/aws-rotate/actions/workflows/unit-tests.yml/badge.svg?event=push&branch=master) [![Coverage Status](https://coveralls.io/repos/github/grahamhar/aws-rotate/badge.svg?branch=master)](https://coveralls.io/github/grahamhar/aws-rotate?branch=master) [![Downloads](http://pepy.tech/badge/aws-rotate)](http://pepy.tech/project/aws-rotate)


Rotate AWS Access Keys and update local credentials file.

It's good practise to rotate access IDs and keys for AWS IAM users, but a pain to do, this simple script automates the process

## Installation
Create a python virtual environment and activate it

```
pip install aws-rotate
```

## Usage

Make sure you have the relevant AWS_PROFILE environment variable set or the default profile will be used see [aws credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html)

```
aws-rotate-keys
```

## Development

Clone this repo and install the dev packages

```
pip install -e ".[dev]"
```

Install pre-commit hooks to help ensure standards are met, or run `isort --profile=black .` with `black -S` before
committing.

```bash
pre-commit install
```

Run the tests (automated on PR opening)

```
pytest
```

Once you have made changes and the test pass create a pull request

## Contributors

[@cagriy](https://github.com/cagriy)
