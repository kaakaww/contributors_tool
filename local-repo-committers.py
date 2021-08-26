import os

import git.exc
from git import Repo
import argparse
from datetime import timedelta


def parse_args():
    parser = argparse.ArgumentParser(description="Count developers on a local repo for the last 90 days")
    parser.add_argument('--dir', default="./", type=str, help="Path to the repository directory")
    args = parser.parse_args()
    return args


def read_repo_committers(repo_obj):
    """
    Looking for email addresses of committers and dates of commit.
    :return: nothing
    """
    repo_authors = {}
    earliest_commit = None
    try:
        for commit in repo_obj.iter_commits():
            if earliest_commit is None:
                earliest_commit = commit.committed_datetime - timedelta(days_back)

            if commit.committed_datetime > earliest_commit:
                if commit.committer.email not in repo_authors:
                    repo_authors[commit.committer.email] = commit.committed_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                break

        print(
            f'In the repository \'{repo_obj.working_dir}\', there are {len(repo_authors)}'
            f' contributor(s) over 90 days with the earliest commit'
            f' on {earliest_commit}.')
        print('Here is the list of contributors email addresses:')
        for author, commit_date in repo_authors.items():
            print(author + ': ' + commit_date)
        print('\n')
    except:
        pass


args = parse_args()
days_back = 90
authors = {}
repo_path = os.path.join(args.dir)
try:
    repo = Repo(repo_path)
    read_repo_committers(repo)
except (TypeError, ValueError, git.exc.NoSuchPathError) as err:
    print(f"Something went wrong with your repo at ${repo_path}. Please check the path and try again.")







