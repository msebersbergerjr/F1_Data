import os
from tqdm import tqdm
import requests, json, pandas as pd, numpy as np
from requests.models import HTTPError
from os.path import exists
from datetime import datetime, timedelta

def pr_red(text): print(f"\033[91m{text}\033[00m")
def pr_light_purple(text): print(f"\033[94m{text}\033[00m")
def pr_yellow(text): print(f"\033[93m{text}\033[00m")

def clear_screen():
    '''
    Clear the terminal screen for a cleaner look
    Cross-Platform by checking if the machine is a windows or unix system
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_input():
    '''Pause CLI until user inputs anything'''
    cmd = input(":: --> ")

def connection(url):
    '''
    Try and Establish a Connection to given website
    Return: data in json format
    '''

    try:
        response = requests.get(url)
        
        if not response.status_code // 100 == 2:
            return("Error: Unexpected response {}".format(response))

        geodata = response.json()
        return(geodata)

    except requests.exceptions.RequestException as e:
        return("Error: {}".format(e))

def search_query(db,col,q):
    '''
    Search Query Functiuon
    db = Table to search in under Data/
    col = column name we are searching through
    q = search item
    '''

    df = pd.read_csv(r'Data/{}.csv'.format(db))

    try:
        result = df.query(f'{col} == "{q}"',)
        status = "Match"

        # Return Likeness of search Query
        if result.empty:
            
            result = df.query(f'{col}.str.contains("{q}", case=False)', engine='python')
            status = "Close Match"

            # No matches were found
            if result.empty:
                result = "\033[91mError: No Matches Found\033[00m"
                status = "No Match"
        
    except KeyError:
        result = "Error"

    # Delete Dataframe
    del result

    return status,result

def get_table(table):
    '''
    Determine which csv needs to be created
    '''

    if table == 'Driver_Table.csv':
        get_drivers()

    elif table == 'Team_Table.csv':
        get_teams()

    elif table == 'Circuit_Table.csv':
        get_circuit()

    elif table == 'Current_Table.csv':
        get_current()

    elif table == 'First_Table.csv':
        get_first()

    elif table == 'Team_History_Table.csv':
        get_team_history()

    elif table == 'Race_History_Table.csv':
        print('WIP')

def get_drivers():
    '''
    Get every driver to ever drive for F1
    '''

    pr_light_purple(f'{"Acquiring Drivers": ^35}')
    pr_light_purple("----------------------------------------")

    # Create Data Table
    column_names = ["driver_id", "race_number", "given_name", "family_name", "dob", "nationality"]
    df_driver = pd.DataFrame(columns=column_names)

    # Fetch all information from API
    data = connection('http://ergast.com/api/f1/drivers.json?limit=1000')
    drivers = data['MRData']['DriverTable']['Drivers']

    # Iterate though all drivers
    for _ in drivers:
        driver_id = _['driverId']
        given_name = _['givenName']
        family_name = _['familyName']
        dob = _['dateOfBirth']
        nationality = _['nationality']
        
        df_driver = df_driver.append({'driver_id': driver_id, 'given_name': given_name, 'family_name': family_name, 'dob': dob, 'nationality': nationality}, ignore_index=True)

    # Export
    df_driver.to_csv(r'Data/Driver_Table.csv', encoding='utf-8', index=False)

    # Delete Dataframe
    del df_driver

def get_circuit():
    '''
    Get every circuit driven ini F1
    '''

    pr_light_purple(f'{"Acquiring Circuits": ^35}')
    pr_light_purple("----------------------------------------")

    # Create Data Table
    column_names = ["circuit_id", "circuit_name", "location", "country"]
    df_circuit = pd.DataFrame(columns=column_names)

    # Fetch all information from API
    data = connection('http://ergast.com/api/f1/circuits.json?limit=1000')
    circuits = data['MRData']['CircuitTable']['Circuits']

    # Iterate though all drivers
    for _ in circuits:
        circuit_id = _['circuitId']
        circuit_name = _['circuitName']
        location = _['Location']['locality']
        country = _['Location']['country']
        
        df_circuit = df_circuit.append({'circuit_id': circuit_id, 'circuit_name': circuit_name, 'location': location, 'country': country}, ignore_index=True)

    # Export
    df_circuit.to_csv(r'Data/Circuit_Table.csv', encoding='utf-8', index=False)

    # Delete Dataframe
    del df_circuit

def get_teams():
    '''
    Get every Team to be in the F1
    '''

    pr_light_purple(f'{"Acquiring Teams": ^35}')
    pr_light_purple("----------------------------------------")

    # Create Data Table
    column_names = ["team_id", "team_name", "nationality"]
    df_teams = pd.DataFrame(columns=column_names)

    # Fetch all information from API
    data = connection('http://ergast.com/api/f1/constructors.json?limit=1000')
    teams = data['MRData']['ConstructorTable']['Constructors']

    # Iterate though all drivers
    for _ in teams:
        team_id = _['constructorId']
        team_name = _['name']
        nationality = _['nationality']
        
        df_teams = df_teams.append({'team_id': team_id, 'team_name': team_name, 'nationality': nationality}, ignore_index=True)

    # Export
    df_teams.to_csv(r'Data/Team_Table.csv', encoding='utf-8', index=False)

    # Delete Dataframe
    del df_teams

def get_current():
    '''
    Current
    id(PK) | driver_id(FK) | team_id(FK) | permanent_number | position | points | wins |
    link : 'http://ergast.com/api/f1/current/driverStandings.json'
    '''
    print("Fetching Current Drivers")
    # Create Data Table
    column_names = ["driver_id", "team_id", "points"]
    df_curr = pd.DataFrame(columns=column_names)

    # Fetch all information from API
    data = connection('http://ergast.com/api/f1/current/driverStandings.json')
    curr = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    # Iterate though all drivers
    for i in curr:
        driver_id = i["Driver"]['driverId']
        team_id = i['Constructors'][0]['constructorId']
        permanent_number = i['Driver']['permanentNumber']
        position = i['position']
        points = i['points']
        wins = i['wins']
        
        df_curr = df_curr.append({'driver_id': driver_id, 'team_id': team_id, 'position': position, 'points': points, 'wins': wins}, ignore_index=True)

    # Export
    df_curr.to_csv(r'Data/Current_Table.csv', encoding='utf-8', index=False)

    # Delete Dataframe
    del df_curr

def get_first():
    '''
    1st place Time
    id(PK) | season | round | circuit_id(FK) | time | driver_id(FK) | 
    '''
    print("Fetching 1st place time for every race")

    # Create Data Table
    column_names = ["season", "round", "circuit_id", "time", "driver_id"]
    df_first = pd.DataFrame(columns=column_names)

    for year in range(1950, 2022):
        # Fetch all information from API
        data = connection(f'http://ergast.com/api/f1/{year}/results.json?limit=1000')
        
        first_results = data['MRData']['RaceTable']['Races']

        for i in first_results:
            season = int(i['season'])
            rround = int(i['round'])
            circuit_id = i['Circuit']['circuitId']
            time = i['Results'][0]['Time']['time']
            driver_id = i['Results'][0]['Driver']['driverId']

            df_first = df_first.append({'season': season, 'round': rround, 'circuit_id': circuit_id, 'time': time, 'driver_id': driver_id, }, ignore_index=True)

    # Sort by Year then round Decending
    df_first = df_first.sort_values(['season', 'round'], ascending=[False, False])

    #Export
    df_first.to_csv(r'Data/First_Table.csv', encoding='utf-8', index=False)

    # Delete Dataframe
    del df_first

def get_team_history():
    '''
    Team History
    id(PK) | season | team_id(FK) | position | points | wins
    link: 'http://ergast.com/api/f1/{year}/constructorStandings.json'
    '''
    print("Fetching Team History")
    # Create Data Table
    column_names = ["season", "team_id", "position", "points", "wins"]
    df_team_his = pd.DataFrame(columns=column_names)

    # Iterate though entire history of F1
    for year in range(1950, 2022):
        # Fetch all information from API
        data = connection(f'http://ergast.com/api/f1/{year}/constructorStandings.json?limit=1000')
        try:
            team_hist = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

            # Iterate though all teams
            for i in team_hist:
                season = year
                team_id = i['Constructor']['constructorId']
                position = i['position']
                points = i['points']
                wins = i['wins']

                df_team_his = df_team_his.append({'season': season, 'team_id': team_id, 'position': position, 'points': points, 'wins': wins}, ignore_index=True)
        except IndexError:
            pass

    # Export
    df_team_his.to_csv(r'Data/Team_History_Table.csv', encoding='utf-8', index=False)

    # Delete Dataframe
    del df_team_his

def get_race_history():
    '''
    Merge all the Driver Response Responses into one csv
    '''

    arr = []

    for _ in range(1, 9):
        if _ == 1:
            arr.append(pd.read_csv('Driver_Responses/Response_' + str(_) + '.csv'))
        else:
            arr.append(pd.read_csv('Driver_Responses/Response_' + str(_) + '.csv'))

    arr.append(pd.read_csv(r'Driver_Responses/Response_Missing.csv'))

    df = pd.concat(arr)

    df.to_csv('Data/Race_History_Table.csv')

    # Delete Dataframe
    del df

def true_time():
    '''
    Get the True Time of a race result in the Race History Table
    Create a new column named "True Time"
    Where we add on the time the driver finished to the driver who finished 1st
    As of now I dont have a answer for drivers who:
        Get Lapped
        DNF
    '''

    # Load driver Dataframe
    df_drivers = pd.read_csv(r'Data/Driver_Table.csv')
    drivers = df_drivers.loc[:, 'driver_id']

    # Load 1st place Dataframe
    df_first = pd.read_csv(r'Data/First_Table.csv')

    # Load Race History Table
    hist_table = pd.read_csv(r'Data/Race_History_Table.csv')

    # Initalize
    hist_table['true_time'] = ""

    # Get Drivers true time for every race
    hist_table['true_time'] = hist_table[['driver_id', 'season', 'round', 'time']].apply(lambda x: get_race_time(*x), axis=1)

    # Drop Time Column from original csv
    hist_table.drop(labels=['time'], axis=1, inplace=True)

def convertHours(raw_time):
    ''' Format H:M:S:Micro '''
    dirty_time = datetime.strptime(raw_time,'%I:%M:%S.%f').time()
    clean_time = timedelta(hours=dirty_time.hour, minutes=dirty_time.minute, seconds=dirty_time.second, microseconds=dirty_time.microsecond)
    return clean_time

def convertMinute(raw_time):
    ''' Format M:S:Micro '''
    dirty_time = datetime.strptime(raw_time,'%M:%S.%f').time()
    clean_time = timedelta(minutes=dirty_time.minute, seconds=dirty_time.second, microseconds=dirty_time.microsecond)
    return clean_time

def convertSeconds(raw_time):
    ''' Format S:Micro '''
    dirty_time = datetime.strptime(raw_time, '%S.%f').time()
    clean_time = timedelta(seconds=dirty_time.second, microseconds=dirty_time.microsecond)
    return clean_time

def get_race_time(driver_id, season, rd, time) -> any:
    '''
    Convert drivers + time to a true time
    '''

    # Time doesn't Exist
    # Ex: +1 Lap, Engine, Throttle etc...
    # For now make it time of 0.0
    if type(time) == float:
        clean_time = timedelta(seconds=0, microseconds=0)
        return str(clean_time)

    # Race winner
    winner_frame = (df_first.loc[(df_first['season'] == season) & (df_first['round'] == rd)])[['time', 'driver_id', 'season', 'round']]

    if winner_frame.iloc[0,0].count(':') == 2:

        # Rare case hours is 0 in the time
        try:
            clean_winner_time = convertHours(winner_frame.iloc[0,0])
        
        except ValueError:
            # Remove the 0 in the hour slot
            bad_time = winner_frame.iloc[0,0]
            better_time = bad_time[2:]

            clean_winner_time = convertMinute(better_time)

    elif winner_frame.iloc[0,0].count(':') == 1:
        clean_winner_time = convertMinute(winner_frame.iloc[0,0])
    
    else:
        clean_winner_time = convertSeconds(winner_frame.iloc[0,0])
    

    # print(type(time), time)

    if winner_frame.iloc[0,1] == driver_id:
        # need to format to actual time later
        return str(clean_winner_time)

    elif '+' in time:

        dirty_time = time[1:]

        # Rare case 's' or 'sec' is in the time
        if 'sec' in dirty_time:
            dirty_time = dirty_time[:-4]

        elif 's' in dirty_time:
            dirty_time = dirty_time[:-1]

        # Formatting of the time
        if ':' in dirty_time:
            # min, sec, micro
            clean_time = convertMinute(dirty_time)

        else:

            try:
                # sec, micro
                clean_time = convertSeconds(dirty_time)


            except ValueError:
                # Rare case Min is => 60
                #print(dirty_time)

                # Separate Seconds and Millseconds
                sec, mill = map(int,dirty_time.split('.'))

                # Get decimal value of Minute and second
                convert = str(round(sec/60,1))

                # Separate Minutes and Seconds
                min, sec = map(int, convert.split('.'))

                # Format into readable time
                new_time = f'{min}:{sec}.{mill}'

                clean_time = convertMinute(new_time)


        # Combine Winner time with driver time
        total_time = str(clean_winner_time + clean_time)
        return total_time

def initalize():
    '''
    Check if Data csv need to be created or not
    '''

    # Check Data Folder
    tables = {'Driver_Table.csv','Team_Table.csv','Circuit_Table.csv','Current_Table.csv','First_Table.csv','Team_History_Table.csv','Race_History_Table.csv'}

    for _ in tables:

        if not exists(r'Data/{}'.format(_)):
            get_table(_)

    # Check Driver Requests folder

    dir = os.listdir("Driver_Requests")

    if(len(dir)) != 8:

        # Data frame of all drivers
        driver_table = pd.read_csv('Data/Driver_Table.csv')

        # Filter all Unique drivers into a list
        udriver = driver_table['driver_id'].unique()

        # Break Down entire list of Drivers into 8 groups
        for _ in range(1, 9):
            if _ == 1:
                drivers = udriver[0:_*106]
                pd.Series(drivers).to_csv('Driver_Requests/Request_' + str(_) + '.csv')
            elif _ == 8:
                drivers = udriver[743:853]
                pd.Series(drivers).to_csv('Driver_Requests/Request_' + str(_) + '.csv')
            else:
                drivers = (udriver[(_-1)*106+1:_*106])
                pd.Series(drivers).to_csv('Driver_Requests/Request_' + str(_) + '.csv')

    main()


def main():
    '''
    Main Menu
    '''

    while True:
        clear_screen()
        pr_red('\n__/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\______/\\\\\\')        
        pr_red(' _\\/\\\\\\///////////___/\\\\\\\\\\\\\\')       
        pr_red('  _\\/\\\\\\_____________\\/////\\\\\\')      
        pr_red('   _\\/\\\\\\\\\\\\\\\\\\\\\\_________\\/\\\\\\')     
        pr_red('    _\\/\\\\\\///////__________\\/\\\\\\')   
        pr_red('     _\\/\\\\\\_________________\\/\\\\\\')   
        pr_red('      _\\/\\\\\\_________________\\/\\\\\\') 
        pr_red('       _\\///__________________\\///\n')
        pr_light_purple(f'{"F1 Database": ^35}')
        pr_light_purple("----------------------------------------")
        print(':: [1] Fetching\n:: [2] Database\n:: [3] Update\n:: [E] Exit')

        cmd = input(":: --> ")

        if cmd.lower() not in {'1','2','3','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()
        
        elif cmd.lower() == '1':
            fetching()

        elif cmd.lower() == '2':
            database()
        
        elif cmd.lower() == '3':
            update()

        else: break

def fetching():
    '''
    Fetch all data from 'http://ergast.com/mrd/'
    '''

    while True:
        clear_screen()
        pr_light_purple(f'{"Fetching": ^35}')
        pr_light_purple("----------------------------------------")
        print(":: [1] Fetch Entire History Data\n:: [2] Fetch Group")
        print(":: [E] Exit")
        cmd = input(":: --> ")

        if cmd.lower() not in {'1','2','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()
        
        elif cmd.lower() == '1':
            fetch_all()

        elif cmd.lower() == '2':
            fetch_group()

        else: break

def fetch_all():
    '''
    Fetch the entire history of all drivers or selected group
    WARNING: this has gotten me IP banned several times
    To help fix this, every driver has been split up into groups 8 total
    If user decides to update the entire history, it was will breaks after
    each group to allow user to use a VPN to help not get IP banned
    '''

    exit = True

    while exit:
        clear_screen()
        pr_red(f'{"WARNING": ^35}')
        pr_red('This process can take up to a hour\nProceed? [Y/N]')
        cmd = input('>>> ')

        if cmd.lower() == 'y': break

        elif cmd.lower() == 'n': exit = False

        else:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

    while exit:
        clear_screen()
        pr_light_purple(f'{"Fetching Entire History": ^35}')
        pr_light_purple("----------------------------------------")

        for _ in range(1,9):
            pr_light_purple(f':: Fetching Group {_}')
            # load driver_table
            df_driver = pd.read_csv(r'Driver_Requests/Request_{}.csv'.format(_))
            drivers = df_driver['0'].tolist()

            # Create Data Table
            column_names = ["season", "round", "circuit_id", "status", "time", "position", "points", "driver_id", "team_id", "date"]
            df = pd.DataFrame(columns=column_names)

            driver_list = list()

            # Progress bar
            with tqdm(total =len(drivers), ascii=False) as pbar:

                # Iterate each driver
                for i in drivers:

                    # Fetch all information from API
                    data = connection(f'http://ergast.com/api/f1/drivers/{i}/results.json?limit=1000')
                    race_results = data['MRData']['RaceTable']['Races']

                    for j in race_results:
                        season = j['season']
                        rround = j['round']
                        circuitId = j['Circuit']['circuitId']
                        try:
                            time = j['Results'][0]['Time']['time']
                        except KeyError:
                            time = "N/A"
                        status = j['Results'][0]['status']
                        position = j['Results'][0]['position']
                        points = j['Results'][0]['points']
                        driver_id = j['Results'][0]['Driver']['driverId']
                        team_id = j['Results'][0]['Constructor']['constructorId']
                        date = j['date']

                        driver_list.append({'season': season, 'round': rround, 'circuit_id': circuitId, 'status': status, 'time': time, 'position': position, 'points': points, 'driver_id': driver_id, 'team_id': team_id, 'date': date, })

                    pbar.update()
                pbar.close()

            #Convert
            df = pd.DataFrame(driver_list)

            # Export
            df.to_csv(r'Driver_Responses/Response_{}.csv'.format(_), encoding='utf-8', index=False)

            # Delete Dataframe
            del df

            # Allow user to switch VPN
            # pr_red(":: VPN SWITCH")
            # wait_for_input()

        # Now fetch missing links
        missing_link = ['ernesto_brambilla',
                        'terra',
                        'goethals',
                        'kling',
                        'modena',
                        'reece',
                        'sullivan']

        # Create Data Table
        column_names = ["season", "round", "circuit_id", "status", "time", "position", "points", "driver_id", "team_id", "date"]
        df = pd.DataFrame(columns=column_names)

        missing_list = list()

        pr_light_purple(f'{"Fetching Missing Links": ^35}')
        pr_light_purple("----------------------------------------")

        # Progress bar
        with tqdm(total =len(missing_link), ascii=False) as pbar:
            for _ in missing_link:

                # Fetch all information from API
                data = connection(f'http://ergast.com/api/f1/drivers/{_}/results.json?limit=1000')
                race_results = data['MRData']['RaceTable']['Races']

                for j in race_results:
                    season = j['season']
                    rround = j['round']
                    circuitId = j['Circuit']['circuitId']
                    try:
                        time = j['Results'][0]['Time']['time']
                    except KeyError:
                        time = "N/A"
                        status = j['Results'][0]['status']
                        position = j['Results'][0]['position']
                        points = j['Results'][0]['points']
                        driver_id = j['Results'][0]['Driver']['driverId']
                        team_id = j['Results'][0]['Constructor']['constructorId']
                        date = j['date']

                    missing_list.append({'season': season, 'round': rround, 'circuit_id': circuitId, 'status': status, 'time': time, 'position': position, 'points': points, 'driver_id': driver_id, 'team_id': team_id, 'date': date, }, ignore_index=True)

                pbar.update()
            pbar.close()

        #Convert
        df = pd.DataFrame(missing_list)

        # Export
        df.to_csv(r'Driver_Responses/Response_Missing.csv', encoding='utf-8', index=False)
        # Delete Dataframe
        del df
        print('Finished!')

def fetch_group():
    '''
    Fetch JUST the drivers in the specified Group
    No need for VPN change since the pull is small
    '''

    exit == True
    group = 0

    while exit:
        clear_screen()
        pr_light_purple(f'{"Fetching Group": ^35}')
        pr_light_purple("----------------------------------------")
        print(":: [E] Exit")
        print(":: Which Group # do you want to Fetch")
        cmd = input(":: --> ")

        if cmd.lower() not in {'1','2','3','4','5','6','7','8','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()
        
        elif cmd.lower() == 'e': exit == False

        else: 
            group = int(cmd)
            break

    while exit:
        clear_screen()
        print(group)
        pr_light_purple(f'       Fetching Group {group}')
        pr_light_purple("----------------------------------------")

        # load driver_table
        df_driver = pd.read_csv(r'Driver_Requests/Request_{}.csv'.format(group))
        drivers = df_driver['0'].tolist()

        # Create Data Table
        column_names = ["season", "round", "circuit_id", "status", "time", "position", "points", "driver_id", "team_id", "date"]
        df = pd.DataFrame(columns=column_names)

        # Progress bar
        with tqdm(total =len(drivers), ascii=False) as pbar:

            # Iterate each driver
            for i in drivers:

                # Fetch all information from API
                data = connection(f'http://ergast.com/api/f1/drivers/{i}/results.json?limit=1000')
                race_results = data['MRData']['RaceTable']['Races']

                for j in race_results:
                    season = j['season']
                    rround = j['round']
                    circuitId = j['Circuit']['circuitId']
                    try:
                        time = j['Results'][0]['Time']['time']
                    except KeyError:
                        time = "N/A"
                    status = j['Results'][0]['status']
                    position = j['Results'][0]['position']
                    points = j['Results'][0]['points']
                    driver_id = j['Results'][0]['Driver']['driverId']
                    team_id = j['Results'][0]['Constructor']['constructorId']
                    date = j['date']

                    df = df.append({'season': season, 'round': rround, 'circuit_id': circuitId, 'status': status, 'time': time, 'position': position, 'points': points, 'driver_id': driver_id, 'team_id': team_id, 'date': date, }, ignore_index=True)

                pbar.update()
            pbar.close()

        # Export
        df.to_csv(r'Driver_Responses/Response_{}.csv'.format(group), encoding='utf-8', index=False)

        # Delete Dataframe
        del df

def database():

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        print(":: [1] Search for Driver\n:: [2] Search For Team\n:: [3] Search for Circuit")
        print(":: [E] Exit")
        cmd = input(':: --> ')

        if cmd.lower() not in {'1','2','3','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()
        
        elif cmd.lower() == '1':
            search_driver()

        elif cmd.lower() == '2':
            search_team()

        elif cmd.lower() == '3':
            search_circuit()
        
        else: break

def search_driver():
    
    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        pr_light_purple(f'{"Driver": ^35}\n')
        print(":: [1] Given Name\n:: [2] Family Name\n:: [3] Driver ID\n:: [4] Nationality")
        print(":: [E] Exit")
        cmd = input(':: --> ')

        if cmd.lower() not in {'1','2','3','4','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()
        
        elif cmd.lower() == '1':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Given Name": ^35}\n')
            print(":: Enter Given Name")
            given_name = input(":: --> ")

            status,results = search_query('Driver_Table','given_name',given_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '2':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Family Name": ^35}\n')
            print(":: Enter Family Name")
            family_name = input(":: --> ")

            status,results = search_query('Driver_Table','family_name',family_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '3':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Driver ID": ^35}\n')
            print(":: Enter Driver ID")
            driver_id = input(":: --> ")

            status,results = search_query('Driver_Table','driver_id',driver_id)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '4':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Nationality": ^35}\n')
            print(":: Enter Driver Nationality")
            nationality = input(":: --> ")

            status,results = search_query('Driver_Table','nationality',nationality)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()
        
        else: break

def search_team():

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        pr_light_purple(f'{"Team": ^35}\n')
        print(":: [1] Team ID\n:: [2] Team Name\n:: [3] Nationality")
        print(":: [E] Exit")
        cmd = input(':: --> ')

        if cmd.lower() not in {'1','2','3','4','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == '1':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Team: Team ID": ^35}\n')
            print(":: Enter Team ID")
            team_id = input(":: --> ")

            status,results = search_query('Team_Table','team_id',team_id)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '2':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Team: Team Name": ^35}\n')
            print(":: Enter Team Name")
            team_name = input(":: --> ")

            status,results = search_query('Team_Table','team_name',team_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '3':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Team: Nationality": ^35}\n')
            print(":: Enter Team Nationality")
            nationality = input(":: --> ")

            status,results = search_query('Team_Table','nationality',nationality)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        else: break

def search_circuit():

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        pr_light_purple(f'{"Circuit": ^35}\n')
        print(":: [1] Circuit ID\n:: [2] Circuit Name\n:: [3] Location\n:: [4] Country")
        print(":: [E] Exit")
        cmd = input(':: --> ')

        if cmd.lower() not in {'1','2','3','4','e'}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == '1':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit ID": ^35}\n')
            print(":: Enter Circuit ID")
            circuit_id = input(":: --> ")

            status,results = search_query('Circuit_Table','circuit_id',circuit_id)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '2':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit Name": ^35}\n')
            print(":: Enter Circuit Name")
            circuit_name = input(":: --> ")

            status,results = search_query('Circuit_Table','circuit_name',circuit_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '3':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit Location": ^35}\n')
            print(":: Enter Circuit Location")
            location = input(":: --> ")

            status,results = search_query('Circuit_Table','location',location)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == '4':
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit Country": ^35}\n')
            print(":: Enter Circuit Country")
            country = input(":: --> ")

            status,results = search_query('Circuit_Table','country',country)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'Status: {status}\n')

            pr_yellow(results)

            wait_for_input()

        else: break

def update():
    print("WIP")

if __name__ == "__main__":
    initalize()