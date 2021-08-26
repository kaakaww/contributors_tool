# StackHawk Contributors Tool
This tool is designed to help development and security team discover how many active committers are participating
in their software development process.

## Install 
This program was developed and intended for Python 3.8. Choose your Python versioning weapon and install 3.8.

Install virtual environment packages with: `pipenv install`

The scrips can be run with `python3 {script_name} {options}` In the case of a pipenv environment 
`pipenv run python3 {script_name} {options}`

## GitHub Specific
The GitHub version of this tool will help inspect a single repository on GitHub or look at many repositories within
a GitHub organization. This will output the name of the repo and the committers on said repo for the last 90 day 
development period or in the case of and Organization scan, each repo and it's committers as well as a summary of 
committers at the end.

```console
usage: github-repo-committers.py [-h] [--access_token ACCESS_TOKEN] [--org_name ORG_NAME] [--max_repos MAX_REPOS] [--repo_name REPO_NAME] [--ghe_hostname GHE_HOSTNAME]

Count developers on a GitHub repo or in a GitHub Organization for the last 90 days

optional arguments:
  -h, --help            show this help message and exit
  --access_token ACCESS_TOKEN
                        Your Github PAT
  --org_name ORG_NAME   Name of the GitHub Organization you want to check in 'org' format
  --max_repos MAX_REPOS
                        HOw many repos in the Org do you want to inspect? Default=100
  --repo_name REPO_NAME
                        Name of the repo you want to check in 'org/repo' format
  --ghe_hostname GHE_HOSTNAME
                        If you use GHE, this is the hostname part of the URL
```


## Local Repository
The GitHub version of this tool will help inspect a single local repository. 
This will output the path of the repo and the committers on said repo for the last 90 day 
development period.

```console
usage: local-repo-committers.py [-h] [--dir DIR] 

Count developers on a GitHub repo or in a GitHub Organization for the last 90 days

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR
                        Path to the local repository. Defaults to current working directory
  
```