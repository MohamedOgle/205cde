from flask import Flask, render_template, redirect, url_for, request
import os
from flask_bootstrap import Bootstrap
import sqlite3

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'details.db'),
    SECRET_KEY='development key'
))
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def nominee():
    if request.method == 'POST':
        email = request.form['email'];
        phonenumber = request.form['phonenumber']
        country = request.form['country']
        moredetails = request.form['moredetails']

        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO details_table (email,phonenumber,country,moredetails) VALUES (?,?,?,?)",
                        (email, phonenumber, country, moredetails))
            con.commit()
    return render_template('index.html')


@app.route('/<path:path>')
def links(path=None):
    return render_template(path)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
    # app.run(debug=True)