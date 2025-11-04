import socket
import threading
import time
from tkinter import *
from tkinter import ttk
import ast

def get_local_ip():
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.connect(("8.8.8.8", 80))	# DNS da google
			print(s.getsockname())
			return s.getsockname()[0]
	except:
		return "erro"

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
def envia_cadastro(input_dic):
	host = input_dic['addr']
	nome = input_dic['nome']
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
		
def envia_mensagem_gui(input_dicentry, input_dic):
	msg = input_dicentry.get('1.0', END)
	input_dicentry.delete('1.0', 'end')
	
	host = input_dic['addr']
	data = mensagem_mensagem(msg)
	data_encoded = data.encode()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		print("mensagem enviada!")
		

# solicita n_atualizacoes ----------------------------------------------
def solicita_atualizacoes(input_dic):
	host = input_dic['addr']
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

def formatar_chat_GUI(chat):
	chat_formatado = ''
	for key in chat:
		msg = chat[key]
		chat_formatado += f'{msg}\n------------------------------------------------------------------------------------------\n'
		
	return chat_formatado
	
def solicita_atualizacoes_e_trata_GUI(chat_text, input_dic, root):
	print("Thread de atualização iniciada!")
	att = 0
	while True:
		try:
			# Verifica se a janela principal ainda existe
			if not root.winfo_exists():
				print('Janela fechada, finalizando thread')
				break
				
			att_atual = solicita_atualizacoes(input_dic)
			print(f"Atualizações: {att_atual} (anterior: {att})")  # DEBUG
			
			if att_atual > att:
				att = att_atual
				chat = eval(solicita_chat(input_dic))
				print(f"Chat recebido: {chat}")  # DEBUG
				
				# Atualiza a GUI na thread principal
				if root.winfo_exists():
					chat_definitivo = formatar_chat_GUI(chat)
					root.after(0, lambda: atualizar_chat(chat_text, chat_definitivo))
			
			time.sleep(0.5)
		except Exception as e:
			print(f"Erro na thread de atualização: {e}")
			time.sleep(1)
			
def atualizar_chat(chat_text, novo_conteudo):
    # Salva a posição atual do scroll
    scroll_pos = chat_text.yview()
    
    # Atualiza o conteúdo
    chat_text.config(state='normal')
    chat_text.delete('1.0', 'end')
    chat_text.insert('end', novo_conteudo)
    chat_text.config(state='disabled')
    
    # Determina se deve scrollar para o final
    estava_no_final = scroll_pos[1] >= 0.99
    
    if estava_no_final:
        chat_text.see('end')
    else:
        # Restaura a posição anterior
        chat_text.yview_moveto(scroll_pos[0])

# solicita o chat atualizado ------------------------------------------
def solicita_chat(input_dic):
	
	host = input_dic['addr']
	data = mensagem_chat()
	data_encoded = data.encode()
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((host,PORT))
		s.sendall(data_encoded)
		#print("solicitacao chat enviada!")
		chat = s.recv(1024)
		chat_decoded = chat.decode('utf-8')
		#print(f"chat recebido : {chat_decoded}")
		return chat_decoded
		
def print_chat_formatado(chat):
	chat_dic = ast.literal_eval(chat)
	half_bar = '-' * 12
	print(f'{half_bar} CHAT {half_bar}')
	for i in range(len(chat_dic)):
		 print(chat_dic[i])
	print("-" * 30)	
	
def tela_cadastro(root, input_dic):	
	root.title("cadastro")
	root.geometry("600x400+0+0") # largura x altura +-x +- y

	inserir_server_label = Label(root, text='Insira o endereço do servidor')
	inserir_server_label.pack(pady=2)

	inserir_server_entry = Entry(root)
	inserir_server_entry.pack(pady=5)
	inserir_server_entry.focus()

	inserir_nome_label = Label (root, text='Insira um nome')
	inserir_nome_label.pack(pady=2)

	inserir_nome_entry = Entry(root)
	inserir_nome_entry.pack(pady=5)
	

	
	def coletar_input(input_dic, root):
		addr = inserir_server_entry.get()
		nome = inserir_nome_entry.get()
		input_dic['addr'] = addr
		input_dic['nome'] = nome
		
		print(input_dic['addr'])
		print(input_dic['nome'])
		
		# fazer checagem do formato e tenta conexão:
		try:
			envia_cadastro(input_dic)	
			root.destroy()
			return input
		#ESSA PARTE NÃO ESTÁ FUNCIONANDO	
		except:
			print("erro de conexão")
		
	confirmar_button = Button(root, text='Confirmar', command = lambda: coletar_input(input_dic, root))
	confirmar_button.pack(pady = 5)
	
	confirmar_button.bind('<Return>', lambda event: coletar_input(input_dic, root))
	
	root.mainloop()

def tela_chat(root, input_dic):
	root.title("chat")
	root.geometry("1500x1000") # largura x altura +-x +- y
	root.resizable(False, False)

	#configura o grid
	root.rowconfigure(0, weight=1)
	root.rowconfigure(1, weight=20)
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=1)

	# cria um campo de Text para imprimir as mensagens do chat
	chat_text = Text(root, state='disabled')
	chat_text.grid(column=0, row=0, columnspan=2, sticky='nsew', pady=25, padx=25)


	# cria o entry para input de mensagens
	input_dicentry = Text(root,height= 3)
	input_dicentry.grid(column=0, row=1, sticky='nsew', pady=10, padx = 25)

	# cria um botão para enviar a mensagem
	chat_button = Button(root, text='enviar',command = lambda: envia_mensagem_gui(input_dicentry, input_dic))
	chat_button.grid(column=1, row=1,sticky='nsew', pady=10, padx=25)
	chat_button.bind('<Return>', lambda event: envia_mensagem_gui(input_dicentry, input_dic))
	input_dicentry.focus()

	# INICIA A THREAD ANTES do mainloop() e passa a referência do root
	att_thread = threading.Thread(
		target=solicita_atualizacoes_e_trata_GUI, 
		args=(chat_text, input_dic, root),
		daemon=True
	)
	att_thread.start()
	print("Thread iniciada antes do mainloop!")

	root.mainloop()

if __name__ == '__main__':
	#setup:
	input_dic = {'addr':'', 'nome':''}
	PORT = 8000
	local_ip = get_local_ip()
	att = 0
	
	# execução grafica
	root = Tk()
	tela_cadastro(root, input_dic)
	
	new_root = Tk()
	tela_chat(new_root, input_dic)
	
	print(input_dic)
#	host = input("Digite o endereço do servidor:\n>>")
#	nome = input("Digite seu nome:\n>>")
#	envia_cadastro(nome)
#	
#	att_thread = threading.Thread(target=solicita_atualizacoes_e_trata)
#	att_thread.start()
#	
#	while True:
#		msg = input("Digite uma mensagem:\n>>")
#		if msg =='q':
#			break
#		else:
#			envia_mensagem(msg)
#	
	
