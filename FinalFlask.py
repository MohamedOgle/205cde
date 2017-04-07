from flask import Flask, request, render_template
import os

app = Flask(__name__)


@app.route('/')
def send_index():
    return render_template('index.html')


@app.route('/login')
def send_login():
    return render_template('Login.html')


@app.route('/report.html')
def send_report():
    return render_template('report.html')



if __name__ == '__main__':
    app.debug = True
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run()

