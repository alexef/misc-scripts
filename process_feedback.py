import re
import csv
import os

def process_file(filename):
    if not os.path.exists(filename):
        return None
    fin = open(filename, 'r')
    lines = fin.readlines()
    answers = []
    mode = 0
    answer = None
    for l in lines:
        if l[0] == '\xef': 
            l = l[3:]
        if re.match(r'[0-9]+\.', l) or l.startswith('1. '):
            if answer is not None:
                answers.append(answer.strip())
            answer = ''
        else:
            answer += l
    answers.append(answer.strip())
    return answers

data = []
for i in range(0, 16):
    a = process_file('%02d.txt' % i)
    if a:
        data.append(a)

with open('result.csv', 'w') as fout:
    writer = csv.writer(fout)
    for d in data:
        writer.writerow(d)

print "Done!"
