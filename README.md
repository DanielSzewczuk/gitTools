# gitTools
Tools for modifying commit metadata in Git repositories.

## Functionalities

- Changing the commit author (name and email)
- Changing the commit date

## Requirements

- Python 3.x
- Git

## Installation

```bash
git clone https://github.com/DanielSzewczuk/gitTools.git
cd gitTools
chmod +x gitt.py
```
You can also add this script to your shell as an alias by adding the following line to your `.bashrc` or `.zshrc` file.


```bash
alias gitt="/path/to/gitt.py"
```

## Usage
```bash
./gitt.py <commit_hash> [--author "Firstname Lastname <email>"] [--date "DD.MM.YYYY HH:MM:SS"] [--push]
```