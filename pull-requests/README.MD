### Easy pull-requests from excel sheet

`$ python filter-pr.py --from-user your-account --to-user easylistpolish --push-to upstream`

```
usage: filters-pr.py [-h] [--from-user FROM_USER] [--to-user TO_USER]
                     [--branch BRANCH] [--repo REPO] [--dir DIR]
                     [--images IMAGES] [--push-to PUSH_TO]
                     [--read-from READ_FROM] [--sheet SHEET]

optional arguments:
  -h, --help            show this help message and exit
  --from-user FROM_USER pull-request FROM this user (default: adblock-filters)
  --to-user TO_USER     pull-request TO this user (default: easylistpolish)
  --branch BRANCH       pull-request to this branch (default: master)
  --repo REPO           path to easylist repository (default: ../../easylistpolish)
  --dir DIR             directory and filenames of filters lists (default: /easylistpolish/easylistpolish_)
  --images IMAGES       link to images (default: https://raw.githubusercontent.com/adblock-filters/filter-scripts/master/screens/)
  --push-to PUSH_TO     origin / github / upstream etc. (default: origin)
  --read-from READ_FROM read filters from specified .xlsx (default: filters.xlsx)
  --sheet SHEET         name of sheet with filters list (default: filters)
```


