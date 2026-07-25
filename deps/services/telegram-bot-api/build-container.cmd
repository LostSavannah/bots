docker build -t telegram-bot-api-local .
IF %ERRORLEVEL% NEQ 0 (
    pause
)