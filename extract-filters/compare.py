from extract import *

MAIN_LIST = 'short-to-extract.xlsx'
SUB_LIST = 'filters-to-extract.xlsx'


def set_of_filters(args):
    df = createDataframe(args)
    only_sites = df['Site'].values.tolist()
    return set(only_sites)


def generate_subset(args):
    args.file = MAIN_LIST
    main_set = set_of_filters(args)
    args.file = SUB_LIST
    sub_set = set_of_filters(args)

    # print(main_set)

    # print("=====================\n\n\n")

    # print(sub_set)

    return main_set - sub_set

def main():
    args = parser()
    sub = list(generate_subset(args))
    sub.sort()
    
    less_useful = []
    for filter in sub:
        if filter.find("/") > -1:   less_useful.append(filter)
        else:                       print(filter)

    for filter in less_useful:
        print(filter)


if __name__== "__main__":
  main()
