# 6p priv - Otimizador do Sistema Windows

Ferramenta de otimização para Windows com interface gráfica, proteção por senha e múltiplas funções de performance.

## 🔐 Acesso
- **Senha:** `clientpriv`
- Requer execução como **Administrador** (o programa solicita elevação automaticamente)

## 🚀 Funcionalidades

### CPU / RAM / GPU Boost
- ✅ Ativa plano de energia **Alto Desempenho**
- ✅ Define prioridade **HIGH** para o processo
- ✅ Otimiza **afinidade de CPU** (reserva Core 0 para sistema)
- ✅ Desativa **CPU Parking** (evita cores estacionados)
- ✅ Ativa **agendamento GPU por hardware** (Windows 10 2004+)
- ✅ Configura **prioridade GPU alta**
- ✅ Otimiza **gerenciamento de memória** (LargeSystemCache, DisablePagingExecutive)
- ✅ Limpa **memória standby** (Working Set)

### Otimizações de Registro
- 📝 Desativar Telemetria Windows
- 📝 Desativar Hibernação
- 📝 Desativar Prefetch/Superfetch (ideal para SSD)
- 📝 Acelerar Menu Iniciar (delay = 0)
- 📝 Desativar Animações
- 📝 Desativar Efeitos Visuais (modo performance)
- 📝 Aumentar Prioridade I/O
- 📝 Desativar Índice de Pesquisa (WSearch)
- 📝 Desativar SysMain (Superfetch service)
- 📝 Otimizar TCP/IP (reduz latência)

### Limpeza de Sistema
- 🗑️ Temp do Usuário (`%TEMP%`)
- 🗑️ Temp do Windows (`C:\Windows\Temp`)
- 🗑️ Prefetch
- 🗑️ Cache Windows Update
- 🗑️ Relatórios de Erro (WER)
- 🗑️ Logs de Instalação
- 🗑️ Cache de Miniaturas
- 🗑️ Cache Navegadores (Edge/Chrome)
- 🗑️ Lixeira

### Ferramentas Rápidas (Atalhos)
- 🛡️ Abrir **Windows Security** (antivírus nativo)
- 🔧 **SFC /scannow** - Verifica arquivos do sistema
- 🔧 **DISM RestoreHealth** - Repara imagem Windows
- 💾 **Limpeza de Disco** (cleanmgr)
- 📊 **Sensor de Armazenamento**
- 🔧 **Otimizar Unidades** (Desfragmentar/Trim)
- 🌐 **Limpar Cache DNS**
- 📋 **Limpar Logs de Eventos**
- 📱 **Desativar Modo Tablet**

## 📦 Instalação e Uso

### Opção 1: Executar direto (Python)
```bash
# 1. Instale dependências
pip install -r requirements.txt

# 2. Execute como Administrador
python main.py
```

### Opção 2: Compilar para .exe (Recomendado)
```bash
# Instala PyInstaller se necessário
pip install pyinstaller

# Compila
python build.py

# Ou usando o .spec diretamente
pyinstaller 6p_priv.spec
```
O executável será gerado em `dist/6p_priv.exe`

### Opção 3: Build com .spec (mais controle)
```bash
pyinstaller 6p_priv.spec
```

## ⚙️ Requisitos
- **Windows 10/11** (64-bit)
- **Python 3.8+** (para desenvolvimento)
- **Privilégios de Administrador** (obrigatório)
- ~50 MB espaço em disco

## ⚠️ Avisos Importantes

1. **Execute SEMPRE como Administrador** - A maioria das otimizações requer elevação
2. **Crie um ponto de restauração** antes de aplicar tweaks de registro
3. **Algumas alterações exigem reinicialização** para ter efeito
4. **Não desative antivírus** - O botão "Windows Security" abre o painel nativo para você gerenciar
5. **Use por sua conta e risco** - Modificações no registro podem afetar a estabilidade

## 🎨 Personalização

### Alterar senha
Edite `main.py`:
```python
login = LoginWindow(root, password="sua_nova_senha", on_success=lambda: start_app(root))
```

### Adicionar ícone personalizado
Coloque `icon.ico` na pasta do projeto e recompile.

### Modificar tweaks de registro
Edite `optimizer.py` - dicionário `REGISTRY_TWEAKS`

### Adicionar pastas de limpeza
Edite `optimizer.py` - dicionário `CLEANUP_PATHS`

## 📁 Estrutura do Projeto
```
6p_priv/
├── main.py           # Ponto de entrada
├── login.py          # Tela de senha
├── optimizer.py      # Lógica de otimização
├── gui.py            # Interface gráfica
├── build.py          # Script de compilação
├── 6p_priv.spec      # Config PyInstaller
├── requirements.txt  # Dependências
├── README.md         # Este arquivo
└── icon.ico          # Ícone (opcional)
```

## 🛠️ Tecnologias
- **Python 3** + **Tkinter** (GUI nativa, sem dependências extras)
- **psutil** - Informações de sistema/processos
- **winreg** - Manipulação de registro Windows
- **ctypes** - APIs nativas do Windows
- **PyInstaller** - Compilação para .exe standalone

## 📄 Licença
Uso pessoal/educacional. Modifique conforme necessário.

---

**Desenvolvido para otimização de performance em Windows** ⚡