import nfldb, json

STAT_STRING_LIST = ['passing_yds', 'passing_tds',  'passing_int', 'rushing_yds','receiving_yds', 'receiving_tds' ,'kickret_tds', 'fumbles_rec_tds', 'fumbles_lost', 'passing_twoptm']	
STAT_STRING_LIST_DEFENSE=['defense_sk', 'defense_int', 'defense_frec', 'defense_safe', 'defense_frec_tds', 'defense_int_tds', 'defense_misc_tds', 'kickret_tds','puntret_tds']
TEAM_NAMES = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAC', 'KC', 'MIA', 'MIN', 'NE', 'NO', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'STL', 'TB', 'TEN', 'WAS', 'NYG', 'NYJ']

	
def showStat(stat_input, team_input, week_input):
	db = nfldb.connect()
	q = nfldb.Query(db)
	q.game(season_year=2012, season_type='Regular',  week=week_input)
	
	
	query_string = stat_input + '__ne'
	query_stat = {}
	query_stat[query_string] = 0;
	query_stat['team'] = team_input
	q.play( **query_stat)
	totals = 0
	for pp in q.as_aggregate():
		totals+= eval('pp.' + stat_input)
		#print pp.player, eval('pp.'+stat_input)
	#print ("Totals Week: " +str(week_input) + " " + team_input + " " + stat_input+ " "+ str(totals) + '\n')
	return totals

def genTeamStatJSON(team_input, week_input):
	statJSON={}
	
	stat_string_list = STAT_STRING_LIST
	stat_season_totals =  [0 for x in range(len(stat_string_list))]
	
	for index in xrange(len(stat_string_list)):
		stat = showStat(stat_string_list[index], team_input, week_input)
		statJSON[stat_string_list[index]] = stat
		stat_season_totals[index] +=stat
	
	#print statJSON
	return statJSON

def genSeasonTeamStat(team_input, weeks):
	statJSON={}
	stat_string_list = STAT_STRING_LIST
	stat_season_totals =  [0 for x in range(len(stat_string_list))]
	stat_season_totals_defense =  [0 for x in range(15)]
	#Open File

	json_data = {}
	
	#Generate JSON
	# For each week generate weekly statistics
	for week in xrange(1,weeks+1):
		#For a given week generate Offensive aggregate stat in stat_string_list		
		for index in xrange(len(stat_string_list)):
			stat = showStat(stat_string_list[index], team_input, week)
			statJSON[stat_string_list[index]] = stat
			stat_season_totals[index] +=stat	
		# compute defense statistics
		defenseJSON = showStatDefense(team_input, week)
		#combine offense and defense
		json_data[week] = dict( statJSON.items() + defenseJSON.items())
		
		#generate defense totals
		list_defense = defenseJSON.items()				
		for index in xrange(len(list_defense)):
			stat_season_totals_defense[index] += list_defense[index][1]
					
	
	#Aggregate Statistics 
	statJSON= {}
	statTotals = {}		
		# Generate Offensive Averages for season across all weeks
	for index in xrange(len(stat_string_list)):			
		statTotals[stat_string_list[index]] = stat_season_totals[index]			
		statJSON[stat_string_list[index]] = stat_season_totals[index]/float(weeks-1)

		
		#Generate Defensive Season Statistics 
	defense_keys = defenseJSON.keys()
	for index in xrange(len(defense_keys)):
		statTotals[defense_keys[index]] = stat_season_totals_defense[index]		
		statJSON[defense_keys[index]] = stat_season_totals_defense[index]/ float(weeks-1)		

	json_data['AVG']= statJSON
	json_data['TOTAL']=statTotals		
	#print (statJSON)		
	#Write to File and Close
	# json_write = open('seasonStatistics.json','w')
	# json_write.write(json.dumps(json_data))
	# json_write.close()
	return json_data
	
