# LanguageTool Usage Instructions

## How to add rules

填写 new_rules.xlsx，message 标签中的建议信息用中文写。



## How to update rules

1.ssh 登录跳板机，进入 10.7.13.73 服务器

2.进入 LanguageTool 的工程目录

```shell
cd sjyan/services/languagetool/
```

3.将包含新规则 XML 的 EXCEL 文件拷贝到 `rules/` 目录下

```shell
cp path/to/new_rules.xlsx rules/new_rules.xlsx
```

4.如果当前有 LanguageTool 服务在运行，则关闭它。

```shell
ps -aux | grep languagetool
kill $process_id
```

5.重启服务

```shell
bash start_server.sh
```



##Chinesization

1. 将 grammar.xml 中 message 标签中的英文纯文本翻译成中文，正则占位符不要动，标点使用英文标点，suggestion 标签中包含的内容无须翻译。
2. 将翻译好的规则文件 grammar.xml 替换 /path-to-languagetool/languagetool-standalone/target/LanguageTool-4.2-SNAPSHOT/LanguageTool-4.2-SNAPSHOT/org/languagetool/rules/en/grammar.xml，无须重新编译。
3. 启动服务