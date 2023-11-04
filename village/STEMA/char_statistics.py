#!/usr/bin/env python3

###############################################################
def make_stat_dict():
    return { '英文字母': 0, '空格': 0, '数字': 0, '其他字符': 0 }

def categorize_char(ds, c):
    if c.isalpha():
        ds['英文字母'] += 1
    elif c.isspace():
        ds['空格'] += 1
    elif c.isdigit():
        ds['数字'] += 1
    else:
        ds['其他字符'] += 1

def display_stats(ds):
    for key in ['英文字母', '空格', '数字', '其他字符']:
        print(ds[key])

###############################################################
def main():
    src = input()
    ds = make_stat_dict()
    for c in src:
        categorize_char(ds, c)
    display_stats(ds)
    


###############################################################
if __name__ == "__main__":
    main()

