from tkinter import *
from tkinter import ttk

def tela_cadastro(root, input_):	
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
	

	
	def coletar_input(input_):
		addr = inserir_server_entry.get()
		nome = inserir_nome_entry.get()
		input_['addr'] = addr
		input_['nome'] = nome
		
		print(input_['addr'])
		print(input_['nome'])
		
		return input
	
	confirmar_button = Button(root, text='Confirmar', command = lambda: coletar_input(input_))
	confirmar_button.pack(pady = 5)
	
	exit_button = Button(root, text='sair', command = lambda: root.quit())
	exit_button.pack(pady = 5)
	
	root.mainloop()

def tela_chat(root):
	root.title("chat")
	root.geometry("1500x1000") # largura x altura +-x +- y
	root.resizable(False, False)
	
	#configura o grid
	root.rowconfigure(0, weight=1)
	root.rowconfigure(1, weight=20)
	root.columnconfigure(0, weight=1)
	root.columnconfigure(1, weight=1)
	
	# cria o entry para input de mensagens
	input_entry = Text(root,height= 3)
	input_entry.grid(column=0, row=1, sticky='nsew', pady=10, padx = 25)
	
	# cria um campo de Text para imprimir as mensagens do chat
	chat_text = Text(root, state='disabled')
	chat_text.grid(column=0, row=0, columnspan=2, sticky='nsew', pady=25, padx=25)
	
	def escreve_msg(input_entry, chat_text):
	
		msg = input_entry.get('1.0', END)
		input_entry.delete('1.0', 'end')
		chat_text.config(state='normal')
		chat_text.delete('1.0', 'end')
		
		chat_text.insert(
			index = '1.0',
			chars= f'{msg}\n'
		)
		chat_text.config(state='disabled')
	
	# cria um botão para enviar a mensagem
	chat_button = Button(root, text='enviar',command = lambda: escreve_msg(input_entry, chat_text))
	chat_button.grid(column=1, row=1,sticky='nsew', pady=10, padx=25)
	
	input_entry.focus()
	root.mainloop()

input_ = {'addr': '', 'nome': ''}

root = Tk()
tela_chat(root)
#tela_cadastro(root,input_) # tela que coleta ip do servidor e nome do usuario



