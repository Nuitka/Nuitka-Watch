# nuitka-project: --standalone
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/data=data
import os
import dulwich.repo


def iter_all_commits(repo):
    # iterate on all changes on the Git repository
    for entry in repo.get_walker(head):
        pass


if __name__ == "__main__":
    repo_path = os.path.join(os.path.dirname(__file__), "data", "asyncio.git")

    repo = dulwich.repo.Repo(repo_path)
    head = repo.head()
    repo.close()

    iter_all_commits(repo)
    repo.close()
