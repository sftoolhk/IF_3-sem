import sys
import os
import random
import time
import curses

# janela principal
screen = curses.initscr()
screen.notimeout(False)
screen.keypad(True)
screen.clear()
#screen.set_title('T O R R E S   D E   H A N O I')

# iniciando cores
curses.start_color()
curses.init_pair( 1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair( 2, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair( 3, curses.COLOR_YELLOW, curses.COLOR_WHITE)
curses.init_pair( 4, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair( 5, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
curses.init_pair( 6, curses.COLOR_CYAN, curses.COLOR_WHITE)
curses.init_pair( 7, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair( 8, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair( 9, curses.COLOR_YELLOW, curses.COLOR_WHITE)
curses.init_pair(10, curses.COLOR_MAGENTA, curses.COLOR_WHITE)

# Define cor das Colunas e da Base da Torre (azul e branco)
curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_WHITE)

# Define cor da Barra de Status (branco e cyan)
curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_CYAN)

curses.init_pair(13, curses.COLOR_GREEN, curses.COLOR_WHITE)

curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_WHITE)
curses.init_pair(15, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(16, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(17, curses.COLOR_BLACK, curses.COLOR_BLUE)
curses.init_pair(18, curses.COLOR_BLACK, curses.COLOR_WHITE)

curses.cbreak()

# Não retorna caracteres na tela
curses.noecho()

# esconde o cursor do mouse e do terminal
curses.curs_set(0)

# Define Constantes
K_CTRL_Q = 17
K_ESC    = 27
K_F1     = 59  # Win
K_1      = 49
K_2      = 50
K_3      = 51
N_DISCOS = 10
PG_CODE  = 9440

# Define Constantes usadas como caracteres especiais
# Single-line
# Chr( 218 ) + Chr( 196 ) + Chr( 191 ) &#9484; &#9472; &#9488;
# Chr( 179 ) + Chr(  32 ) + Chr( 179 ) &#9474;   &#9474;
# Chr( 192 ) + Chr( 196 ) + Chr( 217 ) &#9492; &#9472; &#9496;

c_032 =   32
c_168 = 9608
c_177 = 9617
c_178 = 9618
c_179 = 9474
c_191 = 9488
c_192 = 9492
c_196 = 9472
c_217 = 9496
c_218 = 9484
c_219 = 9604
c_223 = 9600

# Determina a posicao inicial da torre que contera os discos de forma aleatoria
pos_0 = random.randint( 1, 3 )
pos_1 = 2 if pos_0 == 1 else 1
pos_2 = 2 if pos_0 == 3 else 3

TORRE = {}
TORRE[pos_0] = [1,2,3,4,5,6,7,8,9,10]
TORRE[pos_1] = []
TORRE[pos_2] = []

COR = {}
#COR[pos_0] = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10]
COR[pos_0] = random.sample( range(1,11), 10)
COR[pos_1] = []
COR[pos_2] = []

def unichr(ch):
   return chr(ch)

def Hchr(strhex):
   '''
   Funcao para transformar uma cadeia de valores
   em hexadecimal para uma cadeia de caracteres
   '''
   STRING = ''

   for pos in strhex.split(','):
      i = int(pos, 16)
      
      if i < 128:
         STRING = STRING + unichr(i)
      else:
         STRING = STRING + unichr(i + PG_CODE)
         
   return (STRING) 

DISCO = {}
DISCO[ 1] = Hchr('20,20,20,20,20,20,20,20,20,B1,B2,B1,20,20,20,20,20,20,20,20,20')
DISCO[ 2] = Hchr('20,20,20,20,20,20,20,20,B1,B1,B2,B1,B1,20,20,20,20,20,20,20,20')
DISCO[ 3] = Hchr('20,20,20,20,20,20,20,B1,B1,B1,B2,B1,B1,B1,20,20,20,20,20,20,20')
DISCO[ 4] = Hchr('20,20,20,20,20,20,B1,B1,B1,B1,B2,B1,B1,B1,B1,20,20,20,20,20,20')
DISCO[ 5] = Hchr('20,20,20,20,20,B1,B1,B1,B1,B1,B2,B1,B1,B1,B1,B1,20,20,20,20,20')
DISCO[ 6] = Hchr('20,20,20,20,B1,B1,B1,B1,B1,B1,B2,B1,B1,B1,B1,B1,B1,20,20,20,20')
DISCO[ 7] = Hchr('20,20,20,B1,B1,B1,B1,B1,B1,B1,B2,B1,B1,B1,B1,B1,B1,B1,20,20,20')
DISCO[ 8] = Hchr('20,20,B1,B1,B1,B1,B1,B1,B1,B1,B2,B1,B1,B1,B1,B1,B1,B1,B1,20,20')
DISCO[ 9] = Hchr('20,B1,B1,B1,B1,B1,B1,B1,B1,B1,B2,B1,B1,B1,B1,B1,B1,B1,B1,B1,20')
DISCO[10] = Hchr('B1,B1,B1,B1,B1,B1,B1,B1,B1,B1,B2,B1,B1,B1,B1,B1,B1,B1,B1,B1,B1')

if 0:
   DISCO[ 1] = ('         #T#         ')
   DISCO[ 2] = ('        ##T##        ')
   DISCO[ 3] = ('       ###T###       ')
   DISCO[ 4] = ('      ####T####      ')
   DISCO[ 5] = ('     #####T#####     ')
   DISCO[ 6] = ('    ######T######    ')
   DISCO[ 7] = ('   #######T#######   ')
   DISCO[ 8] = ('  ########T########  ')
   DISCO[ 9] = (' #########T######### ')
   DISCO[10] = ('##########T##########')


def pause(tempo):
   # Atualiza a tela
   screen.refresh()

   # Pausa por um tempo
   time.sleep(tempo)

def Hprompt():

   while True:

      key = screen.getch()
      #curses.getmouse()
      
      '''
      if  key = K_LBUTTONUP // botao esquerdo pressionado

         // Verifica em que posicao foi pressionado
         if     TST_BOTAO(04,03,20,23)
            return 1

         elif TST_BOTAO(04,29,20,49)
            return 2

         elif TST_BOTAO(04,55,20,75)
            return 3

      '''

      if key in (K_ESC, K_CTRL_Q):
         # encerra o programa
         ENCERRA(True)

      elif key in (curses.KEY_F1, ord('h'), ord('H')):
         # help acionado
         autor()
         screen.addstr(24, 1, ' ' * 80, curses.color_pair(12))
         screen.addstr(24, 1, ' Tecle algo para sair...', curses.color_pair(12) | curses.A_BOLD)
         screen.getch()
         pause(.05)

         display_tela()
         return 0

      elif key == K_1:
         return 1

      elif key == K_2:
         return 2

      elif key == K_3:
         return 3


def bt_press(n_bt):
   '''
   desenha os botoes acionados
   n_bt = numero do botao
   '''
   screen.addstr(20, n_bt*26-15,  '{:^7}'.format(n_bt), curses.color_pair(14) | curses.A_BOLD)
   #screen.addstr(20, n_bt*26-15,  '{:^7}'.format(n_bt), curses.color_pair(1) | curses.A_BOLD)

   screen.addstr(20, n_bt*26-16, ' ', curses.color_pair(15))
   screen.addstr(21, n_bt*26-15, ' ' * 7, curses.color_pair(15))


def bt_solto(n_bt):
   '''
   desenha os botoes não acionados
   n_bt = numero do botao
   '''
   screen.addstr(20, n_bt*26-16, '{:^7}'.format(n_bt), curses.color_pair(16))
   #screen.addstr(20, n_bt*26-16, '{:^7}'.format(n_bt), curses.color_pair(3))

   screen.addstr(20, n_bt*26- 9, unichr(c_219), curses.color_pair(17))
   screen.addstr(21, n_bt*26-15, unichr(c_223) * 7, curses.color_pair(17))


def Box(lt,ce,lb,cd, cor):
   
   for x in range(lt,lb):
      screen.addstr(x, ce, ' ' * (cd-ce+1), curses.color_pair(cor))


def DispBox(lt,ce,lb,cd, cor):
   
   Box(lt,ce,lb,cd, cor)

   screen.addstr(lt, ce, unichr(c_196) * (cd-ce), curses.color_pair(cor))
   screen.addstr(lt, ce, unichr(c_218), curses.color_pair(cor))
   screen.addstr(lt, cd, unichr(c_191), curses.color_pair(cor))
   
   screen.addstr(lb, ce, unichr(c_196) * (cd-ce), curses.color_pair(cor))
   screen.addstr(lb, ce, unichr(c_192), curses.color_pair(cor))
   screen.addstr(lb, cd, unichr(c_217), curses.color_pair(cor))

   for x in range(lt+1,lb):
      screen.addstr(x, ce, unichr(c_179), curses.color_pair(cor))
      screen.addstr(x, cd, unichr(c_179), curses.color_pair(cor))


def DispBox_Shadow(lt,ce,lb,cd, cor):
   
   DispBox(lt,ce,lb,cd, cor)

   #Desenha a Sombra da Caixa
   for x in range(lt+1,lb+1):
      screen.addstr(x, cd+1, unichr(c_168), curses.color_pair(18))
   
   screen.addstr(lb+1, ce+1, unichr(c_168) * (cd-ce+1), curses.color_pair(18))


def display_tela():

   #Cria uma quadro na tela com char azul e fundo branco
   DispBox( 1,1,18,80, 11)

   #Escreve o titulo
   screen.addstr(3, 24, 'T O R R E S   D E   H A N O I', curses.color_pair(11) | curses.A_BOLD)

   #Desenha a base 
   screen.addstr(18, 1, unichr(c_178) * 80, curses.color_pair(11))

   #Desenha as colunas 
   for i in range(0,11):
      screen.addstr(i+7, 13, unichr(c_178), curses.color_pair(11))
      screen.addstr(i+7, 65, unichr(c_178), curses.color_pair(11))
      screen.addstr(i+7, 39, unichr(c_178), curses.color_pair(11))

   #Apaga/Muda a cor na parte de baixo da tela
   Box(19,1,24,80, 15)

   #Desenha os discos
   for pos_x in range(1,4):
      col = 26 * pos_x - 23

      lin = len(TORRE[pos_x])
      nd = 9-(10-lin)

      for y in range(lin):
         screen.addstr(17-y, col,  DISCO[TORRE[pos_x][nd-y]], curses.color_pair(COR[pos_x][nd-y]))
         pause(0.03)


def ENCERRA(abortado):
   if abortado:
      screen.addstr(24, 1, ' Jogo abortado...                  ', curses.color_pair(12) | curses.A_BOLD)
      pause(2)

   else:
      screen.addstr(24, 1, ' Meus parabéns...  você conseguiu!!!', curses.color_pair(12) | curses.A_BOLD)
      pause(.5)
      screen.getch()

   #Restaura a cor do terminal
   screen.refresh()
   screen.clear()
   screen.keypad(False)
   curses.nocbreak()
   curses.echo()
   curses.endwin()
   sys.exit(0)


def main():

   n_mov = 0

   #Imprimi a tela de abertura
   display_tela()
   autor()
   pause(3)

   '''
   # Fica piscando a tela (mudando de cor)
   for i in range(6):
      pause(.3)
      curses.init_pair(11, curses.COLOR_GREEN, curses.COLOR_WHITE)
      pause(.3)
      curses.init_pair(11, curses.COLOR_BLUE, curses.COLOR_WHITE)
   '''

   display_tela()

   while True:
      # Desenha os botoes
      bt_solto(1)
      bt_solto(2)
      bt_solto(3)

      screen.addstr(24, 1, (' ' * 80), curses.color_pair(12))
      screen.addstr(24, 63, 'Movimentos: %5i' % n_mov, curses.color_pair(12) | curses.A_BOLD)

      #Pede para o usuario fazer o movimento
      screen.addstr(24, 1, ' Entre com o nº da torre de origem ', curses.color_pair(12) | curses.A_BOLD)
      origem = Hprompt()
      if origem == 0: continue
      bt_press(origem)

      if TORRE[origem] == []:
         # Torre vazia
         curses.beep()
         screen.addstr(24, 1, ' Esta torre esta vazia...          ', curses.color_pair(12) | curses.A_BOLD)
         pause(2)
         continue

      screen.addstr(24, 1, ' Entre com o nº da torre de destino', curses.color_pair(12) | curses.A_BOLD)
      destino = Hprompt()
      if destino == 0: continue
      bt_press(destino)
      pause(.1)

      if destino == origem:
         curses.beep()
         continue

      # Verifica se o movimento e valido 
      if TORRE[origem] > TORRE[destino] and TORRE[destino] != []:
         curses.beep()
         screen.addstr(24, 1, ' Movimento ilegal...               ', curses.color_pair(12) | curses.A_BOLD)
         pause(2)
         continue


      #Move o disco de uma torre para a outra

      #Apaga o disco
      col = 26 * origem - 23
      lin = 18 - len(TORRE[origem])
      screen.addstr(lin, col, " "*10 + unichr(c_178) + " "*10, curses.color_pair(11))
      
      n_disco = TORRE[origem][0]
      TORRE[origem] = TORRE[origem][1:]
      TORRE[destino] = [n_disco] + TORRE[destino]

      cor_disco = COR[origem][0]
      COR[origem] = COR[origem][1:]
      COR[destino] = [cor_disco] + COR[destino]

      #Desenha o disco
      col = 26 * destino - 23
      lin = 18 - len(TORRE[destino])
      screen.addstr(lin, col, DISCO[n_disco], curses.color_pair(cor_disco))
      
      n_mov = n_mov + 1

      #Verifica se chegou no fim do jogo
      if len(TORRE[pos_1]) == N_DISCOS or len(TORRE[pos_2]) == N_DISCOS:
         ENCERRA(False)


if __name__ == '__main__':
   try:
      curses.wrapper(main())
   except KeyboardInterrupt:
      curses.endwin()

#   sys.exit(main())
