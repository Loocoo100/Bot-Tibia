@echo off
echo ==========================================
echo    OT CAVEBOT - INSTALADOR AUTOMATICO
echo ==========================================
echo.
echo Iniciando instalacao automatica...
echo Por favor aguarde, isso pode demorar alguns minutos.
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor instale o Python primeiro:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verifica se Node.js esta instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado!
    echo Por favor instale o Node.js primeiro:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [1/4] Instalando dependencias do Python...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO: Falha na instalacao das dependencias Python
    pause
    exit /b 1
)

echo.
echo [2/4] Instalando dependencias do Node.js...
cd ..\frontend
call npm install
if errorlevel 1 (
    echo ERRO: Falha na instalacao das dependencias Node.js
    pause
    exit /b 1
)

echo.
echo [3/4] Configurando MongoDB local...
cd ..
if not exist "data" mkdir data
if not exist "logs" mkdir logs

echo.
echo [4/4] Criando arquivos de configuracao...

REM Criar arquivo .env para backend
echo MONGO_URL=mongodb://localhost:27017 > backend\.env
echo DB_NAME=otbot_database >> backend\.env

REM Criar arquivo .env para frontend
echo REACT_APP_BACKEND_URL=http://localhost:8001 > frontend\.env

echo.
echo ==========================================
echo         INSTALACAO CONCLUIDA!
echo ==========================================
echo.
echo O bot foi instalado com sucesso!
echo.
echo PROXIMO PASSO:
echo 1. Execute o arquivo EXECUTAR_BOT.bat
echo 2. Aguarde abrir a interface no navegador
echo 3. Configure o bot conforme o tutorial
echo.
echo TUTORIAL COMPLETO: Leia o arquivo TUTORIAL_INSTALACAO.md
echo.
pause