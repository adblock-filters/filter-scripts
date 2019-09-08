# git log --pretty=oneline --after="2019-7-25" > "C:\Users\Bartek\OneDrive\02_PROJEKTY\01_Projekty_praca\AdblockPlus\filters\pull-requests\lines.txt"

import datetime

path = 'C:\\Users\\Bartek\\OneDrive\\02_PROJEKTY\\01_Projekty_praca\\AdblockPlus\\filters\\websites\\'
file_read = path + "easylistpolish_specific_block.txt"
file_read_2 = path + "easylistpolish_specific_hide.txt"
file_read_3 = path + "easylistpolish_specific_hide_small.txt"
# file_write = path + str(datetime.datetime.now())[:19].replace(":","-") + ".txt"
file_write = path + str(datetime.datetime.now())[:19].replace(":","-") + ".txt"

# from file
domains = ['.pl', '.com', '.net', '.info','.org']

lines = [line.rstrip('\n') for line in open(file_read_2)]
set = []

def rec_check(line, set):
    for domain in domains:
        result = line.find(domain)

        if (result != -1):
            location = result+len(domain)
            newline = line[location+1:]
            site = line[:location]

            if (line[location:location+1] is ','):
                rec_check(newline, set) # reccur
                if (site.find(',') == -1): set.add(site)
            elif (line[location:location+1] is '#'):
                if (site.find(',') == -1): set.add(site)

def rec_check_upgrade(line):
    for domain in domains:
        check_each_occurence(line, domain)

def check_each_occurence(line, domain):
        result = line.find(domain)
        if (result != -1):
            location = result+len(domain)
            site = line[find(',' in reverse order):location]
            if (line[location:location+1] is ','):
                set.add(site)
                rec_check(line[location+1:], domain) # reccur
            elif (line[location:location+1] is '#'):
                set.add(site)


def websites_to_list(lines):
    websites = set()
    for line in lines:
        rec_check(line, websites)
    websites = list(websites)
    websites.sort()
    return websites


def write_to_file(websites, filepath):
    file = open(filepath, 'x', encoding="utf-8")
    for website in websites:
        # print(website)
        file.write(website + "\n")


def main():
    list = websites_to_list(lines)
    write_to_file(list, file_write)


if __name__== "__main__":
  main()
