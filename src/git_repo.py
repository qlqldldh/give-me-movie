from github import Github

from src.settings import GITHUB_ACCESS_TOKEN, GITHUB_REPO
from src.utils import dict_without_none


class GithubRepo:
    ACCESS_TOKEN = GITHUB_ACCESS_TOKEN
    REPO_NAME = GITHUB_REPO

    def __init__(self):
        self._repo = Github(self.ACCESS_TOKEN).get_repo(self.REPO_NAME)

    def get_issues(self, genre):
        params = {"state": "open", "labels": [genre] if genre else None}
        return self._repo.get_issues(**dict_without_none(params))

    def create_issue(self, item, label: str):
        label = self._repo.get_label(label)
        self._repo.create_issue(
            title=item.title, body=item.markdown_text, labels=[label]
        )
