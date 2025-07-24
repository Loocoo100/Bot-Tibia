@echo off
echo ==========================================
echo    VERIFICADOR DE INSTALACAO - OT CAVEBOT
echo ==========================================
echo.
echo Verificando se tudo esta instalado corretamente...
echo.

set "TUDO_OK=1"

echo [1/7] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python NAO encontrado
    echo    Baixe em: https://www.python.org/downloads/
    set "TUDO_OK=0"
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo ✅ %%i encontrado
)

echo.
echo [2/7] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js NAO encontrado
    echo    Baixe em: https://nodejs.org/
    set "TUDO_OK=0"
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do echo ✅ Node.js %%i encontrado
)

echo.
echo [3/7] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git NAO encontrado
    echo    Baixe em: https://git-scm.com/download/win
    set "TUDO_OK=0"
) else (
    echo ✅ Git encontrado
)

echo.
echo [4/7] Verificando arquivos do backend...
if exist "backend\server.py" (
    echo ✅ Arquivo server.py encontrado
) else (
    echo ❌ Arquivo server.py NAO encontrado
    set "TUDO_OK=0"
)

if exist "backend\requirements.txt" (
    echo ✅ Arquivo requirements.txt encontrado
) else (
    echo ❌ Arquivo requirements.txt NAO encontrado
    set "TUDO_OK=0"
)

echo.
echo [5/7] Verificando arquivos do frontend...
if exist "frontend\package.json" (
    echo ✅ Arquivo package.json encontrado
) else (
    echo ❌ Arquivo package.json NAO encontrado
    set "TUDO_OK=0"
)

if exist "frontend\src\App.js" (
    echo ✅ Arquivo App.js encontrado
) else (
    echo ❌ Arquivo App.js NAO encontrado
    set "TUDO_OK=0"
)

echo.
echo [6/7] Verificando dependencias Python...
if exist "backend\.env" (
    echo ✅ Configuracao backend encontrada
) else (
    echo ⚠️  Configuracao backend nao encontrada (sera criada na instalacao)
)

echo.
echo [7/7] Verificando dependencias Node.js...
if exist "frontend\node_modules" (
    echo ✅ Dependencias Node.js instaladas
) else (
    echo ⚠️  Dependencias Node.js nao instaladas (execute INSTALAR_BOT.bat)
)

echo.
echo ==========================================
if "%TUDO_OK%"=="1" (
    echo          ✅ TUDO PRONTO!
    echo ==========================================
    echo.
    echo Sua instalacao esta correta!
    echo.
    echo PROXIMOS PASSOS:
    echo 1. Se ainda nao instalou: Execute INSTALAR_BOT.bat
    echo 2. Para usar o bot: Execute EXECUTAR_BOT.bat
    echo 3. Leia o TUTORIAL_INSTALACAO.md
) else (
    echo        ❌ PROBLEMAS ENCONTRADOS
    echo ==========================================
    echo.
    echo Corrija os problemas acima antes de continuar.
    echo.
    echo PRECISA DE AJUDA?
    echo 1. Leia o TUTORIAL_INSTALACAO.md
    echo 2. Verifique se baixou todos os programas necessarios
    echo 3. Execute este verificador novamente apos as correcoes
)

echo.
pause