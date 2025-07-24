@echo off
echo ========================================
echo      CONFIGURAR GIT PRIMEIRA VEZ
echo ========================================
echo.

echo Este script vai configurar o Git no seu computador.
echo Você precisa fazer isso apenas uma vez.
echo.

REM Verifica se Git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao encontrado!
    echo.
    echo Por favor instale o Git primeiro:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo Git encontrado! Vamos configurar...
echo.

set /p nome="Digite seu nome completo: "
set /p email="Digite seu email: "

if "%nome%"=="" (
    echo ERRO: Nome nao pode estar vazio!
    pause
    exit /b 1
)

if "%email%"=="" (
    echo ERRO: Email nao pode estar vazio!
    pause
    exit /b 1
)

echo.
echo Configurando Git...

git config --global user.name "%nome%"
git config --global user.email "%email%"

REM Configuracoes adicionais recomendadas
git config --global init.defaultBranch main
git config --global core.autocrlf true

echo.
echo ========================================
echo       CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Git configurado com:
echo Nome: %nome%
echo Email: %email%
echo.
echo Agora você pode usar o Git normalmente!
echo.
echo PROXIMOS PASSOS:
echo 1. Crie uma conta no GitHub (se ainda nao tem)
echo 2. Crie um repositorio
echo 3. Use ATUALIZAR_GITHUB.bat para enviar arquivos
echo.
pause