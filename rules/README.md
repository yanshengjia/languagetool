# 规则汉化

1. 将 grammar.xml 中 \<message\> 标签中的英文纯文本翻译成中文，正则占位符不要动，标点使用英文标点，\<suggestion\> 标签中包含的内容无须翻译。
2. 将翻译好的规则文件 grammar.xml 替换 /path-to-languagetool/languagetool-standalone/target/LanguageTool-4.2-SNAPSHOT/LanguageTool-4.2-SNAPSHOT/org/languagetool/rules/en/grammar.xml，无须重新编译。
3. 运行 start_server.sh