# github-retriever

Retrieve information from GitHub repositories that is not available via the GitHub API.

[![DOI](https://zenodo.org/badge/274931763.svg)](https://zenodo.org/badge/latestdoi/274931763)

# Setup

Python 3 is required. The dependencies are specified in `requirements.txt`.
To install those dependencies execute:

    pip3 install -r requirements.txt

**Optional:** Setup virtual environment with [pyenv](https://github.com/pyenv/pyenv) 
and [virtualenv](https://github.com/pyenv/pyenv-virtualenv) before executing the above command:
    
    # list available versions
    pyenv install --list

    pyenv install <VERSION>
    pyenv virtualenv <VERSION> github-retriever_<VERSION>
    pyenv activate github-retriever_<VERSION>
    
    pip3 install --upgrade pip

# Usage

Basic usage:

    python3 github-retriever.py -i <path_to_input_file> -o <path_to_output_dir> -f <True-or-False> -r <True-or-False> -p <True-or-False> -b <Backup-Frequency>

Call `github-retriever.py` without parameters to get a list of available parameters.

# Configuration

As input, the tool expects a CSV file with one column containing GitHub repository names (`repo_name`).
An exemplary input file can be found [here](input/repos.csv):

| repo_name |
|-------|
| facebook/react  |
| microsoft/vscode  |
| airbnb/javascript  |
| ...   |


To retrieve the activated features (issues, pull requests, discussions, etc.) for the configured repos, you just need to run the following command:

    python3 github-retriever.py -i input/repos.csv -o output -f True -e False -p False

The tool logs the retrieval process:

    2020-06-25 18:26:26,985 github-retriever_logger INFO: Reading repos from input/repos.csv...
    2020-06-25 18:26:27,092 github-retriever_logger INFO: 1000 repos have been imported.
    2020-06-25 18:26:28,872 github-retriever_logger INFO: Successfully accessed repo: facebook/react
    2020-06-25 18:26:28,898 github-retriever_logger INFO: Successfully retrieved features.
    2020-06-25 18:26:30,183 github-retriever_logger INFO: Successfully accessed repo: microsoft/vscode
    2020-06-25 18:26:30,200 github-retriever_logger INFO: Successfully retrieved features.
    ...
    2020-06-25 18:49:32,273 github-retriever_logger INFO: Exporting repos to output/repos.csv...
    2020-06-25 18:49:32,285 github-retriever_logger INFO: 1000 repos have been exported.

And writes the [retrieved data](output/repos.csv) to the configured output directory:

| repo_name | has_code | has_issues | has_pull_requests | has_discussions | has_actions | has_projects | has_wiki | has_security | has_insights |
|------|------|--------|---------------|-------------|---------|----------|------|----------|----------|
| facebook/react | True | True | True | False | True | True | True | True | True |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

Further, to retrieve the content of discussions, execute:

    python3 github-retriever.py -i input/repos_filtered.csv -o output -f False -r True -p True -b 1

The tool logs the retrieval process:

    2020-07-20 22:41:46,702 github-retriever_logger INFO: Reading repos from input/repos_filtered.csv...
    2020-07-20 22:41:46,713 github-retriever_logger INFO: 94 repos have been imported.
    2020-07-20 22:41:47,729 github-retriever_logger INFO: Successfully accessed discussions page 1 of repo: BurntSushi/ripgrep
    2020-07-20 22:41:47,755 github-retriever_logger INFO: 25 discussions found on page: 1
    2020-07-20 22:41:49,276 github-retriever_logger INFO: Successfully accessed discussion posts: https://github.com/BurntSushi/ripgrep/discussions/1643
    2020-07-20 22:41:49,288 github-retriever_logger INFO: Retrieving discussion metadata...
    2020-07-20 22:41:49,293 github-retriever_logger ERROR: Error retrieving emoji of discussion in: https://github.com/BurntSushi/ripgrep/discussions/1643
    2020-07-20 22:41:49,295 github-retriever_logger ERROR: Error retrieving category of discussion in: https://github.com/BurntSushi/ripgrep/discussions/1643
    2020-07-20 22:41:49,297 github-retriever_logger INFO: Retrieving posts...
    ...
    2020-07-21 01:35:57,984 github-retriever_logger INFO: Exporting discussions to output/repos_filtered_discussions.csv...
    2020-07-21 01:35:58,048 github-retriever_logger INFO: 6946 discussion(s) has/have been exported.
    2020-07-21 01:35:58,051 github-retriever_logger INFO: Exporting discussion posts to output/repos_filtered_discussion_posts.csv...
    2020-07-21 01:35:58,981 github-retriever_logger INFO: 28483 discussion post(s) has/have been exported.

And writes the [retrieved discussions](output/repos_filtered_discussions_example.csv)...

| repo_name | discussion | title | number | state | author | timestamp | emoji | category | converted_from_issue |
| --- | ---  | ---  | ---  | ---  | ---  | ---  | ---  | ---  | ---  |
| ... | ...  | ...  | ...  | ...  | ...  | ...  | ...  | ...  | ...  |
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9092|Measurement of build time|9092|Unanswered|baeharam|2020-05-30T03:53:02Z|🙏|Help|True|
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9104|Team Feedback/Transparency|9104|Unanswered|eddiemonge|2020-06-03T18:41:10Z|#️⃣|General|False|
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9106|Thanks for the productivity!!|9106|Answered|kentcdodds|2020-06-04T03:44:17Z|💖|Thanks|False|
| ... | ...  | ...  | ...  | ...  | ...  | ...  | ...  | ...  | ...  |

...and [posts](output/repos_filtered_discussions_posts_example.csv) to the configured output directory.

| repo_name | discussion | author | timestamp | reactions | is_part_of_selected_answer | content |
| --- | ---  | ---  | ---  | ---  | ---  | ---  |
| ... | ...  | ...  | ...  | ...  | ...  | ...  |
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9104|eddiemonge|2020-06-03T18:41:10Z|[['👍', '👀'], [5, 1]]|False|&lt;p&gt;From the community perspective,...|
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9104|petetnt|2020-06-05T08:48:51Z|[['👍', '❤️'], [5, 1]]|False|&ltp&gtHi &lta class="user-mention"...|
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9104|mrmckeb|2020-06-05T13:22:56Z|[['❤️'], [2]]|False|&ltp&gtI must say that I do a lot less than...|
facebook/create-react-app|https://github.com/facebook/create-react-app/discussions/9104|eddiemonge|2020-06-12T16:29:23Z|[['👍', '❤️'], [4, 3]]|False|&lth3&gtFeedback&lt/h3&gt...|
| ... | ...  | ...  | ...  | ...  | ...  | ...  |
