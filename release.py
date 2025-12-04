#!/bin/python

def prepare_files(version: str):
    spec_text = None

    with open('./vicinae.spec', 'r') as f:
        spec_text = f.read()

    url = None

    import re
    url_match = re.search('Source0: (?P<url>.+)\n', spec_text)
    if url_match is None:
        raise Exception('Failed to get URL')
    url = url_match.group('url').replace('%{version}', version)

    prev_version_match = re.search('Version: (?P<version>.+)\n', spec_text)
    if prev_version_match is None:
        raise Exception('Failed to get version')
    prev_version = prev_version_match.group('version')

    spec_text = spec_text.replace(f'Version: {prev_version}', f'Version: {version}')
    spec_text = re.sub('Release: .+\n', 'Release: 0%{?dist}\n', spec_text)

    with open('./vicinae.spec', 'w') as f:
        _ = f.write(spec_text)

    from pathlib import Path
    prev_tarball = Path(f'./v{prev_version}.tar.gz')
    if not prev_tarball.is_file():
        raise Exception('Previous tarball doesn\'t exist?')
    else:
        prev_tarball.unlink()

    import urllib.request
    print('Get', url)
    _ = urllib.request.urlretrieve(url, f'./v{version}.tar.gz')

import sys
import subprocess
version = sys.argv[1]

prev_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True) \
        .stdout.rstrip('\n')
print('Prev hash:', prev_hash)

try:
    prepare_files(version)
    _ = subprocess.run(['git', 'add', '.'])
    _ = subprocess.run(['git', 'commit', '-m', f'chore: Bump to v{version}'])
    _ = subprocess.run(['tito', 'tag', '--accept-auto-changelog'])
    _ = subprocess.run(['git', 'push', '--follow-tags'])
except Exception as e:
    print('Error occured:', e)
    _ = subprocess.run(['git', 'reset', '--hard', prev_hash])
    exit(1)
