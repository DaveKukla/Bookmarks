import sqlite3
import os
import shutil
from PIL import Image
from io import BytesIO


hash_folder = ''
for folder in os.listdir(f'{os.environ["USERPROFILE"]}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'):
    if '.default-release' in str(folder):
        hash_folder = str(folder)

start_folder = f'{os.environ["USERPROFILE"]}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Bookmarks'
firefox_folder = f'{os.environ["USERPROFILE"]}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\{hash_folder}'

shutil.rmtree(f'{start_folder}', ignore_errors=True)
os.mkdir(f'{start_folder}')

conn_places = sqlite3.connect(f'{firefox_folder}\\places.sqlite')
c_places = conn_places.cursor()
conn_favicons = sqlite3.connect(f'{firefox_folder}\\favicons.sqlite')
c_favicons = conn_favicons.cursor()

c_places.execute('SELECT `fk`, `title` FROM `moz_bookmarks` WHERE `fk` NOT NULL')
for bookmark in c_places.fetchall():
    bm_fk, title = bookmark
    c_places.execute('SELECT `url` FROM `moz_places` WHERE `id` = ?', (bm_fk,))
    url = c_places.fetchone()[0]
    short_url = '%' + '/'.join(url.strip().split('/')[0:3]) + '%'

    c_favicons.execute('SELECT `id` FROM `moz_pages_w_icons` WHERE `page_url` LIKE ?', (short_url,))
    try:
        page_id = c_favicons.fetchone()[0]
    except TypeError:
        page_id = 'NULL'

    c_favicons.execute('SELECT `icon_id` FROM `moz_icons_to_pages` WHERE `page_id` = ?', (page_id,))
    try:
        icon_id = c_favicons.fetchone()[0]
    except TypeError:
        icon_id = 'NULL'

    c_favicons.execute('SELECT `data` FROM `moz_icons` WHERE `id` = ?', (icon_id,))
    title = title.replace('/', '_')
    try:
        icon = c_favicons.fetchone()[0]
        icon = BytesIO(icon)
        image = Image.open(icon)
        image.save(f'{start_folder}\\{title}.ico')
    except TypeError:
        pass

    with open(f'{start_folder}\\{title}.txt', encoding='utf-8', mode='w') as f:
        f.write(f'[InternetShortcut]\nURL={url}\nIconFile={start_folder}\\{title}.ico\nIconIndex=0')
    try:
        os.remove(f'{start_folder}\\{title}.url')
    except FileNotFoundError:
        pass
    os.rename(f'{start_folder}\\{title}.txt', f'{start_folder}\\{title}.url')
