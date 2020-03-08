import random
import time
import pprint

from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from random import randint

#!/usr/bin/python
import curses, random

def show_fire():
  screen  = curses.initscr()
  width   = screen.getmaxyx()[1]
  height  = screen.getmaxyx()[0]
  size    = width*height
  char    = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
  b       = []

  curses.curs_set(0)
  curses.start_color()
  curses.init_pair(1,0,0)
  curses.init_pair(2,1,0)
  curses.init_pair(3,3,0)
  curses.init_pair(4,4,0)
  screen.clear
  for i in range(size+width+1): b.append(0)

  j=0
  while j<65:
          for i in range(int(width/9)): b[int((random.random()*width)+width*(height-1))]=65
          for i in range(size):
                  b[i]=int((b[i]+b[i+1]+b[i+width]+b[i+width+1])/4)
                  color=(4 if b[i]>15 else (3 if b[i]>9 else (2 if b[i]>4 else 1)))
                  if(i<size-1):   screen.addstr(  int(i/width),
                                                  i%width,
                                                  char[(9 if b[i]>9 else b[i])],
                                                  curses.color_pair(color) | curses.A_BOLD )

          screen.refresh()
          screen.timeout(30)
          if (screen.getch()!=-1): break
          j+=1

  curses.endwin()




def intro():
  print ("You wake up in a strange place, and you hear the yells of a crowd?! As you look around, you see a heavy set man looking at you.'Wow that took a long time,'He says 'Get ready for battle! It starts in 10 minutes'. He points at a rack of weapons and says 'Pick a weapon.'. There are 5 weapons: a sword, a mace, a bow, a spear and a mage staff")
  print ("")
def intro2():
  
  print("'Nice choice!' says the heavy set man,he says: 'you have been randomly picked to fight in this tournament!, this is the tournament of legends! you will be fighting in 5 minutes so get your armor ready")
  
  
def is_def(attacker, defender):
  print("is_def",attacker, defender)
  varible = rolldie(10)
  if varible >= chars[defender]['def_chance']:
    print("No defense")
    return False
  else:
    print("Defended")
    return True

def pick_weapon(autopick=False):
  if autopick:
    return "sword"
  else:
    reply=input () 
    return reply

def rolldie(sides):
  return random.randint(1,sides)

items = {
  'sword' : {'atk':3, 'magic':False, 'bp': 5},
  'mace' : {'atk':4, 'magic':False, 'bp': 4},
  'bow' : {'atk':3, 'magic':False, 'bp': 5, 'range':True},
  'spear' : {'atk':4, 'magic':False, 'bp': 4, 'range':True},
  'staff' : {'atk':1, 'magic':True, 'bp': 5, 'range':True}
}

chars = {
  'gunter':  {'ac':12, 'dmg': 1,  'hp_start':25,  'hp':None,'def_chance':5, 'weapon':None, },
  'lizard':  {'ac':12, 'dmg': 4,  'hp_start':20,  'hp':None,'def_chance':6,  'weapon':None,},
  'grizzly': {'ac':10, 'dmg': 5,  'hp_start':40,  'hp':None,'def_chance':3,  'weapon':None,},
  'dragon':  {'ac':18, 'dmg': 12, 'hp_start':100, 'hp':None,'def_chance':3,  'weapon':None,},
  'Paladin': {'ac':15, 'dmg': 10, 'hp_start':40, 'hp':None,'def_chance':7, 'weapon':None,},
}




def reset_chars():
  for c in chars.keys():
    chars[c]['hp'] = chars[c]['hp_start']

def show_char(name):
  #print('-----------')
  print("-- Showing ",name)
  print(chars[name])


def did_attack_hit(attacker, defender):
  #print("Attacker is ", attacker, " defender is ", defender)
  roll = rolldie(20)
  defender_stats = chars[defender]
  #print("Defender stats:  ", defender_stats)
  defender_ac = defender_stats['ac']
  print(attacker + " rolled a ",roll,)
  if defender_ac<=roll or roll==20:
    print("Hit")
    return True
  print("Missed")
  return False

