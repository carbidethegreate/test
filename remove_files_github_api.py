import os
import requests

TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = os.getenv('GITHUB_OWNER')
REPO = os.getenv('GITHUB_REPO')
BRANCH = 'main'

if not all([TOKEN, OWNER, REPO]):
    raise SystemExit('GITHUB_TOKEN, GITHUB_OWNER, and GITHUB_REPO must be set')

session = requests.Session()
session.headers.update({'Authorization': f'token {TOKEN}',
                        'Accept': 'application/vnd.github+json'})

base_url = f'https://api.github.com/repos/{OWNER}/{REPO}'

# Get the current SHA of the branch head
ref_resp = session.get(f'{base_url}/git/ref/heads/{BRANCH}')
ref_resp.raise_for_status()
head_sha = ref_resp.json()['object']['sha']

# Create an empty tree
empty_tree_resp = session.post(f'{base_url}/git/trees', json={'tree': []})
empty_tree_resp.raise_for_status()
empty_tree_sha = empty_tree_resp.json()['sha']

# Create a commit with the empty tree and previous commit as parent
commit_resp = session.post(
    f'{base_url}/git/commits',
    json={
        'message': 'Remove all files from branch',
        'tree': empty_tree_sha,
        'parents': [head_sha]
    }
)
commit_resp.raise_for_status()
new_commit_sha = commit_resp.json()['sha']

# Update the branch reference to the new commit
update_resp = session.patch(
    f'{base_url}/git/refs/heads/{BRANCH}',
    json={'sha': new_commit_sha, 'force': True}
)
update_resp.raise_for_status()
print('Branch cleaned:', new_commit_sha)
