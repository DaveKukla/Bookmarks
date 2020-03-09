import sqlite3
import os
from PIL import Image
from io import BytesIO

START_FOLDER = 'C:\\Users\\C1708002\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Bookmarks'
FIREFOX_FOLDER = 'C:\\Users\\C1708002\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\1ynqo9s2.default-release'

conn_places = sqlite3.connect(f'{FIREFOX_FOLDER}\\places.sqlite')
c_places = conn_places.cursor()
conn_favicons = sqlite3.connect(f'{FIREFOX_FOLDER}\\favicons.sqlite')
c_favicons = conn_favicons.cursor()

c_places.execute('SELECT `fk`, `title` FROM `moz_bookmarks` WHERE `fk` NOT NULL')
for bookmark in c_places.fetchall():
    bm_fk, title = bookmark
    c_places.execute('SELECT `url` FROM `moz_places` WHERE `id` = ?', (bm_fk,))
    url: str = c_places.fetchone()[0]
    short_url: str = '%' + '/'.join(url.strip().split('/')[0:3]) + '%'

    c_favicons.execute('SELECT `id` FROM `moz_pages_w_icons` WHERE `page_url` LIKE ?', (short_url,))
    try:
        page_id: str = c_favicons.fetchone()[0]
    except TypeError:
        page_id: str = 'NULL'

    c_favicons.execute('SELECT `icon_id` FROM `moz_icons_to_pages` WHERE `page_id` = ?', (page_id,))
    try:
        icon_id: str = c_favicons.fetchone()[0]
    except TypeError:
        icon_id: str = 'NULL'

    c_favicons.execute('SELECT `data` FROM `moz_icons` WHERE `id` = ?', (icon_id,))
    title = title.replace('/', '_')
    try:
        icon = c_favicons.fetchone()[0]
        icon = BytesIO(icon)
        image = Image.open(icon)
        image.save(f'{START_FOLDER}\\{title}.ico')
    except TypeError:
        pass

    with open(f'{START_FOLDER}\\{title}.txt', encoding='utf-8', mode='w') as f:
        f.write(f'[InternetShortcut]\nURL={url}\nIconFile={START_FOLDER}\\{title}.ico\nIconIndex=0')
    try:
        os.remove(f'{START_FOLDER}\\{title}.url')
    except FileNotFoundError:
        pass
    os.rename(f'{START_FOLDER}\\{title}.txt', f'{START_FOLDER}\\{title}.url')





























# import os, shutil
#
# with open('C:\\Users\\C1708002\\Favorites\\bookmarks.html', encoding='utf-8', mode='r') as f:
#     data = f.read()
#     f.close()
#
# idx_start = 0
# idx_end = 0
#
# end = True
# path = 'C:\\Users\\C1708002\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\bookmarks\\'
#
# shutil.rmtree(path, ignore_errors=True)
# os.mkdir(path)
#
# while end:
#     idx_start = data.find('A HREF="', idx_end)
#     idx_end = data.find('</A>', idx_start)
#
#     if idx_end == -1 or idx_start == -1:
#         end = False
#         break
#
#     row = data[idx_start + 8 : idx_end]
#     addr_end = row.find('" ADD_DATE')
#     addr = row[:addr_end]
#
#     name_start = row.find('">', addr_end)
#     name = row[name_start + 2:]
#     print(addr, name)
#     with open(path + name + '.txt', encoding='utf-8', mode='w') as f:
#         f.write('[InternetShortcut]\nURL=' + addr + '\nIconFile=' + 'C:\\Users\\C1708002\\Documents\\zz__other\\ico\\' + name.lower() + '.ico\nIconIndex=0')
#
#     os.rename(path + name + '.txt', path + name.lower() + '.url')


