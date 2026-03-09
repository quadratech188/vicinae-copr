import json
from pathlib import Path
import re
import subprocess
import urllib.request
import requests

def get_v():
    response = json.loads(requests.get(
        'https://api.github.com/repos/vicinaehq/vicinae/releases/latest'
    ).text)

    tag: str = response['tag_name']
    match = re.match('v(?P<v>[0-9.]+)$', tag)
    if match is None:
        raise Exception('Unknown tag format')
    v = match.group('v')
    return list(map(int, v.split('.')))


def get_prev_v():
    with open('./prev_v', 'r') as f:
        return list(map(int, f.read().split('.')))

def update_prev_v(v: list[int]):
    with open('./prev_v', 'w') as f:
        _ = f.write('.'.join(map(str, v)))

def update_spec(v: list[int]):
    spec = None

    with open('./vicinae.spec', 'r') as f:
        spec = f.readlines()

    version_match = False
    release_match = False

    for i in range(len(spec)):
        if spec[i].startswith('Version: '):
            spec[i] = f'Version: {'.'.join(map(str, v))}\n'
            version_match = True
        if spec[i].startswith('Release: '):
            spec[i] = 'Release: 0%{?dist}\n'
            release_match = True

    if not (version_match and release_match):
        raise Exception('Failed to update spec')

    with open('./vicinae.spec', 'w') as f:
        _ = f.write(''.join(spec))

def update_tarball(prev_v: list[int], v: list[int]):
    url = f'https://github.com/vicinaehq/vicinae/archive/refs/tags/v{'.'.join(map(str, v))}.tar.gz'

    Path(f'./v{'.'.join(map(str, prev_v))}.tar.gz').unlink()
    _ = urllib.request.urlretrieve(url, f'./v{'.'.join(map(str, v))}.tar.gz')

prev_v = get_prev_v()
v = get_v()

if v <= prev_v: exit()

_ = subprocess.run(['git', 'pull'], check=True)

prev_hash = subprocess.run(
    ['git', 'rev-parse', 'HEAD'],
    capture_output=True, text=True,
    check=True
).stdout.rstrip('\n')

update_spec(v)
update_tarball(prev_v, v)
update_prev_v(v)

try:
    _ = subprocess.run(['git', 'add', '.'], check=True)
    _ = subprocess.run(['git', 'commit', '-m', f'chore: Bump to v{'.'.join(map(str, v))}'], check=True)
    _ = subprocess.run(['tito', 'tag', '--accept-auto-changelog'], check=True)
    _ = subprocess.run(['git', 'push', '--follow-tags'], check=True)
except Exception as e:
    _ = subprocess.run(['git', 'reset', '--hard', prev_hash], check=True)
    raise e
