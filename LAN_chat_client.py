import socket
import threading
import time
from tkinter import *
from tkinter import ttk
import ast
import textwrap
from datetime import datetime
import sys  # Adicione esta importação

# Função de setup
def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))    # DNS da google
            print(s.getsockname())
            return s.getsockname()[0]
    except:
        return "erro"

# Funções de formatação de mensagem
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
    
# Funções de envio de requisições 
def envia_cadastro(input_dic):
    host = input_dic['addr']
    nome = input_dic['nome']
    data = mensagem_cadastro(nome)
    data_encoded = data.encode()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,PORT))
        s.sendall(data_encoded)

        print("cadastro_enviado!")
   
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

# Funções de UI/UX
def criar_moldura_esquerda(mensagem, largura_maxima=50):
    """
    Cria moldura para mensagens recebidas (à esquerda)
    """
    linhas = mensagem.split('\n')
    linhas_formatadas = []
    
    for linha in linhas:
        linhas_quebradas = textwrap.wrap(linha, width=largura_maxima)
        linhas_formatadas.extend(linhas_quebradas)
    
    if not linhas_formatadas:
        return ""
    
    comprimento_maximo = max(len(linha) for linha in linhas_formatadas)
    largura_moldura = comprimento_maximo + 4
    
    moldura_superior = '╭' + '─' * (largura_moldura - 2) + '╮'
    moldura_inferior = '╰' + '─' * (largura_moldura - 2) + '╯'
    
    conteudo = []
    conteudo.append(moldura_superior)
    
    for linha in linhas_formatadas:
        espacos = ' ' * (comprimento_maximo - len(linha))
        conteudo.append(f'│ {linha}{espacos} │')
    
    conteudo.append(moldura_inferior)
    
    return '\n'.join(conteudo)

def criar_moldura_direita(mensagem, largura_maxima=50):
    """
    Cria moldura para mensagens enviadas (à direita)
    """
    linhas = mensagem.split('\n')
    linhas_formatadas = []
    
    for linha in linhas:
        linhas_quebradas = textwrap.wrap(linha, width=largura_maxima)
        linhas_formatadas.extend(linhas_quebradas)
    
    if not linhas_formatadas:
        return ""
    
    comprimento_maximo = max(len(linha) for linha in linhas_formatadas)
    largura_moldura = comprimento_maximo + 4
    
    moldura_superior = '╭' + '─' * (largura_moldura - 2) + '╮'
    moldura_inferior = '╰' + '─' * (largura_moldura - 2) + '╯'
    
    conteudo = []
    conteudo.append(moldura_superior)
    
    for linha in linhas_formatadas:
        espacos = ' ' * (comprimento_maximo - len(linha))
        conteudo.append(f'│ {linha}{espacos} │')
    
    conteudo.append(moldura_inferior)
    
    return '\n'.join(conteudo)

def formatar_chat_GUI(chat, meu_nome):
    """
    Formata o chat com mensagens à direita (enviadas) e esquerda (recebidas)
    """
    chat_formatado = ''
    
    for key in chat:
        mensagem_completa = chat[key]
        
        # Verifica se a mensagem é do usuário atual
        if mensagem_completa.startswith(meu_nome + ':'):
            # Mensagem enviada por mim - alinha à direita
            mensagem_sem_nome = mensagem_completa[len(meu_nome + ':'):].strip()
            mensagem_com_moldura = criar_moldura_direita(mensagem_sem_nome)
            
            # Adiciona alinhamento à direita com espaços
            linhas_moldura = mensagem_com_moldura.split('\n')
            comprimento_maximo = max(len(linha) for linha in linhas_moldura)
            
            for linha in linhas_moldura:
                espacos_esquerda = ' ' * (80 - comprimento_maximo)  # Ajuste conforme necessidade
                chat_formatado += espacos_esquerda + linha + '\n'
                
        else:
            # Mensagem recebida de outros - alinha à esquerda
            mensagem_com_moldura = criar_moldura_esquerda(mensagem_completa)
            chat_formatado += mensagem_com_moldura + '\n'
        
        # Adiciona uma linha em branco entre mensagens
        chat_formatado += '\n'
    
    return chat_formatado

