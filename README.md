# Network Programming Port Validator
This is a port validation tool created for COSC1179 Network Programming at RMIT University. The aim of this program is to allow a user to identify unallocated ports and submit this ports to the lecturer, Dr. Fengling Han via email.

Author: Samuel Dowling, s3197340
Tutor: Justin Perrie

## Dependencies:
python 3.7
### Operating System Support
- macOS
- Linux
- BSD

### Packages
A detailed breakdown of required packages is available in `requirements.txt`

## Installation

1. Create a python 3.7 virtual environment. If virtualenv is not installed:
	1. `$ pip install virtualenv`
	2. Navigate to the project root directory and execute `virtualenv --python=/path/to/python3/dist venv`, replacing `/path/to/python3/dist` with the path to your distribution of python3, if it is not default. If python3 is your default python distribution, you can just execute `virtualenv venv`
	3. Actvate virtualenv by executing `source venv/bin/activate`

2. Run `make update` in the project root.

## Execution

Execute the program by issuing the following command:

`python validator.py --snum s1234567 --ports 61000 61001`

The `--snum` flag only takes a student number, so *must* begin with an `s`, and have 7 digits.
The `--ports` flag *must* take two arguments within the range (61000,61999)

You will be prompted to login to your google account, and also enter your student password, which is required to send the email.

## Web Interface

A web interface is also available for this program at:

[https://np-port-validator2.appspot.com/](https://np-port-validator2.appspot.com/)

Note that a valid submission will automatically send an email to the lecturer

## Known Issues

- OAuth 2.0 validation on the website is currently restricted to my student account. If this token expires external access will break
- Web form does not auto-populate with previous values if an entry was unsuccessful
- Web form does not prompt before sending an email