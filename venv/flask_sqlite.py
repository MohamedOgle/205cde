from flask import Flask, render_template, redirect, url_for, request
import os
from flask_inputs import inputs
from wtforms.validators import DataRequired
from wtforms import BooleanField, StringField, PasswordField, validators, TextField
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlite3

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'comment.db'),
    SECRET_KEY='development key'
))
Bootstrap(app)

class CommentForm(Form):
    name = StringField('Name:', validators=[DataRequired()])
    comment = TextAreaField('Comments', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def view_form():
    form = CommentForm()
    if form.validate_on_submit():
        name = form.name.data
        comment = form.comment.data
        with sqlite3.connect(app.config['DATABASE']) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO comment_table (name, comment) VALUES (?,?)", (name, comment))
            con.commit()

        @app.route('/', methods=['GET', 'POST'])
        def nominee():
            if request.method == 'POST':
                Name = request.form['Name'];
                Email = request.form['Email']
                Number = request.form['Number']
                Text = request.form['Text']

                with sqlite3.connect(app.config['DATABASE']) as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO details_table (Name,Email,Number,Text) VALUES (?,?,?,?)",
                                (Name, Email, Number, Text))
                    con.commit()
            return render_template('report.html')

        return redirect(url_for('list_results'))
    return render_template('form_wtf.html', form=form)

@app.route('/display')
def list_results():
    with sqlite3.connect(app.config['DATABASE']) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM comment_table")
        entries = cur.fetchall()
        return render_template('report.html.html', entries=entries)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)