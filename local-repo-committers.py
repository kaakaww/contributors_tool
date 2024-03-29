#!/usr/bin/env python3
import os

import git.exc
from git import Repo
import argparse
import re
from datetime import timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="Count developers on a local repo for the last 90 days")
    parser.add_argument('--dir', default="./", type=str, help="Path to the repository directory")
    parser.add_argument('--count-by', default="email", choices=["name","email"], help="How to count contributors. "
                                                                                      "Either by display name or "
                                                                                      "email address of the author. "
                                                                                      "Default is count by email.")
    args = parser.parse_args()
    return args


def read_repo_committers(repo_obj, count_by):
    """
    Looking for email addresses of committers and dates of commit.
    :return: nothing
    """
    repo_authors = {}
    earliest_commit = None

    for commit in repo_obj.iter_commits(repo_obj.refs):
        if earliest_commit is None:
            earliest_commit = commit.committed_datetime - timedelta(days_back)

        if commit.committed_datetime > earliest_commit:
            if commit.author.email:
                author_email = commit.author.email
                author_name = commit.author.name
            else:
                author_email = commit.committer.email
                author_name = commit.committer.name

            # skip automation users that look like root@1976d98b6ec0
            if re.match(r"^root@\w+$", author_email):
                continue

            if count_by == 'email':
                author = author_email
            elif count_by == 'name':
                author = author_name

            if author not in repo_authors:
                repo_authors[author] = commit.committed_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            break

    print(
        f'In the repository \'{repo_obj.working_dir}\', there are {len(repo_authors)}'
        f' contributor(s) over 90 days with the earliest commit'
        f' on {earliest_commit}.')
    print('Here is the list of GitHub contributors:')
    for author, commit_date in repo_authors.items():
        print(author + ': ' + commit_date)
    print('\n')


args = parse_args()
days_back = 90
authors = {}
repo_path = os.path.join(args.dir)
try:
    repo = Repo(repo_path)
    read_repo_committers(repo, args.count_by)
except (TypeError, ValueError, git.exc.NoSuchPathError) as err:
    print(f"Something went wrong with your repo at ${repo_path}. Please check the path and try again.")







