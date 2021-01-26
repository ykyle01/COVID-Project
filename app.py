import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from flask import Flask, render_template, Response, request

app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET','POST'])
def plot():
    # Read form input
    output = request.form.get('options')
    checked = request.form.getlist('categories')

    # Formatting and setting parameters
    plt.rcParams["figure.figsize"] = (20,10)
    fig, ax = plt.subplots()
    fig.suptitle(output + " by Fuel Category Over 2020", fontsize = 40)
    ax.ticklabel_format(useOffset=False, style='plain')
    url = "/static/images/plot.png"
    
    # Import data and aggregate
    raw_df = pd.read_csv("dataset.csv")
    by_category = raw_df.groupby(['Fuel Category', 'Month']).sum()[['RINs','Volume (Gal.)']].reset_index()
    
    # Filter based on checked fuel categories
    filter_list = []
    for row in by_category['Fuel Category']:
        filter_list.append(row in checked)
    filtered = by_category[filter_list]
    if len(filtered.index) == 0:
        filtered = by_category

    # Plot and save
    pivoted = filtered.pivot(index='Month', columns='Fuel Category', values=output)
    pivoted.fillna(pivoted.mean()).plot(ax = ax)

    plt.savefig('static/images/plot.png')
    # return render_template('plot.html', checked = checked, output = output, url = url)
    return render_template('plot.html', url = url)

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=False)
