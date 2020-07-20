import argparse
import logging

from github.repo_list import RepoList

logger = logging.getLogger('github-retriever_logger')


def get_argument_parser():
    arg_parser = argparse.ArgumentParser(
        description='Retrieve GitHub repo information not available via API,'
    )
    arg_parser.add_argument(
        '-i', '--input-file',
        required=True,
        help='CSV file with repo names.',
        dest='input_file'
    )
    arg_parser.add_argument(
        '-o', '--output-dir',
        required=True,
        help='Path to output directory',
        dest='output_dir'
    )
    arg_parser.add_argument(
        '-d', '--delimiter',
        required=False,
        default=',',
        help='delimiter for CSV files (default: \',\')',
        dest='delimiter'
    )
    arg_parser.add_argument(
        '-f', '--retrieve-features',
        required=False,
        default=False,
        help='retrieve features from repos (default: False)',
        dest='retrieve_features'
    )
    arg_parser.add_argument(
        '-r', '--retrieve-discussions',
        required=False,
        default=False,
        help='retrieve discussions from repos (default: False)',
        dest='retrieve_discussions'
    )
    arg_parser.add_argument(
        '-p', '--retrieve-discussion-posts',
        required=False,
        default=False,
        help='retrieve discussions threads from list of discussions (default: False)',
        dest='retrieve_discussion_posts'
    )
    arg_parser.add_argument(
        '-b', '--backup-frequency',
        required=False,
        default=100,
        help='number of repos to process before saving the current state (default: 100)',
        dest='backup_frequency'
    )
    return arg_parser


def main():
    # parse command line arguments
    parser = get_argument_parser()
    args = parser.parse_args()
    retrieve_features = args.retrieve_features == "True"
    retrieve_discussions = args.retrieve_discussions == "True"
    retrieve_discussion_posts = args.retrieve_discussion_posts == "True"
    backup_frequency = int(args.backup_frequency)

    # process repos
    repo_list = RepoList(args.input_file, args.output_dir, args.delimiter)
    repo_list.read_from_csv()
    repo_list.retrieve_data(backup_frequency, retrieve_features, retrieve_discussions, retrieve_discussion_posts)
    if retrieve_features:
        repo_list.write_repos_to_csv()
    if retrieve_discussions:
        repo_list.write_discussions_to_csv()
    if retrieve_discussion_posts:
        repo_list.write_discussion_posts_to_csv()


if __name__ == '__main__':
    main()
