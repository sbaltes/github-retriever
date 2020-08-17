import unittest

import requests

from github.discussion import Discussion


class DiscussionTest(unittest.TestCase):

    def setUp(self):
        self.session = requests.Session()

    def tearDown(self):
        self.session.close()

    def test_nested_posts(self):
        discussion = Discussion("facebook/create-react-app", "/facebook/create-react-app/discussions/9131")
        discussion.retrieve_discussion_posts(self.session)
        self.assertEqual("<p>Just went through the issues on the v4 project and two of them are locked, one has a PR "
                         "that I think is ready, and the other seems like it would be pretty quick (unless I "
                         "misunderstand it).</p>\n<p>Trying to find where I can pitch in :)</p>",
                         discussion.posts[1].content)


if __name__ == '__main__':
    unittest.main()
