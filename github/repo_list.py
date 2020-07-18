import codecs
import csv
import logging
import os
import time

from github.discussion import Discussion
from github.post import Post
from github.repo import Repo
from util.exceptions import IllegalArgumentError

logger = logging.getLogger("github-retriever_logger")


class RepoList(object):
    """ List of GitHub repos. """

    def __init__(self, input_file, output_dir, delimiter):
        self.filename = ""
        self.input_file = input_file
        self.output_dir = output_dir
        self.delimiter = delimiter
        self.repos = []

    def read_from_csv(self):
        """
        Read repo names from a CSV file (header required).
        """

        # read CSV as UTF-8 encoded file (see also http://stackoverflow.com/a/844443)
        with codecs.open(self.input_file, encoding='utf8') as fp:
            logger.info("Reading repos from " + self.input_file + "...")

            reader = csv.reader(fp, delimiter=self.delimiter)

            # read header
            header = next(reader, None)
            if not header:
                raise IllegalArgumentError("Missing header in CSV file.")

            repo_name_index = header.index("repo_name")

            # read CSV file
            for row in reader:
                if row:
                    self.repos.append(
                        Repo(row[repo_name_index])
                    )
                else:
                    raise IllegalArgumentError("Wrong CSV format.")

        self.filename = os.path.basename(self.input_file)
        logger.info(str(len(self.repos)) + " repos have been imported.")

    def retrieve_data(self, features, discussions, discussion_posts):
        n = len(self.repos)
        for index, repo in enumerate(self.repos):
            if (index+1) % 50 == 0:
                # wait every 50th request for 5 seconds to prevent getting blocked
                time.sleep(5)
            if (index + 1) % 500 == 0:
                progress = round((index + 1)/n*100, 2)
                logger.info("Reached {0}%, backing up retrieved information...".format(progress))
                if features:
                    self.write_repos_to_csv()
                if discussions:
                    self.write_discussions_to_csv()
                if discussion_posts:
                    self.write_discussion_posts_to_csv()
            if features:
                repo.retrieve_features()
            if discussions:
                repo.retrieve_discussions(discussion_posts)

    def write_repos_to_csv(self):
        """
        Export repos along with retrieved features to a CSV file.
        """

        if len(self.repos) == 0:
            logger.info("Nothing to export.")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        file_path = os.path.join(self.output_dir, self.filename)

        # write paper list to UTF8-encoded CSV file (see also http://stackoverflow.com/a/844443)
        with codecs.open(file_path, 'w', encoding='utf8') as fp:
            logger.info('Exporting repos to ' + file_path + '...')
            writer = csv.writer(fp, delimiter=self.delimiter)

            column_names = Repo.get_column_names()

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            for repo in self.repos:
                try:
                    row = repo.get_column_values()
                    if len(row) == len(column_names):
                        writer.writerow(row)
                        count = count + 1
                    else:
                        raise IllegalArgumentError(
                            str(len(column_names) - len(row)) + " parameter(s) is/are missing for repo "
                            + repo.full_name)
                except UnicodeEncodeError:
                    logger.error("Encoding error while writing data for repo: " + repo.full_name)

            logger.info(str(count) + ' repo(s) has/have been exported.')

    def write_discussions_to_csv(self):
        """
        Export discussions retrieved from repos to a CSV file.
        """

        # TODO: Refactor list operations (see similar code above and below)

        if len(self.repos) == 0:
            logger.info("Nothing to export.")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        file_path = os.path.join(self.output_dir, self.filename.replace(".csv", "_discussions.csv"))

        # write discussions to UTF8-encoded CSV file (see also http://stackoverflow.com/a/844443)
        with codecs.open(file_path, 'w', encoding='utf8') as fp:
            logger.info('Exporting discussions to ' + file_path + '...')
            writer = csv.writer(fp, delimiter=self.delimiter)

            column_names = Discussion.get_column_names()

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            for repo in self.repos:
                rows = repo.get_discussion_rows()
                for row in rows:
                    try:
                        if len(row) == len(column_names):
                            writer.writerow(row)
                            count = count + 1
                        else:
                            raise IllegalArgumentError(
                                str(len(column_names) - len(row)) + " parameter(s) is/are missing for discussions"
                                                                    " in repo " + repo.full_name)
                    except UnicodeEncodeError:
                        logger.error("Encoding error while writing discussions in repo: " + repo.full_name)

            logger.info(str(count) + ' discussion(s) has/have been exported.')

    def write_discussion_posts_to_csv(self):
        """
        Export discussion posts retrieved from repos to a CSV file.
        """

        if len(self.repos) == 0:
            logger.info("Nothing to export.")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        file_path = os.path.join(self.output_dir, self.filename.replace(".csv", "_discussion_posts.csv"))

        # write discussions to UTF8-encoded CSV file (see also http://stackoverflow.com/a/844443)
        with codecs.open(file_path, 'w', encoding='utf8') as fp:
            logger.info('Exporting discussion posts to ' + file_path + '...')
            writer = csv.writer(fp, delimiter=self.delimiter)

            column_names = Post.get_column_names()

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            for repo in self.repos:
                rows = repo.get_post_rows()
                for row in rows:
                    try:
                        if len(row) == len(column_names):
                            writer.writerow(row)
                            count = count + 1
                        else:
                            raise IllegalArgumentError(
                                str(len(column_names) - len(row)) + " parameter(s) is/are missing for discussion post"
                                                                    " in repo " + repo.full_name)
                    except UnicodeEncodeError:
                        logger.error("Encoding error while writing discussion posts in repo: " + repo.full_name)

            logger.info(str(count) + ' discussion post(s) has/have been exported.')
