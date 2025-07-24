@echo off
echo ========================================
echo    BAIXAR PROJETO DO GITHUB
echo ========================================
echo.

set /p repo_url="Cole a URL completa do seu repositorio GitHub: "

if "%repo_url%"=="" (
    echo ERRO: URL nao fornecida!
    echo.
    echo Exemplo de URL:
    echo https://github.com/seu-usuario/ot-cavebot-indetectavel.git
    echo.
    pause
    exit /b 1
)

echo.
echo Baixando projeto do GitHub...
echo URL: %repo_url%
echo.

git clone %repo_url%

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao baixar repositorio.
    echo.
    echo Verifique se:
    echo 1. A URL esta correta
    echo 2. Voce tem acesso ao repositorio
    echo 3. O Git esta instalado
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo       DOWNLOAD CONCLUIDO!
echo ========================================
echo.
echo O projeto foi baixado com sucesso!
echo.
echo PROXIMOS PASSOS:
echo 1. Entre na pasta do projeto
echo 2. Execute INSTALAR_BOT.bat
echo 3. Execute EXECUTAR_BOT.bat
echo.
pause