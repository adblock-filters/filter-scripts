### filters info extraction script
```
usage: filters-from-excel.py [-h] [--file FILE] [--begin BEGIN] [--end END]
                             [--sheet SHEET]

optional arguments:
  -h, --help     show this help message and exit
  --file FILE    path to file with filters (default: PolishBFFull.xlsx)
  --begin BEGIN  extract rows FROM (default: 0 - first row)
  --end END      extract rows TO (default: 0 - last row)
  --sheet SHEET  name of sheet with filters (default: 0 - first sheet in file)
```

### filters pull-request script
```
usage: filters-pr.py [-h] [--from-user FROM_USER] [--to-user TO_USER]
                     [--branch BRANCH] [--repo REPO] [--dir DIR]
                     [--images IMAGES] [--push-to PUSH_TO]
                     [--read-from READ_FROM] [--sheet SHEET]

optional arguments:
  -h, --help            show this help message and exit
  --from-user FROM_USER pull-request FROM this user (default: adblock-filters)
  --to-user TO_USER     pull-request TO this user (default: adblock-filters)
  --branch BRANCH       pull-request to this branch (default: master)
  --repo REPO           path to easylist repository (default: ../../easylistpolish)
  --dir DIR             directory and filenames of filters lists (default: /easylistpolish/easylistpolish_)
  --images IMAGES       link to images (default: https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/)
  --push-to PUSH_TO     origin / github / upstream etc. (default: origin)
  --read-from READ_FROM read filters from specified .xlsx (default: filters.xlsx)
  --sheet SHEET         name of sheet with filters list (default: filters)
```

#### storing git credentials
```
git config credential.helper store
git config --global credential.helper store
git push
```
