@echo off
cd /d %~dp0
echo Running AliExpress Coin Collector at %date% %time%
python collect_coins.py
echo Collection completed at %date% %time%
pause