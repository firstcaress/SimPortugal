from m5stack import *
from m5ui import *
import time
import os
import urequests
import gc
import ujson
import random

global gravado
global identifier
identifier = (machine.unique_id())
identifier = str(identifier)
identifier = identifier.replace("[^\w]","")
validLetters = "abcdefghijklmnopqrstuvwxyz0123456789"
identifier = ''.join([char for char in identifier if char in validLetters])

escolha = 1
global turn
turn = 10
global color
global version

version = 0.31
color = [0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF,0xFFFFFF]
         
class Pais(object):
    def __init__(self, posicao, populacao, money, militar, natalidade,felicidade,saude, nome,destruido):
        self.posicao = posicao
        self.populacao = populacao
        self.money = money
        self.militar = militar
        self.natalidade = natalidade
        self.felicidade = felicidade
        self.saude = saude
        self.nome = nome
        self.destruido = destruido


portugal = Pais(0,1000,250000,90,10,50,70, "Portugal",1)
andorra = Pais(1,10,10000,20,10,50,70, "Andorra",0)
espanha = Pais(2,9000,290000,500,10,50,70, "Spain",0)
franca = Pais(3,15000,500000,1000,10,50,70, "France",0)
missanga = Pais(4,150000,500000,5000,10,50,70, "MissangaLand",0)

country_list = [portugal,andorra,espanha,franca,missanga]

class militarianos(object):
    def __init__(self,gastos,contentamento,poder):
        self.gastos = gastos
        self.contentamento = contentamento
        self.poder = poder

militares = militarianos(5000,50,0)


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
    Menu.maximo = 4
    Menu.sair = 0
    Menu.escolha = 1
    clearcolors()
    color[1]=0x0007fd
    while True:
        if Menu.sair == 1:
            Menu.load = "1." + str(Menu.escolha)
            break
        M5TextBox(25, 46, "New Game", lcd.FONT_Default, color[1])
        M5TextBox(25, 66, "Continue Game", lcd.FONT_Default, color[2])
        M5TextBox(25, 86, "Go Online", lcd.FONT_Default, color[3])
        M5TextBox(25, 106, "Quit", lcd.FONT_Default, color[4])
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
    title1 = M5Title(title="SimPortugal v"+str(version), fgcolor=0xFFFFFF, bgcolor=0x0000FF)
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
        time.sleep(4)
        machine.reset()
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
  global turn
  global portugal
  global militares
  try:
    with open("/flash/lib/SimPor.sav","r") as json_file:  
        data = ujson.load(json_file)
        gravado = data["gravado"]
        M5TextBox(155, 66, "*SAVE DETECTED*", lcd.FONT_Default, 0xfffc00)
        time.sleep(1)
        if gravado == 1:
            turn = data["voltas"]
            print (data["gastos"])
            portugal=(Pais(data["posicao"], data["populacao"], data["money"], data["militar"], data["natalidade"],data["felicidade"],data["saude"]))
            militares = militarianos(data["gastos"],data["contentamento"],data["poder"], data["nome"])
            Menu.load = "1.1"
            Menu.sair = 0
            return()
        Menu.sair = 0
        M5TextBox(155, 66, "*NO SAVE DETECTED*", lcd.FONT_Default, 0xfffc00)
        time.sleep(0.5)
        Menu.load = "0.0"
  except:
        print("no savefile")
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
        M5TextBox(25, 126, "Increase Spending", lcd.FONT_Default, color[1])
        M5TextBox(25, 146, "Decrease Spending", lcd.FONT_Default, color[2])
        M5TextBox(25, 166, "Invade Country", lcd.FONT_Default, color[3])
        M5TextBox(25, 186, "Return", lcd.FONT_Default, color[4])
        escolher() 
 
def uploadCloud():
      global Menu
      global portugal
      global militares
      global identifier
      global turn
      json_file = open("/flash/lib/SimPor.sav","r")
      data = ujson.load(json_file)
      print (gc.mem_free())
      gravado = data["gravado"]
      turn = data["voltas"]
      print (gc.mem_free())
      portugal=(Pais(data["posicao"], data["populacao"], data["money"], data["militar"], data["natalidade"],data["felicidade"],data["saude"]))
      militares = militarianos(data["gastos"],data["contentamento"],data["poder"],data["nome"])
      json_file.close()
      dados = {"identifier" : identifier, "gravado" : 1, "voltas" : turn, "saving":"1"}
      dados.update(portugal.__dict__)
      dados.update(militares.__dict__)
      json = ujson.dumps(dados)
      headers = {
    'Content-Type': 'application/json',
    'X-MyHeader': '123',}
      response = urequests.post('https://us-central1-plucky-agency-235912.cloudfunctions.net/function-1', headers=headers, data=json)
      response.close()
      M5TextBox(155, 70, "*UPLOADED TO CLOUD*", lcd.FONT_Default, 0xfffc00)
      time.sleep(2)
      Menu.load = "1.1"

def downloadCloud():
      global Menu
      global portugal
      global militares
      global identifier
      global turn
      dados = {"saving":"0"}
      json = ujson.dumps(dados)
      headers = {
    'Content-Type': 'application/json',
    'X-MyHeader': '123',}
      response = urequests.post('https://us-central1-plucky-agency-235912.cloudfunctions.net/function-1', headers=headers, data=json)
      print(response.json())
      data = response.json()
      turn = data["voltas"]
      print (data["gastos"])
      portugal=(Pais(data["posicao"], data["populacao"], data["money"], data["militar"], data["natalidade"],data["felicidade"],data["saude"]))
      militares = militarianos(data["gastos"],data["contentamento"],data["poder"], data["nome"])
      Menu.load = "1.1"
      Menu.sair = 0
      response.close
      M5TextBox(155, 90, "*LOADED FROM CLOUD*", lcd.FONT_Default, 0xfffc00)
      time.sleep(2)
      Menu.load = "1.1"
      
