def setup():
    """ If any command-line param is set, change default ones """
    if len(sys.argv) == 2:
        BRANCH = str(sys.argv[1]) # to fix
    elif len(sys.argv) == 3:
        REPOPATH = str(sys.argv[2]) # to fix
    elif len(sys.argv) == 4:
        ONLYFIX = str(sys.argv[3]) # to fix

def open_file_to_write():
    """ Create and set the name of the .txt file with pull message in .md format """
    file_write = "pulls\\pull-request-" + str(datetime.datetime.now())[:19].replace(":","") + ".txt"
    openfile = open(file_write, "x")
    return openfile

def openFilterList():
    """ Open particular file from easylistpolish repo """
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
        'WHITEPOPUP': open(REPOPATH + DIRPATH + "whitelist_popup.txt", "a"),
        'GENBLOCK': open(REPOPATH + DIRPATH + "general_block.txt", "a"),
        'GENHIDE': open(REPOPATH + DIRPATH + "general_hide.txt", "a"),
        'GENPOPUP': open(REPOPATH + DIRPATH + "general_block_popup.txt", "a"), 
        }

    return files
    
# WINDOWS   /   LINUX
# slashes in filepaths:
#   //       
#   \
# remotes:
#   origin = repo.remote(name='github')
#   origin = repo.remote(name='origin')