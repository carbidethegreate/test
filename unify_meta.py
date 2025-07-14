import os
import re
from bs4 import BeautifulSoup

ROOT_DOMAIN = "https://gabrielsmithattorney.com"
OG_IMAGE_URL = "https://imagedelivery.net/MqlML99ManDWvfuYMb9PmQ/5c7f86eb-156c-4128-a9d9-e5697d957100/public"

# gather all html files
html_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as fh:
        soup = BeautifulSoup(fh, 'html.parser')

    title_tag = soup.title
    title = title_tag.get_text(strip=True) if title_tag else ''
    desc_tag = soup.find('meta', attrs={'name':'description'})
    desc = desc_tag['content'] if desc_tag else ''

    canonical_path = os.path.relpath(path, '.')
    canonical_path = canonical_path.replace(os.sep, '/')
    canonical_url = f"{ROOT_DOMAIN}/{canonical_path}"

    # Remove old meta tags we will replace
    if soup.head is None:
        continue
    for tag in list(soup.head.children):
        if tag.name in ('title','meta','link'):
            if tag.name == 'title':
                tag.decompose()
            elif tag.name == 'link' and tag.get('rel') == ['canonical']:
                tag.decompose()
            elif tag.name == 'meta':
                if tag.get('name') in ['description','robots','author','twitter:card','twitter:title','twitter:description','twitter:image','twitter:site','twitter:creator']:
                    tag.decompose()
                elif tag.get('property') in ['og:locale','og:type','og:site_name','og:title','og:description','og:url','og:image']:
                    tag.decompose()
                elif tag.has_attr('charset') or tag.get('name') in ['viewport'] or tag.get('http-equiv') == 'X-UA-Compatible':
                    tag.decompose()

    # Build new tags
    new_head = BeautifulSoup('', 'html.parser')
    new_head.append(soup.new_tag('meta', charset='UTF-8'))
    new_head.append(soup.new_tag('meta', **{'http-equiv':'X-UA-Compatible', 'content':'IE=edge'}))
    new_head.append(soup.new_tag('meta', attrs={'name':'viewport', 'content':'width=device-width, initial-scale=1'}))
    t = soup.new_tag('title')
    t.string = title
    new_head.append(t)
    new_head.append(soup.new_tag('link', rel='canonical', href=canonical_url))
    if desc:
        new_head.append(soup.new_tag('meta', attrs={'name':'description', 'content':desc}))
    new_head.append(soup.new_tag('meta', attrs={'name':'author', 'content':'Law Office of Gabriel Smith LLC'}))
    new_head.append(soup.new_tag('meta', attrs={'name':'robots', 'content':'index, follow'}))
    new_head.append(soup.new_tag('meta', attrs={'property':'og:locale', 'content':'en_US'}))
    new_head.append(soup.new_tag('meta', attrs={'property':'og:type', 'content':'website'}))
    new_head.append(soup.new_tag('meta', attrs={'property':'og:site_name', 'content':'Gabriel Law Firm'}))
    new_head.append(soup.new_tag('meta', attrs={'property':'og:title', 'content':title}))
    if desc:
        new_head.append(soup.new_tag('meta', attrs={'property':'og:description', 'content':desc}))
    new_head.append(soup.new_tag('meta', attrs={'property':'og:url', 'content':canonical_url}))
    new_head.append(soup.new_tag('meta', attrs={'property':'og:image', 'content':OG_IMAGE_URL}))
    new_head.append(soup.new_tag('meta', attrs={'name':'twitter:card', 'content':'summary_large_image'}))
    new_head.append(soup.new_tag('meta', attrs={'name':'twitter:title', 'content':title}))
    if desc:
        new_head.append(soup.new_tag('meta', attrs={'name':'twitter:description', 'content':desc}))
    new_head.append(soup.new_tag('meta', attrs={'name':'twitter:image', 'content':OG_IMAGE_URL}))

    # Insert new tags at beginning of head
    for tag in reversed(list(new_head.contents)):
        soup.head.insert(0, tag)

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(soup.prettify())
