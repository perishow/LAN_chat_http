import socket
import threading
import time

def get_local_ip():
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect(("8.8.8.8", 80))	# DNS da google
			print(s.getsockname())
			return s.getsockname()[0]
	except:
		return "erro"

PORT = 8000
host = 0

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
def envia_cadastro(nome):
	data = mensagem_cadastro(nome)
	data_encoded = data.encode()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)

		print("cadastro_enviado!")

# envia mensagem -------------------------------------------------------
def envia_mensagem(msg):
	data = mensagem_mensagem(msg)
	data_encoded = data.encode()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		print("mensagem enviada!")

# solicita n_atualizacoes ----------------------------------------------
def solicita_atualizacoes():
	data = mensagem_atualizacoes()
	data_encoded = data.encode()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		#print("solicitacao atualizacoes enviada!")
		att = s.recv(1024)
		att_decoded = att.decode('utf-8')
		#print(f"atualizacoes recebidas : {att_decoded}")
		return int(att_decoded)

def solicita_atualizacoes_e_trata():
	att = 0
	while True:
		if not threading.main_thread().is_alive():
			print('solicita_atualizacoes_e_trata FINALIZADO')
			break
		att_atual = solicita_atualizacoes()
		if att_atual > att:
			att = att_atual
			chat = solicita_chat()
			print_chat_formatado(chat)
		#print('solicita_atualizacoes_e_trata')
		time.sleep(0.5)
	

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
		#print(f"chat recebido : {chat_decoded}")
		return chat_decoded
		
def print_chat_formatado(chat):
	chat_dic = eval(chat)
	half_bar = '-' * 12
	print(f'{half_bar} CHAT {half_bar}')
	for i in range(len(chat_dic)):
		 print(chat_dic[i])
	print("-" * 30)	
	
if __name__ == '__main__':
	#setup:
	att = 0
	host = input("Digite o endereço do servidor:\n>>")
	nome = input("Digite seu nome:\n>>")
	envia_cadastro(nome)
	
	att_thread = threading.Thread(target=solicita_atualizacoes_e_trata)
	att_thread.start()
	
	while True:
		msg = input("Digite uma mensagem:\n>>")
		if msg =='q':
			break
		else:
			envia_mensagem(msg)
	
	
