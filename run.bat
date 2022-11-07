REM Fancy stuff :)
@title Rayz
@Echo off
cls

REM Anti-Crash system.
:Start

REM Start the bot
python base.py
echo Press Ctrl-C
ping -n 1 localhost

goto Start
REM Anti-Crash system.
