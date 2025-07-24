@echo off
echo ==========================================
echo       PARANDO OT CAVEBOT...
echo ==========================================
echo.

echo Finalizando processos do bot...

REM Para processos Python (backend)
taskkill /f /im python.exe 2>nul
if errorlevel 1 (
    echo Backend ja estava parado.
) else (
    echo Backend finalizado.
)

REM Para processos Node.js (frontend)
taskkill /f /im node.exe 2>nul
if errorlevel 1 (
    echo Frontend ja estava parado.
) else (
    echo Frontend finalizado.
)

REM Para processos do Chrome/navegador se foram abertos pelo bot
taskkill /f /im chrome.exe /fi "WINDOWTITLE eq React*" 2>nul

echo.
echo ==========================================
echo        BOT PARADO COM SUCESSO!
echo ==========================================
echo.
echo Todos os processos do bot foram finalizados.
echo.
echo Para iniciar novamente:
echo Execute o arquivo EXECUTAR_BOT.bat
echo.
pause