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
import json
import csv
import codecs
import xml.etree.ElementTree as ET


class Translater:
    def __init__(self):
        self.version = '4.2'
        self.rules_csv_path = '../rules/grammar.csv'
        self.en_rules_xml_path = '../rules/grammar_' + self.version + '_en.xml'
        self.zh_rules_xml_path = '../rules/grammar_' + self.version + '_zh.xml'
        self.rules = self.load_rules()

    def load_rules(self):
        with codecs.open(self.rules_csv_path, 'r') as in_file:
            rules = []
            reader = csv.DictReader(in_file)
            for line in reader:
                line['zh_msg'] = self.preprocess(line['zh_msg'])
                rules.append(line)
        return rules

    def search_zh_msg(self, type, group_index, rule_id):
        zh_msg = ''
        rule_counter = 1
        for rule in self.rules:
            if type == 'single':
                if rule['\ufefftype'] == type and rule['group_index'] == '' and rule['rule_id'] == rule_id:
                    zh_msg = rule['zh_msg']
                    break
            else:
                if rule['\ufefftype'] == type and int(rule['group_index']) == group_index and rule['rule_id'] == rule_id:
                    zh_msg = rule['zh_msg']
                    break
            rule_counter += 1
        return zh_msg, rule_counter
    
    def preprocess(self, msg):
        if len(msg) > 0 and msg[0] == "\"":
            msg = msg[1:-1]
        return msg

    def translate(self):
        os.system("touch " + self.zh_rules_xml_path)
        os.system("> " + self.zh_rules_xml_path)
        os.system("cat " + self.en_rules_xml_path + " >> " + self.zh_rules_xml_path)

        tree = ET.parse(self.zh_rules_xml_path)
        root = tree.getroot()

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
                            print(e)
                            print(rule_number, type, group_index, rule_id)
                        
                        group_index += 1
                else:
                    msg = rule.find('message')
                    type = 'single'

                    if msg is None:
                        continue
                    
                    try:
                        new_zh_msg, rule_number = self.search_zh_msg(type, group_index, rule_id)
                        new_msg_element = ET.XML(new_zh_msg)
                        rule.remove(msg)
                        rule.append(new_msg_element)
                    except Exception as e:
                        print(e)
                        print(rule_number, type, group_index, rule_id)
        tree.write(self.zh_rules_xml_path)


def main():
    translater = Translater()
    translater.translate()

if __name__ == "__main__":
    main()