def loadOnline():
    
    try:
        import wifisetup
        wifisetup.auto_connect()
        global Menu
        clear_bg(0x222222)
        M5Title(title="You are Online. Congratulations!", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
        Menu.maximo = 2
        Menu.sair = 0
        Menu.escolha = 1
        clearcolors()
        color[1]=0x0007fd
        while True:
            if Menu.sair == 1:
                 Menu.load = "4." + str(Menu.escolha)
                 break
            M5TextBox(25, 70, "Upload Save", lcd.FONT_Default, color[1])
            M5TextBox(25, 90, "Download Save", lcd.FONT_Default, color[2])
            escolher()
            
    except:
        clear_bg(0x222222)
        M5TextBox(25, 106, "No internet available", lcd.FONT_Default, 0x0000FF)
        time.sleep (3)
        Menu.load = "0.0"

def loadEducation():
    clear_bg(0x222222)
    title1 = M5Title(title="Education", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label1 = M5TextBox(25, 46, "Load Saved Game", lcd.FONT_Default, 0x0007fd)  
    time.sleep(2)

def loadEducation():
    clear_bg(0x222222)
    title1 = M5Title(title="Education", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    label1 = M5TextBox(25, 46, "Load Saved Game", lcd.FONT_Default, 0x0007fd)  
    time.sleep(2)

def invadirPais():
    global Menu
    global color
    clear_bg(0x222222)
    
    title1 = M5Title(title="War Room - No Fighting", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
    Menu.sair = 0
    Menu.escolha = 1
    clearcolors()
    color[1]=0x0007fd
    
    while True:
        if Menu.sair == 1:
            if Menu.escolha == b:
                Menu.load = "1.1"
            if Menu.escolha < b:
                fight(Menu.escolha)
            break
        a = 46
        b = 1
        for Pais_class in country_list:
            if Pais_class.destruido == 0:
             M5TextBox(25, a, "Invade " + str(Pais_class.nome) + ". Power: "+str(Pais_class.militar),lcd.FONT_Default, color[b])
             a = a + 20
             b = b +1
        M5TextBox(25, a, "Main Menu", lcd.FONT_Default, color[b])
        Menu.maximo = b
        escolher()

def fight(escolha):
    clear_bg(0x222222)
    for Pais_class in country_list:
        if Pais_class.posicao == int(escolha):
            pais_invadido = Pais_class
    M5TextBox(25, 46, "You have decided to invade "+ str(pais_invadido.nome), lcd.FONT_Default, 0xff0000)
    M5TextBox(25, 66, "It's military power is "+str(pais_invadido.militar), lcd.FONT_Default, 0x0007fd)          
    print (militares.poder)
    print (pais_invadido.militar)
    if (militares.poder * 2) < pais_invadido.militar:
        time.sleep(2)
        M5TextBox(25, 86, "You are not very smart", lcd.FONT_Default, 0x0007fd)
        time.sleep(4)
        clear_bg(0x222222)
        M5TextBox(25, 66, "YOUR COUNTRY IS DESTROYED", lcd.FONT_DejaVu24, 0x0007fd)
        M5TextBox(65, 106, "DESTROYED", lcd.FONT_DejaVu24, 0x0007fd)
        speaker.sing(220, 1)
        speaker.sing(165, 1)
        speaker.sing(330, 1/16)

        
    time.sleep(4)

    
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
    dados = {"identifier" : identifier, "gravado" : 1, "voltas" : turn}
    dados.update(portugal.__dict__)
    dados.update(militares.__dict__)
    print(dados)
    json = ujson.dumps(dados)
    f = open('/flash/lib/SimPor.sav', 'w')
    f.write(json)
    print (gc.mem_free())
    f.close()
    clear_bg(0x222222)
    M5TextBox(65, 106, "GAME SAVED.SHUTTING DOWN", lcd.FONT_Default, 0x0000FF)
    time.sleep(0.2)
    M5TextBox(65, 126, ".", lcd.FONT_Default, 0xFFFFFF)
    time.sleep(0.2)
    M5TextBox(70, 126, ".", lcd.FONT_Default, 0xFFFFFF)
    time.sleep(0.2)
    M5TextBox(75, 126, ".", lcd.FONT_Default, 0xFFFFFF)
    time.sleep(0.2)
    M5TextBox(80, 126, ".", lcd.FONT_Default, 0xFFFFFF)
    time.sleep(0.2)
    M5TextBox(85, 126, ".", lcd.FONT_Default, 0xFFFFFF)
    time.sleep(0.5)
    machine.reset()

startMenu()
while True:
    if Menu.load == "0.0":
        startMenu()
    if Menu.load == "1.1":
        novoJogo()
    if Menu.load == "1.2":
        loadJogo()
    if Menu.load == "1.3":
        loadOnline()
    if Menu.load == "1.4":
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
    if Menu.load == "4.1":
        uploadCloud()
    if Menu.load == "4.2":
        downloadCloud()
    if Menu.load == "5.4":
        novoJogo()
    if Menu.load == "fight":
        fight()

