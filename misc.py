import os
import pandas as pd


def pr_red(text):
    print(f"\033[91m{text}\033[00m")


def pr_light_purple(text):
    print(f"\033[94m{text}\033[00m")


def pr_yellow(text):
    print(f"\033[93m{text}\033[00m")


def clear_screen():
    """
    Clear the terminal screen for a cleaner look
    Cross-Platform by checking if the machine is a windows or unix system
    """
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_input():
    """Pause CLI until user inputs anything"""
    cmd = input(":: --> ")


def search_query(db, col, q):
    """
    Search Query Functiuon
    db = Table to search in under Data/
    col = column name we are searching through
    q = search item
    """

    df = pd.read_csv(r"Data/{}.csv".format(db))

    try:
        result = df.query(
            f'{col} == "{q}"',
        )
        status = "Match"

        # Return Likeness of search Query
        if result.empty:

            result = df.query(f'{col}.str.contains("{q}", case=False)', engine="python")
            status = "Close Match"

            # No matches were found
            if result.empty:
                result = "\033[91mError: No Matches Found\033[00m"
                status = "No Match"

    except KeyError:
        result = "Error"

    # Delete Dataframe
    del df

    return status, result
