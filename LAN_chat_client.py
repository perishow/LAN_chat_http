import socket

def get_local_ip():
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect(("8.8.8.8", 80))	# DNS da google
			print(s.getsockname())
			return s.getsockname()[0]
	except:
		return "erro"

PORT = 8000
host = input("digite o endereço:")

local_ip = get_local_ip()

def mensagem_cadastro(nome):
	tamanho_nome = len(nome)
	data = (
		f'POST /cadastro HTTP/1.1\r\n'
		f'Content-Type: String_encoded\r\n'
		f'Content-Length: {tamanho_nome}\r\n\r\n'
		f'{nome}'
		)
	return data
	
def mensagem_mensagem(msg):
	tamanho_msg = len(msg)
	data = (
	f'POST /mensagem HTTP/1.1\r\n'
	f'Content-Type: String_encoded\r\n'
	f'Content-Length: {tamanho_msg}\r\n\r\n'
	f'{msg}'
	)
	return data

def mensagem_atualizacoes():
	data = (
	f'GET /n_atualizacoes HTTP/1.1\r\n'
	)
	return data

def mensagem_chat():
	data = (
	f'GET /chat HTTP/1.1\r\n'
	)
	return data
	
# cadastra -------------------------------------------------------
nome = input("digite um nome: ")
def envia_cadastro(nome):
	data = mensagem_cadastro(nome)
	data_encoded = data.encode()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)

		print("cadastro_enviado!")
envia_cadastro(nome)

# envia mensagem -------------------------------------------------------
	
msg = input("mande uma mensagem: ")
def envia_mensagem(msg):
	data = mensagem_mensagem(msg)
	data_encoded = data.encode()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		print("mensagem enviada!")
envia_mensagem(msg)

# solicita n_atualizacoes ----------------------------------------------

def solicita_atualizacoes():
	data = mensagem_atualizacoes()
	data_encoded = data.encode()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		print("solicitacao atualizacoes enviada!")
		att = s.recv(1024)
		att_decoded = att.decode('utf-8')
		print(f"atualizacoes recebidas : {att_decoded}")

solicita_atualizacoes()
 
# solicita o chat atualizado ------------------------------------------
def solicita_chat():
	data = mensagem_chat()
	data_encoded = data.encode()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		print("solicitacao chat enviada!")
		chat = s.recv(1024)
		chat_decoded = chat.decode('utf-8')
		print(f"chat recebido : {chat_decoded}")
		
solicita_chat()
	
