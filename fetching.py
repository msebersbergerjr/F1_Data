from tqdm import tqdm
from requests.models import HTTPError
from api_requesting import *
from connection import connection
from misc import *


def fetch_all():
    """
    Fetch the entire history of all drivers or selected group
    WARNING: this has gotten me IP banned several times
    To help fix this, every driver has been split up into groups 8 total
    If user decides to update the entire history, it was will breaks after
    each group to allow user to use a VPN to help not get IP banned
    """

    for _ in range(1, 9):
        pr_light_purple(f":: Fetching Group {_}")
        # load driver_table
        df_driver = pd.read_csv(r"Driver_Requests/Request_{}.csv".format(_))
        drivers = df_driver["0"].tolist()

        # Create Data Table
        column_names = [
            "season",
            "round",
            "circuit_id",
            "status",
            "time",
            "position",
            "points",
            "driver_id",
            "team_id",
            "date",
        ]
        df = pd.DataFrame(columns=column_names)

        driver_list = list()

        # Progress bar
        with tqdm(total=len(drivers), ascii=False) as pbar:

            # Iterate each driver
            for i in drivers:

                # Fetch all information from API
                data = connection(
                    f"http://ergast.com/api/f1/drivers/{i}/results.json?limit=1000"
                )
                race_results = data["MRData"]["RaceTable"]["Races"]

                for j in race_results:
                    season = j["season"]
                    rround = j["round"]
                    circuitId = j["Circuit"]["circuitId"]
                    try:
                        time = j["Results"][0]["Time"]["time"]
                    except KeyError:
                        time = "N/A"
                    status = j["Results"][0]["status"]
                    position = j["Results"][0]["position"]
                    points = j["Results"][0]["points"]
                    driver_id = j["Results"][0]["Driver"]["driverId"]
                    team_id = j["Results"][0]["Constructor"]["constructorId"]
                    date = j["date"]

                    driver_list.append(
                        {
                            "season": season,
                            "round": rround,
                            "circuit_id": circuitId,
                            "status": status,
                            "time": time,
                            "position": position,
                            "points": points,
                            "driver_id": driver_id,
                            "team_id": team_id,
                            "date": date,
                        }
                    )

                pbar.update()
            pbar.close()

        # Convert
        df = pd.DataFrame(driver_list)

        # Export
        df.to_csv(
            r"Driver_Responses/Response_{}.csv".format(_),
            encoding="utf-8",
            index=False,
        )

        # Delete Dataframe
        del df

        # Allow user to switch VPN
        # pr_red(":: VPN SWITCH")
        # wait_for_input()

    # Now fetch missing links
    missing_link = [
        "ernesto_brambilla",
        "terra",
        "goethals",
        "kling",
        "modena",
        "reece",
        "sullivan",
    ]

    # Create Data Table
    column_names = [
        "season",
        "round",
        "circuit_id",
        "status",
        "time",
        "position",
        "points",
        "driver_id",
        "team_id",
        "date",
    ]
    df = pd.DataFrame(columns=column_names)

    missing_list = list()

    pr_light_purple(f'{"Fetching Missing Links": ^35}')
    pr_light_purple("----------------------------------------")

    # Progress bar
    with tqdm(total=len(missing_link), ascii=False) as pbar:
        for _ in missing_link:

            # Fetch all information from API
            data = connection(
                f"http://ergast.com/api/f1/drivers/{_}/results.json?limit=1000"
            )
            race_results = data["MRData"]["RaceTable"]["Races"]

            for j in race_results:
                season = j["season"]
                rround = j["round"]
                circuitId = j["Circuit"]["circuitId"]
                try:
                    time = j["Results"][0]["Time"]["time"]
                except KeyError:
                    time = "N/A"
                    status = j["Results"][0]["status"]
                    position = j["Results"][0]["position"]
                    points = j["Results"][0]["points"]
                    driver_id = j["Results"][0]["Driver"]["driverId"]
                    team_id = j["Results"][0]["Constructor"]["constructorId"]
                    date = j["date"]

                missing_list.append(
                    {
                        "season": season,
                        "round": rround,
                        "circuit_id": circuitId,
                        "status": status,
                        "time": time,
                        "position": position,
                        "points": points,
                        "driver_id": driver_id,
                        "team_id": team_id,
                        "date": date,
                    }
                )

            pbar.update()
        pbar.close()

    # Convert
    df = pd.DataFrame(missing_list)

    # Export
    df.to_csv(r"Driver_Responses/Response_Missing.csv", encoding="utf-8", index=False)
    # Delete Dataframe
    del df
    get_race_history()


def fetch_group(group):
    """
    Fetch JUST the drivers in the specified Group
    No need for VPN change since the pull is small
    """

    # load driver_table
    df_driver = pd.read_csv(r"Driver_Requests/Request_{}.csv".format(group))
    drivers = df_driver["0"].tolist()

    # Create Data Table
    column_names = [
        "season",
        "round",
        "circuit_id",
        "status",
        "time",
        "position",
        "points",
        "driver_id",
        "team_id",
        "date",
    ]
    df = pd.DataFrame(columns=column_names)

    group_list = list()

    # Progress bar
    with tqdm(total=len(drivers), ascii=False) as pbar:

        # Iterate each driver
        for i in drivers:

            # Fetch all information from API
            data = connection(
                f"http://ergast.com/api/f1/drivers/{i}/results.json?limit=1000"
            )
            race_results = data["MRData"]["RaceTable"]["Races"]

            for j in race_results:
                season = j["season"]
                rround = j["round"]
                circuitId = j["Circuit"]["circuitId"]
                try:
                    time = j["Results"][0]["Time"]["time"]
                except KeyError:
                    time = "N/A"
                status = j["Results"][0]["status"]
                position = j["Results"][0]["position"]
                points = j["Results"][0]["points"]
                driver_id = j["Results"][0]["Driver"]["driverId"]
                team_id = j["Results"][0]["Constructor"]["constructorId"]
                date = j["date"]

                group_list.append(
                    {
                        "season": season,
                        "round": rround,
                        "circuit_id": circuitId,
                        "status": status,
                        "time": time,
                        "position": position,
                        "points": points,
                        "driver_id": driver_id,
                        "team_id": team_id,
                        "date": date,
                    }
                )

            pbar.update()
        pbar.close()

    # Convert
    df = pd.DataFrame(group_list)

    # Export
    df.to_csv(
        r"Driver_Responses/Response_{}.csv".format(group),
        encoding="utf-8",
        index=False,
    )

    # Delete Dataframe
    del df
