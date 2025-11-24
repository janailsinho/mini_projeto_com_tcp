# Chat Multiusuário com Sockets TCP (Equipe 11)

Este projeto consiste na implementação de um sistema de chat cliente-servidor utilizando **Sockets TCP**. O sistema permite que múltiplos clientes se conectem a uma sala única, troquem mensagens em tempo real e visualizem o histórico recente de conversas ao entrar.

O projeto foi desenvolvido para a disciplina CIN0143, atendendo aos requisitos de conexão persistente e confiabilidade nativa do protocolo TCP.

## 📋 Funcionalidades

* **Conexão TCP Persistente:** Mantém um canal de comunicação estável e confiável entre o cliente e o servidor.
* **Broadcast de Mensagens:** O servidor retransmite imediatamente qualquer mensagem válida recebida de um cliente para todos os outros usuários conectados.
* **Histórico de Mensagens (Buffer):** O servidor armazena em memória as últimas `N` mensagens enviadas (configurável). Quando um novo usuário se conecta, ele recebe esse histórico completo antes de começar a ver novas mensagens.
* **Protocolo de Aplicação:** Implementação manual de comandos específicos para conexão, envio e encerramento (`CONNECT`, `SEND`, `DISCONNECT`).

## 📂 Estrutura do Projeto

* `servidor.py`: Gerencia o socket principal, aceita conexões, cria *threads* para cada cliente, mantém o buffer de histórico e realiza o *broadcast*.
* `cliente.py`: Interface que conecta ao servidor TCP e permite ao usuário digitar os comandos do protocolo manualmente.
* `commands.py`: Definição das constantes dos comandos do protocolo.
* `utils.py`: Utilitários para coloração e formatação no terminal.

## 🚀 Como Executar

Certifique-se de ter o **Python 3** instalado.

###  Iniciando o Servidor e o Cliente
Abra um terminal na pasta do projeto e execute:

```bash
python servidor.py

O servidor iniciará na porta 5000 e aguardará conexões.

  Iniciando o Servidor

Iniciando um Cliente
Abra um novo terminal (para cada usuário) e execute:

python cliente.py

Após conectar, utilize os comandos descritos abaixo para interagir.

📡 Uso do Protocolo
O chat funciona através de comandos textuais que devem ser digitados explicitamente pelo usuário para demonstrar o funcionamento do protocolo:

Ação	Comando a digitar	Descrição
Entrar na Sala	CONNECT <seu_nome>	
Registra seu usuário e baixa o histórico de mensagens.


Ex: CONNECT Jose

Enviar Mensagem	SEND <mensagem>	
Envia uma mensagem para todos na sala.


Ex: SEND Olá pessoal!

Sair	DISCONNECT	Encerra a conexão e fecha o programa.

⚙️ Configurações
No arquivo servidor.py, você pode ajustar:

HOST: IP do servidor (Padrão: 'localhost').

PORT: Porta (Padrão: 5000).

HISTORY_SIZE: Quantidade de mensagens salvas no histórico (Padrão: 100).

👥 Autores - Equipe 11

Jorge Guilherme
José Janailson
Kleberson de Araujo Bezerra
Lucas dos Santos da Silva
Sofia Ribeiro de Santana





