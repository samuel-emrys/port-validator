import argparse
import re
import mail

from email.message import EmailMessage


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

    if True:
        send_email(snum, ports)
        print("Return from send email")

    print("Out of if condition")
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
    pass


def send_email(snum, ports):
    port = 587
    sender_email = "%s@student.rmit.edu.au" % snum
    destination_email = "sam.dowling@hotmail.com"
    smtp_server = "smtp-mail.outlook.com"
    message = "Hi Fengling,\nThe ports I'm choosing are:\n\t- Port 1: %s\n\t- Port 2: %s\nKind Regards" % (ports[0], ports[1])

    msg = EmailMessage()
    msg['Subject'] = "Port Selection for COSC1179 Network Programming"
    msg['From'] = sender_email
    msg['To'] = destination_email
    msg.set_content(message)

    mail.send(
        port=port,
        from_addr=sender_email,
        to_addr=destination_email,
        smtp_server=smtp_server,
        msg=msg
        )


if __name__ == "__main__":
    main()
