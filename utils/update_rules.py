# !/usr/bin/env python3
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-09-18 Tuesday
# @email: i@yanshengjia.com
# Copyright @ Shengjia Yan. All Rights Reserved.
'''
This module updates the rules of LanguageTool.
'''

import os
import xlrd
import json
import csv
import codecs
import xml.etree.ElementTree as ET

class RuleManager:
    def __init__(self):
        self.version = '4.2'
        self.new_rules_path = 'rules/new_rules.xlsx'
        self.empty_grammar_xml_path = 'rules/empty_grammar.xml'
        self.temp_grammar_xml_path = 'rules/temp_grammar.xml'
        self.grammar_xml_path = 'rules/grammar.xml'
        self.head_lines = 38
        self.new_rule_xmls = self._load_new_rules()
    
    def _load_new_rules(self):
        xmls = []
        r_workbook = xlrd.open_workbook(self.new_rules_path)
        sheet_names = r_workbook.sheet_names()
        sheet_quantity = len(sheet_names)
        
        for sheet_index in range(sheet_quantity):
            print("Processing sheet: " + sheet_names[sheet_index])
            r_worksheet = r_workbook.sheet_by_index(sheet_index)
            offset = 0
            for row_index in range(r_worksheet.nrows):
                if row_index <= offset:  # skip headers
                    continue
                xml = r_worksheet.cell_value(row_index, 6)
                if xml != '':
                    xmls.append(xml)
        return xmls
    
    def build_new_grammar_xml(self):
        tree = ET.parse(self.empty_grammar_xml_path)
        root = tree.getroot()
        for category in root:
            category_id = category.get('id')
            if category_id == 'GRAMMAR':
                for xml in self.new_rule_xmls:
                    new_rule_element = ET.XML(xml)
                    category.append(new_rule_element)
        tree.write(self.temp_grammar_xml_path)

        os.system("touch " + self.grammar_xml_path)
        os.system("> " + self.grammar_xml_path)
        os.system("head -" + str(self.head_lines) + ' ' + self.empty_grammar_xml_path + ' > ' + self.grammar_xml_path)
        os.system("cat " + self.temp_grammar_xml_path + " >> " + self.grammar_xml_path)

def main():
    rule_manager = RuleManager()
    rule_manager.build_new_grammar_xml()

if __name__ == '__main__':
    main()


