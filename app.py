import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, Response, request
import numpy as np
import calendar

app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET','POST'])
def plot():
    # Read form input
    output = request.form.get('options')
    checked = request.form.getlist('categories')
    if output is None:
        output = "RINs"

    # Formatting and setting parameters
    plt.rcParams["figure.figsize"] = (20,10)
    fig, ax = plt.subplots()
    fig.suptitle(output + " by Fuel Category Over 2020", fontsize = 40)
    ax.ticklabel_format(useOffset=False, style='plain')
    line_url = 'static/images/line_plot.png'
    pie_url = 'static/images/pie_plot.png'

    # Import data and aggregate
    raw_df = pd.read_csv("dataset.csv")
    by_category = raw_df.groupby(['Fuel Category', 'Month']).sum()[['RINs','Volume (Gal.)']].reset_index()
    print(by_category.head())

    # Filter based on checked fuel categories
    filter_list = []
    for row in by_category['Fuel Category']:
        filter_list.append(row in checked)
    filtered = by_category[filter_list]
    if len(filtered.index) == 0:
        filtered = by_category

    # Plot and save line graph
    pivoted = filtered.pivot(index = 'Month', columns='Fuel Category', values=output)
    plt.xticks(np.arange(12), calendar.month_abbr[1:13], rotation=20)
    pivoted.fillna(pivoted.mean()).plot(ax = ax)
    plt.savefig(line_url)

    # Plot and save pie chart
    consolidated = filtered.groupby(['Fuel Category']).sum()[['RINs','Volume (Gal.)']].reset_index()
    consolidated.set_index('Fuel Category', inplace = True)
    ax.clear()
    consolidated.plot(ax = ax, y = output, kind = 'pie', labeldistance = None)
    plt.savefig(pie_url)

    # return render_template('plot.html', checked = checked, output = output, url = url)
    return render_template('plot.html', line_url = line_url, pie_url = pie_url)

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
