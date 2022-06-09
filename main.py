
from tqdm import main
from queries_and_functions import oversigt_affald, oversigt_areas, oversigt_sensedata
import mysql.connector as mc
from beautifultable import BeautifulTable


def main():
    main_menu = int(input('''
--------------------------------------------------
Hej Bruger - Vælg en menu for at fortsætte 

1. Oversigt over skraldespande
2. Oversigt over lokationer
3. Sensor data

Indtast valg (nummer): '''))

    if main_menu == 1:
        oversigt_affald()

    elif main_menu == 2:
        oversigt_areas()
        valg = int(input('''
1. Gå tilbage til main-menu
2. afslut

Indtast valg: '''))

        if valg == 1:
            main()

        else:
            exit()

    elif main_menu == 3:
        oversigt_sensedata()
        valg = int(input('''
1. Gå tilbage til main-menu
2. afslut

Indtast valg: '''))

        if valg == 1:
            main()

        else:
            exit()

    else:
        main()


if __name__ == '__main__':
    main()
