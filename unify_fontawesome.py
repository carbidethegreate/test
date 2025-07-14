import os
from bs4 import BeautifulSoup

FA_HREF = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
FA_INTEGRITY = "sha512-yH+xTq5Vf3L7hIwrKyYVJZZzKzbwQ6VykBLL8GMDJ9ZhDJW60F7uO3cu6UytzszbmWzxubUAN4+Y3qFjqZ4gJw=="

html_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as fh:
        soup = BeautifulSoup(fh, 'html.parser')

    head = soup.head
    if not head:
        continue

    # remove Material Icons
    for link in head.find_all('link', href=lambda h: h and 'fonts.googleapis.com/icon?family=Material+Icons' in h):
        link.decompose()

    # handle Font Awesome
    fa_links = [link for link in head.find_all('link', href=lambda h: h and 'font-awesome' in h)]
    if fa_links:
        # keep first, remove rest
        main = fa_links[0]
        for extra in fa_links[1:]:
            extra.decompose()
        main['href'] = FA_HREF
        main['rel'] = 'stylesheet'
        main['integrity'] = FA_INTEGRITY
        main['crossorigin'] = 'anonymous'
        main['referrerpolicy'] = 'no-referrer'
    else:
        new_link = soup.new_tag('link', rel='stylesheet', href=FA_HREF)
        new_link['integrity'] = FA_INTEGRITY
        new_link['crossorigin'] = 'anonymous'
        new_link['referrerpolicy'] = 'no-referrer'
        style_link = head.find('link', href=lambda h: h and 'style.css' in h)
        if style_link:
            style_link.insert_after(new_link)
        else:
            head.append(new_link)

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(soup.prettify())
