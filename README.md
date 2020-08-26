# Clone gists

This script will use [PyGithub](https://github.com/PyGithub/PyGithub)
to retrieve the list of your gists and `git clone`/`git pull` them.

# Usage

1. Create a [Github Personal token](https://github.com/settings/tokens)
2. `export GITHUB_API_TOKEN=...`
3. `pip install pygithub`
4. `python clone_gists.py`
