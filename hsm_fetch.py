#!/usr/bin/env python
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import os
import imp

config = None
s3conn = None

BASEDIR = os.path.abspath(os.path.realpath(__file__))
DEF_CONFIG_PATH = os.path.join(BASEDIR, 'config_local.py')


def load_config(path):
    """
    """
    global config
    config = imp.load_module('.', path)
    return config


def fetch_from_s3(remote_path, dest_file):
    """
    Checks status of s3 archive.
    """
    bucket = s3conn.create_bucket(config.ORG_BUCKET)
    key = Key(bucket)
    key.key = remote_path
    key.get_contents_to_filename(dest_file)
    return key


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote-path", required=True, type=str)
    parser.add_argument("--dest", required=True, type=str)
    parser.add_argument('--config', default=DEF_CONFIG_PATH, type=str)
    args = parser.parse_args()

    load_config(args.config)

    s3conn = S3Connection(
        config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_KEY)
    key = fetch_from_s3(args.remote_path, args.dest)