def get_screen_size(root):
    """Obtém o tamanho da tela e retorna dimensões escaladas"""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Define tamanhos base para referência (para uma tela 1920x1080)
    base_width = 1920
    base_height = 1080
    
    # Calcula fatores de escala
    width_scale = screen_width / base_width
    height_scale = screen_height / base_height
    
    # Usa o menor fator de escala para manter proporções
    scale_factor = min(width_scale, height_scale)
    
    # Calcula dimensões escaladas
    scaled_width = int(800 * scale_factor)
    scaled_height = int(600 * scale_factor)
    
    return scaled_width, scaled_height, scale_factor


##################### THREAD

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

# -- MAIN DA THREAD --
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
            #print(f"Atualizações: {att_atual} (anterior: {att})")  # DEBUG
            
            if att_atual > att:
                att = att_atual
                chat = eval(solicita_chat(input_dic))
                print(f"Chat recebido: {chat}")  # DEBUG
                
                # Atualiza a GUI na thread principal
                if root.winfo_exists():
                    chat_definitivo = formatar_chat_GUI(chat, input_dic['nome'])
                    root.after(0, lambda: atualizar_chat(chat_text, chat_definitivo))
            
            time.sleep(0.5)
        except Exception as e:
            print(f"Erro na thread de atualização: {e}")
            time.sleep(1)

#####################     
        
# Interface Gráfica
def tela_cadastro(root, input_dic):    
    root.title("cadastro")
    
    # Variável para controlar se o cadastro foi concluído com sucesso
    cadastro_concluido = False
    
    # Obtém dimensões escaladas
    width, height, scale_factor = get_screen_size(root)
    
    # Centraliza a janela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(True, True)
    
    # Configura o que acontece quando o usuário fecha a janela
    def on_closing():
        nonlocal cadastro_concluido
        if not cadastro_concluido:
            print("Cadastro cancelado pelo usuário")
            root.destroy()
            # Encerra a aplicação completamente
            sys.exit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Configura o grid para ser responsivo
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=0)
    root.rowconfigure(3, weight=0)
    root.rowconfigure(4, weight=0)
    root.rowconfigure(5, weight=1)

    # Calcula font size escalado
    font_size = max(10, int(12 * scale_factor))
    padding_y = max(2, int(5 * scale_factor))
    padding_x = max(10, int(20 * scale_factor))

    # Widgets com configurações responsivas
    inserir_server_label = Label(root, text='Insira o endereço do servidor', font=("Arial", font_size))
    inserir_server_label.grid(column=0, row=0, pady=padding_y, padx=padding_x, sticky='ew')

    inserir_server_entry = Entry(root, font=("Arial", font_size))
    inserir_server_entry.grid(column=0, row=1, pady=padding_y, padx=padding_x, sticky='ew')
    inserir_server_entry.focus()

    inserir_nome_label = Label(root, text='Insira um nome', font=("Arial", font_size))
    inserir_nome_label.grid(column=0, row=2, pady=padding_y, padx=padding_x, sticky='ew')

    inserir_nome_entry = Entry(root, font=("Arial", font_size))
    inserir_nome_entry.grid(column=0, row=3, pady=padding_y, padx=padding_x, sticky='ew')

    def coletar_input(input_dic, root):
        nonlocal cadastro_concluido
        addr = inserir_server_entry.get()
        nome = inserir_nome_entry.get()
        input_dic['addr'] = addr
        input_dic['nome'] = nome
        
        print(input_dic['addr'])
        print(input_dic['nome'])
        
        # fazer checagem do formato e tenta conexão:
        try:
            envia_cadastro(input_dic)
            cadastro_concluido = True  # Marca que o cadastro foi concluído com sucesso
            root.destroy()
            return input_dic    
        except:
            print("erro de conexão")
        
    confirmar_button = Button(root, text='Confirmar', 
                            command=lambda: coletar_input(input_dic, root),
                            font=("Arial", font_size))
    confirmar_button.grid(column=0, row=4, pady=padding_y*2, padx=padding_x, sticky='ew')
    
    root.bind('<Return>', lambda event: coletar_input(input_dic, root))
    
    root.mainloop()

