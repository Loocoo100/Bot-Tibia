@echo off
echo ========================================
echo    ENVIANDO ATUALIZACOES PARA GITHUB
echo ========================================
echo.

REM Verifica se o Git esta configurado
git config user.name >nul 2>&1
if errorlevel 1 (
    echo ERRO: Git nao esta configurado!
    echo.
    echo Configure primeiro com:
    echo git config --global user.name "Seu Nome"
    echo git config --global user.email "seuemail@exemplo.com"
    echo.
    pause
    exit /b 1
)

echo Verificando status do repositorio...
git status

echo.
echo Adicionando arquivos modificados...
git add .

echo.
set /p mensagem="Digite uma mensagem para esta atualizacao: "

if "%mensagem%"=="" (
    set mensagem=Atualizacao automatica
)

echo.
echo Criando commit com mensagem: "%mensagem%"
git commit -m "%mensagem%"

if errorlevel 1 (
    echo.
    echo Nenhuma mudanca detectada ou erro no commit.
    echo Verifique se ha arquivos modificados.
    pause
    exit /b 1
)

echo.
echo Enviando para GitHub...
git push

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao enviar para GitHub.
    echo.
    echo Possiveis causas:
    echo 1. Problema de autenticacao (usuario/senha/token)
    echo 2. Sem conexao com internet
    echo 3. Repositorio nao configurado
    echo.
    echo Para configurar repositorio:
    echo git remote add origin https://github.com/SEU_USUARIO/NOME_REPOSITORIO.git
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo      ATUALIZACAO CONCLUIDA!
echo ========================================
echo.
echo Suas mudanças foram enviadas para o GitHub com sucesso!
echo Você pode ver em: https://github.com/SEU_USUARIO/NOME_REPOSITORIO
echo.
pause