#!/bin/bash
echo "Cleaning..."
mvn clean

echo "Moving properties..."
rm ./languagetool-core/src/main/resources/org/languagetool/MessagesBundle_en.properties
cp ./rules/MessagesBundle_zh.properties ./languagetool-core/src/main/resources/org/languagetool/MessagesBundle_en.properties

echo "Building..."
./build.sh languagetool-standalone package -DskipTests

echo "Translating..."
rm ./languagetool-standalone/target/LanguageTool-4.2-SNAPSHOT/LanguageTool-4.2-SNAPSHOT/org/languagetool/rules/en/grammar.xml
cp ./rules/grammar_zh.xml ./languagetool-standalone/target/LanguageTool-4.2-SNAPSHOT/LanguageTool-4.2-SNAPSHOT/org/languagetool/rules/en/grammar.xml

echo "Start the server"
cd ./languagetool-standalone/target/LanguageTool-4.2-SNAPSHOT/LanguageTool-4.2-SNAPSHOT
nohup java -cp languagetool-server.jar org.languagetool.server.HTTPServer &