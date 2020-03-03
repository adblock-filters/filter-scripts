import argparse
import pandas as pd

OUTPUTFILE = 'output.xlsx'


def parser():
    """ Parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--file",   default='filters-to-extract.xlsx',help="path to file with filters")
    parser.add_argument("--begin",  default=0,                  help="extract rows FROM")
    parser.add_argument("--end",    default=0,                  help="extract rows TO")
    parser.add_argument("--sheet",  default=0,                  help="name of sheet with filters")
    
    return parser.parse_args()


def openSheet(args):
    """ Open and return .xls sheet """
    sheet = pd.read_excel(args.file, sheet_name=args.sheet)
    sheet = sheet.fillna('')

    if int(args.end) > 0: 
        sheet = sheet.loc[ int(args.begin) : int(args.end) , :]

    return sheet


def openTxt(args):
    with open(args.file) as f:
        lines = f.read().splitlines() 
        if int(args.end) > 0: 
            lines = lines[int(args.begin) : int(args.end)]
        return lines


def rowsToList(args):
    """ Rows from txt/xlsx to list """
    if args.file[-4:] == ".txt":
        rows = openTxt(args)
    else:
        sheet = openSheet(args)
        rows = []
        for i in sheet.index:
            rows.append(sheet[sheet.columns.tolist()[0]][i]) # get first column
    return rows


def whichFilterType(filter):
    """ Extract filtername, its site and select type of filter"""

    if filter.find('@@') != -1:
        return extWhitelist(filter)

    elif filter.find('domain=') != -1:
        return extBlockDomain(filter, 'BLOCK')

    elif filter.find('third-party') != -1:
        return extThirdparty(filter, 'THIRDPARTY')

    elif filter.find('||') != -1:
        return extBlock(filter, 'BLOCK')

    elif filter.find('##') != -1: 
        return extHide(filter, 'HIDE')

    elif filter.find('#?') != -1:
        return extHide(filter, 'HIDE')
        
    elif filter.find('#@#') != -1:
        return extHide(filter, 'WHITELIST')


    elif filter.find('! ***') != -1:
        return ['','','','']

    else:
        return extOther(filter)


def extBlockDomain(filter, type):
    cut = filter.find('$')
    cut2 = filter.find('domain=')

    filtername = filter[:cut]
    sites = filter[cut2+7:]

    if sites.find('|') != -1:
        return extractBlockSites(sites, filter, filtername)
    else:
        return [filter, filtername, sites, type]


def extBlock(filter, type):
    cut = filter.find('^')

    if cut != -1: 
        site = filter[2:cut]        # ||example.com^*^ad
        filtername = filter[cut:]
    else: 
        site = filter[2:]         # ||example.com/ad
        filtername = filter
   
    return [filter, filtername, site, type]


def extHide(filter, type):
    cut = filter.find('#')

    sites = filter[:cut]
    filtername = filter[cut:]

    if sites.find(',') != -1:
        return extractHideSites(sites, filter, filtername)
    else:
        return [filter, filtername, sites, type]


def extWhitelist(filter):
    if filter.find('domain=') != -1:
        return extBlockDomain(filter[2:], 'WHITELIST')

    elif filter.find('||') != -1:
        return extBlock(filter[4:], 'WHITELIST')


def extThirdparty(filter, type):
    cut = filter.find('$')
    if filter.find('||') != -1: 
        filtername = filter[2:cut]
    else: 
        filtername = filter[:cut]
    return [filter, filtername, '', type]


def extOther(filter):
    return [filter, '', '', 'OTHER']


def extractBlockSites(sites, filter, filtername):
    splitted = sites.split('|')
    joined = []
    for site in splitted:
        joined.append([filter, filtername, site, 'BLOCK'])
    return joined


def extractHideSites(sites, filter, filtername):
    splitted = sites.split(',')
    joined = []
    for site in splitted:
        joined.append([filter, filtername, site, 'HIDE'])
    return joined


def createDataframe(args):
    filterlist = []
    rows = rowsToList(args)

    for row in rows:
        r = whichFilterType(row)

        if any(isinstance(i, list) for i in r):     # if r is nested list
            filterlist = filterlist + r
        else:
            filterlist.append(r)

    df=pd.DataFrame(filterlist,columns=['Filter','Name','Site','Type'])
    df['Checked'] = 'TO CHECK'
    df['IsCommited'] = 'no'
    df['ExtraAds'] = ''

    return df


def main():
    args = parser()
    df = createDataframe(args)
    df.to_excel(OUTPUTFILE, sheet_name='filters') 
    print("> extracted to output.xlsx \n") 


if __name__== "__main__":
  main()
