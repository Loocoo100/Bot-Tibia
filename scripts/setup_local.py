#!/usr/bin/env python3
"""
Script de configuração local para OT Cavebot
Prepara o ambiente para execução local no Windows
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

def print_header():
    print("=" * 50)
    print("    OT CAVEBOT - CONFIGURAÇÃO LOCAL")
    print("=" * 50)
    print()

def check_requirements():
    """Verifica se os pré-requisitos estão instalados"""
    print("Verificando pré-requisitos...")
    
    requirements = {
        'python': 'Python',
        'node': 'Node.js',
        'git': 'Git'
    }
    
    missing = []
    
    for cmd, name in requirements.items():
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            print(f"✅ {name} encontrado")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name} NÃO encontrado")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  ERRO: Faltam os seguintes programas: {', '.join(missing)}")
        print("\nPor favor, instale-os primeiro:")
        print("- Python: https://www.python.org/downloads/")
        print("- Node.js: https://nodejs.org/")
        print("- Git: https://git-scm.com/download/win")
        return False
    
    print("\n✅ Todos os pré-requisitos encontrados!")
    return True

def setup_directories():
    """Cria diretórios necessários"""
    print("\nCriando diretórios...")
    
    dirs = ['data', 'logs', 'config', 'scripts']
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Diretório {dir_name} criado/verificado")

def create_env_files():
    """Cria arquivos de configuração .env"""
    print("\nCriando arquivos de configuração...")
    
    # Backend .env
    backend_env = """MONGO_URL=mongodb://localhost:27017
DB_NAME=otbot_database
ENVIRONMENT=local
DEBUG=true
"""
    
    backend_env_path = Path('backend/.env')
    backend_env_path.parent.mkdir(exist_ok=True)
    
    with open(backend_env_path, 'w') as f:
        f.write(backend_env)
    print("✅ Configuração do backend criada")
    
    # Frontend .env
    frontend_env = """REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_ENVIRONMENT=local
GENERATE_SOURCEMAP=false
"""
    
    frontend_env_path = Path('frontend/.env')
    frontend_env_path.parent.mkdir(exist_ok=True)
    
    with open(frontend_env_path, 'w') as f:
        f.write(frontend_env)
    print("✅ Configuração do frontend criada")

def install_dependencies():
    """Instala dependências do Python e Node.js"""
    print("\nInstalando dependências...")
    
    # Python dependencies
    print("Instalando dependências do Python...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'
        ], check=True, cwd=os.getcwd())
        print("✅ Dependências Python instaladas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências Python: {e}")
        return False
    
    # Node.js dependencies
    print("Instalando dependências do Node.js...")
    try:
        subprocess.run(['npm', 'install'], check=True, cwd='frontend')
        print("✅ Dependências Node.js instaladas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências Node.js: {e}")
        return False
    
    return True

def create_startup_scripts():
    """Cria scripts de inicialização personalizados"""
    print("\nCriando scripts de inicialização...")
    
    # Script para iniciar apenas o backend
    backend_only = """@echo off
title OT Cavebot - Backend
echo Iniciando apenas o backend...
cd backend
python server.py
pause
"""
    
    with open('EXECUTAR_APENAS_BACKEND.bat', 'w', encoding='utf-8') as f:
        f.write(backend_only)
    
    # Script para iniciar apenas o frontend
    frontend_only = """@echo off
title OT Cavebot - Frontend
echo Iniciando apenas o frontend...
cd frontend
npm start
pause
"""
    
    with open('EXECUTAR_APENAS_FRONTEND.bat', 'w', encoding='utf-8') as f:
        f.write(frontend_only)
    
    print("✅ Scripts de inicialização criados")

def save_config():
    """Salva configurações locais"""
    config = {
        "setup_completed": True,
        "version": "1.0.0",
        "local_mode": True,
        "installation_date": str(Path().absolute()),
        "features": {
            "local_database": True,
            "auto_updates": False,
            "telemetry": False
        }
    }
    
    with open('config/setup.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuração salva")

def main():
    print_header()
    
    if not check_requirements():
        input("\nPressione Enter para sair...")
        return 1
    
    setup_directories()
    create_env_files()
    
    if not install_dependencies():
        input("\nPressione Enter para sair...")
        return 1
    
    create_startup_scripts()
    save_config()
    
    print("\n" + "=" * 50)
    print("         CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print("\n🎉 O OT Cavebot foi configurado com sucesso!")
    print("\nPRÓXIMOS PASSOS:")
    print("1. Execute EXECUTAR_BOT.bat para iniciar")
    print("2. Abra http://localhost:3000 no navegador")
    print("3. Configure o bot e divirta-se!")
    print("\nLeia o TUTORIAL_INSTALACAO.md para mais detalhes.")
    
    input("\nPressione Enter para continuar...")
    return 0

if __name__ == "__main__":
    sys.exit(main())