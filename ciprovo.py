f = open("1-premierleague.csv", "r")
f_out = open("tables.csv", "w")



import random, math

'''
Squadra[nome] = [
0 --> gm_h
1 --> gm_t
2 --> gs_h
3 --> gs_t
4 --> atk_h
5 --> atk_t
6 --> def_h
7 --> def_t
8 --> punti_camionato
]
'''

GM_H = 0 #goals made at home
GM_T = 0 #goals made at transfert
TOT_GOALS = 0 #sum of all goals
N_MATCHS = 0 #total number of matches
WON_H = 0 #vinte in casa
HOME_ADVG = 0

SQUADRE = {}
HOME_GAMES = 19
OUTS_GAMES = 20

def parser(f):
	'''Dato un file csv, estrapola tutte le info necessarie. '''
	global N_MATCHS
	global TOT_GOALS
	global GM_H
	global GM_T
	global SQUADRE
	global WON_H 
		
	for line in f:
		
		if N_MATCHS != 0: #se non è la riga introduttiva
			tokens = line.split(",")

			home_team = tokens[1] #nome squadre
			outs_team = tokens[2]
				

			goals = tokens[3].split("-")
			home_goals = int(goals[0])
			outs_goals = int(goals[1])
			tot_goals = home_goals + outs_goals #tot goals della partita

			TOT_GOALS += tot_goals #aggiunge alle variabili "globali"
			GM_H += home_goals
			GM_T += outs_goals

			if home_team not in SQUADRE.keys(): #nel caso non ci sia la squadra in SQUADRE
				SQUADRE[home_team] = [0 for _ in range(9)]
			if outs_team not in SQUADRE.keys():
				SQUADRE[outs_team] = [0 for _ in range(9)]
				
			SQUADRE[home_team][0] += home_goals #gol fatti in casa
			SQUADRE[home_team][2] += outs_goals #gol fatti fuori casa
			SQUADRE[outs_team][1] += outs_goals #gol subiti in casa
			SQUADRE[outs_team][3] += home_goals #gol subiti fuori casa

			if home_goals > outs_goals:
				WON_H += 1
				

		N_MATCHS += 1


parser(f)

print("\nAVG_GM_H:" + str(GM_H/N_MATCHS))
print("AVG_GM_T:" + str(GM_T/N_MATCHS))
print("TOT_GOALS:" + str(TOT_GOALS))
print("AVG_GxMATCH:" + str(TOT_GOALS/N_MATCHS))
print("HOME ADVANTAGE PARAMETER:" + str(WON_H/N_MATCHS))
print(SQUADRE)

f_out.write("TEAM,GM_H,GM_T,GS_H,GS_T\n")
for sq in SQUADRE.keys():
	str_list = str(SQUADRE[sq])
	f_out.write(sq + "," + str_list.replace("[", "").replace("]", "").replace(", ", ",") + "\n")
	
# --------

AVG_GM_H = AVG_GS_T = GM_H/N_MATCHS #avg_goalmade_home
AVG_GM_T = AVG_GS_H = GM_T/N_MATCHS
HOME_ADVG = WON_H/N_MATCHS

def calculate_parameters(team):
	team[4] = (team[0] / HOME_GAMES) / AVG_GM_H #atk_h
	team[5] = (team[1] / OUTS_GAMES) / AVG_GM_T #atk_t
	team[6] = (team[2] / HOME_GAMES) / AVG_GS_H #def_h
	team[7] = (team[3] / OUTS_GAMES) / AVG_GS_T #def_t
	
for team in SQUADRE.keys():
	calculate_parameters(SQUADRE[team])

def poisson_random_number(gamma):
	L = math.exp(-gamma)
	k = 0
	p = 1

	while p>L:
		k += 1
		p *= random.random()
	return k - 1
	
def partita(squadra1, squadra2):
	atk_1 = squadra1[4]
	atk_2 = squadra2[5]
	def_1 = squadra1[6]
	def_2 = squadra2[7]

	#questi calcoli di gamma sono molto più realistici di quelli descritti
	#nel paper, quindi uso questi
	#gamma_1 = atk_1*def_2*AVG_GM_H + HOME_ADVG
	#gamma_2 = atk_2*def_1*AVG_GM_T

	gamma_1 = math.exp(atk_1-def_2+HOME_ADVG)
	gamma_2 = math.exp(atk_2-def_1)

	goal_1 = poisson_random_number(gamma_1)
	goal_2 = poisson_random_number(gamma_2)

	print(goal_1, goal_2)
	
	table = [[0.0 for x in range(6)] for _ in range(2)]
	
	#for x in range(6):
	#	table[0][x] = math.exp(-gamma_1) * math.pow(gamma_1, x) / math.factorial(x)
	#	table[1][x] = math.exp(-gamma_2) * math.pow(gamma_2, x) / math.factorial(x)

	
	#for line in table:
	#	for el in line:
	#		print("%.4f" % el, end = ", ")
	#	print()

	#goal_1 = table[0].index(max(table[0]))
	#goal_2 = table[1].index(max(table[1]))

	if goal_1 > goal_2:
		squadra1[8] += 3
	elif goal_1 < goal_2:
		squadra2[8] += 3
	else:
		squadra1[8] += 1
		squadra2[8] += 1
		
	#print(max(table[0]), str(table[0].index(max(table[0]))))
	#print(max(table[1]), str(table[1].index(max(table[1]))))

	calculate_parameters(squadra1)
	calculate_parameters(squadra2)

#-------

def fixtures(teams):  
    #if len(teams) % 2:
    #   teams.append(Squadra('Day off'))  
	# if team number is odd - use 'day off' as fake team     

    rotation = list(teams)       # copy the list

    fixtures = []
    for i in range(0, len(teams)-1):
        fixtures.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
    return fixtures

def campionato_di_ritorno(campionato):
	for giornata in campionato:
		for i in range(0, 20, 2):
			sq_a = giornata[i]
			sq_b = giornata[i+1]
			giornata[i] = sq_b
			giornata[i+1] = sq_a

	return campionato
	
campionato_andata = fixtures(SQUADRE.keys())
campionato_ritorno = campionato_di_ritorno(campionato_andata)
campionato = campionato_andata + campionato_ritorno

for giornata in campionato:
	print(giornata)
print(str(len(campionato)))

for giornata in campionato:
	for i in range(0, 20, 2):
		print(giornata[i], "-", giornata[i+1], end="\t")
		partita(SQUADRE[giornata[i]], SQUADRE[giornata[i+1]])

classifica = []
for squadra in SQUADRE.keys():
	classifica.append( [squadra, SQUADRE[squadra][8]] )

print(sorted(classifica, key=lambda x: x[1]))
	
