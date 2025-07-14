import os
from bs4 import BeautifulSoup

FOOTER_TEMPLATE = """<footer class=\"footer\">\n   <div class=\"container\">\n    <p><i class=\"fa-solid fa-phone\" aria-hidden=\"true\"></i> <a href=\"tel:+13347501729\">(334) 750-1729</a> or <i class=\"fa-solid fa-envelope\" aria-hidden=\"true\"></i> <a href=\"mailto:Gabrielthecryptolawyer@gmail.com\">Gabrielthecryptolawyer@gmail.com</a></p>\n    <p><i class=\"fa-solid fa-map-marker-alt\" aria-hidden=\"true\"></i> Downtown Opelika, AL</p>\n    <p><a href=\"https://www.facebook.com/GabrielSmithAttorney/\">Facebook</a></p>\n    <p>\u00a9 2025 Law Office of Gabriel Smith. All rights reserved.</p>\n    <p><a href=\"{disclaimer_path}\">Disclaimer</a></p>\n   </div>\n  </footer>"""

html_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

for path in html_files:
    rel = os.path.relpath(path, '.').replace(os.sep, '/')
    if rel == 'contact.html':
        continue
    with open(path, 'r', encoding='utf-8') as fh:
        soup = BeautifulSoup(fh, 'html.parser')
    footer = soup.find('footer')
    if not footer:
        continue
    disclaimer_path = os.path.relpath('disclaimer.html', os.path.dirname(path)).replace(os.sep, '/')
    new_footer = BeautifulSoup(FOOTER_TEMPLATE.format(disclaimer_path=disclaimer_path), 'html.parser')
    footer.replace_with(new_footer)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(soup.prettify())
