1. [Easy pull-request](../master/pull-requests) - to automate branch-commit-PR with photo/link attachement (for filters from excel sheet)
2. [Filter feature extraction](../master/extract-filters) - to transform filter list to more easy-readable format
3. [Issue answers](../master/pull-requests) - list of most common user concerns with answers, categorized

### filters info extraction script
```
usage: extract.py [-h] [--file FILE] [--begin BEGIN] [--end END]
                  [--sheet SHEET]

optional arguments:
  -h, --help     show this help message and exit
  --file FILE    path to file with filters (default: filters-to-extract.xlsx)
  --begin BEGIN  extract rows FROM (default: 0)
  --end END      extract rows TO (default: 0)
  --sheet SHEET  name of sheet with filters (default: 0)
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

For example

`python filter-pr.py --from-user adblock-filters --to-user easylistpolish --push-to upstream`

will 


#### storing git credentials
```
git config credential.helper store
git config --global credential.helper store
git push
```
