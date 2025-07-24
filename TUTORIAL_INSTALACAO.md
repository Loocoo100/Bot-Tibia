# 🏰 Tutorial de Instalação - OT Cavebot Indetectável

## 📋 **O que é este programa?**

Este é um bot automático para Open Tibia que pode:
- ✅ Curar automaticamente quando sua vida está baixa
- ✅ Atacar monstros automaticamente 
- ✅ Coletar itens do chão (loot)
- ✅ Andar por waypoints automáticamente
- ✅ Usar comida quando necessário
- ✅ **INDETECTÁVEL** - Simula movimentos humanos

---

## 🖥️ **Requisitos do seu Computador**

Antes de começar, você precisa ter:
- ✅ Windows 10 ou 11
- ✅ Pelo menos 4GB de RAM
- ✅ Conexão com internet
- ✅ Tibia instalado no seu computador

---

## 📥 **PASSO 1: Baixar os Programas Necessários**

### 1.1 - Baixar Python
1. Acesse: https://www.python.org/downloads/
2. Clique no botão verde **"Download Python"**
3. Execute o arquivo baixado
4. ⚠️ **IMPORTANTE**: Marque a opção **"Add Python to PATH"**
5. Clique em **"Install Now"**
6. Aguarde a instalação terminar

### 1.2 - Baixar Git
1. Acesse: https://git-scm.com/download/win
2. Baixe a versão para Windows
3. Execute o arquivo e clique **"Next"** em todas as telas
4. Aguarde a instalação terminar

### 1.3 - Baixar Node.js
1. Acesse: https://nodejs.org/
2. Baixe a versão **LTS** (recomendada)
3. Execute o arquivo e clique **"Next"** em todas as telas
4. Aguarde a instalação terminar

---

## 💾 **PASSO 2: Baixar o Bot**

1. **Crie uma pasta** no seu computador (por exemplo: `C:\MeuBot`)
2. **Abra o Prompt de Comando**:
   - Pressione `Windows + R`
   - Digite `cmd` e pressione Enter
3. **Navegue até sua pasta**:
   ```
   cd C:\MeuBot
   ```
4. **Baixe o bot**:
   ```
   git clone https://github.com/seu-usuario/ot-cavebot.git
   cd ot-cavebot
   ```

---

## ⚙️ **PASSO 3: Instalação Automática**

Criei um script que instala tudo automaticamente para você!

### 3.1 - Execute o Instalador
1. **Clique duplo** no arquivo `INSTALAR_BOT.bat`
2. Aguarde a instalação (pode demorar alguns minutos)
3. Quando aparecer **"Instalação concluída!"**, feche a janela

### 3.2 - Se o instalador não funcionar:
Execute estes comandos no Prompt de Comando (um por vez):

```bash
# Instalar dependências do backend
cd backend
pip install -r requirements.txt

# Instalar dependências do frontend  
cd ../frontend
npm install

# Voltar para a pasta principal
cd ..
```

---

## 🚀 **PASSO 4: Executar o Bot**

### 4.1 - Iniciar o Sistema
1. **Clique duplo** no arquivo `EXECUTAR_BOT.bat`
2. Duas janelas vão abrir:
   - Uma janela preta (servidor)
   - Uma janela do navegador (interface)

### 4.2 - Se não abrir automaticamente:
1. Abra seu navegador
2. Digite: `http://localhost:3000`

---

## 🎮 **PASSO 5: Configurar o Bot**

### 5.1 - Primeira Configuração
1. Na interface web, vá na aba **"⚙️ Configurações"**
2. **Configure os básicos**:
   - Nome do Bot: `Meu Primeiro Bot`
   - Magia de Cura: `exura` (ou sua magia de cura)
   - Curar em HP: `70` (cura quando vida chegar a 70%)
   - Magia de Ataque: `exori` (ou sua magia de ataque)

### 5.2 - Configurar Alvos
1. **Criaturas para atacar**: Digite separado por vírgula
   ```
   rat, cave rat, rotworm
   ```

2. **Itens para coletar**: Digite separado por vírgula
   ```
   gold coin, platinum coin, crystal coin
   ```

3. **Itens para descartar**: Digite separado por vírgula
   ```
   leather armor, studded armor, chain armor
   ```

### 5.3 - Salvar Configuração
1. Clique em **"💾 Salvar Configurações"**
2. Aguarde aparecer "Configuração salva com sucesso!"

---

## 🗺️ **PASSO 6: Criar Waypoints (Opcional)**

