import logging

logger = logging.getLogger("github-retriever_logger")


class Post(object):
    """ A GitHub Discussion Post. """

    def __init__(self, discussion):
        self.discussion = discussion
        self.author = None
        self.timestamp = None
        self.reactions = None
        self.is_part_of_selected_answer = None
        self.content = None

    def get_column_values(self):
        return [self.discussion.repo.full_name, self.discussion.uri, self.author, self.timestamp, self.reactions,
                self.is_part_of_selected_answer, self.content]

    @classmethod
    def get_column_names(cls):
        return ["repo_name", "discussion", "author", "timestamp", "reactions", "is_part_of_selected_answer", "content"]
