from m5stack import *
from m5ui import *
import time
import os
import random
import ujson


global identifier
identifier = random.randint(1,1000000000)

#dados = {"jorge" : "12", "isabel" : "15"}
#teste = open("/flash/lib/Teste.sav", "r")
#json = ujson.dumps(dados)
#teste.write(json)
#teste.close()
#print(dados)

with open('/flash/lib/Teste.sav') as json_file:  
    data = ujson.load(json_file)
    print (data["jorge"])

try:
    print(os.stat("/flash/lib/SimPor.sav"))
    f = open("/flash/lib/SimPor.sav", "r")
    print (f.read())
    f.close()
except:
    f = open("/flash/lib/SimPor.sav", "w")
    f.write(str(identifier)+",0")
    f.close()
    print("oi")




escolha = 1
global turn
turn = 10
global color
global version
version = 0.22
color = [0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF]
         
class Pais(object):
    def __init__(self, populacao, money, militar, natalidade,felicidade,saude):
        self.populacao = populacao
        self.money = money
        self.militar = militar
        self.natalidade = 1.01
        self.felicidade = 50
        self.saude = 70
        
portugal = Pais(1000,250000,90,10,50,70)
andorra = Pais(10,10000,20,10,50,70)
espanha = Pais(9000,290000,500,10,50,70)
franca = Pais(15000,500000,1000,10,50,70)


class militares(object):
    def __init__(self,gastos,contentamento,poder):
        self.gastos = 0
        self.contentamento = 0
        self.poder = 0

militares.gastos = 5000
militares.poder = 0

class Menu(object):
    def __init__(self,escolha,maximo, sair,load):
        self.escolha = 1
        self.maximo = 1
        self.sair = 0
        self.load = "nada"

        
