# !/usr/bin/env python3
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-08-18 Saturday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.
'''
This module translates the English rule messages of LanguageTool.
'''

import os
import xlrd
import json
import csv
import codecs
import xml.etree.ElementTree as ET


class Translater:
    def __init__(self):
        self.version = '4.2'
        self.rules_path = '../rules/grammar.xls'
        self.en_rules_xml_path = '../rules/grammar_' + self.version + '_en.xml'
        self.zh_rules_xml_path = '../rules/grammar_' + self.version + '_zh.xml'
        self.grammar_xml_path = '../rules/grammar.xml'
        self.head_lines = 38
        self.trashed_rules_path = '../rules/trashed_rules_list.txt'
        self.rules = self.load_rules()

    def load_rules(self):
        rules = []
        keys = []
        r_workbook = xlrd.open_workbook(self.rules_path)
        sheet_names = r_workbook.sheet_names()
        sheet_quantity = len(sheet_names)
        
        for sheet_index in range(sheet_quantity):
            print("Processing sheet: " + sheet_names[sheet_index])
            r_worksheet = r_workbook.sheet_by_index(sheet_index)
            offset = 0  # change this depending on how many header rows are present
            for row_index in range(r_worksheet.nrows):
                if row_index <= offset:  # skip headers
                    for col_index in range(r_worksheet.ncols):
                        keys.append(r_worksheet.cell_value(row_index, col_index))
                row_dict = {}
                for col_index in range(r_worksheet.ncols):
                    row_dict[keys[col_index]] = r_worksheet.cell_value(row_index, col_index)
                rules.append(row_dict)
        return rules

    def search_zh_msg(self, type, group_index, rule_id):
        zh_msg = ''
        rule_counter = 0
        for rule in self.rules:
            if type == 'single':
                if rule['type'] == type and rule['group_index'] == '' and rule['rule_id'] == rule_id:
                    zh_msg = rule['zh_msg']
                    return zh_msg, rule_counter
            else:
                if rule['type'] == type and int(rule['group_index']) == group_index and rule['rule_id'] == rule_id:
                    zh_msg = rule['zh_msg']
                    return zh_msg, rule_counter
            rule_counter += 1
        return 'grammar.xls doesnt have such msg', -1
    
    def preprocess(self, msg):
        if len(msg) > 0 and msg[0] == "\"":
            msg = msg[1:-1]
        return msg

    def translate(self):
        os.system("touch " + self.zh_rules_xml_path)
        os.system("> " + self.zh_rules_xml_path)
        os.system("cat " + self.en_rules_xml_path + " >> " + self.zh_rules_xml_path)

        with open(self.trashed_rules_path, 'a') as o_file:
            o_file.seek(0)
            o_file.truncate()

            tree = ET.parse(self.zh_rules_xml_path)
            root = tree.getroot()
            trashed_rule_counter = 0

            for category in root:
                category_id = category.get('id')
                category_name = category.get('name')
                category_type = category.get('type')
                for rule in category:
                    rule_id = rule.get('id')
                    rule_name = rule.get('name')
                    if rule.tag == "rulegroup":
                        group_index = 0
                        for r in rule:
                            msg = r.find('message')
                            type = 'group'

                            if msg is None:
                                group_index += 1
                                continue
                            
                            try:
                                new_zh_msg, rule_number = self.search_zh_msg(type, group_index, rule_id)
                                new_msg_element = ET.XML(new_zh_msg)
                                r.remove(msg)
                                r.append(new_msg_element)
                            except Exception as e:
                                trashed_rule_counter += 1
                                trashed_rule_str = "{} {} {} {} {}".format(rule_number, type, group_index, rule_id, e)
                                o_file.write(trashed_rule_str + '\n')
                            
                            group_index += 1
                    else:
                        msg = rule.find('message')
                        type = 'single'
                        group_index = ''

                        if msg is None:
                            continue
                        
                        try:
                            new_zh_msg, rule_number = self.search_zh_msg(type, group_index, rule_id)
                            new_msg_element = ET.XML(new_zh_msg)
                            rule.remove(msg)
                            rule.append(new_msg_element)
                        except Exception as e:
                            trashed_rule_counter += 1
                            trashed_rule_str = "{} {} {} {} {}".format(rule_number, type, group_index, rule_id, e)
                            o_file.write(trashed_rule_str + '\n')
            tree.write(self.zh_rules_xml_path)
            print("Trashed rule quantity: {}".format(trashed_rule_counter))

    def produce_xml(self):
        os.system("touch " + self.grammar_xml_path)
        os.system("> " + self.grammar_xml_path)
        os.system("head -" + str(self.head_lines) + ' ' + self.en_rules_xml_path + ' > ' + self.grammar_xml_path)
        os.system("cat " + self.zh_rules_xml_path + " >> " + self.grammar_xml_path)

def main():
    translater = Translater()
    translater.translate()
    translater.produce_xml()

if __name__ == "__main__":
    main()

