import os
import sys
import requests

OWNER = os.getenv('REPO_OWNER')
REPO = os.getenv('REPO_NAME')
TOKEN = os.getenv('GITHUB_TOKEN')

if not all([OWNER, REPO, TOKEN]):
    sys.exit('REPO_OWNER, REPO_NAME and GITHUB_TOKEN must be set')

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github+json'
}

branches_url = f'https://api.github.com/repos/{OWNER}/{REPO}/branches'
resp = requests.get(branches_url, headers=headers)
if resp.status_code != 200:
    sys.exit(f'Failed to list branches: {resp.status_code} {resp.text}')

branches = [b['name'] for b in resp.json()]
for branch in branches:
    if branch in ('main', 'master'):
        continue
    del_url = f'https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{branch}'
    r = requests.delete(del_url, headers=headers)
    if r.status_code not in (200, 204):
        sys.exit(f'Failed to delete {branch}: {r.status_code} {r.text}')
    print(f'Deleted {branch}')
print('CLEANUP OK')