def startMenu():
    clear_bg(0x222222)
    title1 = M5Title(title="Welcome to SimPortugal v"+str(version) , fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    menuMode = M5TextBox(135, 213, "Select", lcd.FONT_Default, 0xfffc00)
    menuMinus = M5TextBox(52, 213, "Previous", lcd.FONT_Default, 0x00ff3b)
    menuPlus = M5TextBox(237, 213, "Next", lcd.FONT_Default, 0xff0000)
    Menu.maximo = 3
    Menu.sair = 0
    Menu.escolha = 1
    clearcolors()
    color[1]=0x0007fd
    while True:
        if Menu.sair == 1:
            Menu.load = "1." + str(Menu.escolha)
            break
        label1 = M5TextBox(25, 46, "New Game", lcd.FONT_Default, color[1])
        label2 = M5TextBox(25, 66, "Continue Game", lcd.FONT_Default, color[2])
        label3 = M5TextBox(25, 86, "Quit", lcd.FONT_Default, color[3])
        escolher()
    
def escolher():
    global color
    while True:
      if buttonA.isPressed():   # M5Cloud upload     
         Menu.escolha = (Menu.escolha - 1)
         if Menu.escolha == 0:
           Menu.escolha = Menu.maximo
         clearcolors()
         color[Menu.escolha]=0x0007fd
         time.sleep(0.2)
         return()
      if buttonC.isPressed():   # M5Cloud upload     
         Menu.escolha = (Menu.escolha + 1)
         if Menu.escolha == (Menu.maximo + 1):
           Menu.escolha = 1
         clearcolors()
         color[Menu.escolha]=0x0007fd
         time.sleep(0.2)
         return()
      if buttonB.isPressed():
          Menu.sair = 1
          time.sleep(0.2)
          return()
         
def clearcolors():
    global color
    color[1]=0xFFFFFF
    color[2]=0xFFFFFF
    color[3]=0xFFFFFF
    color[4]=0xFFFFFF
    color[5]=0xFFFFFF
    color[6]=0xFFFFFF
    color[7]=0xFFFFFF    
    color[8]=0xFFFFFF
    color[9]=0xFFFFFF    

def novoJogo():
    global turn
    
    clear_bg(0x222222)
    title1 = M5Title(title="SimPortugal v0.14", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    Menu.maximo = 8
    Menu.sair = 0
    Menu.escolha = 1
    M5TextBox(25, 26, "Turns Until Election :", lcd.FONT_Default, 0xec0000)
    M5TextBox(180, 26, str(turn), lcd.FONT_Default, 0xFFFFFF)
    M5TextBox(135, 213, "Select", lcd.FONT_Default, 0xfffc00)
    M5TextBox(52, 213, "Previous", lcd.FONT_Default, 0x00ff3b)
    M5TextBox(237, 213, "Next", lcd.FONT_Default, 0xff0000)
    clearcolors()
    color[1]=0x0007fd
    while True:
        print (Menu.escolha)
        print (Menu.sair)
        if Menu.sair == 1:
            Menu.load = "2." + str(Menu.escolha)
            if Menu.escolha == 6:
                endturncalculations()
            break

        M5TextBox(25, 70, "Country Data", lcd.FONT_Default, color[1])
        M5TextBox(25, 90, "Player Profile", lcd.FONT_Default, color[2])
        M5TextBox(25, 110, "Education", lcd.FONT_Default, color[3])
        M5TextBox(25, 130, "Military", lcd.FONT_Default, color[4])
        M5TextBox(25, 150, "Health", lcd.FONT_Default, color[5])
        M5TextBox(25, 170, "End Turn", lcd.FONT_Default, color[6])
        M5TextBox(25, 190, "Save & Quit", lcd.FONT_Default, color[7])
        M5TextBox(160, 70, "Other Options", lcd.FONT_Default, color[8])
        escolher()

def endturncalculations():
    global turn
    turn = turn -1
    portugal.money = portugal.money - militares.gastos
    if portugal.money < 1:
        clear_bg(0x222222)
        M5TextBox(25, 46, "YOU ARE BROKE, GAME OVER", lcd.FONT_Default, 0x0007fd)
    militares.poder = militares.poder + (militares.gastos / 1000)
    if turn == 0:
        clear_bg(0x222222)
        M5TextBox(135, 213, "Select", lcd.FONT_Default, 0xfffc00)
        M5TextBox(52, 213, "Previous", lcd.FONT_Default, 0x00ff3b)
        M5TextBox(237, 213, "Next", lcd.FONT_Default, 0xff0000)
        M5TextBox(25, 46, "ELECTION TIME!", lcd.FONT_Default, 0xff0000)
        time.sleep(0.2)
        M5TextBox(25, 66, "Would you like to commit fraud?", lcd.FONT_Default, 0xFFFFFF)
        M5TextBox(25, 106, "Yes", lcd.FONT_Default, 0x0007fd)
        M5TextBox(25, 126, "No", lcd.FONT_Default, 0xFFFFFF)
        Menu.maximo = 2
        Menu.sair = 0
        Menu.escolha = 1
        while True:
          escolher()
          if Menu.sair == 1:
              if Menu.escolha == 1:
                  M5TextBox(25, 146, "MALANDRO", lcd.FONT_Default, 0x0007fd)
              if Menu.escolha == 2:
                  M5TextBox(25, 146, "Honest man!", lcd.FONT_Default, 0x0007fd)
           
          if Menu.escolha == 1:
            M5TextBox(25, 106, "Yes", lcd.FONT_Default, 0x0007fd)
            M5TextBox(25, 126, "No", lcd.FONT_Default, 0xFFFFFF)
          if Menu.escolha == 2:
            M5TextBox(25, 106, "Yes", lcd.FONT_Default, 0xFFFFFF)
            M5TextBox(25, 126, "No", lcd.FONT_Default, 0x0007fd)


def loadJogo():
  global Menu
  try:
    print(os.stat("/flash/lib/SimPor.sav"))
  except:
    print("no file")
    Menu.sair = 0
    M5TextBox(155, 66, "*NO SAVE DETECTED*", lcd.FONT_Default, 0xfffc00)
    time.sleep(0.5)
    Menu.load = "0.0"
   
  
  

def loadProfile():
    clear_bg(0x222222)
    title1 = M5Title(title="Profile", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label1 = M5TextBox(25, 46, "Load Saved Game", lcd.FONT_Default, 0x0007fd)    

def loadMilitary():
    global color
    clear_bg(0x222222)
    M5Title(title="Military", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    Menu.maximo = 4
    Menu.sair = 0
    Menu.escolha = 1
    M5TextBox(25, 26, "Military Spending: ", lcd.FONT_Default, 0x0007fd)
    M5TextBox(25, 46, str(militares.gastos), lcd.FONT_Default, 0xFFFFFF)
    M5TextBox(25, 66, "Military Power: ", lcd.FONT_Default, 0x0007fd)
    M5TextBox(25, 86, str(militares.poder), lcd.FONT_Default, 0xFFFFFF)
    
    M5TextBox(135, 213, "Select", lcd.FONT_Default, 0xfffc00)
    M5TextBox(52, 213, "Previous", lcd.FONT_Default, 0x00ff3b)
    M5TextBox(237, 213, "Next", lcd.FONT_Default, 0xff0000)
    clearcolors()
    color[1]=0x0007fd
    while True:
        
        if Menu.sair == 1 and Menu.escolha == 1:
            M5TextBox(25, 46, str(militares.gastos), lcd.FONT_Default, 0x222222)
            militares.gastos = militares.gastos + 1000
            M5TextBox(25, 46, str(militares.gastos), lcd.FONT_Default, 0xFFFFFF)
            Menu.sair = 0
            continue
        if Menu.sair == 1 and Menu.escolha == 2:
            M5TextBox(25, 46, str(militares.gastos), lcd.FONT_Default, 0x222222)
            militares.gastos = militares.gastos - 1000
            if militares.gastos < 0:
                militares.gastos = 0
            M5TextBox(25, 46, str(militares.gastos), lcd.FONT_Default, 0xFFFFFF)
            Menu.sair = 0
            continue            
        if Menu.sair == 1:
            Menu.load = "3." + str(Menu.escolha)
            break
        label1 = M5TextBox(25, 126, "Increase Spending", lcd.FONT_Default, color[1])
        label2 = M5TextBox(25, 146, "Decrease Spending", lcd.FONT_Default, color[2])
        label3 = M5TextBox(25, 166, "Invade Country", lcd.FONT_Default, color[3])
        label4 = M5TextBox(25, 186, "Return", lcd.FONT_Default, color[4])
        escolher() 
    
def loadHealth():
    clear_bg(0x222222)
    title1 = M5Title(title="Health", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label1 = M5TextBox(25, 46, "Load Saved Game", lcd.FONT_Default, 0x0007fd) 
    time.sleep(2)

def loadEducation():
    clear_bg(0x222222)
    title1 = M5Title(title="Education", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label1 = M5TextBox(25, 46, "Load Saved Game", lcd.FONT_Default, 0x0007fd)  
    time.sleep(2)

def invadirPais():
    clear_bg(0x222222)
    title1 = M5Title(title="War Room - No Fighting", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    while True:
        label1 = M5TextBox(25, 46, "lol", lcd.FONT_Default, 0x0007fd)  
    
def quitJogo():
    clear_bg(0x222222)
    M5Title(title="Welcome to SimPortugal v"+str(version), fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    M5TextBox(25, 46, "OH :( Goodby then!", lcd.FONT_Default, 0x0007fd)
    time.sleep(2)
    machine.reset()
 
def loadCountryData():
    clear_bg(0x222222)
    M5Title(title="Country Data", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    M5TextBox(25, 46, "PORTUGAL", lcd.FONT_Default, 0xff0000)
    M5TextBox(25, 66, "Population: ", lcd.FONT_Default, 0x0000FF)
    M5TextBox(165, 66, str(portugal.populacao), lcd.FONT_Default, 0xFFFFFF)
    M5TextBox(25, 86, "Age Expectancy: ", lcd.FONT_Default, 0x0000FF)
    M5TextBox(165, 86, str(portugal.saude), lcd.FONT_Default, 0xFFFFFF)
    M5TextBox(25, 106, "Money: ", lcd.FONT_Default, 0x0000FF)
    M5TextBox(165, 106, str(portugal.money), lcd.FONT_Default, 0xFFFFFF)
    M5TextBox(25, 126, "Happyness", lcd.FONT_Default, 0x0000FF)
    M5TextBox(165, 126, str(portugal.felicidade), lcd.FONT_Default, 0xFFFFFF)
    M5TextBox(135, 213, "Previous", lcd.FONT_Default, 0x00ff3b)
    while True:
        if buttonB.isPressed():
            time.sleep(0.2)
            Menu.load = "3.4"
            break
    
clear_bg(0x222222)

btnA = M5Button(name="ButtonA", text="ButtonA", visibility=False)
btnB = M5Button(name="ButtonB", text="ButtonB", visibility=False)
btnC = M5Button(name="ButtonC", text="ButtonC", visibility=False)


def loadSave():
    f = open('/flash/lib/SimPor.sav', 'w')
    f.write(portugal())
    f.close()




startMenu()
while True:
    if Menu.load == "0.0":
        startMenu()
    if Menu.load == "1.1":
        novoJogo()
    if Menu.load == "1.2":
        loadJogo()
    if Menu.load == "1.3":
        quitJogo()
    if Menu.load == "2.1":
        loadCountryData()
    if Menu.load == "2.2":
        loadProfile()
    if Menu.load == "2.3":
        loadEducation()
    if Menu.load == "2.4":
        loadMilitary()
    if Menu.load == "2.5":
        loadHealth()
    if Menu.load == "2.7":
        loadSave()
    if Menu.load == "3.3":
        invadirPais()
    if Menu.load == "2.6":
        novoJogo()
    if Menu.load == "3.4":
        novoJogo()



