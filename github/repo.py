import logging
import requests
import time

from random import randint
from lxml import html

logger = logging.getLogger("github-retriever_logger")


class Repo(object):
    """ A GitHub repository. """

    def __init__(self, repo_name):
        self.full_name = str(repo_name)
        self.uri = "https://github.com/" + self.full_name

        # features
        self.code = False
        self.issues = False
        self.pull_requests = False
        self.discussions = False
        self.actions = False
        self.projects = False
        self.wiki = False
        self.security = False
        self.insights = False

        # session for data retrieval
        self.session = requests.Session()

        # count number of attempts
        self.attempts = 0

    def retrieve_activated_feature(self):
        # deal with failing requests...
        while self.all_features_false():
            self.retrieve_features()
            if self.attempts > 100:
                logger.error("Reached 100 attempts, giving up.")
                return

    def retrieve_features(self):
        # reduce request frequency to prevent getting blocked
        delay_ms = randint(100, 1000)
        time.sleep(delay_ms / 1000)

        self.attempts = self.attempts + 1
        response = None
        try:
            # retrieve repo start page
            response = self.session.get(self.uri)
        except ConnectionError:
            logger.error("An error occurred while accessing repo: " + str(self))

        if response and response.ok:
            logger.info("Successfully accessed repo: " + str(self))
            tree = html.fromstring(response.content)
            items = tree.xpath('//ul[contains(@class, "UnderlineNav-body")]/li')
            for item in items:
                feature = item.xpath('a/span/text()')
                self.process_feature(feature)
            if self.all_features_false():
                logger.info("Feature retrieval failed, trying again...")
            else:
                logger.info("Successfully retrieved features.")
        else:
            logger.error("An error occurred while accessing repo: " + str(self))

    def process_feature(self, feature):
        # feature can be either be the name of the feature or the name plus a number
        # (e.g., number of open issues)
        feature_name = None
        if len(feature) == 1 or len(feature) == 2:
            feature_name = str(feature[0])
        else:
            logger.error("Unknown feature: " + str(feature))

        if feature_name == "Code":
            self.code = True
        elif feature_name == "Issues":
            self.issues = True
        elif feature_name == "Pull requests":
            self.pull_requests = True
        elif feature_name == "Discussions":
            self.discussions = True
        elif feature_name == "Actions":
            self.actions = True
        elif feature_name == "Projects":
            self.projects = True
        elif feature_name == "Wiki":
            self.wiki = True
        elif feature_name == "Security":
            self.security = True
        elif feature_name == "Insights":
            self.insights = True
        else:
            logger.error("Unknown feature: " + feature_name)

    def all_features_false(self):
        return (self.code or self.issues or self.pull_requests or self.discussions or self.actions or\
                self.projects or self.wiki or self.security or self.insights) is False

    def get_column_values(self):
        return [self.full_name, self.code, self.issues, self.pull_requests, self.discussions, self.actions,
                self.projects, self.wiki, self.security, self.insights]

    @classmethod
    def get_column_names(cls):
        return ["repo_name", "code", "issues", "pull_requests", "discussions", "actions",
                "projects", "wiki", "security", "insights"]

    def __str__(self):
        return str(self.full_name)
