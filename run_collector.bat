@echo off
cd /d %~dp0
echo Running AliExpress Coin Collector at %date% %time% >> collection_log.txt
python collect_coins.py >> collection_log.txt 2>&1
echo Collection completed at %date% %time% >> collection_log.txt