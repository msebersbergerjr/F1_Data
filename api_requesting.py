import pandas as pd
from connection import connection


def get_drivers():
    """
    Get every driver to ever drive for F1
    """

    # Create Data Table
    column_names = [
        "driver_id",
        "race_number",
        "given_name",
        "family_name",
        "dob",
        "nationality",
    ]
    df_driver = pd.DataFrame(columns=column_names)

    # Fetch all information from API
    data = connection("http://ergast.com/api/f1/drivers.json?limit=1000")
    drivers = data["MRData"]["DriverTable"]["Drivers"]

    drivers_list = list()

    # Iterate though all drivers
    for _ in drivers:
        driver_id = _["driverId"]
        given_name = _["givenName"]
        family_name = _["familyName"]
        dob = _["dateOfBirth"]
        nationality = _["nationality"]

        drivers_list.append(
            {
                "driver_id": driver_id,
                "given_name": given_name,
                "family_name": family_name,
                "dob": dob,
                "nationality": nationality,
            }
        )

    # Convert
    df_driver = pd.DataFrame(drivers_list)

    # Export
    df_driver.to_csv(r"Data/Driver_Table.csv", encoding="utf-8", index=False)

    # Delete Dataframe
    del df_driver


def get_circuit():
    """
    Get every circuit driven ini F1
    """

    # Create Data Table
    column_names = ["circuit_id", "circuit_name", "location", "country"]
    df_circuit = pd.DataFrame(columns=column_names)

    # Fetch all information from API
    data = connection("http://ergast.com/api/f1/circuits.json?limit=1000")
    circuits = data["MRData"]["CircuitTable"]["Circuits"]

    circuits_list = list()

    # Iterate though all drivers
    for _ in circuits:
        circuit_id = _["circuitId"]
        circuit_name = _["circuitName"]
        location = _["Location"]["locality"]
        country = _["Location"]["country"]

        circuits_list.append(
            {
                "circuit_id": circuit_id,
                "circuit_name": circuit_name,
                "location": location,
                "country": country,
            }
        )
    # Convert
    df_circuit = pd.DataFrame(circuits_list)

    # Export
    df_circuit.to_csv(r"Data/Circuit_Table.csv", encoding="utf-8", index=False)

    # Delete Dataframe
    del df_circuit


def get_teams():
    """
    Get every Team to be in the F1
    """

    # Create Data Table
    column_names = ["team_id", "team_name", "nationality"]
    df_teams = pd.DataFrame(columns=column_names)

    teams_list = list()

    # Fetch all information from API
    data = connection("http://ergast.com/api/f1/constructors.json?limit=1000")
    teams = data["MRData"]["ConstructorTable"]["Constructors"]

    # Iterate though all drivers
    for _ in teams:
        team_id = _["constructorId"]
        team_name = _["name"]
        nationality = _["nationality"]

        teams_list.append(
            {"team_id": team_id, "team_name": team_name, "nationality": nationality}
        )

    # Convert
    df_teams = pd.DataFrame(teams_list)

    # Export
    df_teams.to_csv(r"Data/Team_Table.csv", encoding="utf-8", index=False)

    # Delete Dataframe
    del df_teams


def get_current():
    """
    Current
    id(PK) | driver_id(FK) | team_id(FK) | permanent_number | position | points | wins |
    link : 'http://ergast.com/api/f1/current/driverStandings.json'
    """

    # Create Data Table
    column_names = ["driver_id", "team_id", "points"]
    df_curr = pd.DataFrame(columns=column_names)

    curr_list = list()

    # Fetch all information from API
    data = connection("http://ergast.com/api/f1/current/driverStandings.json")
    curr = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    # Iterate though all drivers
    for i in curr:
        driver_id = i["Driver"]["driverId"]
        team_id = i["Constructors"][0]["constructorId"]
        permanent_number = i["Driver"]["permanentNumber"]
        position = i["position"]
        points = i["points"]
        wins = i["wins"]

        curr_list.append(
            {
                "driver_id": driver_id,
                "team_id": team_id,
                "position": position,
                "points": points,
                "wins": wins,
            }
        )

    # Convert
    df_curr = pd.DataFrame(curr_list)

    # Export
    df_curr.to_csv(r"Data/Current_Table.csv", encoding="utf-8", index=False)

    # Delete Dataframe
    del df_curr


def get_first():
    """
    1st place Time
    id(PK) | season | round | circuit_id(FK) | time | driver_id(FK) |
    """

    # Create Data Table
    column_names = ["season", "round", "circuit_id", "time", "driver_id"]
    df_first = pd.DataFrame(columns=column_names)

    first_list = list()

    for year in range(1950, 2022):
        # Fetch all information from API
        data = connection(f"http://ergast.com/api/f1/{year}/results.json?limit=1000")

        first_results = data["MRData"]["RaceTable"]["Races"]

        for i in first_results:
            season = int(i["season"])
            rround = int(i["round"])
            circuit_id = i["Circuit"]["circuitId"]
            time = i["Results"][0]["Time"]["time"]
            driver_id = i["Results"][0]["Driver"]["driverId"]

            first_list.append(
                {
                    "season": season,
                    "round": rround,
                    "circuit_id": circuit_id,
                    "time": time,
                    "driver_id": driver_id,
                }
            )

    # Convert
    df_first = pd.DataFrame(first_list)

    # Sort by Year then round Decending
    df_first = df_first.sort_values(["season", "round"], ascending=[False, False])

    # Export
    df_first.to_csv(r"Data/First_Table.csv", encoding="utf-8", index=False)

    # Delete Dataframe
    del df_first


def get_team_history():
    """
    Team History
    id(PK) | season | team_id(FK) | position | points | wins
    link: 'http://ergast.com/api/f1/{year}/constructorStandings.json'
    """

    # Create Data Table
    column_names = ["season", "team_id", "position", "points", "wins"]
    df_team_his = pd.DataFrame(columns=column_names)

    team_hist_list = list()

    # Iterate though entire history of F1
    for year in range(1950, 2022):
        # Fetch all information from API
        data = connection(
            f"http://ergast.com/api/f1/{year}/constructorStandings.json?limit=1000"
        )
        try:
            team_hist = data["MRData"]["StandingsTable"]["StandingsLists"][0][
                "ConstructorStandings"
            ]

            # Iterate though all teams
            for i in team_hist:
                season = year
                team_id = i["Constructor"]["constructorId"]
                position = i["position"]
                points = i["points"]
                wins = i["wins"]

                team_hist_list.append(
                    {
                        "season": season,
                        "team_id": team_id,
                        "position": position,
                        "points": points,
                        "wins": wins,
                    }
                )

        except IndexError:
            pass

    # Convert
    df_team_his = pd.DataFrame(team_hist_list)

    # Export
    df_team_his.to_csv(r"Data/Team_History_Table.csv", encoding="utf-8", index=False)

    # Delete Dataframe
    del df_team_his


def get_race_history():
    """
    Merge all the Driver Response Responses into one csv
    """

    arr = []

    try:
        for _ in range(1, 9):
            filename = "Driver_Responses/Response_" + str(_) + ".csv"
            if _ == 1:
                arr.append(pd.read_csv(filename))
            else:
                arr.append(pd.read_csv(filename))

                arr.append(pd.read_csv(r"Driver_Responses/Response_Missing.csv"))

        df = pd.concat(arr)

        df.to_csv("Data/Race_History_Table.csv")

        # Delete Dataframe
        del df

        return 1

    except FileNotFoundError:
        return 0
