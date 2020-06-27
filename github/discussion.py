import logging

logger = logging.getLogger("github-retriever_logger")


class Discussion(object):
    """ A GitHub Discussion. """

    def __init__(self, repo, relative_uri):
        self.repo = repo
        self.uri = "https://github.com" + relative_uri

    def get_column_values(self):
        return [self.repo.full_name, self.uri]

    @classmethod
    def get_column_names(cls):
        return ["repo_name", "discussion"]
