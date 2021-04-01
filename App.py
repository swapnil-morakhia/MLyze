from flask import Flask, render_template, request
from TextAnalysis import TextAnalysis

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/analysis')
def analysis():
    return render_template('analysispage.html', dictionary_response=dict())

@app.route('/analyzing', methods=['GET', 'POST'])
def analyzing():
    if request.method == 'POST':
        text_analysis = TextAnalysis(request.form['text'])
        print(text_analysis.get_response())
        return render_template('analysispage.html', dictionary_response=text_analysis.get_response())
    else:
        return render_template('analysispage.html', dictionary_response=dict())

if __name__ == '__main__':
    app.run(debug=True)
