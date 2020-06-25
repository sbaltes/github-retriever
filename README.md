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

    python3 github-retriever.py -i <path_to_input_file> -o <path_to_output_dir>

Call without parameters to get information about possible parameters:

    python3 <VERSION>-retriever.py
    
    usage: ...
    
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

    python3 github-retriever.py -i input/repos.csv -o output/

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

| repo | code | issues | pull_requests | discussions | actions | projects | wiki | security | insights |
|------|------|--------|---------------|-------------|---------|----------|------|----------|----------|
| facebook/react | True | True | True | False | True | True | True | True | True |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
