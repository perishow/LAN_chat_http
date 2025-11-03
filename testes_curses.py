import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time

message = 'hahaha'

def main(stdscr):
	stdscr.clear()
	stdscr.border()
	stdscr.addstr(1,1,"teste daora") # (row, collum, string)
	stdscr.refresh()
	stdscr.getch()

	altura, largura = stdscr.getmaxyx() 
	
	altura_new_win = int(altura/5)
	y_new_win = altura - altura_new_win - 1
	new_win = curses.newwin(altura_new_win,largura-2,y_new_win,1) # (altura, largura, y, x)
	new_win.box()
	#new_win.addstr(1,1,"JANELA de input")
	new_win.refresh()
	
	box = Textbox(new_win)
	box.edit()
	
	message = box.gather()
	
	stdscr.addstr(2,1,message)
	stdscr.getch()
	
wrapper(main)

print(message)
