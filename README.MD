1. [Filter 'features' extraction](../master/extract-filters) - to transform filter list to easy-readable excel sheet
2. [Easy pull-request](../master/pull-requests) - to automate branch-commit-PR with photo/link attachement (for filters from excel sheet)
3. [Issue answers](../master/pull-requests) - list of most common user concerns with answers, categorized

---

## Filter 'features' extraction

to create excel sheet (*output.xlsx*) with filtername, filter, website and type from specified file

`$ python extract.py --file easylist_specific_hide.txt`

to create *output.xlsx* from specified file with only rows 10-20 from sheetname *filters*

`$ python extract.py --file filters-to-extract.xlsx --begin 10 --end 20 -sheet filters`

---

## Easy pull-request

to make pull-requests to forked repo from your account
```
$ python filter-pr.py --from-user your-account --to-user easylistpolish --push-to upstream
```

### Example


* *filters.xlsx* contains 2 filters:
![filters](../master/screens/readme_2.png)

* `$ python filter-pr.py --from-user your-account --to-user your-account --repo "../easylistpolish" `

* creates first branch: `filterpatch-1` with commit `example.com` which modifies the *easylistpolish_specific_hide.txt* by adding an extra line: `example.com##.big-advert` 
* commit and branch are pushed
* pull request is created with message:
```
-[example.com](http://example.com)
![image](https://your-repo-with-screenshots/example.com.png)
```

Then takes another line(s) (branch: `filterpatch-2` with commit `example.com-left-banner` which modifies the *easylistpolish_specific_block.txt* by adding an extra line: `||example.com^*^big-advert` and PR) and so on.

### Requirements - hub

Script is using [hub](https://github.com/github/hub) - git tool with extra features. 
**Install it with:**


platform | manager | command to run
---------|---------|---------------
Windows | [Chocolatey](https://chocolatey.org/) | `choco install hub`
Ubuntu | [Snap](https://snapcraft.io) | `snap install hub --classic`


```
# it might be useful to store your credentials
$ hub create
$ git config credential.helper store
$ git push

# or to indicate that you prefer HTTPS to SSH git clone URLs
$ git config --global hub.protocol https
```
[Login problems](https://github.com/github/hub/issues/899)