def tela_chat(root, input_dic):
    root.title("chat")
    
    # Obtém dimensões escaladas
    width, height, scale_factor = get_screen_size(root)
    
    # Ajusta para a tela de chat ser maior
    width = int(width * 1.5)
    height = int(height * 1.2)
    
    # Centraliza a janela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(True, True)

    # Configura o grid para ser responsivo
    root.rowconfigure(0, weight=1)  # Área do chat
    root.rowconfigure(1, weight=0)  # Área de input
    root.columnconfigure(0, weight=3)  # Campo de texto
    root.columnconfigure(1, weight=1)  # Botão enviar

    # Calcula font size e padding escalados
    font_size = max(10, int(12 * scale_factor))
    padding_y = max(5, int(10 * scale_factor))
    padding_x = max(10, int(20 * scale_factor))

    # Cria um frame para o chat com scrollbar
    chat_frame = Frame(root)
    chat_frame.grid(column=0, row=0, columnspan=2, sticky='nsew', pady=padding_y, padx=padding_x)
    chat_frame.columnconfigure(0, weight=1)
    chat_frame.rowconfigure(0, weight=1)

    # Cria um campo de Text para imprimir as mensagens do chat com scrollbar
    # Usa fonte monoespaçada para manter o alinhamento das molduras
    chat_text = Text(chat_frame, state='disabled', font=("Courier New", font_size-1), 
                    bg='#f5f5f5', relief='sunken', padx=10, pady=10)
    chat_text.grid(column=0, row=0, sticky='nsew')

    # Adiciona scrollbar ao chat
    scrollbar = Scrollbar(chat_frame, orient=VERTICAL, command=chat_text.yview)
    scrollbar.grid(column=1, row=0, sticky='ns')
    chat_text.config(yscrollcommand=scrollbar.set)

    # Frame para área de input
    input_frame = Frame(root)
    input_frame.grid(column=0, row=1, columnspan=2, sticky='nsew', pady=padding_y, padx=padding_x)
    input_frame.columnconfigure(0, weight=3)
    input_frame.columnconfigure(1, weight=1)
    input_frame.rowconfigure(0, weight=1)

    # Cria o entry para input de mensagens
    input_dicentry = Text(input_frame, height=3, font=("Arial", font_size))
    input_dicentry.grid(column=0, row=0, sticky='nsew', pady=5, padx=(0, 10))

    # Cria um botão para enviar a mensagem
    chat_button = Button(input_frame, text='Enviar', 
                        command=lambda: envia_mensagem_gui(input_dicentry, input_dic),
                        font=("Arial", font_size))
    chat_button.grid(column=1, row=0, sticky='nsew')

    input_dicentry.focus()

    # Configura bindings
    def on_enter_press(event):
        envia_mensagem_gui(input_dicentry, input_dic)
        return "break"  # Previne quebra de linha extra

    input_dicentry.bind('<Return>', on_enter_press)
    input_dicentry.bind('<Shift-Return>', lambda e: input_dicentry.insert(END, '\n'))

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
    # setup:
    input_dic = {'addr':'', 'nome':''}
    PORT = 8000
    local_ip = get_local_ip()
    att = 0
    
    # execução grafica
    root = Tk()
    tela_cadastro(root, input_dic)
    
    # Só abre a tela de chat se o cadastro foi preenchido
    if input_dic['addr'] and input_dic['nome']:
        new_root = Tk()
        tela_chat(new_root, input_dic)
    
    print(input_dic)
