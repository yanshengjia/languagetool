# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-08-03 Friday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.

import xml.etree.ElementTree as ET
import json
import codecs

en_rules_path = '../rules/grammar_en.xml'
zh_rules_path = '../rules/grammar_zh.xml'
no_msg_rules_path = '../rules/no_msg_rules.json'
no_suggestion_rules_path = '../rules/no_suggestion_rules.json'
no_msg_rules = []
no_suggestion_rules = []

def parse_rules(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rule_counter = 0
    for category in root:
        category_id = category.get('id')
        category_name = category.get('name')
        category_type = category.get('type')
        for rule in category:
            rule_id = rule.get('id')
            rule_name = rule.get('name')
            if rule.tag == "rulegroup":
                for r in rule:
                    rule_counter += 1
                    rule_dict = {}
                    msg = r.find('message')
                    if msg is None:
                        rule_dict['type']          = 'NO_MSG'
                        rule_dict['category_id']   = category_id
                        rule_dict['category_name'] = category_name
                        rule_dict['category_type'] = category_type
                        rule_dict['rule_id']       = rule_id
                        rule_dict['rule_name']     = rule_name
                        no_msg_rules.append(rule_dict)
                    else:
                        if msg.find('suggestion') is None:
                            rule_dict['type']          = 'NO_SUGGESTION'
                            rule_dict['message']       = "".join(msg.itertext())
                            rule_dict['category_id']   = category_id
                            rule_dict['category_name'] = category_name
                            rule_dict['category_type'] = category_type
                            rule_dict['rule_id']       = rule_id
                            rule_dict['rule_name']     = rule_name
                            no_suggestion_rules.append(rule_dict)
            else:
                rule_counter += 1
                rule_dict = {}
                msg = rule.find('message')
                if msg is None:
                    rule_dict['type']          = 'NO_MSG'
                    rule_dict['category_id']   = category_id
                    rule_dict['category_name'] = category_name
                    rule_dict['category_type'] = category_type
                    rule_dict['rule_id']       = rule_id
                    rule_dict['rule_name']     = rule_name
                    no_msg_rules.append(rule_dict)
                else:
                    if msg.find('suggestion') is None:
                        rule_dict['message']       = "".join(msg.itertext())
                        rule_dict['category_id']   = category_id
                        rule_dict['category_name'] = category_name
                        rule_dict['category_type'] = category_type
                        rule_dict['rule_id']       = rule_id
                        rule_dict['rule_name']     = rule_name
                        no_suggestion_rules.append(rule_dict)
    print("Rule quantity: {}".format(rule_counter))

def save_suspicious_rules():
    with codecs.open(no_msg_rules_path, 'a') as o_file:
        o_file.seek(0)
        o_file.truncate()
        for rule in no_msg_rules:
            rule_str = json.dumps(rule)
            o_file.write(rule_str + '\n')
    
    with codecs.open(no_suggestion_rules_path, 'a') as o_file:
        o_file.seek(0)
        o_file.truncate()
        for rule in no_suggestion_rules:
            rule_str = json.dumps(rule)
            o_file.write(rule_str + '\n')

def main():
    parse_rules(en_rules_path)
    save_suspicious_rules()

if __name__ == "__main__":
    main()

