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
    return arg_parser


def main():
    # parse command line arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    # process venues
    repo_list = RepoList(args.input_file, args.output_dir, args.delimiter)
    repo_list.read_from_csv()
    repo_list.retrieve_features(args.retrieve_features, args.retrieve_discussions)
    repo_list.write_to_csv()


if __name__ == '__main__':
    main()
