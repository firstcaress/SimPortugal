from m5stack import *
from m5ui import *
import time
import urequests
import os
import ujson
import random
import gc


global color

color = [0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF,
				 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0xFFFFFF]

btnA = M5Button(name="ButtonA", text="ButtonA", visibility=False)
btnB = M5Button(name="ButtonB", text="ButtonB", visibility=False)
btnC = M5Button(name="ButtonC", text="ButtonC", visibility=False)


class Pais(object):
	turn = 20
	identifier = id(machine)
	version = 0.40
	idade = 20
	dinheiro = 0
	carisma = 0
	authoritan = 0
	religious = 0
	conservative = 0
	science = 0

	def __init__(self, posicao, populacao, money, militarpoder, natalidade, felicidade, saude, nome, destruido,
							 militargastos, impostos, ordenadomedio):
		self.posicao = posicao
		self.populacao = populacao
		self.money = money
		self.militarpoder = militarpoder
		self.militargastos = militargastos
		self.militarcontentamento = 50
		self.natalidade = natalidade
		self.felicidade = felicidade
		self.saude = saude
		self.nome = nome
		self.destruido = destruido
		self.impostos = impostos
		self.ordenadomedio = ordenadomedio
		self.economia = 1
		self.economiaagricultura = 1
		self.educacaogastos = 5000
		self.educacaonivel = 0
		self.gastossaude = 5000
		self.socialreligion = 0
		self.socialconservative = 50
		self.socialscience = 0
		self.artinfluence = 0



portugal = Pais(0, 1000, 25000, 0, 10, 50, 70, "Portugal", 1, 5000, 30, 1000)
andorra = Pais(1, 10, 10000, 20, 10, 50, 70, "Andorra", 0, 500, 15, 5000)
espanha = Pais(2, 9000, 290000, 500, 10, 50, 70, "Spain", 0, 500, 15, 2500)
franca = Pais(3, 15000, 500000, 1000, 10, 50, 70, "France", 0, 500, 15, 3000)
missanga = Pais(4, 150000, 500000, 5000, 10, 50, 70, "MissangaLand", 0, 500, 15, 6000)

country_list = [portugal, andorra, espanha, franca, missanga]

estatisticas = {
	"Population": portugal.populacao,
	"Money": portugal.money,
	"Military Power": portugal.militarpoder
}


class Menu(object):
	def __init__(self, escolha, maximo, sair, load):
		self.escolha = 1
		self.maximo = 1
		self.sair = 0
		self.load = "nada"


def id(machine):
	machine = str(machine.unique_id())
	machine = machine.replace("[^\w]", "")
	validLetters = "abcdefghijklmnopqrstuvwxyz0123456789"
	machine = ''.join([char for char in identifier if char in validLetters])
	return (machine)


def displayButtons():
	M5TextBox(135, 213, "Select", lcd.FONT_Default, 0xfffc00)
	M5TextBox(52, 213, "Previous", lcd.FONT_Default, 0x00ff3b)
	M5TextBox(237, 213, "Next", lcd.FONT_Default, 0xff0000)


