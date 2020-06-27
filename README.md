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

    python3 github-retriever.py -i <path_to_input_file> -o <path_to_output_dir> -f <True-or-False> -r <True-or-False>

Call without parameters to get information about possible parameters:

    usage: github-retriever.py [-h] -i INPUT_FILE -o OUTPUT_DIR [-d DELIMITER] -f
                               RETRIEVE_FEATURES -r RETRIEVE_DISCUSSIONS
    github-retriever.py: error: the following arguments are required: -i/--input-file, -o/--output-dir, -f/--retrieve-features, -r/--retrieve-discussions
    
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

    python3 github-retriever.py -i input/repos.csv -o output/ -f True -e False

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

    python3 github-retriever.py -i input/repos_filtered.csv -o output/ -f False -e True

The tool logs the retrieval process:

    2020-06-27 11:00:17,692 github-retriever_logger INFO: Reading repos from input/repos_filtered.csv...
    2020-06-27 11:00:17,714 github-retriever_logger INFO: 90 repos have been imported.
    2020-06-27 11:00:19,185 github-retriever_logger INFO: Successfully accessed discussions page 1 of repo: twbs/bootstrap
    2020-06-27 11:00:19,210 github-retriever_logger INFO: 25 discussions found on page: 1
    2020-06-27 11:00:19,896 github-retriever_logger INFO: Successfully accessed discussions page 2 of repo: twbs/bootstrap
    2020-06-27 11:00:19,937 github-retriever_logger INFO: 25 discussions found on page: 2
    2020-06-27 11:00:20,419 github-retriever_logger INFO: Successfully accessed discussions page 3 of repo: twbs/bootstrap
    2020-06-27 11:00:20,430 github-retriever_logger INFO: 1 discussions found on page: 3
    2020-06-27 11:00:20,821 github-retriever_logger INFO: Successfully accessed discussions page 4 of repo: twbs/bootstrap
    2020-06-27 11:00:20,842 github-retriever_logger INFO: No discussions found on page: 4
    ...
    2020-06-27 11:04:20,577 github-retriever_logger INFO: Exporting discussions to output/repos_filtered_discussions.csv...
    2020-06-27 11:04:20,606 github-retriever_logger INFO: 5306 discussion(s) has/have been exported.

And writes the [retrieved data](output/repos_filtered_discussions.csv) to the configured output directory:

| repo_name | discussion |
|------|------|
| twbs/bootstrap | https://github.com/twbs/bootstrap/discussions/31146 |
| twbs/bootstrap | https://github.com/twbs/bootstrap/discussions/30887 |
| twbs/bootstrap | https://github.com/twbs/bootstrap/discussions/31147 |
| twbs/bootstrap | https://github.com/twbs/bootstrap/discussions/31159 |
| twbs/bootstrap | https://github.com/twbs/bootstrap/discussions/31158 |
| ... | ... |
