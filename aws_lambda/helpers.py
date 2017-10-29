# -*- coding: utf-8 -*-
import datetime as dt
import os
import re
import zipfile


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def read(path, loader=None, binary_file=False):
    open_mode = 'rb' if binary_file else 'r'
    with open(path, mode=open_mode) as fh:
        if not loader:
            return fh.read()
        return loader(fh.read())


def archive(src, dest, filename):
    output = os.path.join(dest, filename)
    zfh = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)

    for root, _, files in os.walk(src):
        for file in files:
            zfh.write(os.path.join(root, file))
    zfh.close()
    return os.path.join(dest, filename)


def timestamp(fmt='%Y-%m-%d-%H%M%S'):
    now = dt.datetime.utcnow()
    return now.strftime(fmt)


def get_environment_variable_value(val):
    env_val = val
    if val is not None and isinstance(val, str):
        match = re.search(r'^\${(?P<environment_key_name>\w+)*}$', val)
        if match is not None:
            env_val = os.environ.get(match.group('environment_key_name'))
    return env_val
