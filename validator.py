import argparse
import re
import mail
import itertools

# import gspread
# from oauth2client import ServiceAccountCredentials
from email.message import EmailMessage

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def main():

    parser = argparse.ArgumentParser(
        description="Confirm valid port use\
        for COSC1179 Network Programming"
    )

    parser.add_argument("--snum", type=str, nargs=1, required=True)
    parser.add_argument("--ports", type=int, nargs=2, required=True)

    args = parser.parse_args()
    if not validate_args(args):
        exit()

    snum = args.snum[0]
    ports = args.ports

    port_availability = check_port_availability(ports)
    if (False not in port_availability):
        selection = input('The selected ports %s and %s are available. Send email to Fengling? [Y/N]')

        if (selection.lower() == 'y'):
            send_email(snum, ports)
    else:
        # invalid = [x for x in port_availability if x is not True]
        invalid = list(itertools.compress(ports, [not i for i in port_availability]))
        invalid_str = ("%s" * len(invalid))

        if (len(invalid) == 1):
            out = "Port %s is not available" % invalid
        else:
            out = "Ports %s are not available." % ', '.join(str(i) for i in ports)

        print(out)
    exit()


def validate_args(args):
    if not (re.match(r"^s[0-9]{7}$", args.snum[0])):
        print("%s is not a valid student number" % args.snum[0])
        return False
    elif (args.ports[0] < 61000) or (args.ports[0] > 61999):
        print(
            "Port argument 1 is out of the specified range. Please specify a port in the range 61000 - 61999"
        )
        return False
    elif (args.ports[1] < 61000) or (args.ports[1] > 61999):
        print(
            "Port argument 2 is out of the specified range. Please specify a port in the range 61000 - 61999"
        )
        return False
    elif args.ports[0] == args.ports[1]:
        print("Please specify two different ports.")
        return False

    return True


def check_port_availability(ports):

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1jARjtBtEqd8nPOWnFIRtTB5MDmiScoLHb7VcXM0PypA'
    RANGE_NAME = 'checking!A6:B7'
    PORT_RANGE = 'checking!B6'
    availability = []

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    for i, port in enumerate(ports):
        # Update port value in google sheet
        request = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=PORT_RANGE,
            valueInputOption='USER_ENTERED',
            body={"values": [[port]]}
            )
        response = request.execute()

        # Query result of changed port
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
            ).execute()
        values = result.get('values', [])

        # Construct boolean list of port availability
        if not values:
            availability.append(False)

        elif (int(values[0][1]) != port):
            print("An error occurred querying the port. Please try again.")
            exit()

        elif (values[1][1] == 'Not Taken and Talk to your tutor to add'):
            availability.append(True)

        elif (values[1][1] == 'Already Taken, Change Please'):
            availability.append(False)

        else:
            availability.append(False)

    return availability


def send_email(snum, ports):
    port = 587
    from_addr = "%s@student.rmit.edu.au" % snum
    to_addr = "fengling.han@rmit.edu.au"
    smtp_server = "smtp-mail.outlook.com"
    message = "Hi Fengling,\nThe ports I'm choosing are:\n\t- Port 1: %s\n\t- Port 2: %s\nKind Regards" % (ports[0], ports[1])

    msg = EmailMessage()
    msg['Subject'] = "%s's Port Selection for COSC1179 Network Programming" % snum
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg.set_content(message)

    mail.send(
        port=port,
        from_addr=from_addr,
        smtp_server=smtp_server,
        msg=msg
        )


if __name__ == "__main__":
    main()
