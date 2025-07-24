# 📚 Como Salvar seu OT Cavebot no GitHub - Guia Completo

## 🤔 **O que é o GitHub?**

O GitHub é como um "Google Drive" para programadores, onde você pode:
- ✅ Salvar seus projetos na nuvem
- ✅ Fazer backup automático
- ✅ Compartilhar com outras pessoas
- ✅ Versionar seu código (histórico de mudanças)
- ✅ Acessar de qualquer computador

---

## 📝 **PASSO 1: Criar Conta no GitHub**

### 1.1 - Acesse o GitHub
1. Vá para: https://github.com
2. Clique em **"Sign up"** (Cadastrar)

### 1.2 - Preencha os Dados
1. **Username**: Escolha um nome de usuário (ex: `meunomedeusuario`)
2. **Email**: Seu email pessoal
3. **Password**: Uma senha forte
4. Clique **"Create account"**

### 1.3 - Verificar Email
1. Vá no seu email
2. Procure um email do GitHub
3. Clique no link de verificação

---

## 💻 **PASSO 2: Instalar Git no Windows**

### 2.1 - Baixar Git
1. Acesse: https://git-scm.com/download/win
2. Baixe a versão para Windows
3. Execute o arquivo baixado

### 2.2 - Instalar Git
1. Clique **"Next"** em todas as telas
2. ⚠️ **IMPORTANTE**: Na tela "Configuring the line ending conversions", deixe selecionado **"Checkout Windows-style, commit Unix-style line endings"**
3. Continue clicando **"Next"** até o final
4. Clique **"Install"**

---

## ⚙️ **PASSO 3: Configurar Git no seu Computador**

### 3.1 - Abrir Prompt de Comando
1. Pressione `Windows + R`
2. Digite `cmd` e pressione Enter

### 3.2 - Configurar suas Informações
Digite estes comandos (um por vez):

```bash
git config --global user.name "Seu Nome Aqui"
git config --global user.email "seuemail@exemplo.com"
```

**Exemplo:**
```bash
git config --global user.name "João Silva"
git config --global user.email "joao.silva@gmail.com"
```

---

## 🏗️ **PASSO 4: Criar Repositório no GitHub**

### 4.1 - Criar Novo Repositório
1. Faça login no GitHub
2. Clique no **"+"** no canto superior direito
3. Clique **"New repository"**

### 4.2 - Configurar Repositório
1. **Repository name**: `ot-cavebot-indetectavel`
2. **Description**: `Sistema avançado de automação indetectável para Open Tibia`
3. **Visibilidade**: 
   - ✅ **Private** (só você vê)
   - ⚠️ **Public** (todos podem ver)
4. ✅ Marque **"Add a README file"**
5. ✅ Marque **"Add .gitignore"** e escolha **"Python"**
6. Clique **"Create repository"**

---

## 📤 **PASSO 5: Enviar seu Projeto para o GitHub**

### 5.1 - Navegar até a Pasta do Projeto
No Prompt de Comando:
```bash
cd C:\caminho\para\sua\pasta\do\bot
```

**Exemplo:**
```bash
cd C:\MeuBot\ot-cavebot
```

### 5.2 - Inicializar Git na Pasta
```bash
git init
```

### 5.3 - Conectar com seu Repositório GitHub
Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub:
```bash
git remote add origin https://github.com/SEU_USUARIO/ot-cavebot-indetectavel.git
```

**Exemplo:**
```bash
git remote add origin https://github.com/joaosilva/ot-cavebot-indetectavel.git
```

### 5.4 - Adicionar Todos os Arquivos
```bash
git add .
```

### 5.5 - Criar o Primeiro Commit
```bash
git commit -m "Primeira versão do OT Cavebot Indetectável"
```

### 5.6 - Enviar para o GitHub
```bash
git branch -M main
git push -u origin main
```

**⚠️ Vai pedir login:**
- **Username**: Seu nome de usuário do GitHub
- **Password**: Sua senha do GitHub

---

## 🔄 **PASSO 6: Como Atualizar no Futuro**

Sempre que fizer mudanças no seu bot:

### 6.1 - Adicionar Mudanças
```bash
git add .
```

### 6.2 - Criar Commit com Descrição
```bash
git commit -m "Descrição do que você mudou"
```

