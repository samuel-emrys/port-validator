# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import make_response
from form import Form
import validator
import mail
import itertools


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/')
def index():
    """Return the submission form"""
    form = Form()
    print("index")
    return render_template("index.html", form=form)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    print("submit")
    form = None
    if request.method == 'POST':
        form = Form(request.form)

        if (len(form.errors) == 0):
            port_availability = validator.check_port_availability(form.ports)
            if (False not in port_availability):
                try:
                    validator.send_email(form.snum, form.ports, form.password)
                    form.success = True
                    form.success_msg = 'The selected ports %s and %s were available! Email sent to fengling.han@rmit.edu.au.' % (form.ports[0], form.ports[1])
                except Exception as e:
                    print(e)
                    form.errors.append("Email Authentication Unsuccessful.")
            else:
                invalid = list(itertools.compress(form.ports, [not i for i in port_availability]))

                if (len(invalid) == 1):
                    out = "Port %s is not available" % invalid[0]
                else:
                    out = "Ports %s are not available." % ', '.join(str(i) for i in form.ports)

                form.errors.append(out)

        # Prepare response
        response = make_response(render_template('index.html', form=form))
        return response


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
