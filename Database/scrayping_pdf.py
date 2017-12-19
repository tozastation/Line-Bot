#!/usr/bin/env python3
# coding:utf-8
import re
import json
line_list = []
with open('Database/NoClass.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        lines = line.split(' ')
        if len(lines) >= 3:
            line_list.append(lines)
text_list = []
for line in line_list:
    status = ''
    buffer_date = re.split('[(*)]', line[1])
    date = buffer_date[0]
    day = buffer_date[1]
    class_time = buffer_date[2]
    buffer = re.split('[(*)]', line[2])
    lesson = buffer[0]
    target = ''
    teacher = ''
    if len(buffer) > 3:
        teacher = buffer[1] + buffer[2]
        target = buffer[3]
    else:
        teacher = buffer[1]
        target = buffer[2]

    for element in line:
        if element in '休講':
            status = element
        elif element in '補講':
            status = element

    text_json = {
        'status': status,
        'date': date,
        'day': day,
        'class_time': class_time,
        'class_name': lesson,
        'teacher': teacher,
        'target_course': target
    }
    text_list.append(text_json)

with open('Database/NoClass.json', 'w') as f:
    json.dump(text_list, f, ensure_ascii=False)

for text in text_list:
    print(text)





