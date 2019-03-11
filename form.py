import re


class Form:
    snum = ''
    ports = []
    errors = []

    def __init__(self, form):
        self.snum = form['snum']
        self.ports = [int(form['port1']), int(form['port2'])]
        self.validate()

    def validate(self):
        errors = []
        if not (re.match(r"^s[0-9]{7}$", self.snum)):
            errors.append("%s is not a valid student number" % self.snum)

        if (self.ports[0] < 61000) or (self.ports[0] > 61999):
            errors.append(
                "Port 1 is out of the specified range. Please specify a port in the range 61000 - 61999"
            )

        if (self.ports[1] < 61000) or (self.ports[1] > 61999):
            errors.append(
                "Port 2 is out of the specified range. Please specify a port in the range 61000 - 61999"
            )

        if self.ports[0] == self.ports[1]:
            errors.append("Please specify two different ports.")

        return errors
