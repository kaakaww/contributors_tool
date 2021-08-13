import argparse
import datetime

from github import Github
from git import Repo


def parse_args():
    parser = argparse.ArgumentParser(description="Count developers on a GitHub repo for the last 90 days")
    parser.add_argument('--access_token', type=str, help="Your Github PAT")
    parser.add_argument('--repo_name', type=str, help="Name of the repo you want to check in 'org/repo' format")
    parser.add_argument('--ghe_hostname', type=str, help="If you use GHE, this is the hostname part of the URL")

    args = parser.parse_args()

    if args.ghe_hostname is None:
        args.ghe_hostname = 'api.github.com'

    if args.access_token is None:
        print('You must specify --access_token')
        parser.print_usage()
        parser.print_help()
        quit()

    if args.repo_name is None:
        print('You must specify --repo_name')
        parser.print_usage()
        parser.print_help()
        quit()

    return args


def repo_details(github_obj, repo):
    repo_authors = {}
    earliest_commit = None
    commits = github_obj.get_repo(repo).get_commits()
    for commit in commits.__iter__():
        commit_date = datetime.datetime.strptime(commit.raw_data['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
        if earliest_commit is None:
            earliest_commit = commit_date - datetime.timedelta(days_back)

        if commit_date > earliest_commit:
            if commit.raw_data['commit']['committer']['email'] not in repo_authors:
                repo_authors[commit.raw_data['commit']['committer']['email']] = commit.raw_data['commit']['committer'][
                    'date']
        else:
            break

    print(
        f'In the repository \'{args.repo_name}\', there are {len(repo_authors)}'
        f' contributor(s) over 90 days with the earliest commit'
        f' on {earliest_commit}.')
    print('Here is the list of contributors email addresses:')
    for author, date in repo_authors.items():
        print(author + ': ' + date)
    return repo_authors


def org_iterator(github_obj):
    for repo in github_obj.get_organization().get_repos().__iter__():
        repo_details(github_obj, repo)


args = parse_args()
days_back = 90
authors = {}

g = Github(login_or_token=args.access_token)

#repo_details(g)

org = g.get_organization("StackHawk")
for repo in org.get_repos().__iter__():
    print(repo)
    authors.update(repo_details(g, repo.full_name))




