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

def readFFTeamsStats():
	json_file = open ('../Data/ffTeamsStatsJSON.json', 'r')
	json_data = json.load(json_file)
	season_json = {}
			
	json_file.close()
	return json_data		
	
def main():
	allTeamStatistics()
if __name__ == "__main__":
	main()
