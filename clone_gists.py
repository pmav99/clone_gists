#!/usr/bin/env python

import contextlib
import json
import logging
import os
import pathlib
import shlex
import subprocess

from github import Github


logging.basicConfig(level=20)
logger = logging.getLogger()

BASE_DIR = pathlib.Path(__file__).parent.resolve()
REPOS_DIR = BASE_DIR / "repos"


@contextlib.contextmanager
def chdir(target_dir):
    curdir = os.getcwd()
    os.chdir(target_dir)
    try:
        yield
    finally:
        os.chdir(curdir)


def retrieve_upstream_gists():
    client = Github(os.environ["GITHUB_API_TOKEN"])
    return client.get_user().get_gists()


def clone_gist(gist):
    cmd = f"git clone '{gist.git_pull_url}' repos/{gist.id}"
    subprocess.run(shlex.split(cmd), check=True)


def pull_gist(gist):
    with chdir(REPOS_DIR / gist.id):
        cmd = f"git pull"
        subprocess.run(shlex.split(cmd), check=True)


def create_gist_index(upstream_gists):
    gist_data = []
    for gist in upstream_gists:
        gist_data.append({
            "id"            : gist.id,
            "description"   : gist.description,
            "public"        : gist.public,
            "clone"         : gist.git_pull_url,
            "updated"       : gist.updated_at.isoformat(),
            "url"           : gist.url,
            "path"          : (REPOS_DIR / gist.id).as_posix(),
        })
    with open("index.json", "w") as f:
        f.write(json.dumps(gist_data, indent=4) + "\n")


def main():
    upstream_gists = retrieve_upstream_gists()
    create_gist_index(upstream_gists)
    for gist in upstream_gists:
        if (REPOS_DIR / gist.id).exists():
            logger.info("gist already exists. Pulling to get new versions")
            pull_gist(gist)
        else:
            logger.info("gist is a new one. Cloning")
            clone_gist(gist)


if __name__ == "__main__":
    main()
