# title == bookmarks(title)
# url == bookmarks(fk) = places(id) > places(url)
# icon == bookmarks(id) = [favicons]icons_to_pages(page_id) > [favicons]icons_to_pages(icon_id) > [favicons]icons(id)


import os, shutil

with open('C:\\Users\\C1708002\\Favorites\\bookmarks.html', encoding='utf-8', mode='r') as f:
    data = f.read()
    f.close()

idx_start = 0
idx_end = 0

end = True
path = 'C:\\Users\\C1708002\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\bookmarks\\'

shutil.rmtree(path, ignore_errors=True)
os.mkdir(path)

while end:
    idx_start = data.find('A HREF="', idx_end)
    idx_end = data.find('</A>', idx_start)

    if idx_end == -1 or idx_start == -1:
        end = False
        break

    row = data[idx_start + 8 : idx_end]
    addr_end = row.find('" ADD_DATE')
    addr = row[:addr_end]

    name_start = row.find('">', addr_end)
    name = row[name_start + 2:]
    print(addr, name)
    with open(path + name + '.txt', encoding='utf-8', mode='w') as f:
        f.write('[InternetShortcut]\nURL=' + addr + '\nIconFile=' + 'C:\\Users\\C1708002\\Documents\\zz__other\\ico\\' + name.lower() + '.ico\nIconIndex=0')

    os.rename(path + name + '.txt', path + name.lower() + '.url')        


