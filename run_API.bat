REM Fancy stuff :)
@title Rayz API
@Echo off
cls

REM Anti-Crash system.
:Start

REM Start the bot
waitress-serve --port=5000 API:app
echo Press Ctrl-C
ping -n 1 localhost

goto Start
REM Anti-Crash system.
