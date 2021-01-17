from flask import Flask, render_template, request
from reddit_data import get_from_reddit, get_graph_data

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST', 'GET'])
def success():
    
    if request.method == 'POST':
        query = request.form['query'].lower()
        data = get_from_reddit(query)
        graphdata = get_graph_data(query)

        #data: reddit posts
        #graphdata: data displayed in the chart
        if data:
            return render_template("index.html", data=data, ca=graphdata)
    
    return render_template("index.html")
        
if __name__ == '__main__':
    app.run()
