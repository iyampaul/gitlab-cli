# GitLab-CLI

CLI tool to simplify many common administative tasks using the GitLab API

# Use

```./gitlab-cli -h```

# Contribute

There's a difference between an action (like `--search`) and a modifier (like `-u` or `-i`) arguments, where the `--search` is the action you want to perform and `-u` or `-i` are added to ingest the search queries.  Example:

Search for any user account which contains the term `bob`:
```./gitlab-cli --search -u bob``` 

Search for a number of terms/data from a local file named `users.txt`:
```./gitlab-cli --search -i users.txt```

## Adding Features

- Add the commandline arguments in `gl_proc.py` 
    1. `ingestArgs()` is the flags themselves
    1. `action()` is where to act on the submitted flag(s)
    1. Create a new function in `gl_proc.py` to describe how to act on the flag(s)
- Add new interactions with the GitLab API in `gl_api.py`