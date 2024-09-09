# StackHawk Contributors Tool
This tool is designed to help development and security teams discover how many active committers are participating
in their software development process.

## Is This Accurate?
It can be, but this method will require some clean-up and validation from the owner of the repositories being analyzed. This tool will definitely uncover all contributors in your Git project(s), but there may be some noise in the results. For example, a single person could commit under different names or email addresses, and then would look like more than one contributor. The _most_ accurate way to count a number of contributors is to use the "GitHub Specific" method below, counting by GitHub usernames (which is the default). In the end, we recommend you review the results and watch out for duplicate contributors (with slightly different names or email addresses) and remove automation committers. 

## Running the Scripts with Docker

The easiest way to check your repos for active committers is to use our containerized scripts. All you need to run them is a container runtime such as [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Check a Local Repo

To check a local repo for active committers, run the `ghcr.io/kaakaww/contributors-local` against it. To allow the container to see your local repository, you will need to mount it as a volume to the `/repo` directory within the container using the `--volume` flag.

For example, on Mac or Linux, open a terminal and `cd` to the root of your local repo and run the following command:

```shell
docker run --volume $(pwd):/repo ghcr.io/kaakaww/contributors-local
```

On Windows, open Powershell and `cd` to the root of your local repo and run the following command:

```shell
docker run --volume ${PWD}:/repo ghcr.io/kaakaww/contributors-local
```

### Check a GitHub Repo or Org

To check GitHub directly for active committers, use the `ghcr.io/kaakaww/contributors-github` container. You will need a [GitHub Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), which we will refer to as `ACCESS_TOKEN` in the following examples.

Since this container is looking at your remote GitHub repository, you do not need to check out your repository, `cd` to it, or refer to it in any way.

For example, to check a single GitHub repo, `kaakaww/contributors_tool`, run the following command:

```shell
docker run ghcr.io/kaakaww/contributors-github --access_token ACCESS_TOKEN --repo kaakaww/contributors_tool
```

Or to check **all** the repos in a GitHub organization, `ORG_NAME`, run the following (this could take a while):

```shell
docker run ghcr.io/kaakaww/contributors-github --access_token ACCESS_TOKEN --org_name ORG_NAME
```

Use the `-h` flag to see other options for this script.

```shell
docker run ghcr.io/kaakaww/contributors-github -h
```

## Building and Running the Scripts Locally

### Prerequisites
These scripts were developed for Python 3.8 and higher. Verify your version of Python with:
```shell
python3 --version
```

If you need help installing Python for your platform, a good place to start is the [Python Beginner's Guide Download](https://wiki.python.org/moin/BeginnersGuide/Download) page.

These scripts require `git`. If you do not have `git` installed on your machine, you can find it at the [Git Downloads](https://git-scm.com/downloads) page.

These scripts require [Pipenv](https://pipenv.pypa.io/en/latest/) to install their dependencies. For detailed Pipenv installation guidance, see [Installing Pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv). On most platforms, you can install `pipenv` with `pip3` like so:
```shell
pip3 install --user pipenv
```

### Install

Install the scripts' dependencies into a virtual environment with:
```shell
pipenv install
```

To install the dependencies globally, use:
```shell
pipenv install --system
```

The scripts can be run with:
```shell
pipenv run python3 {script_name} {options}
```

If you installed dependencies globally, you can run the scripts without Pipenv, like so:
```shell
python3 {script_name} {options}
```

### Check a GitHub Repo or Org
The GitHub version of this tool will help inspect a single repository on GitHub or look at many repositories within
a GitHub organization. This will output the name of the repo and the committers on said repo for the last 90 day 
development period or in the case of and Organization scan, each repo and it's committers as well as a summary of 
committers at the end.

```console
usage: github-repo-committers.py [-h] --access_token ACCESS_TOKEN [--org_name ORG_NAME]
                                 [--max_repos MAX_REPOS] [--repo_name REPO_NAME]
                                 [--commit_urls | --no-commit_urls]
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
  --commit_urls, --no-commit_urls
                        Controls outputting commit URLs, defaults to '--no-commit-urls'                        
  --ghe_hostname GHE_HOSTNAME
                        If you use GHE, this is the hostname part of the URL
  --count-by {username,name,email}
                        How to count contributors. Either by GitHub username, display name or email
                        address of the author. Default is count by GitHub username.
```

### Check a Local Repo
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

## `git` CLI Verification
Here's an alternative way to verify these results with the `git` command:

```
git shortlog -sen --all --since=$(date -j -v-90d -f %Y-%m-%d $(git log --pretty="%ad" --date=short -1 --all) +%Y-%m-%d) | cat - | grep -v '\<root@\w\+\>' | wc -l
```
This command has been verified on a Mac. Commands may differ on a Linux environment. Removing the `| wc-l` will allow you to inspect the results. To count by name, remove the `-e` option from the `git shortlog` command.
