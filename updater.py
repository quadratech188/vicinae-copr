from pathlib import Path
from typing import override
import dotenv
import logging
import os
import pygit2
import re
import requests
import time
import urllib.parse

class Forge:
    def latest_version(self) -> str:
        raise NotImplementedError

    @classmethod
    def get(cls, url: str):
        if 'github' in url:
            return Github(url)
        else:
            raise Exception('Unknown forge')

class Github(Forge):
    def __init__(self, url: str):
        parsed = urllib.parse.urlsplit(url)

        (account, repo) = parsed.path[1:].split('/')

        self.account: str = account
        self.repo: str = repo

    @override
    def latest_version(self) -> str:
        url = f'https://api.github.com/repos/{self.account}/{self.repo}/releases/latest'
        response = requests.get(url)
        response.raise_for_status()
        tag = str(response.json()['tag_name']) # pyright: ignore[reportAny]

        match = re.match('v(?P<v>[0-9.]+)$', tag)
        if match is None:
            raise Exception('Unknown tag format')
        return match.group('v')

class Spec:
    def __init__(self, text: str):
        self.lines: list[str] = text.splitlines()

        properties = [
            'Name: ',
            'Version: ',
            'Release: ',
            '%global forgeurl '
        ]

        self.property_indices: dict[str, int] = {}

        for i, line in enumerate(self.lines):
            for property in properties:
                if line.startswith(property):
                    self.property_indices[property] = i

        self.forge: Forge = Forge.get(self.get_property('%global forgeurl '))

    def get_property(self, name: str):
        line = self.lines[self.property_indices[name]]
        return line.removeprefix(name)

    def set_property(self, name: str, value: str):
        self.lines[self.property_indices[name]] = name + value

    @property
    def version(self):
        return self.get_property('Version: ')
    @version.setter
    def version(self, value: str):
        self.set_property('Version: ', value)

    @property
    def name(self):
        return self.get_property('Name: ')

    @property
    def release(self):
        return int(self.get_property('Release: ').removesuffix('%{?dist}'))
    @release.setter
    def release(self, value: int):
        self.set_property('Release: ', str(value) + '%{?dist}')

    def text(self):
        return '\n'.join(self.lines)

def version_cmp(a: str, b: str):
    a_list = list(map(int, a.split('.')))
    b_list = list(map(int, b.split('.')))
    return a_list < b_list

signature = pygit2.Signature('Autoupdater', 'quadratech188@gmail.com', int(time.time()), 0)

logger = logging.getLogger(__name__)

visited_repos: set[Path] = set()

push_queue: set[pygit2.Repository] = set()
webhook_queue: set[str] = set()

def update(dir: Path):
    path_str = pygit2.discover_repository(dir)
    if path_str is None: return

    repo_path = Path(path_str).resolve()
    repo = pygit2.Repository(repo_path)
    repo_config = dotenv.dotenv_values(repo_path / '../.env')

    repo_username = repo_config['GIT_USERNAME']
    repo_password = repo_config['GIT_PASSWORD']
    if repo_username is None or repo_password is None:
        raise Exception('Username / password was not provided')

    if repo_path not in visited_repos:
        visited_repos.add(repo_path)

        if len(repo.remotes) != 1:
            raise Exception('Repository has more than one remote')

        remote = repo.remotes[0]

        logger.info(f'{repo_path}: Fetch {remote.url}')

        credentials = pygit2.UserPass(repo_username, repo_password)
        _ = remote.fetch(callbacks=pygit2.RemoteCallbacks(credentials), prune=pygit2.enums.FetchPrune.PRUNE)

        branch = repo.lookup_branch(repo.head.shorthand)

        logger.info(f'{repo_path}: Reset to {branch.upstream.shorthand}')
        repo.reset(branch.upstream.target, pygit2.enums.ResetMode.HARD)

    for spec_path in dir.glob('*.spec'):
        spec = Spec(spec_path.read_text())

        latest_version = spec.forge.latest_version()

        if spec.version >= latest_version: continue

        spec.version = latest_version
        spec.release = 0

        _ = spec_path.write_text(spec.text())

        repo.index.add(spec_path)
        repo.index.write()

        commit_message = f'auto: Bump {spec_path.name} to version {spec.version}'

        logger.info(f'{repo_path}: Create commit | {commit_message}')
        _ = repo.create_commit(
            repo.head.name,
            signature,
            signature,
            commit_message,
            repo.index.write_tree(),
            [repo.head.target]
        )

        tag_name = f'{spec.name}-{spec.version}-{spec.release}'

        logger.info(f'{repo_path}: Create tag | {tag_name}')
        _ = repo.create_tag(tag_name, repo.head.target, pygit2.enums.ObjectType.COMMIT, signature, '')

        push_queue.add(repo)

        if 'WEBHOOK_URL' in repo_config:
            webhook_queue.add(f'{repo_config['WEBHOOK_URL']}{spec.name}/')

def push():
    for repo in push_queue:
        remote = repo.remotes[0]

        logger.info(f'{repo.path}: Push {remote.url}')

        repo_config = dotenv.dotenv_values(Path(repo.path) / '../.env')

        repo_username = repo_config['GIT_USERNAME']
        repo_password = repo_config['GIT_PASSWORD']
        if repo_username is None or repo_password is None:
            raise Exception('Username / password was not provided')

        credentials = pygit2.UserPass(repo_username, repo_password)
        remote.push([repo.head.name], callbacks=pygit2.RemoteCallbacks(credentials))

def webhooks():
    for url in webhook_queue:
        requests.post(url).raise_for_status()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    update(Path('.'))
    push()
    webhooks()
