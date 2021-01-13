def app():
    import streamlit as st


    about_page = """
## Dashboard Implementation

### Streamlit
This dashboard was built using [Streamlit](streamlit.io). I chose Streamlit over something like [Flask](flask.com) for simplicity and quick delivery.

With Streamlit, we have:
* The ability to run any Python code server-side
* No need to set up a full web framework
* Markdown integration for writing text and laying sections out
* Built-in widgets like dropdown boxes, datepickers, etc that work with any Python functions

### Heroku
I deployed on Heroku, which provides a somewhat-limited free tier for hosting web apps.

The Heroku app tracks a GitHub repository, and automatically builds after commits are pushed to the repository's main branch. In fact, I also deployed a test version of the app that tracks the repository's development branch. That lets me build and test new features on the dashboard without breaking the "live" one.

### Visualizations

#### Optional Contributions Chart: Plot.ly
This plot, technically a *Sankey Chart*, was made using [Plotly](plot.ly). Lots of great things to say about this software. Ploty provides multiple interfaces for creating charts. If you need a standard chart and not much customization, you can use **Plotly express**. For complicated things (like this chart), they provide the *Graph Objects* interface.

#### Everything else: Altair
Most of the plots herein are made with [Altair](altair-viz.github.io). Altair is actually a Python wrapper for Vega-Lite, a JSON specification for data visualizations.

Altair/Vega-Lite provide, in my experience, the easiest approach to linking selections across charts. That's something we see in the **Project Analysis** chart. As you mouse-over the bar chart, points are highlighted in the scatter chart and text is displayed in the bottom corner.

Moreover, these charts are completely rendered by JavaScript and D3. What's so great about that? We can place interactive charts in static HTML, and all computation is handled on the client-side (the user's computer). So even though the charts are shown here on Streamlit, which has Python running server-side, we could actually host them on something like GitHub Pages.

### Data / Analytics

#### Main Data Warehouse
Currently, I'm working just from flat CSV files as provided by DonorsChoose. For a full deployment, the obvious choice would be SQL. The data exists in separate tables with clear relational keys, so it would be a straightforward deployment.

For this, I would probably set up a managed PostgreSQL database through AWS. AWS RDS server also allows for *spot instances*, which mean we don't get charged for the database when it's not in use. Since this is an example dashboard and not a real production system, that would be most of the time.


#### Analytics data warehouse

Currently, I am running all analytics locally in Jupyter notebooks. In a real-world setting, in which we have new data streaming in constantly, I would be using SQL again. This would be a good place for a managed service like BigQuery or RedShift. With the amount of data we currently have, BigQuery would likely be cheaper.


#### Caching results
This dashboard only makes weekly and monthly reports, which makes it easy to pre-compute and cache results. Why is this helpful? Let's compare it to the other approach: query our database / CSV files and generate the report live.
* On my machine, it takes around 20 seconds to load the original data and another 10 seconds to run the report. This computation takes in about 4 gigabytes of data and produces results around 0.5% that size.
* We couldn't run those computations on this Heroku app even if we wanted to. Free Heroku apps don't have enough memory to fit all that data. Even if they did, we would still have to wait around for results.
* If we ran a query on BigQuery every time, we would spend about 0.0002$ every time we wanted to view the page. And again... we would still have to wait.

To speed things up, I computed every single report the dashboard needed, and then hosted them on Amazon S3. Then, the app just downloads a little CSV report from S3 when it needs to display results.
"""

    st.markdown("")
    st.markdown(about_page)

if __name__=='__main__':
    app()