Waypoints fazem o bot andar automaticamente por locais específicos.

### 6.1 - Adicionar Waypoints
1. Vá na aba **"🗺️ Waypoints"**
2. **No jogo**:
   - Posicione seu personagem onde quer o waypoint
   - Volte na interface do bot
   - Clique **"📍 Capturar Posição Atual"**
3. Digite um nome para o waypoint (ex: "Entrada da Cave")
4. Clique **"➕ Adicionar Waypoint"**
5. Repita para outros locais

### 6.2 - Configurar Movimento
1. Escolha o modo de movimento:
   - **🔄 Loop Contínuo**: Anda infinitamente pelos waypoints
   - **↔️ Ida e Volta**: Vai até o final e volta
   - **1️⃣ Uma Vez**: Passa por todos apenas uma vez

2. Marque **"🚶 Ativar Auto Walk"** se quiser que o bot ande

---

## 🎯 **PASSO 7: Usar o Bot**

### 7.1 - Preparar o Jogo
1. **Abra o Tibia**
2. **Entre com seu personagem**
3. **Posicione-se** no local onde quer que o bot atue
4. **Minimize o jogo** (deixe visível, mas pode minimizar)

### 7.2 - Iniciar o Bot
1. **Na interface web**, clique **"▶️ Iniciar"**
2. **O bot vai começar** a funcionar automaticamente
3. **Você pode acompanhar** as estatísticas em tempo real

### 7.3 - Controlar o Bot
- **⏸️ Pausar**: Para temporariamente o bot
- **⏹️ Parar**: Para completamente o bot
- **Estatísticas**: Veja tempo rodando, curas usadas, ataques, etc.

---

## 📊 **PASSO 8: Monitorar o Bot**

### 8.1 - Dashboard em Tempo Real
A interface mostra:
- ⏱️ **Tempo Ativo**: Há quanto tempo o bot está rodando
- 💚 **Curas**: Quantas vezes usou magia de cura
- ⚔️ **Ataques**: Quantos ataques fez
- 🏆 **Criaturas Mortas**: Quantos monstros matou
- 💰 **Itens Coletados**: Quantos itens pegou do chão

### 8.2 - Histórico de Sessões
1. Vá na aba **"📊 Sessões"**
2. Veja todas as sessões anteriores
3. Analise seu desempenho

---

## ⚠️ **DICAS IMPORTANTES**

### 🔒 **Segurança**
- ✅ Este bot é **indetectável** pois simula movimentos humanos
- ✅ Use delays realistas (não muito rápido)
- ✅ Não use 24 horas por dia
- ✅ Varie os horários de uso

### 🎮 **Gameplay**
- ✅ Configure **HP de emergência baixo** (10-15%) para logout automático
- ✅ Use **"Lootar Tudo e Filtrar"** se for conta Free
- ✅ Teste sempre em locais seguros primeiro
- ✅ Monitore as primeiras horas de uso

### 🔧 **Troubleshooting**
- ❌ **Bot não inicia**: Verifique se o Tibia está aberto
- ❌ **Não detecta HP/MP**: Aguarde, é simulado para teste
- ❌ **Interface não abre**: Tente http://localhost:3000
- ❌ **Erro de instalação**: Execute como administrador

---

## 🆘 **PROBLEMAS COMUNS**

### Problema: "Python não é reconhecido"
**Solução**: Reinstale o Python marcando "Add to PATH"

### Problema: "Node não é reconhecido"  
**Solução**: Reinstale o Node.js

### Problema: Bot não funciona no jogo
**Solução**: 
1. Certifique-se que o Tibia está na tela
2. Teste em modo janela (não fullscreen)
3. Configure as coordenadas corretas

### Problema: Interface não carrega
**Solução**:
1. Aguarde 1-2 minutos após iniciar
2. Tente atualizar a página
3. Verifique se ambos os serviços estão rodando

---

## 🎉 **PRONTO!**

Agora você tem um bot totalmente funcional e indetectável para Open Tibia!

**Lembre-se**:
- 🔄 Sempre salve suas configurações
- 📊 Monitore as estatísticas  
- ⚡ Use com responsabilidade
- 🎮 Divirta-se!

---

## 📞 **Suporte**

Se tiver dúvidas:
1. Releia este tutorial
2. Verifique a seção "Problemas Comuns"
3. Consulte os logs na janela preta
4. Entre em contato para suporte

**Bom jogo! 🏰⚔️**