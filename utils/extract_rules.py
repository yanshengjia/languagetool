# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-08-08 Wednesday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.
"""
This module extracts rule information from LanguageTool grammar.xml
"""

import xml.etree.ElementTree as ET
import json
import csv
import codecs


def show_statistics(rules_path):
    tree = ET.parse(rules_path)
    root = tree.getroot()
    for category in root:
        category_id = category.get('id')
        category_name = category.get('name')
        category_type = category.get('type')
        print("category id: {}, name: {}, type: {}".format(category_id, category_name, category_type))

def extract_rules_by_category(xml_path, cat):
    rules = []
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rule_counter = 0
    for category in root:
        category_id = category.get('id')
        category_name = category.get('name')
        category_type = category.get('type')
        if category_id == cat:
            for rule in category:
                rule_id = rule.get('id')
                rule_name = rule.get('name')
                if rule.tag == "rulegroup":
                    group_id = 0
                    for r in rule:
                        rule_dict = {}
                        msg = r.find('message')
                        rule_dict['type']          = 'group'
                        rule_dict['group_id']      = group_id
                        rule_dict['category_id']   = category_id
                        rule_dict['category_name'] = category_name
                        rule_dict['category_type'] = category_type
                        rule_dict['rule_id']       = rule_id
                        rule_dict['rule_name']     = rule_name
                        if msg is None:
                            rule_dict['message']   = ""
                        else:
                            rule_dict['message']   = "".join(msg.itertext())
                        rule_dict['error_type']    = ""
                        rules.append(rule_dict)
                        group_id += 1
                else:
                    rule_dict = {}
                    msg = rule.find('message')
                    rule_dict['type']          = 'single'
                    rule_dict['group_id']      = ''
                    rule_dict['category_id']   = category_id
                    rule_dict['category_name'] = category_name
                    rule_dict['category_type'] = category_type
                    rule_dict['rule_id']       = rule_id
                    rule_dict['rule_name']     = rule_name
                    if msg is None:
                        rule_dict['message']   = ""
                    else:
                        rule_dict['message']   = "".join(msg.itertext())
                    rule_dict['error_type']    = ""
                    rules.append(rule_dict)
    return rules

def save_rules(result_path, rules):
    with codecs.open(result_path, 'w') as o_file:
        writer = csv.DictWriter(o_file, rules[0].keys())
        writer.writeheader()
        for row in rules:
            writer.writerow(row)

def main():
    rules_path = '../rules/grammar.xml'
    en_rules_path = '../rules/grammar_en.xml'
    zh_rules_path = '../rules/grammar_zh.xml'
    zh_rules_csv_path = '../rules/grammar.csv'
    result_path = '../rules/grammar_rules.csv'
    

if __name__ == "__main__":
    main()
