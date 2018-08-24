# !/usr/bin/env python3
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-08-24 Friday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.


import csv
import xlrd
import codecs

before_grammar_filepath = './grammar_before.csv'
after_grammar_filepath = './grammar_after.xlsx'
new_grammar_filepath = './new_grammar.csv'

def get_zh_msg():
    rules = []
    with codecs.open(before_grammar_filepath, 'r') as in_file:
        reader = csv.DictReader(in_file)
        for line in reader:
            rules.append(line)

    infos = []
    r_workbook = xlrd.open_workbook(after_grammar_filepath)
    sheet_names = r_workbook.sheet_names()
    sheet_quantity = len(sheet_names)
    
    for sheet_index in range(sheet_quantity):
        print("Processing sheet: " + sheet_names[sheet_index])
        r_worksheet = r_workbook.sheet_by_index(sheet_index)
        offset = 0  # change this depending on how many header rows are present
        for i, row in enumerate(range(r_worksheet.nrows)):
            if i <= offset:  # skip headers
                continue
            info_dict = {}
            line = r_worksheet.cell_value(i, 0)
            info = line.split('\t')

            if len(info) != 10:
                continue
            
            info_dict['type'] = info[0]
            if info[1] == '':
                info_dict['group_index'] = info[1]
            else:
                info_dict['group_index'] = int(info[1])
            info_dict['rule_id'] = info[5]
            info_dict['zh_msg'] = info[9]
            infos.append(info_dict)

    for rule in rules:
        type = rule['\ufefftype']
        group_index = rule['group_index']
        rule_id = rule['rule_id']

        for info in infos:
            if type == info['type'] and group_index == info['group_index'] and rule_id == info['rule_id']:
                rule['zh_msg'] = info['zh_msg']
                break

    with open(new_grammar_filepath, mode='w', encoding="utf8", errors='ignore') as out_file:
        writer = csv.DictWriter(out_file, rules[0].keys())
        writer.writeheader()
        for row in rules:
            writer.writerow(row)

def main():
    get_zh_msg()


if __name__ == "__main__":
    main()