def readSeasonStat():
	json_file = open ('seasonStatistics.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data

def printSeason(json_data, weeks):
	# for key,value in json_data.items():
		# print key, value
	print "[[[[[[SEASON AVERAGE]]]]]]]"
	list = json_data['AVG'].items()	
	print list
	
	print "[[[[[[SEASON TOTALS]]]]]]]"
	list = json_data['TOTAL'].items()	
	print list
	for index in xrange(1,weeks+1):
		print 'Week' + str(index) + '>>>>>>>>>>>>>>>>>>>>>'
		for stuff in json_data[unicode(str(index))].items():
			print stuff[0],stuff[1]

def printSeasonTotals(json_data):
	print "[[[[[[SEASON AVERAGE]]]]]]]"
	list = json_data['AVG'].items()	
	for index in xrange(len(list)):
		print list[index][0], list[index][1]
		
	print "[[[[[[SEASON TOTALS]]]]]]]"
	list = json_data['TOTAL'].items()	
	for index in xrange(len(list)):
		print list[index][0], list[index][1]

			

def searchPlayer(player_name, position_name):
	db = nfldb.connect()
	player, dist = nfldb.player_search(db, player_name, position=position_name)
	print 'Similarity score: %d, Player: %s' % (dist, player)
	return player
	
	
def showPlayerStat(player_ID, week_input):
	statJSON={}	
	stat_string_list = STAT_STRING_LIST
	
	db = nfldb.connect()
	q = nfldb.Query(db)
		
	q.game(season_year=2012, season_type='Regular',  week=week_input)	
	q.player(player_id=player_ID)
	
	# for p in q.sort([('gsis_id', 'asc'), ('time', 'asc')]).as_plays():
		# print p	
	
	for p in q.as_aggregate():
		
		for index in xrange(len(stat_string_list)):
			key = stat_string_list[index]
			value = eval('p.'+stat_string_list[index])
			statJSON[key]=value
			#print key, value
	#Check for empty week stat due to BYE week
	if len(q.as_aggregate() )==0:
		for index in xrange(len(stat_string_list)):
			key = stat_string_list[index]			
			statJSON[key]=0	
	return statJSON

def genPlayerSeasonJSON(player_ID, weeks):
	statJSON={}
	stat_string_list = STAT_STRING_LIST
	stat_season_totals =  [0 for x in range(len(STAT_STRING_LIST))]
	
	for index in xrange(1,weeks +1):
		stat = showPlayerStat(player_ID, index)
		statJSON[index] = stat		
		for counter in xrange(len(stat_string_list)):
			stat_season_totals[counter] +=stat[stat_string_list[counter]]
	
	statAVG= {}
	statTotals = {}
	
	for index in xrange(len(stat_string_list)):			
		statTotals[stat_string_list[index]] = stat_season_totals[index]			
		statAVG[stat_string_list[index]] = stat_season_totals[index]/float(weeks-1)
	statJSON['AVG']= statAVG
	statJSON['TOTAL']=statTotals
		
	#print statJSON
	return statJSON

	
def showStatDefense(team_input, week_input):
	statJSON = {}
	#STAT_STRING_LIST_DEFENSE=['defense_sk', 'defense_int', 'defense_frec', 'defense_safe', 'defense_frec_tds', 'defense_int_tds', 'defense_misc_tds', 'kickret_tds']
	stat_string_list = STAT_STRING_LIST_DEFENSE	
	stat_season_totals =  [0 for x in range(len(stat_string_list))]
	#stat_string_list = ['puntret_tds']	
	db = nfldb.connect()
	q = nfldb.Query(db)
	q.game(season_year=2012, season_type='Regular',  week=week_input, team=team_input)
		
	for p in q.as_games():				
		if p.away_team == team_input:
			statJSON['points_allowed']= p.home_score
		else:
			statJSON['points_allowed']= p.away_score
	
	#check for bye week all stats = 0
	if len(q.as_games())==0:
		team_home_away = 'bye'
		for index in xrange(len(stat_string_list)):
			statJSON[stat_string_list[index]] = 0
			return statJSON
	
	for index in xrange(len(stat_string_list)):
			stat = showStat(stat_string_list[index], team_input, week_input)
			statJSON[stat_string_list[index]] = stat
			#stat_season_totals[index] +=stat	
	
	statJSON['defense_touchdowns'] = statJSON['defense_int_tds'] + statJSON['defense_frec_tds'] + statJSON['defense_misc_tds']
	#	for key, index in statJSON.items():	
		#print ("Totals Week: " +str(week_input) + " " + team_input + " " + key+ " "+ str(index) + '\n')	
	return statJSON

def allTeamStatistics():
	team_names = TEAM_NAMES
	json_data = {}
	
	for index in xrange(len(team_names)):		
		team = team_names[index]
		print "Generating", team
		json_data[team] = genSeasonTeamStat(team,17)
			
	json_write = open('teamSeasonStatistics.json','w')
	json_write.write(json.dumps(json_data))
	json_write.close()	

def readTeamSeasonStat():
	json_file = open ('teamSeasonStatistics.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data	
	
def readFFRoster():
	txt_file = open ('FFTeams.txt', 'r')
	json_data = {}
	json_team = {}
	counter = 0
		
	for line in txt_file:
		read_word = line.strip()		
		words = read_word.split('\t')				
		if(words[0] =="TEAM"):
			print "Team: ", words[1], " has players: "
			team = words[1]
			json_data[team] = {}
			json_team = {}
			counter = 0
		else:
			print "Player", words[1], " at position: ", words[0]		
			player = {}
			player['player_name'] = words[1]
			player['position'] = words[0]
			print player
			json_team[str(counter)] = player
			counter+=1
			json_data[team]= json_team
	
	txt_file.close()
	
	json_write = open('ffTeamsJSON.json','w')
	json_write.write(json.dumps(json_data))
	json_write.close()	
	#print json_data
	#return json_data

def readFFTeams():
	json_file = open ('../Data/ffTeamsJSON.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data	

def readFFTeamsStats():
	json_file = open ('../Data/ffTeamsStatsJSON.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data		
	
def createSeasonPlayerStats():
	ff_league = readFFTeams()
	
	for key_team, team in ff_league.iteritems():
		print key_team
	
		for key, player in  team.iteritems():
			#print key, player
			#print player['position'], player['player_name']
			if( player['position'] != "DEF"):
				player_search = searchPlayer(player['player_name'], player['position'])
				stats = genPlayerSeasonJSON(player_search.player_id, 17)
				player['stats']= stats
			else:
				stat = genSeasonTeamStat(player['player_name'],17)
				player['stats'] = stat
			
	#print team_object
	json_write = open('ffTeamsStatsJSON.json','w')
	json_write.write(json.dumps(ff_league))
	json_write.close()	

		
def main():
	
	#genSeasonTeamStat('SEA',17)
	#printSeason(readSeasonStat(),17)
	#player =  searchPlayer('Brees', 'QB')	
	#print showPlayerStat(player.player_id, 1)
	
	#>>>>>>>>>>>> Player Testing
	#player =  searchPlayer('Brady', 'QB')	
	#print showPlayerStat(player.player_id, 9)	
	#temp1 = genPlayerSeasonJSON(player.player_id,17)	
	#temp = genPlayerSeasonJSON(player.player_id,17)	.items()	
	# for counter in xrange(len(temp)):
		# print temp[counter]
	
	createSeasonPlayerStats()
	#readFFRoster()
	#>>>>>>>>>>>> Defense Stat
	#showStatDefense( 'SF', 15)
	#genSeasonTeamStat('ARI',17)
	#printSeason(readSeasonStat(),3)
	#printSeasonTotals(readSeasonStat())
	#allTeamStatistics()
if __name__ == "__main__":
	main()
