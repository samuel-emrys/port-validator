import re


class Form:
    snum = ''
    password = ''
    ports = []
    errors = []
    success_msg = None
    success = False

    def __init__(self, form=None):

        if form is not None:
            self.snum = form['snum']
            self.ports = [form['port1'], form['port2']]
            self.success = False
            self.success_msg = None
            self.password = form['password']
            self.validate()

    def validate(self):
        self.errors = []

        ports_int = []
        for port in self.ports:
            try:
                port_int = int(port)
                ports_int.append(port_int)
            except ValueError:
                self.errors.append("%s is not a valid port number" % port)

        self.ports = ports_int

        if not (re.match(r"^s[0-9]{7}$", self.snum)):
            self.errors.append("%s is not a valid student number" % self.snum)

        if (len(self.ports) > 0):
            if (self.ports[0] < 61000) or (self.ports[0] > 61999):
                self.errors.append(
                    "Port 1 is out of the specified range. Please specify a port in the range 61000 - 61999"
                )

            if (self.ports[1] < 61000) or (self.ports[1] > 61999):
                self.errors.append(
                    "Port 2 is out of the specified range. Please specify a port in the range 61000 - 61999"
                )

            if self.ports[0] == self.ports[1]:
                self.errors.append("Please specify two different ports.")
