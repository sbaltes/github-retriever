import logging

from lxml.html import HtmlElement

from github.post import Post
from util.requests import delay_next_request
from lxml import html

logger = logging.getLogger("github-retriever_logger")


class Discussion(object):
    """ A GitHub Discussion. """

    def __init__(self, repo, relative_uri):
        self.repo = repo
        self.uri = "https://github.com" + relative_uri

        # discussion metadata
        self.title = None
        self.number = None
        self.state = None
        self.author = None
        self.timestamp = None
        self.emoji = None
        self.category = None
        self.converted_from_issue = None

        # discussion posts
        self.posts = []

    def get_column_values(self):
        return [self.repo.full_name, self.uri, self.title, self.number, self.state, self.author, self.timestamp,
                self.emoji, self.category, self.converted_from_issue]

    @classmethod
    def get_column_names(cls):
        return ["repo_name", "discussion", "title", "number", "state", "author", "timestamp",
                "emoji", "category", "converted_from_issue"]

    def __str__(self):
        return str(self.uri)

    def retrieve_discussion_posts(self, session):
        delay_next_request()
        response = None
        try:
            # retrieve discussion posts
            response = session.get(self.uri)
        except ConnectionError:
            logger.error("An error occurred while accessing discussion posts: " + str(self))

        if response and response.ok:
            logger.info("Successfully accessed discussion posts: " + str(self))
            tree = html.fromstring(response.content)
            self._retrieve_discussion_metadata(tree)
            self._retrieve_discussion_posts(tree)
        else:
            logger.info("No data found in discussion posts: " + str(self))

    def _retrieve_discussion_metadata(self, root):
        logger.info("Retrieving discussion metadata...")

        self.title = _retrieve_element_content(root, "span", "js-issue-title")
        if self.title is None:
            logger.error("Error retrieving title of discussion in: " + str(self))

        self.number = int(_retrieve_element_content(root, "span", "gh-header-number").replace("#", ""))
        if self.number is None:
            logger.error("Error retrieving number of discussion in: " + str(self))

        header_prefix = '//' + _select_elements_with_class("div", "gh-header-meta")

        self.state = _retrieve_element_content(root, "span", "State", "text", header_prefix)
        if self.state is None:
            logger.error("Error retrieving state of discussion in: " + str(self))

        self.author = _retrieve_element_content(root, "a", "author", "@href", header_prefix)
        if self.author is None:
            logger.error("Error retrieving author of discussion in: " + str(self))
        else:
            self.author = self.author.replace("/", "")

        self.emoji = _retrieve_element_content(root, "g-emoji", "f5", "text", header_prefix)
        if self.emoji is None:
            logger.error("Error retrieving emoji of discussion in: " + str(self))

        self.category = _retrieve_element_content(root, "g-emoji", "f5", "parent-text", header_prefix)
        if self.category is None:
            logger.error("Error retrieving category of discussion in: " + str(self))

        self.timestamp = _retrieve_element_content(root, "time-ago", None, "@datetime", header_prefix)
        if self.timestamp is None:
            logger.error("Error retrieving timestamp of discussion in: " + str(self))

        sidebar_prefix = "//" + _select_elements_with_class("div", "discussion-sidebar-item")
        conversion_remark = _retrieve_element_content(root, "svg", "octicon-issue-opened", "parent-text",
                                                      sidebar_prefix)
        self.converted_from_issue = conversion_remark is not None \
                                    and conversion_remark.strip() == "Converted from issue"

    def _retrieve_discussion_posts(self, root):
        logger.info("Retrieving posts...")

        post_divs = root.xpath('.//' + _select_elements_with_class("div", "discussion")
                               + '//' + _select_elements_with_class("div", "timeline-comment"))

        for post_div in post_divs:
            post = Post(self)

            post.author = _retrieve_element_content(post_div, "a", "author", "@href")
            if post.author is None:
                logger.error("Error retrieving author of discussion post in: " + str(self))
            else:
                post.author = post.author.replace("/", "")

            post.timestamp = _retrieve_element_content(post_div, "time-ago", None, "@datetime")
            if post.timestamp is None:
                logger.error("Error retrieving timestamp of discussion post in: " + str(self))

            post.is_part_of_selected_answer =\
                len(post_div.xpath('.//' + _select_elements_with_class("svg", "octicon-check"))) > 0 \
                or len(post_div.xpath('.//ancestor::' + _select_elements_with_class("div", "discussion-comment") + '//'
                                      + _select_elements_with_class("svg", "octicon-check"))) > 0

            content_elements = post_div.xpath('.//' + _select_elements_with_class("td", "comment-body") + '/node()')
            post.content = "\n".join(list(map(lambda elem: str(
                html.tostring(elem, pretty_print=True, encoding="unicode", with_tail=False)).strip(),
                                              filter(lambda elem: type(elem) is HtmlElement, content_elements))))
            if post.content is None:
                logger.error("Error retrieving content of discussion post in: " + str(self))

            emojis = post_div.xpath('./*/*/*/*/' + _select_elements_with_class("form", "js-pick-reaction")
                                    + '//g-emoji/text()')
            counts = post_div.xpath('./*/*/*/*/' + _select_elements_with_class("form", "js-pick-reaction")
                                    + '//span/text()')
            if len(emojis) > 0 and len(counts) > 0:
                post.reactions = [emojis, list(map(lambda count: int(count), counts))]
            else:
                post.reactions = None

            self.posts.append(post)


def _retrieve_element_content(root, element, class_name=None, target="text", prefix=None):
    if prefix:
        xpath_expression = prefix
    else:
        xpath_expression = ""

    if class_name:
        element_selector = _select_elements_with_class(element, class_name)
    else:
        element_selector = element

    if target == "text":
        xpath_expression = xpath_expression + '//' + element_selector + '/text()'
    elif target == "parent-text":
        xpath_expression = xpath_expression + '//' + element_selector + '/../text()'
    elif target.startswith("@"):
        xpath_expression = xpath_expression + '//' + element_selector + '/' + target
    else:
        logger.error("Invalid target: " + target)

    content = list(filter(lambda elem: len(elem) > 0,
                          map(lambda elem: elem.strip(),
                              root.xpath("." + xpath_expression))))

    if len(content) > 0:
        return str(content[0]).strip()
    else:
        return None


def _select_elements_with_class(element, class_name):
    # see https://stackoverflow.com/a/9133579
    return element + '[contains(concat(" ", normalize-space(@class), " "), " ' + class_name + ' ")]'
