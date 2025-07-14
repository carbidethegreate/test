# Gabriel Smith Law Firm Website

Static website for the Law Office of Gabriel Smith LLC located in Opelika, Alabama. The site is structured for deployment on Cloudflare Pages.

## Structure
- **css/style.css** – main stylesheet
- **js/menu.js** – mobile navigation script

- **index.html**, **about.html**, **contact.html** – core pages
- **practice-areas/** – category pages for legal services
- **resources/** – blog and FAQ pages
- **images/** – static image assets

This repository contains placeholder content and structure for numerous practice area pages. Customize each HTML file with the appropriate text and metadata.
All HTML files now live at the project root (e.g., `practice-areas/`) after removing the old `pages/` directory.

To clean a branch using GitHub API, set `GITHUB_TOKEN`, `GITHUB_OWNER`, and `GITHUB_REPO` environment variables and run `python3 remove_files_github_api.py`. The script rewrites the branch history to an empty commit.
