import sqlite3
import os
import shutil
from PIL import Image
from io import BytesIO

START_FOLDER = f'{os.environ["USERPROFILE"]}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Bookmarks'
FIREFOX_FOLDER = f'{os.environ["USERPROFILE"]}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\risvndmx.default-release'

shutil.rmtree(f'{START_FOLDER}', ignore_errors=True)
os.mkdir(f'{START_FOLDER}')

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
