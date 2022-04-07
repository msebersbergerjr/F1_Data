import os
import pandas as pd
from os.path import exists

from misc import *
from api_requesting import *
from transforming import *


def initalize():
    """
    Check if Data CSV's need to be created or not
    """

    # List of CSV's to check for
    tables = {
        "Driver_Table.csv",
        "Team_Table.csv",
        "Circuit_Table.csv",
        "Current_Table.csv",
        "First_Table.csv",
        "Team_History_Table.csv",
        "Race_History_Table.csv",
    }

    for _csv in tables:

        if not exists(r"Data/{}".format(_csv)):
            get_csv(_csv)

    # Check if Driver Requests folder exist
    dir = os.listdir("Driver_Requests")

    # Check
    if (len(dir)) != 8:

        # Data frame of all drivers
        driver_table = pd.read_csv("Data/Driver_Table.csv")

        # Filter all Unique drivers into a list
        udriver = driver_table["driver_id"].unique()

        # Break Down entire list of Drivers into 8 groups
        for _ in range(1, 9):
            if _ == 1:
                drivers = udriver[0 : _ * 106]
                pd.Series(drivers).to_csv("Driver_Requests/Request_" + str(_) + ".csv")
            elif _ == 8:
                drivers = udriver[743:853]
                pd.Series(drivers).to_csv("Driver_Requests/Request_" + str(_) + ".csv")
            else:
                drivers = udriver[(_ - 1) * 106 + 1 : _ * 106]
                pd.Series(drivers).to_csv("Driver_Requests/Request_" + str(_) + ".csv")


def get_csv(_csv):
    """
    Determine which csv needs to be created
    """

    if _csv == "Driver_Table.csv":
        pr_light_purple(f':: {"Acquiring Drivers": ^35}')
        pr_light_purple("----------------------------------------")
        get_drivers()

    elif _csv == "Team_Table.csv":
        pr_light_purple(f':: { "Acquiring Teams": ^35}')
        pr_light_purple("----------------------------------------")
        get_teams()

    elif _csv == "Circuit_Table.csv":
        pr_light_purple(f':: {"Acquiring Circuits": ^35}')
        pr_light_purple("----------------------------------------")
        get_circuit()

    elif _csv == "Current_Table.csv":
        pr_light_purple(f':: {"Acquiring Current Drivers": ^35}')
        pr_light_purple("----------------------------------------")
        get_current()

    elif _csv == "First_Table.csv":
        pr_light_purple(f':: {"Acquiring 1st place time": ^35}')
        pr_light_purple("----------------------------------------")
        get_first()

    elif _csv == "Team_History_Table.csv":
        pr_light_purple(f':: {"Acquiring Team History": ^35}')
        pr_light_purple("----------------------------------------")
        get_team_history()

    elif _csv == "Race_History_Table.csv":
        pr_light_purple(f':: {"Merge all the Driver Response Responses": ^35}')
        pr_light_purple("----------------------------------------")

        if get_race_history() == False:
            pr_red(":: Error: Missing Files")
            pr_red(":: Either Fetch the group or Fetch All to populate")
            pr_red(":: Then re-run Initialize")
            cmd = input(":: --> ")
        else:
            pr_light_purple(":: Converting Driver times")
            pr_light_purple("----------------------------------------")
            true_time()
            pr_yellow(":: Completed!")
            wait_for_input()
