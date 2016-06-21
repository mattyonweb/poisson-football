#f = open("1-premierleague.csv", "r")
f_out = open("tables.csv", "w")
import math, random, os, collections

class Stats():
	''' I parametri globali, cioè le statistiche complessive '''
	MATCHES = 0 #TOTALE MATCH GIOCATI
	WON_H = 0 #TOTALE MATCH VINTI DA SQUADRA DI CASA
	GM_H = 0 #GOL MADE AT HOME
	GM_T = 0 #GOL MADE AT TRANSFERT
	TOT_GOALS = 0 #EVERY GOAL COUNTER
	AVG_GM_H = 0 #AVERAGE GOALS MADE AT HOME
	AVG_GM_T = 0 #AVERAGE GOALS MADE AT TRANSFERT
	AVG_GS_H = 0 #AVERAGE GOALS SUMBITTED AT HOME
	AVG_GS_T = 0 #AVERAGE GOALS SUMBITEED AT TRANSFERT
	HOME_ADVG = 0

	@staticmethod
	def clear():
		Stats.MATCHES = 0 #TOTALE MATCH GIOCATI
		Stats.WON_H = 0 #TOTALE MATCH VINTI DA SQUADRA DI CASA
		Stats.GM_H = 0 #GOL MADE AT HOME
		Stats.GM_T = 0 #GOL MADE AT TRANSFERT
		Stats.TOT_GOALS = 0 #EVERY GOAL COUNTER
		Stats.AVG_GM_H = 0 #AVERAGE GOALS MADE AT HOME
		Stats.AVG_GM_T = 0 #AVERAGE GOALS MADE AT TRANSFERT
		Stats.AVG_GS_H = 0 #AVERAGE GOALS SUMBITTED AT HOME
		Stats.AVG_GS_T = 0 #AVERAGE GOALS SUMBITEED AT TRANSFERT
		Stats.HOME_ADVG = 0

	
class Squadra():

	#Dizionario con tutte le squadre. Forma: {Nome_squadra : obj_squadra}
	all_squadre = {}
	
	def __init__(self, nome):
		self.nome = nome
		
		self.gm_h = 0
		self.gm_t = 0
		self.gs_h = 0
		self.gs_t = 0
		
		self.atk_h = 0
		self.def_h = 0
		self.atk_t = 0
		self.def_t = 0

		self.points = 0

		self.home_games = 0
		self.outs_games = 0

		Squadra.all_squadre[self.nome] = self

		self.posizioni = []
		
	def return_csv(self):
		''' Ritorna la stringa csv della squadra '''
		csv = self.nome + "," + str(self.gm_h) + "," + str(self.gm_t) + "," + str(self.gs_h) + "," + str(self.gs_t)
		
		csv += "," + str(round(self.gm_h/self.home_games,2)) + "," + str(round(self.gm_t/self.outs_games, 2)) + \
				"," + str(round(self.gs_h/self.home_games,2)) + "," + str(round(self.gs_t/self.outs_games, 2)) + "\n"
		return csv

	def clear(self):
		self.gm_h = 0
		self.gm_t = 0
		self.gs_h = 0
		self.gs_t = 0
		
		self.atk_h = 0
		self.def_h = 0
		self.atk_t = 0
		self.def_t = 0

		self.points = 0

		self.home_games = 0
		self.outs_games = 0


	@staticmethod
	def total_goals_made(home = False, out = False):
		''' Ritorna il numero complessivo di gol fatti, con l'opzione di
		ritornare solo quelli fatti in casa o fuori o comunque tutti '''
		total = 0

		for squadra in Squadra.all_squadre.values():
			if home and out:
				total += squadra.gm_h + squadra.gm_t
			elif home and not out:
				total += squadra.gm_h
			elif not home and out:
				total += squadra.gm_t
			else:
				return "ERROR"

		return total

	@staticmethod
	def return_csv_table(filename):
		''' Scrive su "filename" l'insieme delle stringhe csv di tutte le
		squadre '''
		
		table = "Nome,gm_h,gm_t,gs_h,gs_t,avg_gm_h,avg_gm_t,avg_gs_h,avg_gs_t\n"

		for squadra in sorted(Squadra.all_squadre.keys()):
			table += Squadra.all_squadre[squadra].return_csv()

		new_file = open(filename, "w")
		
		new_file.write(table)

