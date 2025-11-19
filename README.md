# Sistema de Chat em Rede Local

Um sistema de chat cliente-servidor que funciona via rede local, desenvolvido em Python com interface gráfica intuitiva.

## 📋 Sobre o Projeto

Este projeto consiste em um servidor de chat centralizado e múltiplos clientes que se conectam via rede local. O sistema permite comunicação em tempo real entre usuários através de uma interface amigável.

## ✨ Características Principais

### 🏗️ Arquitetura
- **Cliente-Servidor** com comunicação via sockets TCP IPv4
- **Protocolo HTTP-like** para troca de mensagens
- **Interface gráfica** responsiva com Tkinter

### 🔄 Funcionalidades Avançadas
- **Thread de atualização** em background para receber mensagens sem bloquear a interface
- **Sistema de cadastro** de usuários por IP
- **Atualizações em tempo real** do chat
- **Interface responsiva** que se adapta a diferentes tamanhos de tela

### 🎨 Interface do Usuário
- **Molduras estilizadas** para mensagens (esquerda para recebidas, direita para enviadas)
- **Scroll automático** mantendo a posição de leitura
- **Layout responsivo** que escala conforme o tamanho da tela
- **Atalhos de teclado** (Enter para enviar, Shift+Enter para nova linha)

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado
- Todos os dispositivos na mesma rede local

### Executando o Servidor

1. Navegue até o diretório do projeto
2. Execute o servidor:
```bash
python LAN_chat_server.py
```

O servidor irá:
- Exibir o IP local onde está hospedado
- Iniciar na porta 8000
- Aguardar conexões de clientes

### Executando os Clientes

1. Em cada máquina cliente, execute:
```bash
python LAN_chat_client.py
```

2. Na tela de cadastro:
   - Insira o **IP do servidor** (ex: `192.168.1.100`)
   - Digite seu **nome de usuário**
   - Clique em "Confirmar" ou pressione Enter

3. Após o cadastro, você será redirecionado para a sala de chat

## 📡 Protocolo de Comunicação

O sistema utiliza um protocolo simples baseado em HTTP:

- **POST /cadastro** - Registrar usuário
- **POST /mensagem** - Enviar mensagem  
- **GET /n_atualizacoes** - Verificar novas mensagens
- **GET /chat** - Obter histórico completo

## 🛠️ Estrutura Técnica

### Servidor
- Gerencia usuários conectados
- Armazena histórico de mensagens
- Distribui atualizações para todos os clientes conectados

### Cliente
- **Thread principal**: Interface do usuário e envio de mensagens
- **Thread secundária**: Verificação periódica de atualizações
- **Sincronização**: Atualização segura da interface entre threads

## 💡 Dicas de Uso

- Certifique-se de que o firewall permite conexões na porta 8000
- Use IPs estáticos para facilitar as conexões
- O sistema é ideal para redes locais corporativas ou domésticas

## 🔧 Solução de Problemas

- **Conexão recusada**: Verifique se o servidor está rodando e o IP está correto
- **Mensagens não atualizam**: Confirme que as portas estão liberadas no firewall
- **Interface travada**: O cliente usa threads separadas para evitar bloqueios

---

Desenvolvido para comunicação eficiente em ambientes de rede local.
