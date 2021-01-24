import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, Response, request

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def plot():
    # Formatting
    plt.rcParams["figure.figsize"] = (20,10)
    fig, ax = plt.subplots()
    fig.suptitle("RINs by Fuel Category Over 2020", fontsize = 40)
    ax.ticklabel_format(useOffset=False, style='plain')

    # Import data and aggregate
    rin_df = pd.read_csv("dataset.csv")
    by_category = rin_df.groupby(['Fuel Category', 'Month']).sum()[['RINs','Volume (Gal.)']].reset_index()
    df = by_category.pivot(index='Month',columns='Fuel Category', values='RINs')
    
    df.plot(ax = ax)
    plt.savefig('static/images/plot.png')
    url = "/static/images/plot.png"

    output = request.form.get('options')
    return render_template('plot.html', output = output, url = url)

if __name__ == "__main__":
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)
