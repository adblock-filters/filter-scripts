1. [Easy pull-request](../master/pull-requests) - to automate branch-commit-PR with photo/link attachement (for filters from excel sheet)
2. [Filter 'features' extraction](../master/extract-filters) - to transform filter list to easy-readable excel sheet
3. [Issue answers](../master/pull-requests) - list of most common user concerns with answers, categorized

### Filter 'features' extraction

`python extract.py --file easylist_specific_hide.txt`

create excel sheet (*output.xlsx*) with filtername, filter, website and type from specified file

`python extract.py --file filters-to-extract.xlsx --begin 10 --end 20 -sheet filters`

create *output.xlsx* from specified file with only rows 10-20 from sheetname *filters*



### Easy pull-request


`python filter-pr.py --from-user your-account --to-user easylistpolish --push-to upstream`

pull-requests to forked repo from your account

Script is using [hub](https://github.com/github/hub) - git tool with extra features. Install it with:


platform | manager | command to run
---------|---------|---------------
Windows | [Chocolatey](https://chocolatey.org/) | `choco install hub`
Ubuntu | [Snap](https://snapcraft.io) | `snap install hub --classic`


```
# indicate that you prefer HTTPS to SSH git clone URLs
git config --global hub.protocol https

```



`python filter-pr.py  --from-user FROM_USER] [--to-user TO_USER]
                     [--branch BRANCH] [--repo REPO] [--dir DIR]
                     [--images IMAGES] [--push-to PUSH_TO]
                     [--read-from READ_FROM] [--sheet SHEET]`

create *output.xlsx* from specified file with only rows 10-20 from sheetname *filters*


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
# or
git config --global credential.helper store
git push
```
