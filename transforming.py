import pandas as pd
from datetime import datetime, timedelta


def true_time():
    """
    Get the True Time of a race result in the Race History Table
    Create a new column named "True Time"
    Where we add on the time the driver finished to the driver who finished 1st
    As of now I dont have a answer for drivers who:
        Get Lapped
        DNF
    """

    # Load Driver Table
    df_drivers = pd.read_csv(r"Data/Driver_Table.csv")
    drivers = df_drivers.loc[:, "driver_id"]

    # Load 1st place Table
    df_first = pd.read_csv(r"Data/First_Table.csv")

    # Load Race History Table
    hist_table = pd.read_csv(r"Data/Race_History_Table.csv")

    # Initalize new Column true time
    hist_table["true_time"] = ""

    # Get Drivers true time for every race
    hist_table["true_time"] = hist_table[
        ["driver_id", "season", "round", "time"]
    ].apply(lambda x: get_race_time(*x, df_first), axis=1)

    # Drop Time Column from original csv
    hist_table.drop(labels=["time"], axis=1, inplace=True)

    # Drops the Unnamed: 0 column that gets generated from Pandas
    hist_table.drop(labels=["Unnamed: 0"], axis=1, inplace=True)

    # Sort by Season, Round so most current race is on top
    hist_table = hist_table.sort_values(["season", "round"], ascending=False)

    # Overwrite Race History Table with true track time
    hist_table.to_csv("Data/Race_History_Table.csv", index=False)

    del hist_table
    del df_drivers
    del df_first


def convertHours(raw_time):
    """Format H:M:S:Micro"""
    dirty_time = datetime.strptime(raw_time, "%I:%M:%S.%f").time()
    clean_time = timedelta(
        hours=dirty_time.hour,
        minutes=dirty_time.minute,
        seconds=dirty_time.second,
        microseconds=dirty_time.microsecond,
    )
    return clean_time


def convertMinute(raw_time):
    """Format M:S:Micro"""
    dirty_time = datetime.strptime(raw_time, "%M:%S.%f").time()
    clean_time = timedelta(
        minutes=dirty_time.minute,
        seconds=dirty_time.second,
        microseconds=dirty_time.microsecond,
    )
    return clean_time


def convertSeconds(raw_time):
    """Format S:Micro"""
    dirty_time = datetime.strptime(raw_time, "%S.%f").time()
    clean_time = timedelta(
        seconds=dirty_time.second, microseconds=dirty_time.microsecond
    )
    return clean_time


def get_race_time(driver_id, season, rd, time, df_first) -> any:
    """
    Convert Drivers time, either winning time or + time to complete track time
    API has alot of dirty data so alot of cleaning is required
    """

    # Time doesn't Exist
    # Ex: +1 Lap, Engine, Throttle etc...
    # For now make it time of 0.0
    if type(time) == float:
        clean_time = timedelta(seconds=0, microseconds=0)
        # print(driver_id,season,rd,clean_time)
        return str(clean_time)

    # Gets Race winner
    winner_frame = (
        df_first.loc[(df_first["season"] == season) & (df_first["round"] == rd)]
    )[["time", "driver_id", "season", "round"]]

    if winner_frame.iloc[0, 0].count(":") == 2:
        # Rare case hours if 0 in the time then removes the 0 in the hour slot
        try:
            clean_winner_time = convertHours(winner_frame.iloc[0, 0])

        except ValueError:
            bad_time = winner_frame.iloc[0, 0]
            better_time = bad_time[2:]
            clean_winner_time = convertMinute(better_time)

    elif winner_frame.iloc[0, 0].count(":") == 1:
        clean_winner_time = convertMinute(winner_frame.iloc[0, 0])

    else:
        clean_winner_time = convertSeconds(winner_frame.iloc[0, 0])

    if winner_frame.iloc[0, 1] == driver_id:
        return str(clean_winner_time)

    # Removes + in front of the times
    elif "+" in time:

        dirty_time = time[1:]

        # Rare case 's' or 'sec' is in the time
        # or
        # Rare case there is a space infront of the hour time EX: ' 1.06.7'
        if "sec" in dirty_time:
            dirty_time = dirty_time[:-4]

        elif "s" in dirty_time:
            dirty_time = dirty_time[:-1]

        elif dirty_time[:1] == " ":
            dirty_time = dirty_time[1:]

        # Formatting of the time
        # Rare case where There is a time with no seconds; adds .0 seconds to time EX: '1:10'
        if ":" in dirty_time:
            try:
                # min, sec, micro
                clean_time = convertMinute(dirty_time)
            except ValueError:

                dirty_time += ".0"
                clean_time = convertMinute(dirty_time)

        else:
            try:
                # sec, micro
                clean_time = convertSeconds(dirty_time)

            except ValueError:
                # Rare case Min is => 60
                # print(dirty_time)

                # Separate Seconds and Millseconds
                sec, mill = map(int, dirty_time.split("."))

                # Get decimal value of Minute and second
                convert = str(round(sec / 60, 1))

                # Separate Minutes and Seconds
                min, sec = map(int, convert.split("."))

                # Format into readable time
                new_time = f"{min}:{sec}.{mill}"
                clean_time = convertMinute(new_time)

        # Combine Winner time with driver time to get total lap time
        total_time = str(clean_winner_time + clean_time)
        return total_time
