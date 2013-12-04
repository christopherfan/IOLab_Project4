import json

def readTeamSeasonStat():
	json_file = open ('../Data/teamSeasonStatistics.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data	

def readFFTeams():
	json_file = open ('../Data/ffTeamsJSON.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data	

def generateTeamStatCSV():
	json_data = readTeamSeasonStat()
	string_array = []
	array = []
	counter = 0
	
	for key_team, value_team in json_data.iteritems():		
		#print key_team
		string_array = []		
		for key_week, value_week in value_team.iteritems():
			#print key_week
			string = key_team + ','+key_week+','
			string_array.append(string)
			stat_names = ','.join(value_week.keys())
			stats = ','.join(str(x) for x in value_week.values())
			array.append(string + stats+'\n')
	header_string = 'team_name' +','+'week'+ ','+stat_names	+'\n'
		
	file_write = open('teamCSV.txt','w')
	print header_string
	file_write.write(header_string)
	for lines in array:	
		print lines
		file_write.write(lines)
	file_write.close()			
	
	
def readFFTeamsStats():
	json_file = open ('../Data/ffTeamsStatsJSON.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data		
	
def main():
	generateTeamStatCSV()
	
if __name__ == "__main__":
	main()
