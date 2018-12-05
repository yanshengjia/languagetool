# !/usr/bin/env python3
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
                        rule_dict = {}
                        msg = r.find('message')
                        rule_dict['type']          = 'group'
                        rule_dict['group_index']   = group_index
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
                        group_index += 1
                else:
                    rule_dict = {}
                    msg = rule.find('message')
                    rule_dict['type']          = 'single'
                    rule_dict['group_index']   = ''
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

def parse_rules(rules_path):
    rules = []
    tree = ET.parse(rules_path)
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
                    rule_dict = {}
                    msg = r.find('message')
                    if msg is None:
                        rule_dict['msg']    = ""
                    else:
                        msg_content = ET.tostring(msg, encoding='unicode')
                        # msg_content = msg_content.encode('utf-8').decode('unicode_escape')
                        msg_content = msg_content.strip()
                        rule_dict['msg']    = msg_content
                    rule_dict['type']          = 'group'
                    rule_dict['group_index']   = group_index
                    rule_dict['category_id']   = category_id
                    rule_dict['category_name'] = category_name
                    rule_dict['category_type'] = category_type
                    rule_dict['rule_id']       = rule_id
                    rule_dict['rule_name']     = rule_name
                    rule_dict['error_type']    = ""
                    rules.append(rule_dict)
                    group_index += 1
            else:
                rule_dict = {}
                msg = rule.find('message')
                if msg is None:
                    rule_dict['msg']    = ""
                else:
                    msg_content = ET.tostring(msg, encoding='unicode')
                    # msg_content = msg_content.encode('utf-8').decode('unicode_escape')
                    msg_content = msg_content.strip()
                    rule_dict['msg']    = msg_content
                rule_dict['type']          = 'single'
                rule_dict['group_index']   = ''
                rule_dict['category_id']   = category_id
                rule_dict['category_name'] = category_name
                rule_dict['category_type'] = category_type
                rule_dict['rule_id']       = rule_id
                rule_dict['rule_name']     = rule_name
                rule_dict['error_type']    = ""
                rules.append(rule_dict)
    return rules

def get_example(rules_path):
    rules = []
    tree = ET.parse(rules_path)
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
                    rule_dict = {}
                    example = r.find('example')
                    if example is None:
                        rule_dict['example']       = ""
                        rule_dict['plain_example'] = ""
                    else:
                        example_content = ET.tostring(example, encoding='unicode')
                        # msg_content = msg_content.encode('utf-8').decode('unicode_escape')
                        example_content = example_content.strip()
                        rule_dict['example']       = example_content
                        rule_dict['plain_example'] = "".join(example.itertext())
                    rule_dict['type']          = 'group'
                    rule_dict['group_index']   = group_index
                    rule_dict['category_id']   = category_id
                    rule_dict['category_name'] = category_name
                    rule_dict['category_type'] = category_type
                    rule_dict['rule_id']       = rule_id
                    rule_dict['rule_name']     = rule_name
                    rule_dict['error_type']    = ""
                    rules.append(rule_dict)
                    group_index += 1
            else:
                rule_dict = {}
                example = rule.find('example')
                if example is None:
                    rule_dict['example']       = ""
                    rule_dict['plain_example'] = ""
                else:
                    example_content = ET.tostring(example, encoding='unicode')
                    # msg_content = msg_content.encode('utf-8').decode('unicode_escape')
                    example_content = example_content.strip()
                    rule_dict['example']       = example_content
                    rule_dict['plain_example'] = "".join(example.itertext())
                rule_dict['type']          = 'single'
                rule_dict['group_index']   = ''
                rule_dict['category_id']   = category_id
                rule_dict['category_name'] = category_name
                rule_dict['category_type'] = category_type
                rule_dict['rule_id']       = rule_id
                rule_dict['rule_name']     = rule_name
                rule_dict['error_type']    = ""
                rules.append(rule_dict)
    return rules

def get_translation(en_rules_path, zh_rules_path):
    rules = []
    en_rules = parse_rules(en_rules_path)
    zh_rules = parse_rules(zh_rules_path)

    for en_rule in en_rules:
        rule_dict = {}
        en_rule_id = en_rule['rule_id']

        zh_msg = ''
        for zh_rule in zh_rules:
            zh_rule_id = zh_rule['rule_id']
            if en_rule_id == zh_rule_id:
                zh_msg = zh_rule['msg']
                break

        rule_dict['type']          = en_rule['type']
        rule_dict['group_index']   = en_rule['group_index']
        rule_dict['category_id']   = en_rule['category_id']
        rule_dict['category_name'] = en_rule['category_name']
        rule_dict['category_type'] = en_rule['category_type']
        rule_dict['rule_id']       = en_rule['rule_id']
        rule_dict['rule_name']     = en_rule['rule_name']
        rule_dict['error_type']    = en_rule['error_type']
        rule_dict['en_msg']        = en_rule['msg']
        rule_dict['zh_msg']        = zh_msg
        rules.append(rule_dict)
    return rules

def save_rules_as_csv(result_path, rules):
    with codecs.open(result_path, encoding='utf8', mode='w') as o_file:
        writer = csv.DictWriter(o_file, rules[0].keys())
        writer.writeheader()
        for row in rules:
            writer.writerow(row)

def save_rules_as_json(result_path, rules):
    with codecs.open(result_path, 'a') as o_file:
        o_file.seek(0)
        o_file.truncate()
        for rule in rules:
            rule_str = json.dumps(rule, ensure_ascii=False)
            o_file.write(rule_str + '\n')


def main():
    rules_path = '../rules/grammar.xml'
    en_rules_path = '../rules/grammar_4.2_en.xml'
    zh_rules_path = '../rules/grammar_4.0_zh.xml'
    zh_rules_csv_path = '../rules/grammar.csv'
    zh_rules_json_path = '../rules/grammar.json'
    result_path = '../rules/example_sents.csv'

    rules = get_example(en_rules_path)
    save_rules_as_csv(result_path, rules)

if __name__ == "__main__":
    main()
