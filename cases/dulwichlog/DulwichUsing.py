# nuitka-project: --standalone
import os

import dulwich.repo


def find_checkout_root(start_dir):
    candidate = os.path.abspath(start_dir)

    while True:
        if os.path.isdir(os.path.join(candidate, ".git")):
            return candidate

        parent = os.path.dirname(candidate)

        if parent == candidate:
            raise RuntimeError("Could not find a Git checkout root.")

        candidate = parent


def iter_last_commits(repo):
    # Iterate on a small number of commits from HEAD, enough to exercise walking.
    for entry in repo.get_walker(max_entries=3):
        pass


if __name__ == "__main__":
    repo_path = find_checkout_root(os.getcwd())

    repo = dulwich.repo.Repo(repo_path)
    iter_last_commits(repo)
    repo.close()
