# StackHawk Contributors Tool
This tool is designed to help development and security teams discover how many active committers are participating
in their software development process.

## Is This Accurate?
It can be, but this method will require some clean-up and validation from the owner of the repositories being analyzed. This tool will definitely uncover all contributors in your Git project(s), but there may be some noise in the results that need cleaning up. For example, a single person could commit under different names or email addresses, and then would look like more than one contributor. The _most_ accurate way to count a number of contributors is to use the "GitHub Specific" method below, counting by GitHub usernames (which is the default). In the end, we recommend you review the results and watch out for duplicate contributors (with slightly different names or email addresses) and remove automation committers. 

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
usage: github-repo-committers.py [-h] --access_token ACCESS_TOKEN [--org_name ORG_NAME]
                                 [--max_repos MAX_REPOS] [--repo_name REPO_NAME]
                                 [--ghe_hostname GHE_HOSTNAME] [--count-by {login,name,email}]

Count developers on a GitHub repo or in a GitHub Organization for the last 90 days

optional arguments:
  -h, --help            show this help message and exit
  --access_token ACCESS_TOKEN
                        Your Github PAT
  --org_name ORG_NAME   Name of the GitHub Organization you want to check in 'org' format
  --max_repos MAX_REPOS
                        How many repos in the Org do you want to inspect? Default=100
  --repo_name REPO_NAME
                        Name of the repo you want to check in 'org/repo' format
  --ghe_hostname GHE_HOSTNAME
                        If you use GHE, this is the hostname part of the URL
  --count-by {username,name,email}
                        How to count contributors. Either by GitHub username, display name or email
                        address of the author. Default is count by GitHub username.
```


## Local Repository
The GitHub version of this tool will help inspect a single local repository. 
This will output the path of the repo and the committers on said repo for the last 90 day 
development period.

```console
usage: local-repo-committers.py [-h] [--dir DIR] [--count-by {name,email}]

Count developers on a local repo for the last 90 days

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR             Path to the repository directory
  --count-by {name,email}
                        How to count contributors. Either by display name or email address of the
                        author. Default is count by email.
```

### Command Line
Here's an alternative way to verify these results with a command-line command:
```
git shortlog -sen --all --since=$(date -j -v-90d -f %Y-%m-%d $(git log --pretty="%ad" --date=short -1 --all) +%Y-%m-%d) | cat - | grep -v '\<root@\w\+\>' | wc -l
```
This command has been verified on a Mac. Commands may differ on a Linux environment. Removing the `| wc-l` will allow you to inspect the results. To count by name, remove the `-e` option from the `git shortlog` command.