accepted = ['Reading', 'Sunderland', 'Tottenham', 'Man City', 'QPR', 'Aston Villa', 'Newcastle', 'Southampton', 'Swansea', 'Wigan', 'Everton', 'Chelsea', 'Fulham', 'Stoke', 'Liverpool', 'Arsenal', 'Man United', 'West Brom', 'Norwich', 'West Ham']

for sq_name in accepted:
	Squadra(sq_name)
	
	
def parser(f):
	'''Dato un file csv, estrapola tutte le info necessarie. '''		

	for line in f:
		
		if line[0] != "D": #se non è la riga introduttiva
			tokens = line.split(",")

			home_team_name = tokens[1] #nome squadre
			outs_team_name = tokens[2]

			goals = tokens[3].split("-")
			home_goals = int(goals[0])
			outs_goals = int(goals[1])
			
			#se non esiste una squadra con il nome indicato nel csv, allora
			#creane una, sennò prendi quella che c'è già.

			if home_team_name in Squadra.all_squadre.keys():
				home_team = Squadra.all_squadre[home_team_name]
				home_team.home_games += 1
				home_team.gm_h += home_goals
				home_team.gs_h += outs_goals
				Stats.TOT_GOALS += home_goals
			else:
				pass

			if outs_team_name in Squadra.all_squadre.keys():
				outs_team = Squadra.all_squadre[outs_team_name]
				outs_team.outs_games += 1
				outs_team.gs_t += home_goals
				outs_team.gm_t += outs_goals
				
				Stats.TOT_GOALS += outs_goals
			else:
				pass
				
			#se la squadra di casa vince, aumenta il conteggio globale delle
			#partite vinte in casa (WON_H)
			if home_goals > outs_goals:
				Stats.WON_H += 1
				
		#incrementa il numero complessivo di partite giocate
			Stats.MATCHES += 1 #TODO

def importer(f):
	#Stats.clear()
	#for squadra in Squadra.all_squadre:
	#	Squadra.all_squadre[squadra].clear()
		
	parser(f)

	Stats.GM_H = Squadra.total_goals_made(home=True)
	Stats.GM_T = Squadra.total_goals_made(out=True)

	Stats.AVG_GM_H = Stats.AVG_GS_T = Stats.GM_H / Stats.MATCHES #avg_goalmade_home
	Stats.AVG_GM_T = Stats.AVG_GS_H = Stats.GM_T / Stats.MATCHES
	Stats.HOME_ADVG = Stats.WON_H / Stats.MATCHES

def exporter(f_out):
	Squadra.return_csv_table("giorgio")


filenames = os.listdir("csvs")

for filename in filenames:
	f = open(os.path.join("csvs/" + filename), "r")
	importer(f)

f.close()

exporter(f_out)

def calculate_parameters(team):
	team.atk_h = (team.gm_h / team.home_games) / Stats.AVG_GM_H #atk_h
	team.atk_t = (team.gm_t / team.outs_games) / Stats.AVG_GM_T #atk_t
	team.def_h = (team.gs_h / team.home_games) / Stats.AVG_GS_H #def_h
	team.def_t = (team.gs_t / team.outs_games) / Stats.AVG_GS_T #def_t

	Stats.AVG_GM_H = Stats.AVG_GS_T = Stats.GM_H / Stats.MATCHES #avg_goalmade_home
	Stats.AVG_GM_T = Stats.AVG_GS_H = Stats.GM_T / Stats.MATCHES
	Stats.HOME_ADVG = Stats.WON_H / Stats.MATCHES

for team in Squadra.all_squadre:
	calculate_parameters(Squadra.all_squadre[team])

def poisson_random_number(gamma):
	L = math.exp(-gamma)
	k = 0
	p = 1

	while p>L:
		k += 1
		p *= random.random()
	return k - 1

