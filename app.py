import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def plot():
    plt.rcParams["figure.figsize"] = (20,10)
    rin_df = pd.read_csv("dataset.csv")
    by_category = rin_df.groupby(['Fuel Category', 'Month']).sum()[['RINs','Volume (Gal.)']].reset_index()
    df = by_category.pivot(index='Month',columns='Fuel Category', values='RINs')
    df.plot()
    plt.savefig('static/images/plot.png')
    return render_template('plot.html', url ='/static/images/new_plot.png')

if __name__ == "__main__":
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)
