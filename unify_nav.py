import os
from bs4 import BeautifulSoup

NAV_TEMPLATE = """
   <div class="navbar container">
    <a class="navbar-brand" href="{home_link}">
     Gabriel Smith Attorney at Law
    </a>
    <button aria-label="Open navigation" class="menu-toggle">
     ☰
    </button>
    <ul class="navbar-menu">
     <li>
      <a {home_class} href="{home_link}">
       <i class="fa-solid fa-house" aria-hidden="true"></i> Home
      </a>
     </li>
     <li>
      <a {practice_class} href="{practice_link}">
       <i class="fa-solid fa-scale-balanced" aria-hidden="true"></i> Practice Areas
      </a>
     </li>
     <li>
      <a {about_class} href="{about_link}">
       <i class="fa-solid fa-user" aria-hidden="true"></i> About
      </a>
     </li>
     <li>
      <a {blog_class} href="{blog_link}">
       <i class="fa-solid fa-newspaper" aria-hidden="true"></i> Blog
      </a>
     </li>
     <li>
      <a {faq_class} href="{faq_link}">
       <i class="fa-solid fa-circle-question" aria-hidden="true"></i> FAQ
      </a>
     </li>
     <li>
      <a class="btn{contact_current}" href="{contact_link}">
       <i class="fa-solid fa-phone" aria-hidden="true"></i> Contact
      </a>
     </li>
    </ul>
   </div>
"""

html_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    with open(path, 'r', encoding='utf-8') as fh:
        soup = BeautifulSoup(fh, 'html.parser')

    header = soup.find('header', class_='header')
    if not header:
        header = soup.find('header')
    if not header:
        continue

    for div in header.find_all('div'):
        classes = div.get('class', [])
        if 'navbar' in classes:
            div.decompose()

    rel = os.path.relpath(path, '.').replace(os.sep, '/')
    base_dir = os.path.dirname(path)

    def rel_to(target):
        return os.path.relpath(target, base_dir).replace(os.sep, '/')

    links = {
        'home_link': rel_to('index.html'),
        'practice_link': rel_to('practice-areas/index.html'),
        'about_link': rel_to('about.html'),
        'blog_link': rel_to('resources/blog.html'),
        'faq_link': rel_to('resources/faq.html'),
        'contact_link': rel_to('contact.html'),
    }

    home_class = 'class="current"' if rel == 'index.html' else ''
    practice_class = 'class="current"' if rel.startswith('practice-areas/') else ''
    about_class = 'class="current"' if rel == 'about.html' else ''
    blog_class = 'class="current"' if rel == 'resources/blog.html' else ''
    faq_class = 'class="current"' if rel == 'resources/faq.html' else ''
    contact_current = ' current' if rel == 'contact.html' else ''

    nav_html = NAV_TEMPLATE.format(home_class=home_class or '',
                                   practice_class=practice_class or '',
                                   about_class=about_class or '',
                                   blog_class=blog_class or '',
                                   faq_class=faq_class or '',
                                   contact_current=contact_current,
                                   **links)

    header.insert(0, BeautifulSoup(nav_html, 'html.parser'))

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(soup.prettify())
