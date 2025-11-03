import socket

# ==== DEFINIÇÃO DE FUNÇÕES ====

def get_local_ip():
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect(("8.8.8.8", 80))	# DNS da google
			print(s.getsockname())
			return s.getsockname()[0]
	except:
		return "erro"

def cadastrar_nome(ip, msg, usuarios):
	nome = msg.split()[7]
	usuarios[ip] = nome
	
def enviar_atualizacoes(sock, n_atualizacoes):
	att_encoded = str(n_atualizacoes).encode()
	sock.sendall(att_encoded)
	
def enviar_chat(sock, chat):
	chat_encoded = str(chat).encode()
	sock.sendall(chat_encoded)

def adicionar_mensagem(chat, n_att, msg, ip, usuarios):
	# formatar mensagem
	n_att +=  1
	usuario = usuarios[ip]
	mensagem = msg.split()[7]
	msg_formatada = f"{usuario}: {mensagem}"
	chat[n_atualizações] = msg_formatada
	print(n_atualizações)
	return n_att
	
# ==== SETUP ====
		
ADDR = get_local_ip()
PORT = 8000

# ==== ESTRUTURA DE DADOS ====

usuarios = {"ip_exemplo" : "nome"}
chat = {0:"msg inicial"} # {int: string}
n_atualizações = 0

#==== LOOP DE EXECUÇÃO ====

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((ADDR, PORT))
		s.listen(5)
		print(f'servidor funcionando em {ADDR}:{PORT}')
		while n_atualizações < 4:	
			new_sock, addr = s.accept()
			data = new_sock.recv(1024)
			data_utf = data.decode('utf-8')
			data_splitted = data_utf.split()
			
			ip, _ = addr
			#----------------------
			if data_splitted[0] == 'POST':
				if data_splitted[1] == '/cadastro':
					cadastrar_nome(ip, data_utf, usuarios)
					print('usuario_cadastrado')
					print(usuarios)
				if data_splitted[1] == '/mensagem':
					n_atualizações = adicionar_mensagem(chat, n_atualizações, data_utf,ip ,usuarios)
					print("mensagem adicionada")
					print(chat)
			if data_splitted[0] == 'GET':
				print(data_splitted)
				if data_splitted[1] == '/n_atualizacoes':
					print('entrou nas atualizacoes')
					enviar_atualizacoes(new_sock, n_atualizações)
				if data_splitted[1] == '/chat':
					print('entrou no if chat')
					enviar_chat(new_sock, chat)
			# ---------------------
			
			print(chat)
except Exception as e:
	print(f"erro: {e}")
