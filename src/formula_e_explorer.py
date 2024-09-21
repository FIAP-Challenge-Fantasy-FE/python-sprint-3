import json

# Constants for menu choices
MENU_OPTIONS = {
    '1': 'view_driver_standings',
    '2': 'view_team_standings',
    '3': 'view_race_results',
    '4': 'compare_drivers',
    '5': 'view_season_calendar',
    '6': 'view_driver_profile',
    '7': 'search_races_by_location',
    '8': 'exit_program'
}

def load_data(filename='formula_e_data.json'):
    """
    Loads Formula E data from a JSON file.
    Returns a dictionary containing seasons, drivers, teams, and race results.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

# Data Access Functions
def get_entity_name(data, entity_type, entity_id):
    """
    Returns the name of an entity (driver or team) given its ID.
    """
    return data[entity_type][entity_id]['name']

def get_entity_profile(data, entity_type, entity_id):
    """
    Returns the profile information of an entity (driver or team).
    """
    return data[entity_type][entity_id]

def find_entity_id_by_name(data, entity_type, name):
    """
    Finds and returns the entity ID given the entity's name.
    """
    for entity_id, info in data[entity_type].items():
        if info['name'].lower() == name.lower():
            return entity_id
    return None

def get_season_data(data, season):
    """
    Returns the data for a specific season.
    """
    return data['seasons'].get(season)

def get_standings(data, season, standings_type):
    """
    Returns the standings (drivers or teams) for a given season.
    """
    season_data = get_season_data(data, season)
    if season_data:
        return season_data['standings'][standings_type]
    return None

def get_races(data, season):
    """
    Returns the races for a given season.
    """
    season_data = get_season_data(data, season)
    if season_data:
        return season_data['races']
    return None

def get_race(data, season, race_name):
    """
    Returns a specific race from a season.
    """
    races = get_races(data, season)
    if races:
        return races.get(race_name)
    return None

def search_races(data, location):
    """
    Searches and returns races that took place in a specific location.
    """
    results = []
    for season_key, season_info in data['seasons'].items():
        for race_name, race_info in season_info['races'].items():
            if location.lower() in race_info['location'].lower():
                results.append({
                    'season': season_key,
                    'race_name': race_name,
                    'date': race_info['date']
                })
    return results

def calculate_total_points(data, driver_id):
    """
    Calculates the total points for a driver across all seasons.
    """
    total_points = 0
    for season_info in data['seasons'].values():
        for driver in season_info['standings']['drivers']:
            if driver['driver_id'] == driver_id:
                total_points += driver['points']
    return total_points

# Action Functions
def view_driver_standings(data):
    season = input("Enter the season (e.g., '2019-2020'): ")
    standings = get_standings(data, season, 'drivers')
    if standings:
        print(f"\nDriver Standings for {season}:")
        for i, driver in enumerate(standings):
            driver_name = get_entity_name(data, 'drivers', driver['driver_id'])
            print(f"{i+1}. {driver_name} - {driver['points']} points")
    else:
        print("Season not found.")

def view_team_standings(data):
    season = input("Enter the season (e.g., '2019-2020'): ")
    standings = get_standings(data, season, 'teams')
    if standings:
        print(f"\nTeam Standings for {season}:")
        for i, team in enumerate(standings):
            team_name = get_entity_name(data, 'teams', team['team_id'])
            print(f"{i+1}. {team_name} - {team['points']} points")
    else:
        print("Season not found.")

def view_race_results(data):
    season = input("Enter the season (e.g., '2019-2020'): ")
    race_name = input("Enter the race name (e.g., 'Diriyah E-Prix'): ")
    race = get_race(data, season, race_name)
    if race:
        print(f"\nResults for {race_name} in {season}:")
        for result in race['results']:
            position = result['position']
            driver_name = get_entity_name(data, 'drivers', result['driver_id'])
            team_name = get_entity_name(data, 'teams', result['team_id'])
            points = result['points']
            print(f"{position}. {driver_name} ({team_name}) - {points} points")
    else:
        print("Race or season not found.")

def compare_drivers(data):
    driver_name1 = input("Enter the first driver's name: ")
    driver_id1 = find_entity_id_by_name(data, 'drivers', driver_name1)
    if not driver_id1:
        print(f"Driver '{driver_name1}' not found.")
        return
    driver_name2 = input("Enter the second driver's name: ")
    driver_id2 = find_entity_id_by_name(data, 'drivers', driver_name2)
    if not driver_id2:
        print(f"Driver '{driver_name2}' not found.")
        return
    points1 = calculate_total_points(data, driver_id1)
    points2 = calculate_total_points(data, driver_id2)
    print(f"\nComparing {driver_name1} and {driver_name2}:")
    print(f"{driver_name1} total points: {points1}")
    print(f"{driver_name2} total points: {points2}")
    if points1 > points2:
        print(f"{driver_name1} has more points.\n")
    elif points1 < points2:
        print(f"{driver_name2} has more points.\n")
    else:
        print("Both drivers have equal points.\n")

def view_season_calendar(data):
    season = input("Enter the season (e.g., '2019-2020'): ")
    races = get_races(data, season)
    if races:
        print(f"\nRace Calendar for {season}:")
        for race_name, race_info in races.items():
            print(f"{race_info['date']}: {race_name}")
    else:
        print("Season not found.")

def view_driver_profile(data):
    driver_name = input("Enter the driver's name: ")
    driver_id = find_entity_id_by_name(data, 'drivers', driver_name)
    if driver_id:
        profile = get_entity_profile(data, 'drivers', driver_id)
        team_name = get_entity_name(data, 'teams', profile['team_id'])
        print(f"\nDriver Profile: {profile['name']}")
        print(f"Nationality: {profile['nationality']}")
        print(f"Team: {team_name}")
    else:
        print("Driver not found.")

def search_races_by_location(data):
    location = input("Enter the location to search for races: ")
    races = search_races(data, location)
    if races:
        print(f"\nRaces in '{location}':")
        for race in races:
            print(f"{race['date']} - {race['race_name']} ({race['season']})")
    else:
        print("No races found at that location.")

def exit_program(data):
    print("Thank you for using the Formula E Fan Explorer!")
    exit(0)

def invalid_choice(data):
    print("Invalid choice. Please try again.")

# Main Function
def main():
    """
    Main function to run the interactive command-line interface.
    """
    data = load_data()
    actions = {
        'view_driver_standings': view_driver_standings,
        'view_team_standings': view_team_standings,
        'view_race_results': view_race_results,
        'compare_drivers': compare_drivers,
        'view_season_calendar': view_season_calendar,
        'view_driver_profile': view_driver_profile,
        'search_races_by_location': search_races_by_location,
        'exit_program': exit_program
    }

    while True:
        print("\nWelcome to the Formula E Fan Explorer!")
        print("Choose an option:")
        for key, action in MENU_OPTIONS.items():
            description = action.replace('_', ' ').title()
            print(f"{key}. {description}")
        choice = input("Enter your choice: ")
        action_name = MENU_OPTIONS.get(choice, 'invalid_choice')
        action = actions.get(action_name, invalid_choice)
        action(data)

if __name__ == '__main__':
    main()