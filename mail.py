import ssl
import smtplib
import getpass


def send(smtp_server, port, from_addr, msg):
    password = getpass.getpass("Type your account password and press enter: ")
    context = ssl.create_default_context()

    server = smtplib.SMTP(smtp_server, port)
    try:
        server.connect(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(from_addr, password)
        server.send_message(msg)
    except Exception as e:
        print(e)
    finally:
        server.quit()
