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

version = '4.2'
rules_csv_path = '../rules/grammar.csv'
en_rules_xml_path = '../rules/grammar_' + version + '_en.xml'
zh_rules_xml_path = '../rules/grammar_' + version + '_zh.xml'


def load_rules(rules_path):
    with codecs.open(rules_path, 'r') as in_file:
        rules = []
        reader = csv.DictReader(in_file)
        for line in reader:
            rules.append(line)
    return rules

def translate(zh_rules_path, en_rules_path, rules):
    os.system("touch " + zh_rules_path)
    os.system("> " + zh_rules_path)
    os.system("cat " + en_rules_path + " >> " + zh_rules_path)

    tree = ET.parse(zh_rules_path)
    root = tree.getroot()

    for category in root:
        category_id = category.get('id')
        category_name = category.get('name')
        category_type = category.get('type')
        if category_id == cat:
            for rule in category:
                rule_id = rule.get('id')
                rule_name = rule.get('name')
                if rule.tag == "rulegroup":
                    group_index = 0
                    for r in rule:
                        

                        
                        group_index += 1
                else:
                    pass



def main():
    rules = load_rules(rules_csv_path)
    translate(zh_rules_xml_path, en_rules_xml_path, rules)

if __name__ == "__main__":
    main()

