#!/usr/bin/env python3

import datetime
import sys
import pandas as pd
from git import Repo


REPOPATH = "C:\\Users\\Bartek\\OneDrive\\02_PROJEKTY\\01_Projekty_praca\\AdblockPlus\\easylistpolish"
DIRPATH = "\\easylistpolish\\easylistpolish_"

BRANCH = "update-proposals-2"
FILEREAD = "filters.xlsx"
FILTERSHEET = 'filters'
ONLYFIX = 'no'


# correct folders
# optional: add fix commit/filter option

def setup():
    if len(sys.argv) == 2:
        BRANCH = str(sys.argv[1])
    elif len(sys.argv) == 3:
        ONLYFIX = str(sys.argv[2])
    elif len(sys.argv) == 4:
        REPOPATH = str(sys.argv[3])


def open_file_to_write():
    file_write = "pulls\\pull-request-" + str(datetime.datetime.now())[:19].replace(":","") + ".txt"
    openfile = open(file_write, "x")
    return openfile


def open_filter_lists():
    files = {
        'BLOCK': open(REPOPATH + DIRPATH + "specific_block.txt", "a"),
        'HIDE': open(REPOPATH + DIRPATH + "specific_hide.txt", "a"),
        'POPUP': open(REPOPATH + DIRPATH + "specific_block_popup.txt", "a"),
        '3RD': open(REPOPATH + DIRPATH + "thirdparty.txt", "a"),
        '3RDPOPUP': open(REPOPATH + DIRPATH + "thirdparty_popup.txt", "a"), 
        'AD': open(REPOPATH + DIRPATH + "adservers.txt", "a"),
        'ADPOPUP': open(REPOPATH + DIRPATH + "adservers_popup.txt", "a"), 
        'WHITE': open(REPOPATH + DIRPATH + "whitelist.txt", "a"),
        'WHITEDIM': open(REPOPATH + DIRPATH + "whitelist_dimensions.txt", "a"), 
        'WHITEPOPUP': open(REPOPATH + DIRPATH + "whitelist_popup.txt", "a") 
        }
    return files


def write_filter_to_file(filtertype, filter):
    files = open_filter_lists()
    filter_file = files.get(filtertype)
    filter_file.write(filter  + "\n")
    filter_file.close()


def open_sheet(file_path,sheetname):
    sheet = pd.read_excel(file_path, sheetname)
    sheet = sheet.fillna('')
    return sheet


def domains_to_list(file_path):
    domains_sheet = pd.read_excel(file_path, 'domains')
    domains = []
    for i in domains_sheet.index:
        domains.append(domains_sheet['Domain'][i])
    return domains


def repo_open(repo_path, branch):
    repo = Repo(repo_path)
    assert not repo.bare
    repo.git.checkout(branch)
    return repo


def repo_commit(repo, message):
    repo.git.add(update=True)
    repo.git.commit('-m', message)
    print("> commit: \t\t" + message)


def get_site_from_link(link, domains):
    newlink = link[link.find('://')+3:]    
    if newlink[:3] == 'www': 
        newlink = newlink[4:]

    for domain in domains:
        result = newlink.find(domain)
        if result != -1:
            location = result+len(domain)
            return newlink[:location]


def convert_to_md_link(link, notes, domains):
    site = get_site_from_link(link, domains)
    if notes == "":
        return "[" + link + "]("+ site + ")\n", site
    else:
        return "[" + link + "]("+ site + " - " + notes + ")\n", site + " - " + notes
    

def add_commit_create_pull(sheet, repo):
    domains = domains_to_list(FILEREAD)
    pull = open_file_to_write()
    commit_msg = ""

    for i in range(5): # sheet.index:
        CHECK = sheet['Check'][i]
        PUSH = sheet['Push'][i]
        LINK = sheet['Link'][i]
        
        if (CHECK=='yes' and PUSH=='no'):

            NUMBER = str(sheet['No'][i])[:-2]
            FILTER = sheet['Filter'][i]
            FILTERTYPE = sheet['Type'][i]
            COMMIT = str(sheet['Commit'][i])
            if LINK != "":
                MD_LINK = convert_to_md_link(LINK, sheet['Notes'][i], domains)

            if NUMBER is "":
                if FILTER is "":
                    pull.write(MD_LINK[0])
                else:
                    write_filter_to_file(FILTERTYPE, FILTER)

            else:
                if commit_msg != "":
                    repo_commit(repo, commit_msg)

                write_filter_to_file(FILTERTYPE, FILTER)
                commit_msg = MD_LINK[1]

                pull.write("\n")
                pull.write("__________________________\n")
                pull.write("**# " + NUMBER + "**\n")
                pull.write(COMMIT + "\n")
                pull.write(MD_LINK[0])   

    if commit_msg != "":
        repo_commit(repo, commit_msg)


def main():
    print("__start")

    setup()

    sheet = open_sheet(FILEREAD, FILTERSHEET)
    repo = repo_open(REPOPATH, BRANCH)

    add_commit_create_pull(sheet, repo)

    print("__end")


if __name__== "__main__":
  main()

