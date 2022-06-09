from time import sleep
import mysql.connector as mc
from beautifultable import BeautifulTable
import email
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes


# Fixed variables

HOSTNAME = "localhost"
HOSTUSER = "root"
HOSTPASS = "Nga42pcc"
DATABASE = "O-Waste"

# Function for email-notification


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    # set the plain text body
    msg.set_content('This is a plain text body.')

    # now create a Content-ID for the image
    image_cid = make_msgid(domain='gmail.com')

    msg.add_alternative("""\
<html>
    <body>
        <p>
        <br>
        Hej Jens Jensen
        <br>
        <br>
        Skraldespand er næsten fyldt, så det anbefales at den tømmes snarest.
        <br><br>

        ID: {}<br>
        Materiale: {}<br>
        Lokation: {}<br>
        Volume: {}%<br>


        <br>
        Best Regards,
        Ø-Waste
        </p>
        <img src="cid:{image_cid}">
    </body>
</html>
""".format(spand_ID, materiale, lokation_navn, opdater_volume, image_cid=image_cid[1:-1]), subtype='html')

    # now open the image and attach it to the email
    with open('logo.png', 'rb') as img:

        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # attach it
        msg.get_payload()[1].add_related(img.read(),
                                         maintype=maintype,
                                         subtype=subtype,
                                         cid=image_cid)

    user = "sohrabmalek16@gmail.com"
    msg["from"] = user
    password = "neyfxknxmjnwjqvr"

    # Server parameters
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


def prettyprint(result, th, context):
    table = BeautifulTable()
    table.columns.header = th
    table.set_style(BeautifulTable.STYLE_RST)
    for row in result:
        table.rows.append(row)
    print(60*'-')
    print(context)
    print(table)
    print(len(result), 'row(s) returned')


def oversigt_affald():
    mydb = mc.connect(
        host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
        user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
        password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
        # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
        database=DATABASE
    )

    # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
    cursor = mydb.cursor()
    cursor.execute('select * from skraldespand')

    data = cursor.fetchall()

    th = ['ID', 'Materiale', 'Type', 'Volume (%)', 'Lokation_ID']
    title = '\nOversigt over skraldespande & affaldscontainere'

    # Display results nicely
    prettyprint(data, th, title)

    # Disconnect
    mydb.close()

    valg = int(input('''
1. Opdatér fyldningsniveauet (volume) for en spand
2. Gå tilbage til main-menu

Indtast valg (nummer): '''))

    if valg == 1:
        global spand_ID, opdater_volume
        spand_ID = int(input("Indtast ID: "))

        mydb = mc.connect(
            host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
            user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
            password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
            # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
            database=DATABASE)

        # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
        cursor = mydb.cursor()
        cursor.execute(f'select * from skraldespand where ID = {spand_ID}')

        data = cursor.fetchall()

        th = ['ID', 'Materiale', 'Type', 'Volume', 'Lokation_ID']

        # Display results nicely
        prettyprint(data, th, title)

        opdater_volume = int(input("\nIndtast ny volume (%): "))

        if opdater_volume >= 80:
            global Message
            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                database=DATABASE
            )

            cursor = mydb.cursor()
            cursor.execute(
                f"update skraldespand set volume = {opdater_volume} where ID = {spand_ID};")

            mydb.commit()

            cursor = mydb.cursor()

            cursor.execute(
                f"select materiale from skraldespand where ID = {spand_ID}")

            for x in cursor.fetchone():
                global materiale
                materiale = x

            cursor.execute(
                f"select Lokation_ID from skraldespand where ID = {spand_ID}")

            for x in cursor.fetchone():
                Lokation_ID = x

            cursor.execute(
                f"select navn from lokation where ID = {Lokation_ID}")

            for x in cursor.fetchone():
                global lokation_navn
                lokation_navn = x

             # Disconnect
            mydb.close()

            print(
                f"\nSkraldespand (ID: {spand_ID} - Materiale: {materiale}) er næsten fyldt")
            sleep(1)
            print("\nEmail-notifikation sendes.....")

            Subject = f"Affaldsnotifikation ♻️ "

            Message = f'''
Skraldespand er næsten fyldt, så det anbefales at den tømmes snarest.
Tak for at du er med til at gøre Ø'en grønnere!

ID: {spand_ID}
Materiale: {materiale}
Lokation: {lokation_navn}
Volume: {opdater_volume}%



Best Regards,
Ø-Waste'''

            Message = ""

            To = ["sohr0009@stud.kea.dk", "matspeeder@gmail.com", "sebsommer1999@gmail.com",
                  "gustav.mogensen@gmail.com", "emilbernekilde@hotmail.com"]

            email_alert(Subject, Message,
                        To)
            sleep(1)
            print(".")
            sleep(1)
            print("..")
            sleep(1)
            print("...")
            sleep(1)
            print("....")
            sleep(1)
            print(".....")
            print("\nEmail sendt!")

            valg2 = int(input('''
1. Gå tilbage til main-menu
2. Afslut

Indtast valg: '''))

            if valg2 == 1:
                main()

            elif valg2 == 2:
                print("Tak for at bruge vores system")
                exit()

        elif opdater_volume <= 79:

            mydb = mc.connect(
                host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
                user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
                password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
                # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
                database=DATABASE
            )

            cursor = mydb.cursor()
            cursor.execute(
                f"update skraldespand set volume = {opdater_volume} where ID = {spand_ID};")

            mydb.commit()
            # Disconnect
            mydb.close()

            print(f"Skraldespand med ID: {spand_ID} er nu opdateret")

            valg2 = int(input('''
1. Gå tilbage til main-menu
2. Afslut

Indtast valg: '''))

            if valg2 == 1:
                main()

            elif valg2 == 2:
                print("Tak for at bruge vores system")
                exit()

    else:
        main()


def oversigt_areas():

    mydb = mc.connect(
        host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
        user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
        password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
        # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
        database=DATABASE
    )

    # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
    cursor = mydb.cursor()
    cursor.execute('select * from lokation')

    data = cursor.fetchall()

    th = ['ID', 'Navn', 'Område', 'Antal skraldespande']
    title = 'Oversigt over lokationer for skraldespande & affaldscontainere'

    # Display results nicely
    prettyprint(data, th, title)

    # Disconnect
    mydb.close()


def oversigt_sensedata():
    mydb = mc.connect(
        host=HOSTNAME,         # HOSTNAME hentes fra serverinfo.py
        user=HOSTUSER,         # HOSTUSER hentes fra serverinfo.py
        password=HOSTPASS,     # HOSTPASS hentes fra serverinfo.py
        # Det er en forudsætning, at SharePlugDB.py er eksekveret, før denne variabel kan tage effekt
        database=DATABASE
    )

    # Cursor defineres og fungerer som en pegepind - Hvis en pegepind ikke er til stede, vil programmet ikke handle på vegne af databasen
    cursor = mydb.cursor()
    cursor.execute('select * from sensor')

    data = cursor.fetchall()

    th = ['ID', 'Navn', 'Lokation_ID', 'IP-Adresse', 'Status']
    title = 'Oversigt over sensorer'

    # Display results nicely
    prettyprint(data, th, title)

    # Disconnect
    mydb.close()