def startMenu():
	clear_bg(0x222222)
	M5Title(title="Welcome to SimPortugal v" + str(Pais.version), fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	displayButtons()
	Menu.maximo = 5
	Menu.sair = 0
	Menu.escolha = 1
	clearcolors()
	color[1] = 0x0007fd
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
		if buttonA.isPressed():  # M5Cloud upload
			Menu.escolha = (Menu.escolha - 1)
			if Menu.escolha == 0:
				Menu.escolha = Menu.maximo
			clearcolors()
			color[Menu.escolha] = 0x0007fd
			time.sleep(0.2)
			return ()
		if buttonC.isPressed():  # M5Cloud upload
			Menu.escolha = (Menu.escolha + 1)
			if Menu.escolha == (Menu.maximo + 1):
				Menu.escolha = 1
			clearcolors()
			color[Menu.escolha] = 0x0007fd
			time.sleep(0.2)
			return ()
		if buttonB.isPressed():
			Menu.sair = 1
			time.sleep(0.2)
			return ()


def clearcolors():
	color[0] = 0xFFFFFF
	color[1] = 0xFFFFFF
	color[2] = 0xFFFFFF
	color[3] = 0xFFFFFF
	color[4] = 0xFFFFFF
	color[5] = 0xFFFFFF
	color[6] = 0xFFFFFF
	color[7] = 0xFFFFFF
	color[8] = 0xFFFFFF
	color[9] = 0xFFFFFF
	color[10] = 0xFFFFFF
	color[11] = 0xFFFFFF
	color[12] = 0xFFFFFF
	color[13] = 0xFFFFFF


def novoJogo():
	clear_bg(0x222222)
	M5Title(title="SimPortugal v" + str(Pais.version), fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	Menu.maximo = 10
	Menu.sair = 0
	Menu.escolha = 1
	M5TextBox(25, 26, "Turns Until Election :", lcd.FONT_Default, 0xec0000)
	M5TextBox(180, 26, str(Pais.turn), lcd.FONT_Default, 0xFFFFFF)
	displayButtons()
	clearcolors()
	color[1] = 0x0007fd
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
		M5TextBox(160, 70, "Budget", lcd.FONT_Default, color[8])
		M5TextBox(160, 90, "Economy", lcd.FONT_Default, color[9])
		M5TextBox(160, 110, "Other Options", lcd.FONT_Default, color[10])
		escolher()


def loadJogo():
	global Menu
	global portugal
	global militares
	try:
		with open("/flash/lib/SimPor.sav", "r") as json_file:
			data = ujson.load(json_file)
			#		Pais.turn = data["voltas"]
			#		portugal = (
			#	Pais(data["posicao"], data["populacao"], data["money"], data["militar"], data["natalidade"], data["felicidade"],
			#				 data["saude"]))
			#	militares = militarianos(data["gastos"], data["contentamento"], data["poder"], data["nome"])
			Menu.load = "1.1"
			Menu.sair = 0
			M5TextBox(155, 66, "*SAVE DETECTED*", lcd.FONT_Default, 0xfffc00)
			time.sleep(1)
			return ()
	except:
		Menu.sair = 0
		M5TextBox(155, 66, "*NO SAVE DETECTED*", lcd.FONT_Default, 0xfffc00)
		time.sleep(0.5)
		Menu.load = "startMenu"


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
	M5TextBox(25, 46, str(portugal.militargastos), lcd.FONT_Default, 0xFFFFFF)
	M5TextBox(25, 66, "Military Power: ", lcd.FONT_Default, 0x0007fd)
	M5TextBox(25, 86, str(portugal.militarpoder), lcd.FONT_Default, 0xFFFFFF)
	displayButtons()
	clearcolors()
	color[1] = 0x0007fd
	while True:
		if Menu.sair == 1 and Menu.escolha == 1:
			M5TextBox(25, 46, str(portugal.militargastos), lcd.FONT_Default, 0x222222)
			portugal.militargastos = portugal.militargastos + 1000
			M5TextBox(25, 46, str(portugal.militargastos), lcd.FONT_Default, 0xFFFFFF)
			Menu.sair = 0
			continue
		if Menu.sair == 1 and Menu.escolha == 2:
			M5TextBox(25, 46, str(portugal.militargastos), lcd.FONT_Default, 0x222222)
			portugal.militargastos = portugal.militargastos - 1000
			if portugal.militargastos < 0:
				portugal.militargastos = 0
			M5TextBox(25, 46, str(portugal.militargastos), lcd.FONT_Default, 0xFFFFFF)
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
	json_file = open("/flash/lib/SimPor.sav", "r")
	data = ujson.load(json_file)
	print(gc.mem_free())
	gravado = data["gravado"]
	Pais.turn = data["voltas"]
	print(gc.mem_free())
	portugal = (
		Pais(data["posicao"], data["populacao"], data["money"], data["militar"], data["natalidade"], data["felicidade"],
				 data["saude"]))
	militares = militarianos(data["gastos"], data["contentamento"], data["poder"], data["nome"])
	json_file.close()
	dados = {"identifier": identifier, "gravado": 1, "voltas": Pais.turn, "saving": "1"}
	dados.update(portugal.__dict__)
	dados.update(militares.__dict__)
	json = ujson.dumps(dados)
	headers = {
		'Content-Type': 'application/json',
		'X-MyHeader': '123', }
	response = urequests.post('https://us-central1-plucky-agency-235912.cloudfunctions.net/function-1', headers=headers,
														data=json)
	response.close()
	M5TextBox(155, 70, "*UPLOADED TO CLOUD*", lcd.FONT_Default, 0xfffc00)
	time.sleep(2)
	Menu.load = "1.1"


def downloadCloud():
	global Menu
	global portugal
	global militares
	global identifier
	dados = {"saving": "0"}
	json = ujson.dumps(dados)
	headers = {
		'Content-Type': 'application/json',
		'X-MyHeader': '123', }
	response = urequests.post('https://us-central1-plucky-agency-235912.cloudfunctions.net/function-1', headers=headers,
														data=json)
	print(response.json())
	data = response.json()
	Pais.turn = data["voltas"]
	print(data["gastos"])
	portugal = (
		Pais(data["posicao"], data["populacao"], data["money"], data["militar"], data["natalidade"], data["felicidade"],
				 data["saude"]))
	militares = militarianos(data["gastos"], data["contentamento"], data["poder"], data["nome"])
	Menu.load = "1.1"
	Menu.sair = 0
	response.close()
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
		Menu.maximo = 3
		Menu.sair = 0
		Menu.escolha = 1
		clearcolors()
		color[1] = 0x0007fd
		while True:
			if Menu.sair == 1:
				Menu.load = "4." + str(Menu.escolha)
				break
			M5TextBox(25, 70, "Upload Save", lcd.FONT_Default, color[1])
			M5TextBox(25, 90, "Download Save", lcd.FONT_Default, color[2])
			M5TextBox(25, 110, "Update Game & Restart", lcd.FONT_Default, color[3])
			escolher()

	except:
		clear_bg(0x222222)
		M5TextBox(25, 106, "No internet available", lcd.FONT_Default, 0x0000FF)
		time.sleep(3)
		Menu.load = "startMenu"


def updateGame():
	import usocket
  url='https://raw.githubusercontent.com/firstcaress/SimPortugal/master/game.py'
	def urlopen(url, data=None, method="GET"):
		if data is not None and method == "GET":
			method = "POST"
		try:
			proto, dummy, host, path = url.split("/", 3)
		except ValueError:
			proto, dummy, host = url.split("/", 2)
			path = ""
		if proto == "http:":
			port = 80
		elif proto == "https:":
			import ussl
			port = 443
		else:
			raise ValueError("Unsupported protocol: " + proto)

		if ":" in host:
			host, port = host.split(":", 1)
			port = int(port)

		ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
		ai = ai[0]

		s = usocket.socket(ai[0], ai[1], ai[2])
		try:
			s.connect(ai[-1])
			if proto == "https:":
				s = ussl.wrap_socket(s, server_hostname=host)

			s.write(method)
			s.write(b" /")
			s.write(path)
			s.write(b" HTTP/1.0\r\nHost: ")
			s.write(host)
			s.write(b"\r\n")

			if data:
				s.write(b"Content-Length: ")
				s.write(str(len(data)))
				s.write(b"\r\n")
			s.write(b"\r\n")
			if data:
				s.write(data)

			l = s.readline()
			l = l.split(None, 2)
			# print(l)
			status = int(l[1])
			while True:
				l = s.readline()
				if not l or l == b"\r\n":
					break
				# print(l)
				if l.startswith(b"Transfer-Encoding:"):
					if b"chunked" in l:
						raise ValueError("Unsupported " + l)
				elif l.startswith(b"Location:"):
					raise NotImplementedError("Redirects not yet supported")
		except OSError:
			s.close()
			raise

		return s











def none():
	clear_bg(0x222222)
	gc.collect()
	print(gc.mem_free())
	url = 'https://raw.githubusercontent.com/firstcaress/SimPortugal/master/game.py'
	filename = 'glame.py'
	r = urequests.get(url, stream=True)


#	with open(urequests.get('https://raw.githubusercontent.com/firstcaress/SimPortugal/master/game.py', stream=True)) as response:
#		print(str(response.text))
#	print(gc.mem_free())
#	response.close
#	print(gc.mem_free())
#	with open(response.text,"r") as fileHandler:
#		for line in fileHandler:
#			print(line.strip())
#	response.close

#	response.close()
#	f = open('gamere.py', 'w')
#	f.write(newversion)
#	f.close()
#	machine.reset()


def loadEducation():
	clear_bg(0x222222)
	title1 = M5Title(title="Education", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	label1 = M5TextBox(25, 46, "Load Saved Game", lcd.FONT_Default, 0x0007fd)
	time.sleep(2)


def invadirPais():
	clear_bg(0x222222)
	M5Title(title="War Room - No Fighting", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	Menu.sair = 0
	Menu.escolha = 1
	clearcolors()
	color[1] = 0x0007fd

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
				M5TextBox(25, a, "Invade " + str(Pais_class.nome) + ". Power: " + str(Pais_class.militarpoder),
									lcd.FONT_Default, color[b])
				Pais_class.posicao = b
				a = a + 20
				b = b + 1
		M5TextBox(25, a, "Main Menu", lcd.FONT_Default, color[b])
		Menu.maximo = b
		escolher()


def fight(escolha):
	clear_bg(0x222222)
	for Pais_class in country_list:
		if Pais_class.posicao == int(escolha):
			pais_invadido = Pais_class
	M5TextBox(25, 46, "You have decided to invade " + str(pais_invadido.nome), lcd.FONT_Default, 0xff0000)
	M5TextBox(25, 66, "It's military power is " + str(pais_invadido.militarpoder), lcd.FONT_Default, 0x0007fd)
	print(portugal.militarpoder)
	print(pais_invadido.militarpoder)
	if (portugal.militarpoder * 2) < pais_invadido.militarpoder:
		time.sleep(2)
		M5TextBox(25, 86, "You are not very smart", lcd.FONT_Default, 0x0007fd)
		time.sleep(4)
		clear_bg(0x222222)
		M5TextBox(25, 66, "YOUR COUNTRY IS", lcd.FONT_DejaVu24, 0x0007fd)
		M5TextBox(86, 106, "DESTROYED", lcd.FONT_DejaVu24, 0x0007fd)
		speaker.sing(220, 1)
		speaker.sing(165, 1)
		speaker.sing(330, 1 / 8)
		time.sleep(1)
		machine.reset()
	time.sleep(1)
	M5TextBox(25, 106, "After a long battle", lcd.FONT_Default, 0x0007fd)
	time.sleep(0.3)
	M5TextBox(45, 112, ".", lcd.FONT_Default, 0x0007fd)
	time.sleep(0.3)
	M5TextBox(46, 112, ".", lcd.FONT_Default, 0x0007fd)
	time.sleep(0.3)
	M5TextBox(47, 112, ".", lcd.FONT_Default, 0x0007fd)
	time.sleep(2)
	clear_bg(0x222222)
	M5TextBox(25, 66, "YOUR COUNTRY IS", lcd.FONT_DejaVu24, 0x0007fd)
	print((portugal.militarpoder / 1.3) + random.uniform(1, portugal.militarpoder))
	if ((portugal.militarpoder / 1.3) + random.uniform(1, portugal.militarpoder)) > (
					(pais_invadido.militarpoder / 1.3) + random.uniform(1, pais_invadido.militarpoder)):
		time.sleep(0.5)
		M5TextBox(86, 106, "VICTORIOUS", lcd.FONT_DejaVu24, 0x0007fd)
		for Pais_class in country_list:
			if Pais_class == pais_invadido:
				Pais_class.destruido = 1
		time.sleep(2)
		return
	if ((portugal.militarpoder / 1.3) + random.uniform(1, portugal.militarpoder)) < (
					(pais_invadido.militarpoder / 1.3) + random.uniform(1, pais_invadido.militarpoder)):
		time.sleep(0.5)
		M5TextBox(86, 106, "DEFEATED", lcd.FONT_DejaVu24, 0x0007fd)
		time.sleep(2)
		return


def quitJogo():
	clear_bg(0x222222)
	M5Title(title="Welcome to SimPortugal v" + str(Pais.version), fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	M5TextBox(25, 46, "OH :( Goodby then!", lcd.FONT_Default, 0x0007fd)
	time.sleep(2)
	machine.reset()


def loadCountryData():
	clear_bg(0x222222)
	M5Title(title="Country Data", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	M5TextBox(135, 213, "Main Menu", lcd.FONT_Default, 0xfffc00)
	M5TextBox(15, 213, "Previous Menu", lcd.FONT_Default, 0x00ff3b)
	M5TextBox(237, 213, "Next Menu", lcd.FONT_Default, 0xff0000)
	M5TextBox(25, 46, "PORTUGAL", lcd.FONT_Default, 0xff0000)
	M5TextBox(25, 66, "Population: ", lcd.FONT_Default, 0x0000FF)
	M5TextBox(165, 66, str(portugal.populacao), lcd.FONT_Default, 0xFFFFFF)
	M5TextBox(25, 86, "Age Expectancy: ", lcd.FONT_Default, 0x0000FF)
	M5TextBox(165, 86, str(portugal.saude), lcd.FONT_Default, 0xFFFFFF)
	M5TextBox(25, 106, "Money: ", lcd.FONT_Default, 0x0000FF)
	M5TextBox(165, 106, str(portugal.money), lcd.FONT_Default, 0xFFFFFF)
	M5TextBox(25, 126, "Happyness", lcd.FONT_Default, 0x0000FF)
	M5TextBox(165, 126, str(portugal.felicidade), lcd.FONT_Default, 0xFFFFFF)
	while True:
		if buttonB.isPressed():
			time.sleep(0.2)
			Menu.load = "3.4"
			print("we have chosen B BUTTON!!!!!!!")
			break
		if buttonC.isPressed():
			time.sleep(0.2)
			Menu.load = "loadCountryData2"
			break


def loadCountryData2():
	if buttonB.isPressed():
		time.sleep(0.2)
		Menu.load = "3.4"
		clear_bg(0x222222)
		while True:
			M5TextBox(25, 106, "Money: ", lcd.FONT_Default, 0x0000FF)


clear_bg(0x222222)


def loadEconomy():
	global color
	clear_bg(0x222222)
	clearcolors()
	color[1] = 0x0007fd
	M5Title(title="MONEY MONEY", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	Menu.maximo = 4
	Menu.sair = 0
	Menu.escolha = 1
	while True:
		if Menu.sair == 1 and Menu.escolha == 1:
			M5TextBox(25, 46, str(portugal.impostos), lcd.FONT_Default, 0x222222)
			portugal.impostos = portugal.impostos + 1
			M5TextBox(25, 46, str(portugal.impostos), lcd.FONT_Default, 0xFFFFFF)
			Menu.sair = 0
			continue
		if Menu.sair == 1 and Menu.escolha == 2:
			M5TextBox(25, 46, str(portugal.impostos), lcd.FONT_Default, 0x222222)
			portugal.impostos = portugal.impostos - 1
			if portugal.impostos < 0:
				portugal.impostos = 0
			M5TextBox(25, 46, str(portugal.impostos), lcd.FONT_Default, 0xFFFFFF)
			Menu.sair = 0
			continue
		if Menu.sair == 1:
			Menu.load = "3." + str(Menu.escolha)
			break
		M5TextBox(25, 26, "Taxes: ", lcd.FONT_Default, 0x0007fd)
		M5TextBox(25, 46, str(portugal.impostos), lcd.FONT_Default, 0xFFFFFF)
		M5TextBox(25, 126, "Increase Taxes", lcd.FONT_Default, color[1])
		M5TextBox(25, 146, "Decrease Taxes", lcd.FONT_Default, color[2])
		M5TextBox(25, 166, "Yay", lcd.FONT_Default, color[3])
		M5TextBox(25, 186, "Return", lcd.FONT_Default, color[4])
		escolher()


def loadSave():
	dados = {"identifier": Pais.identifier, "gravado": 1, "voltas": Pais.turn}
	dados.update(portugal.__dict__)
	dados.update(militares.__dict__)
	print(dados)
	json = ujson.dumps(dados)
	f = open('/flash/lib/SimPor.sav', 'w')
	f.write(json)
	print(gc.mem_free())
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


def otherOptions():
	clear_bg(0x222222)
	M5Title(title="Testing Options", fgcolor=0xFFFFFF, bgcolor=0x0000FF)
	Menu.sair = 0
	Menu.escolha = 1
	clearcolors()
	color[1] = 0x0007fd
	while True:
		a = 46
		b = 1
		for k, v in estatisticas.items():
			M5TextBox(25, a, str(k), lcd.FONT_Default, color[1])
			M5TextBox(25, a + 20, str(v), lcd.FONT_Default, color[1])
			a = a + 40


def endturncalculations():
	Pais.turn = (Pais.turn - 1)
	portugal.natalidade = ((portugal.felicidade - 50) / 1000) + 1
	portugal.populacao = int(portugal.populacao * portugal.natalidade)
	portugal.felicidade = portugal.felicidade + 30 - portugal.impostos
	portugal.money = (portugal.money - portugal.militargastos - portugal.educacaogastos - portugal.gastossaude + int(
		portugal.populacao * portugal.impostos * portugal.ordenadomedio) / 10000)
	if portugal.money < 1:
		clear_bg(0x222222)
		M5TextBox(25, 46, "YOU ARE BROKE", lcd.FONT_Default, 0x0007fd)
		time.sleep(2)
		M5TextBox(25, 66, "THE FMI SAVES YOU", lcd.FONT_Default, 0x0007fd)
		time.sleep(2)
		M5TextBox(25, 86, "BUT PEOPLE ARE UNHAPPY", lcd.FONT_Default, 0x0007fd)
		portugal.felicidade = portugal.felicidade / 3
		portugal.militargastos = 0
		Menu.load = "1.1"

	portugal.militarpoder = portugal.militarpoder + (portugal.militargastos / 1000)
	if Pais.turn == 0:
		eleicoes()


def eleicoes():
	clear_bg(0x222222)
	displayButtons()
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


startMenu()
while True:
	print(gc.mem_free())
	if Menu.load == "startMenu":
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
	if Menu.load == "4.3":
		updateGame()
	if Menu.load == "5.4":
		novoJogo()
	if Menu.load == "fight":
		fight()
	if Menu.load == "loadCountryData2":
		loadCountryData2()
	if Menu.load == "2.10":
		otherOptions()
	if Menu.load == "2.9":
		loadEconomy()
