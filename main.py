from initalize import *
from database import *
from fetching import *
from misc import *


def main():
    """
    Main Menu
    """

    while True:
        clear_screen()
        pr_red("\n__/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\______/\\\\\\")
        pr_red(" _\\/\\\\\\///////////___/\\\\\\\\\\\\\\")
        pr_red("  _\\/\\\\\\_____________\\/////\\\\\\")
        pr_red("   _\\/\\\\\\\\\\\\\\\\\\\\\\_________\\/\\\\\\")
        pr_red("    _\\/\\\\\\///////__________\\/\\\\\\")
        pr_red("     _\\/\\\\\\_________________\\/\\\\\\")
        pr_red("      _\\/\\\\\\_________________\\/\\\\\\")
        pr_red("       _\\///__________________\\///\n")
        pr_light_purple(f'{"F1 Database": ^35}')
        pr_light_purple("----------------------------------------")
        print(
            ":: [1] Fetching\n:: [2] Database\n:: [3] Update\n:: [4] Initialize\n:: [E] Exit"
        )

        cmd = input(":: --> ")

        if cmd.lower() not in {"1", "2", "3", "4", "e"}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == "1":
            fetching_menu()

        elif cmd.lower() == "2":
            database_menu()

        elif cmd.lower() == "3":
            update()

        elif cmd.lower() == "4":
            initalize()

        else:
            break


def fetching_menu():
    """
    Fetching Menu
    Fetch all data from 'http://ergast.com/mrd/'
    """

    while True:
        clear_screen()
        pr_light_purple(f'{"Fetching": ^35}')
        pr_light_purple("----------------------------------------")
        print(":: [1] Fetch Entire History Data\n:: [2] Fetch Group")
        print(":: [E] Exit")
        cmd = input(":: --> ")

        if cmd.lower() not in {"1", "2", "e"}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == "1":
            while True:
                clear_screen()
                pr_red(f'{"WARNING": ^35}')
                pr_red("This process can take up to a hour\nProceed? [Y/N]")
                cmd = input(">>> ")

                if cmd.lower() == "y":
                    clear_screen()
                    pr_light_purple(f'{"Fetching Entire History": ^35}')
                    pr_light_purple("----------------------------------------")
                    fetch_all()
                    break

                elif cmd.lower() == "n":
                    break

                else:
                    pr_red(":: Error: Invalid Input")
                    wait_for_input()

        elif cmd.lower() == "2":
            group = 0

            while True:
                clear_screen()
                pr_light_purple(f'{"Fetching Group": ^35}')
                pr_light_purple("----------------------------------------")
                print(":: [E] Exit")
                print(":: Which Group # do you want to Fetch")
                cmd = input(":: --> ")

                if cmd.lower() not in {"1", "2", "3", "4", "5", "6", "7", "8", "e"}:
                    pr_red(":: Error: Invalid Input")
                    wait_for_input()

                elif cmd.lower() == "e":
                    break

                else:
                    group = int(cmd)
                    clear_screen()
                    pr_light_purple(f"       Fetching Group {group}")
                    pr_light_purple("----------------------------------------")
                    fetch_group(group)
                    break
        else:
            break


def database_menu():
    """
    Database Menu
    """

    while True:
        clear_screen()
        pr_light_purple(f'{"Database": ^35}')
        pr_light_purple("----------------------------------------")
        print(
            ":: [1] Search for Driver\n:: [2] Search For Team\n:: [3] Search for Circuit"
        )
        print(":: [E] Exit")
        cmd = input(":: --> ")

        if cmd.lower() not in {"1", "2", "3", "e"}:
            pr_red(":: Error: Invalid Input")
            wait_for_input()

        elif cmd.lower() == "1":
            search_driver()

        elif cmd.lower() == "2":
            search_team()

        elif cmd.lower() == "3":
            search_circuit()

        else:
            break


def update():
    print("WIP")


if __name__ == "__main__":
    initalize()
    main()
