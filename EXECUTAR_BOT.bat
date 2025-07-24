@echo off
title OT Cavebot - Executando
echo ==========================================
echo         OT CAVEBOT INICIANDO...
echo ==========================================
echo.

REM Verifica se as dependencias foram instaladas
if not exist "backend\requirements.txt" (
    echo ERRO: Arquivos do bot nao encontrados!
    echo Execute primeiro o INSTALAR_BOT.bat
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ERRO: Dependencias nao instaladas!
    echo Execute primeiro o INSTALAR_BOT.bat
    pause
    exit /b 1
)

echo Iniciando servidor backend...
echo.

REM Inicia o backend em uma nova janela
start "Backend - OT Cavebot" cmd /k "cd backend && python server.py"

echo Aguardando servidor backend inicializar...
timeout /t 5 /nobreak >nul

echo Iniciando interface frontend...
echo.

REM Inicia o frontend em uma nova janela
start "Frontend - OT Cavebot" cmd /k "cd frontend && npm start"

echo.
echo ==========================================
echo           BOT INICIADO COM SUCESSO!
echo ==========================================
echo.
echo O bot esta rodando nos seguintes enderecos:
echo.
echo Frontend (Interface): http://localhost:3000
echo Backend (Servidor):   http://localhost:8001
echo.
echo IMPORTANTE:
echo - Mantenha estas janelas abertas enquanto usar o bot
echo - A interface deve abrir automaticamente no seu navegador
echo - Se nao abrir, acesse manualmente: http://localhost:3000
echo.
echo Para PARAR o bot:
echo 1. Feche esta janela
echo 2. Feche as janelas "Backend" e "Frontend"
echo.
echo Bom jogo! 🏰⚔️
echo.
pause