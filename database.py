from misc import *


def search_driver():

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        pr_light_purple(f'{"Driver": ^35}\n')
        print(
            ":: [1] Given Name\n:: [2] Family Name\n:: [3] Driver ID\n:: [4] Nationality"
        )
        print(":: [E] Exit")
        cmd = input(":: --> ")

        if cmd.lower() not in {"1", "2", "3", "4", "e"}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == "1":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Given Name": ^35}\n')
            print(":: Enter Given Name")
            given_name = input(":: --> ")

            status, results = search_query("Driver_Table", "given_name", given_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "2":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Family Name": ^35}\n')
            print(":: Enter Family Name")
            family_name = input(":: --> ")

            status, results = search_query("Driver_Table", "family_name", family_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "3":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Driver ID": ^35}\n')
            print(":: Enter Driver ID")
            driver_id = input(":: --> ")

            status, results = search_query("Driver_Table", "driver_id", driver_id)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "4":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Driver: Nationality": ^35}\n')
            print(":: Enter Driver Nationality")
            nationality = input(":: --> ")

            status, results = search_query("Driver_Table", "nationality", nationality)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        else:
            break


def search_team():

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        pr_light_purple(f'{"Team": ^35}\n')
        print(":: [1] Team ID\n:: [2] Team Name\n:: [3] Nationality")
        print(":: [E] Exit")
        cmd = input(":: --> ")

        if cmd.lower() not in {"1", "2", "3", "4", "e"}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == "1":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Team: Team ID": ^35}\n')
            print(":: Enter Team ID")
            team_id = input(":: --> ")

            status, results = search_query("Team_Table", "team_id", team_id)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "2":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Team: Team Name": ^35}\n')
            print(":: Enter Team Name")
            team_name = input(":: --> ")

            status, results = search_query("Team_Table", "team_name", team_name)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "3":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Team: Nationality": ^35}\n')
            print(":: Enter Team Nationality")
            nationality = input(":: --> ")

            status, results = search_query("Team_Table", "nationality", nationality)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        else:
            break


def search_circuit():

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        pr_light_purple(f'{"Circuit": ^35}\n')
        print(":: [1] Circuit ID\n:: [2] Circuit Name\n:: [3] Location\n:: [4] Country")
        print(":: [E] Exit")
        cmd = input(":: --> ")

        if cmd.lower() not in {"1", "2", "3", "4", "e"}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == "1":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit ID": ^35}\n')
            print(":: Enter Circuit ID")
            circuit_id = input(":: --> ")

            status, results = search_query("Circuit_Table", "circuit_id", circuit_id)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "2":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit Name": ^35}\n')
            print(":: Enter Circuit Name")
            circuit_name = input(":: --> ")

            status, results = search_query(
                "Circuit_Table", "circuit_name", circuit_name
            )

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "3":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit Location": ^35}\n')
            print(":: Enter Circuit Location")
            location = input(":: --> ")

            status, results = search_query("Circuit_Table", "location", location)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        elif cmd.lower() == "4":
            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f'{"Circuit: Circuit Country": ^35}\n')
            print(":: Enter Circuit Country")
            country = input(":: --> ")

            status, results = search_query("Circuit_Table", "country", country)

            clear_screen()
            pr_light_purple(f'{"Database": ^35}')
            pr_light_purple("----------------------------------------")
            pr_light_purple(f"Status: {status}\n")

            pr_yellow(results)

            wait_for_input()

        else:
            break
