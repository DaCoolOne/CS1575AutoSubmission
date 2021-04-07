#!/usr/bin/env python3

# From:
# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

NAME_COLUMN_WIDTH = 20
RESULT_COLUMN_WIDTH = 110

EXTRA_WIDTH = 1

def parse(line: str, sep=',') -> str:
    out = []
    in_string = False
    for seg in line.split(sep):
        if in_string:
            out[-1] += seg
        else:
            out.append(seg)

        if seg.count('"') % 2 == 1:
            in_string = not in_string
    return out

def constrain_to_size(str_list, size):
    out = []
    for s in str_list:
        while(len(s) > size):
            if s[:size].find(' ') == -1:
                out.append(s[:size])
                s = s[size:]
            else:
                s_index = s.rfind(' ',0,size)
                out.append(s[:s_index])
                s = s[s_index + 1:]
        out.append(s)
    return out

def gen_color(c: str) -> str:
    if c == 'pass':
        return bcolors.OKGREEN
    if c == 'fail':
        return bcolors.FAIL
    if c.lower().count('error') > 0:
        return bcolors.WARNING
    if c == "Probably crashed":
        return bcolors.FAIL
    
    if c.isdigit():
        if int(c):
            return bcolors.WARNING
        else:
            return bcolors.OKBLUE

    return bcolors.ENDC

if __name__ == "__main__":
    with open("results.csv") as f:
        raw_lines = [ line for line in f.readlines() ]
        lines = []
        in_string = False
        for seg in raw_lines:
            if in_string:
                lines[-1] += seg
            else:
                lines.append(seg)

            if seg.count('"') % 2 == 1:
                in_string = not in_string

    test_names = parse(lines[0].strip())
    results = parse(lines[1].strip())

    e = '-' * (NAME_COLUMN_WIDTH + EXTRA_WIDTH) + '+' + '-' * (RESULT_COLUMN_WIDTH + EXTRA_WIDTH)

    for i in range(len(test_names)):
        color = gen_color(results[i])
        test_name_lines = constrain_to_size(test_names[i].splitlines(), NAME_COLUMN_WIDTH)
        result_name_lines = constrain_to_size(results[i].splitlines(), RESULT_COLUMN_WIDTH)
        for j in range(max(len(test_name_lines), len(result_name_lines))):
            tl = test_name_lines[j] if j < len(test_name_lines) else ''
            rl = result_name_lines[j] if j < len(result_name_lines) else ''
            print(
                bcolors.OKCYAN + tl.ljust(NAME_COLUMN_WIDTH + EXTRA_WIDTH) + bcolors.ENDC,
                color + rl.rjust(RESULT_COLUMN_WIDTH + EXTRA_WIDTH), sep='|')
        print(bcolors.ENDC + e)