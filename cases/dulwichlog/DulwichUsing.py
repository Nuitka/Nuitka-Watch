# nuitka-project: --standalone
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/data=data
import os

import dulwich.repo


def iter_last_commits(repo):
    # Iterate on a small number of commits from HEAD, enough to exercise walking.
    for entry in repo.get_walker(max_entries=3):
        pass


if __name__ == "__main__":
    repo_path = os.path.join(os.path.dirname(__file__), "data", "asyncio.git")

    repo = dulwich.repo.Repo(repo_path)
    iter_last_commits(repo)
    repo.close()
