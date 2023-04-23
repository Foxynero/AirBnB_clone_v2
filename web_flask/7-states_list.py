#!/usr/bin/python3
"""Script that runs a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states():
    """List all states"""
    states = storage.all("State")
    # states_dic = {state['id']: state['name'] for state in states.values()}
    return render_template('7-states_list.html',
                           Table="States", states=states)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