class Campionato:

	year = 0
	classifica = {}

	home_games = [0,0,0]

	def __init__(self, squadre):
		self.squadre = squadre
		self.campionato = self.totale()

		if Campionato.year == 0:
			for squadra in self.squadre:
				Campionato.classifica[squadra] = list()
		else:
			for squadra in self.squadre:
				self.squadre[squadra].points = 0
		Campionato.year += 1

	def andata(self, lista):
		''' Crea un campionato di andata '''
		matches = []
		random.shuffle(lista)

		l1 = lista[0 : int(len(lista)/2)]
		l2 = lista[int(len(lista)/2) : len(lista)+1]

		giornata = []
		for x in range(len(l1)):
			giornata.append(l1[x])
			giornata.append(l2[x])
		matches.append(giornata)

		for n in range(len(lista)-2):
			giornata = []
			l8 = list(l1)
			l9 = list(l2)
			l8[2:len(l1)] = l1[1:len(l1)-1]
			l9[:len(l8)-1] = l2[1:len(l2)]
			l8[1] = l2[0]
			l9[-1] = l1[-1]
			for x in range(len(l8)):
				giornata.append(l8[x])
				giornata.append(l9[x])
			l1 = l8[:]
			l2 = l9[:]
			matches.append(giornata)
			
		return matches

	def ritorno(self, campionato_):
		for giornata in campionato_:
			for i in range(0, 20, 2):
				sq_a = giornata[i]
				sq_b = giornata[i+1]
				giornata[i] = sq_b
				giornata[i+1] = sq_a

		return campionato_

	def totale(self):
		nomi_squadre = list(self.squadre.keys())
		c_andata = self.andata(nomi_squadre)
		c_ritorno = self.ritorno(c_andata)
		return c_andata + c_ritorno

		
	def partita(self, squadra1, squadra2):
		squadra1.home_games += 1
		squadra2.outs_games += 1

		atk_1 = squadra1.atk_h
		atk_2 = squadra2.atk_t
		def_1 = squadra1.def_h
		def_2 = squadra2.def_t


		#questi calcoli di gamma sono molto più realistici di quelli descritti
		#nel paper, quindi uso questi
		gamma_1 = atk_1 * def_2 * Stats.AVG_GM_H# + Stats.HOME_ADVG
		gamma_2 = atk_2 * def_1 * Stats.AVG_GM_T

		goal_1 = poisson_random_number(gamma_1)
		goal_2 = poisson_random_number(gamma_2)

		Stats.GM_H += goal_1
		Stats.GM_T += goal_2

		squadra1.gm_h += goal_1
		squadra2.gs_h += goal_2
		squadra2.gm_t += goal_2
		squadra1.gs_t += goal_1

		#print(goal_1, goal_2)

		if goal_1 > goal_2:
			squadra1.points += 3
			Campionato.home_games[0] += 1
		elif goal_1 < goal_2:
			squadra2.points += 3
			Campionato.home_games[2] += 1
		else:
			squadra1.points += 1
			squadra2.points += 1
			Campionato.home_games[1] += 1

		calculate_parameters(squadra1)
		calculate_parameters(squadra2)

		Stats.MATCHES += 1

		return goal_1, goal_2

	def gioca(self):
		for giornata in self.campionato:
			for i in range(0, 20, 2):
				#print(giornata[i], "-", giornata[i+1], end="\t")
				self.partita(self.squadre[giornata[i]], self.squadre[giornata[i+1]])

		classifica = []
		for squadra in self.squadre:
			classifica.append( [squadra, self.squadre[squadra].points] )

		classifica = sorted(classifica, key=lambda x: x[1], reverse = True)
		for el in classifica:
			print(el)
			Campionato.classifica[el[0]].append( classifica.index(el) + 1)

	def mostra_storico(self):
		for sq in Campionato.classifica:
			print(sq, collections.Counter(Campionato.classifica[sq]).most_common(3))

		print(Campionato.home_games)



#-----------

#campionato_andata = maches(list(Squadra.all_squadre.keys()))
#for giornata in campionato_andata:
#	print(giornata)

#campionato_ritorno = campionato_di_ritorno(campionato_andata)
#campionato = campionato_andata + campionato_ritorno

print("Stats.MATCHES   = ", str(Stats.MATCHES))
print("Stats.HOME_ADVG = ", str(Stats.HOME_ADVG))
print("Stats.TOT_GOALS = ", str(Stats.TOT_GOALS))
print("Stats.AVG_GM_H  = ", str(Stats.AVG_GM_H))
print("Stats.AVG_GM_T  = ", str(Stats.AVG_GM_T))

print("-----------------")

campionato = Campionato(Squadra.all_squadre)
for _ in range(40):
	campionato = Campionato(Squadra.all_squadre)
	campionato.gioca()
	print("_____________")
campionato.mostra_storico()
