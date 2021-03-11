from flask import Flask, render_template, request, redirect, url_for
from ProcessText import ProcessText

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/aboutUs')
def about():
    return render_template('aboutUs.html')

@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        text = request.form['text']
        process_text = ProcessText('amazon_small.json')
        prediction = process_text.predict(text)
        return redirect(url_for('prediction', prediction=prediction))
    else:
        return render_template('text.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/<prediction>')
def prediction(prediction):
    return f'<h1>{prediction}</h1>'

if __name__ == '__main__':
    app.run(debug=True)
