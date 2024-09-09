#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta
import time

from github import Github
from github import RateLimitExceededException

import re


class CommitterInfo:
    def __init__(self, date, commit_url):
        self.date = date
        self.commit_url = commit_url


def parse_args():
    parser = argparse.ArgumentParser(description="Count developers on a GitHub repo or in a GitHub Organization "
                                                 "for the last 90 days")
    parser.add_argument('--access_token', required=True, type=str, help="Your Github PAT")
    parser.add_argument('--org_name', type=str, help="Name of the GitHub Organization you want to "
                                                     "check in 'org' format")
    parser.add_argument('--max_repos', default=100, type=str, help="How many repos in the Org do you want "
                                                                   "to inspect? Default=100")
    parser.add_argument('--repo_name', type=str, help="Name of the repo you want to check in 'org/repo' format")
    parser.add_argument('--commit_urls', type=bool,
                        help="Controls outputting commit URLs, defaults to '--no-commit-urls'",
                        default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument('--ghe_hostname', type=str, help="If you use GHE, this is the hostname part of the URL")
    parser.add_argument('--count-by', default="username", choices=["username", "name", "email"],
                        help="How to count contributors. Either by GitHub username, display name or email address of "
                             "the author. Default is count by GitHub username.")

    args = parser.parse_args()

    if args.ghe_hostname is None:
        args.ghe_hostname = 'api.github.com'

    if args.access_token is None:
        print('You must specify --access_token')
        parser.print_usage()
        parser.print_help()
        quit()

    if args.repo_name is not None and args.org_name is not None:
        print('You can either inspect a repository OR The Repositories in 1 Organization, not both')
        parser.print_usage()
        parser.print_help()
        quit()

    if args.repo_name is None and args.org_name is None:
        print('You must specify --repo_name or --org_name')
        parser.print_usage()
        parser.print_help()
        quit()

    if args.max_repos is None:
        args.max_repos = 100

    return args


def rate_limited_retry():
    #  Reference https://github.com/clockfort/GitHub-Backup/pull/44/files
    #  Because reties
    def decorator(func):
        def ret(*args, **kwargs):
            for _ in range(3):
                try:
                    return func(*args, **kwargs)
                except RateLimitExceededException:
                    limits = g.get_rate_limit()
                    print(f"Rate limit exceeded")
                    print("Search:", limits.search, "Core:", limits.core, "GraphQl:", limits.graphql)

                    if limits.search.remaining == 0:
                        limited = limits.search
                    elif limits.graphql.remaining == 0:
                        limited = limits.graphql
                    else:
                        limited = limits.core
                    reset = limited.reset.replace(tzinfo=timezone.utc)
                    now = datetime.now(timezone.utc)
                    seconds = (reset - now).total_seconds() + 30
                    print(f"Reset is in {seconds} seconds.")
                    if seconds > 0.0:
                        print(f"Waiting for {seconds} seconds...")
                        time.sleep(seconds)
                        print("Done waiting - resume!")
            raise Exception("Failed too many times")

        return ret

    return decorator


@rate_limited_retry()
def repo_details(repo_name, count_by):
    global g
    repo_authors = {}
    earliest_commit = None
    repo = g.get_repo(repo_name)
    for branch in repo.get_branches():
        for commit in repo.get_commits(sha=branch.name):
            commit_date = datetime.strptime(commit.raw_data['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            if earliest_commit is None:
                earliest_commit = commit_date - timedelta(days_back)

            if commit_date > earliest_commit:
                if 'author' in commit.raw_data['commit']:
                    author_email = commit.raw_data['commit']['author']['email']
                    author_name = commit.raw_data['commit']['author']['name']
                else:
                    author_email = commit.raw_data['commit']['committer']['email']
                    author_name = commit.raw_data['commit']['committer']['name']

                if 'author' in commit.raw_data and commit.raw_data['author'] and 'login' in commit.raw_data['author']:
                    author_login = commit.raw_data['author']['login']
                else:
                    author_login = None

                # skip automation users that look like root@1976d98b6ec0
                if re.match(r"^root@\w+$", author_email):
                    continue

                if count_by == 'username' and author_login:
                    author = author_login
                elif count_by == 'email':
                    author = author_email
                elif count_by == 'name':
                    author = author_name
                else:
                    author = author_email

                if author not in repo_authors:
                    repo_authors[author] = CommitterInfo(commit.raw_data['commit']['committer']['date'],
                                                         commit.raw_data['html_url'])
            else:
                break

    print(
        f'In the repository \'{repo_name}\', there are {len(repo_authors)}'
        f' contributor(s) over 90 days with the earliest commit'
        f' on {earliest_commit}.')
    print('Here is the list of Github contributors:')
    for author, committer_info in repo_authors.items():
        print(author + ': ' + committer_info.date, end='')
        if args.commit_urls:
            print(',', committer_info.commit_url, end='')
        print()
    print('\n')
    return repo_authors


@rate_limited_retry()
def org_iterator(org_name, count_by):
    global authors
    global g
    org = g.get_organization(org_name)
    repos = org.get_repos(sort="updated")
    i = 0
    max_repos = int(args.max_repos)
    for repo in repos:
        if i < max_repos:
            i += 1
            authors.update(repo_details(repo.full_name, count_by))
        else:
            break
    print("In total you have " + str(len(authors)) + " contributors over the last 90 day in " + str(i)
          + " repositories.")


args = parse_args()
days_back = 90
authors = {}
g = Github(login_or_token=args.access_token)
count_by = args.count_by

if args.repo_name is not None:
    authors.update(repo_details(args.repo_name, count_by))
elif args.org_name is not None:
    org_iterator(args.org_name, count_by)
    for author, date in authors.items():
        print(author + ": " + date)
else:
    print("I didn't have a repository or a GitHub Organization to inspect. Please run again with -h to see the help.")
