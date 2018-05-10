mvn clean
./build.sh languagetool-standalone package -DskipTests
cd ./languagetool-standalone/target/LanguageTool-4.2-SNAPSHOT/LanguageTool-4.2-SNAPSHOT
nohup java -cp languagetool-server.jar org.languagetool.server.HTTPServer &