def damage(attacker, defender):
    # look up damage
  d= rolldie(6)
  print("Damage roll: ",d)
  return d



def simple_gameloop():
  # keep looping forever
  while True:

    # did the attack work?
    is_hit = did_attack_hit('gunter','lizard')
    # if it did, figure out damage
    if is_hit:
      dmg = damage('gunter','lizard')
      chars['lizard']['hp'] -= dmg

      # show attacker and defender stats
      show_char('gunter')
      show_char('lizard')

    # did the opponent die?
    if chars['lizard']['hp']<=0:
      chars['lizard']['state']='D'
      print('lizard died')
      break

    time.sleep(1)

#simple_gameloop()





# --------------------------------------------

def do_attack_step(attacker,defender):
    # show attacker and defender stats
    print(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ")
    print(attacker + " attacks " + defender)

    # did the attack work?
    is_hit = did_attack_hit(attacker,defender)

    # if it did, figure out damage
    if is_def(attacker, defender)== True:
      pass
    elif is_hit:
      dmg = damage(attacker,defender)
      chars[defender]['hp'] -= dmg

      show_char(attacker)
      show_char(defender)
        

    

    # did the opponent die?
    if chars[defender]['hp']<=0:
      chars[defender]['state']='D'
      print(defender + ' died')
      return True

    return False


def fancy_gameloop(fighters,delay=0):
  # keep looping forever
  while True:

    attacker = fighters[0]
    defender = fighters[1]

    died = do_attack_step(attacker, defender)
    time.sleep(delay)
    if died: return attacker

    attacker = fighters[1]
    defender = fighters[0]

    died = do_attack_step(attacker, defender)
    time.sleep(delay)
    if died: return attacker


# ------

show_fire()


def list_players():
  pprint.pprint(chars)
  print("--- Hit Enter")
  answer = input("") 


def multi_battle(rounds=1,delay=0):
  intro()

  #weapon='sword'
  autopick=False
  weapon=pick_weapon(autopick)

  print("You chose:",weapon)

  intro2()


      #time.sleep(1)
  fighters = ['gunter', 'grizzly']

  score={
    fighters[0]:0,
    fighters[1]:0
    }

  for i in range(0,rounds):
    reset_chars()
    random.shuffle( fighters )
    print(fighters)
    winner = fancy_gameloop( fighters, delay )
    #winner = simple_gameloop()
    print('----------------------------------')
    print("WINNER:",winner)

    score[winner]+=1

  print("FINAL SCORE",score)

  print("--- Hit Enter")
  answer = input("") 



def single_battle():
  multi_battle(1,delay=1)




# Import the necessary packages
import time
from consolemenu import *
from consolemenu.items import *

# Create the menu
menu = ConsoleMenu("DnD Battle v0.01", "Copyleft 2020 (c) Roberts Creek Code Club")


# A FunctionItem runs a Python function when selected
item_battle = FunctionItem("Single Battle", single_battle, [])
item_battle_m = FunctionItem("Multi Battle", multi_battle, [50])
item_list = FunctionItem("List", list_players, [])
item_show_fire = FunctionItem("Fire", show_fire, [])
# A CommandItem runs a console command
#command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])

selection_menu2 = ConsoleMenu("DnD Battle2", "(c) RC Code Club")
#selection_menu2.append_item(function_item2)

# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)
submenu_item2 = SubmenuItem("Submenu item2", selection_menu2, menu)

# Once we're done creating them, we just add the items to the menu
menu.append_item(item_battle)
menu.append_item(item_battle_m)
menu.append_item(item_list)
#menu.append_item(command_item)
menu.append_item(submenu_item)
menu.append_item(submenu_item2)
menu.append_item(item_show_fire)

# Finally, we call show to show the menu and allow the user to interact
menu.show()
