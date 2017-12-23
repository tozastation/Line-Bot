#!/usr/bin/env python3
# coding:utf-8
import json

from Main.Module import model

with model.db.transaction():
    with open('Database/NoClass.json', 'r') as f:
        model.db.create_tables([model.NoClass], safe=True)
        for no_class in json.load(f):
            print(no_class)
            model.NoClass.create(status=no_class['status'],
                                 class_date=no_class['date'],
                                 class_day=no_class['day'],
                                 class_time=no_class['class_time'],
                                 class_name=no_class['class_name'],
                                 class_teacher=no_class['teacher'],
                                 class_target=no_class['target_course'])
model.db.commit()