**Exemplos de mensagens:**
- `"Adicionei nova funcionalidade de auto-loot"`
- `"Corrigi bug na detecção de HP"`
- `"Melhorei a interface do usuário"`

### 6.3 - Enviar para GitHub
```bash
git push
```

---

## 📋 **SCRIPT AUTOMÁTICO PARA ATUALIZAR**

Criei um script que faz tudo automaticamente!

### ATUALIZAR_GITHUB.bat
```batch
@echo off
echo ========================================
echo    ENVIANDO ATUALIZACOES PARA GITHUB
echo ========================================
echo.

echo Adicionando arquivos...
git add .

echo.
set /p mensagem="Digite uma mensagem para esta atualizacao: "

echo.
echo Criando commit...
git commit -m "%mensagem%"

echo.
echo Enviando para GitHub...
git push

echo.
echo ========================================
echo      ATUALIZACAO CONCLUIDA!
echo ========================================
echo.
pause
```

**Como usar:**
1. Clique duplo no arquivo `ATUALIZAR_GITHUB.bat`
2. Digite uma mensagem descrevendo o que você mudou
3. Pressione Enter
4. Pronto!

---

## 🔐 **PASSO 7: Configurar Token de Acesso (Recomendado)**

O GitHub pode pedir um "token" em vez de senha:

### 7.1 - Criar Token
1. No GitHub, vá em **Settings** (no seu perfil)
2. Clique **"Developer settings"** (no final do menu)
3. Clique **"Personal access tokens"** → **"Tokens (classic)"**
4. Clique **"Generate new token"** → **"Generate new token (classic)"**
5. **Note**: `Token para OT Cavebot`
6. **Expiration**: `No expiration` (sem expiração)
7. **Scopes**: Marque apenas `repo`
8. Clique **"Generate token"**
9. **⚠️ COPIE O TOKEN** (só aparece uma vez!)

### 7.2 - Usar Token
Quando pedir senha, use o **token** em vez da sua senha normal.

---

## 📁 **PASSO 8: Estrutura Recomendada no GitHub**

Seu repositório ficará assim:
```
ot-cavebot-indetectavel/
├── README.md
├── TUTORIAL_INSTALACAO.md
├── GUIA_RAPIDO.md
├── INSTALAR_BOT.bat
├── EXECUTAR_BOT.bat
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env
└── config/
    └── local_settings.json
```

---

## 🔄 **PASSO 9: Como Baixar em Outro Computador**

Para usar seu bot em outro PC:

### 9.1 - Clonar Repositório
```bash
git clone https://github.com/SEU_USUARIO/ot-cavebot-indetectavel.git
cd ot-cavebot-indetectavel
```

### 9.2 - Instalar e Usar
1. Execute `INSTALAR_BOT.bat`
2. Execute `EXECUTAR_BOT.bat`
3. Pronto!

---

## 🆘 **PROBLEMAS COMUNS**

| Problema | Solução |
|----------|---------|
| "Git não reconhecido" | Reinstale o Git |
| "Permission denied" | Use token em vez de senha |
| "Repository not found" | Verifique se o nome está correto |
| "Authentication failed" | Verifique usuário e senha/token |

---

## 📱 **BÔNUS: GitHub Desktop (Interface Gráfica)**

Se você prefere interface visual:

### 1. Baixar GitHub Desktop
- https://desktop.github.com/

### 2. Fazer Login
- Use sua conta do GitHub

### 3. Clonar Repositório
- File → Clone repository
- Escolha seu repositório

### 4. Fazer Mudanças
- Edite arquivos normalmente
- O GitHub Desktop detecta automaticamente

### 5. Commit e Push
- Digite mensagem
- Clique "Commit to main"
- Clique "Push origin"

---

## 🎉 **PRONTO!**

Agora você sabe:
- ✅ Criar conta no GitHub
- ✅ Criar repositório
- ✅ Enviar seu projeto
- ✅ Atualizar quando fizer mudanças
- ✅ Baixar em outros computadores
- ✅ Usar interface gráfica (opcional)

**Seu OT Cavebot agora está seguro na nuvem! 🏰☁️**

---

## 📞 **Precisa de Ajuda?**

1. **Documentação oficial**: https://docs.github.com/pt
2. **Tutoriais em vídeo**: Procure "Como usar GitHub" no YouTube
3. **GitHub Desktop**: Mais fácil para iniciantes

**Qualquer dúvida, me pergunte! 😊**