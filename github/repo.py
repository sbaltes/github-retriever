import logging
import requests

from lxml import html

from github.discussion import Discussion
from util.requests import delay_next_request

logger = logging.getLogger("github-retriever_logger")


class Repo(object):
    """ A GitHub repository. """

    def __init__(self, repo_name):
        self.full_name = str(repo_name)
        self.uri = "https://github.com/" + self.full_name

        # features
        self.has_code = False
        self.has_issues = False
        self.has_pull_requests = False
        self.has_discussions = False
        self.has_actions = False
        self.has_projects = False
        self.has_wiki = False
        self.has_security = False
        self.has_insights = False

        # session for data retrieval
        self.session = requests.Session()

        # count number of attempts
        self.attempts = 0

        # discussion in this repo
        self.discussions = []

    def get_column_values(self):
        return [self.full_name, self.has_code, self.has_issues, self.has_pull_requests, self.has_discussions, self.has_actions,
                self.has_projects, self.has_wiki, self.has_security, self.has_insights]

    @classmethod
    def get_column_names(cls):
        return ["repo_name", "has_code", "has_issues", "has_pull_requests", "has_discussions", "has_actions",
                "has_projects", "has_wiki", "has_security", "has_insights"]

    def get_discussion_rows(self):
        rows = []
        if len(self.discussions) == 0:
            rows.append([self.full_name] + ["n/a"] * 9)
        else:
            for discussion in self.discussions:
                rows.append(discussion.get_column_values())
        return rows

    def get_post_rows(self):
        rows = []
        for discussion in self.discussions:
            for post in discussion.posts:
                rows.append(post.get_column_values())
        return rows

    def __str__(self):
        return str(self.full_name)

    def retrieve_features(self):
        # deal with failing requests...
        while self.all_features_false():
            self._retrieve_features()
            if self.attempts > 100:
                logger.error("Reached 100 attempts, giving up.")
                return

    def _retrieve_features(self):
        delay_next_request()
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
                logger.error("Feature retrieval failed, trying again...")
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
            self.has_code = True
        elif feature_name == "Issues":
            self.has_issues = True
        elif feature_name == "Pull requests":
            self.has_pull_requests = True
        elif feature_name == "Discussions":
            self.has_discussions = True
        elif feature_name == "Actions":
            self.has_actions = True
        elif feature_name == "Projects":
            self.has_projects = True
        elif feature_name == "Wiki":
            self.has_wiki = True
        elif feature_name == "Security":
            self.has_security = True
        elif feature_name == "Insights":
            self.has_insights = True
        else:
            logger.error("Unknown feature: " + feature_name)

    def all_features_false(self):
        return (self.has_code or self.has_issues or self.has_pull_requests or self.has_discussions or self.has_actions or \
                self.has_projects or self.has_wiki or self.has_security or self.has_insights) is False

    def retrieve_discussions(self, discussion_posts):
        delay_next_request()
        response = None
        page = 1
        try:
            # retrieve first discussion page
            response = self._retrieve_discussions_page(page)
        except ConnectionError:
            logger.error("An error occurred while accessing discussions page of repo: " + str(self))

        while response and response.ok:
            if page > 1 and self.reached_last_page(response):
                break
            logger.info("Successfully accessed discussions page " + str(page) + " of repo: " + str(self))
            tree = html.fromstring(response.content)
            links = tree.xpath('//a[contains(@data-hovercard-type, "discussion")]/@href')
            if len(links) > 0:
                logger.info(str(len(links)) + " discussions found on page: " + str(page))
            else:
                break
            for link in links:
                discussion = Discussion(self, link)
                self.discussions.append(discussion)
                if discussion_posts:
                    discussion.retrieve_discussion_posts(self.session)
            page = page + 1
            response = self._retrieve_discussions_page(page)

        logger.info("No discussions found on page: " + str(page))

    def _retrieve_discussions_page(self, page):
        return self.session.get(self.uri + "/discussions?page=" + str(page))

    @staticmethod
    def reached_last_page(response):
        tree = html.fromstring(response.content)
        h3 = tree.xpath('//div[contains(@class, "blankslate")]/h3/text()')
        return h3 and str(h3).strip() == "There aren't any discussions."
