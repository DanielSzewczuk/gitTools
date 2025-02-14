#!/usr/bin/env python3
import subprocess
import argparse
from datetime import datetime

def validate_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        return parsed_date.strftime("%a %b %d %H:%M:%S %Y +0000")
    except ValueError:
        raise ValueError("Invalid date format. Required format: DD.MM.YYYY HH:MM:SS")

def validate_author(author_str):
    if "<" not in author_str or ">" not in author_str:
        raise ValueError("Invalid author. Please use: 'Firstname Lastname <email>'")
    return author_str

def change_commit_info(commit_hash, new_author=None, new_date=None):
    env_filter_commands = []
    
    if new_author:
        author_name, author_email = new_author.split(" <", 1)
        author_email = author_email.rstrip(">")
        env_filter_commands.extend([
            f'export GIT_AUTHOR_NAME="{author_name}"',
            f'export GIT_AUTHOR_EMAIL="{author_email}"',
            f'export GIT_COMMITTER_NAME="{author_name}"',
            f'export GIT_COMMITTER_EMAIL="{author_email}"'
        ])
    
    if new_date:
        formatted_date = validate_date(new_date)
        env_filter_commands.extend([
            f'export GIT_AUTHOR_DATE="{formatted_date}"',
            f'export GIT_COMMITTER_DATE="{formatted_date}"'
        ])
    
    env_filter_cmd = f'if [ $GIT_COMMIT = {commit_hash} ]; then {" ; ".join(env_filter_commands)} ; fi'
    
    try:
        subprocess.run(
            ["git", "filter-branch", "-f", "--env-filter", env_filter_cmd],
            check=True
        )
        if args.push:
            subprocess.run(["git", "push", "--force"], check=True)
            print("Changes pushed to the remote repository.")
        print(f"Commit updated! {commit_hash}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Changing commit metadata in Git.')
    parser.add_argument('commit_hash', help='The commit hash to modify.')
    parser.add_argument('--author', help='Firstname Lastname <email>')
    parser.add_argument('--date', help='New date in the format "DD.MM.YYYY HH:MM:SS"')
    parser.add_argument('--push', help='Automatically push changes to the remote repository.')
    args = parser.parse_args()
    
    if not args.author and not args.date:
        parser.error("You must specify at least one option (–author or –date).")
    

    try:
        if args.author:
            args.author = validate_author(args.author)
        change_commit_info(args.commit_hash, args.author, args.date)
    except ValueError as e:
        print(f"Error: {e}")
