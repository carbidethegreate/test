# GitHub API Cleanup Script

This repository includes a script that uses the GitHub REST API to remove
all files from a branch. Running the script will create an empty commit on
`main` so that the branch contains no files.

## Usage

1. Create a GitHub personal access token with the `repo` scope.
2. Set these environment variables:
   - `GITHUB_TOKEN` – your personal access token
   - `GITHUB_OWNER` – repository owner
   - `GITHUB_REPO` – repository name
3. Run the script:
   ```bash
   python remove_files_github_api.py
   ```

The script fetches the current commit on `main`, creates an empty tree and
commit, and then updates the branch reference to point to the new commit.
