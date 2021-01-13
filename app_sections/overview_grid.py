def get_data(data_directory=None):
    import pandas as pd
    import os
    from dotenv import load_dotenv
    load_dotenv()
    if data_directory is None:
        data_directory = os.environ.get("data-directory")

    df = pd.read_csv(f'{data_directory}/monthly_analytics.csv', index_col=0,
                     parse_dates=['start_date']).set_index('start_date')

    return df
def app():
    import pandas as pd
    import streamlit as st

    import altair as alt
    import os


    data_directory = os.environ.get("data-directory")


    months = ['January', 'February', 'March',
              'April', 'May', 'June',
              'July', 'August', 'September',
              'October', 'November', 'December']

    st.markdown(f"## Monthly Summary:")
    st.markdown("Select a month and year to view results.")

    df = get_data().round(2)
    month_col, year_col = st.beta_columns(2)

    with year_col:
        year = st.selectbox('Year', range(2013, 2018))

    with month_col:
        if year == 2018:
            month = st.selectbox('Month', ['January', 'February', 'March', 'April'])
        else:
            month = st.selectbox('Month', months)

    row = df.loc[month + ' ' + str(year)]
    st.markdown(f"### Month of {month} {year}")

    datestring = pd.to_datetime(f"{month} {year}").strftime('%Y-%m')
    funding = pd.read_csv(f'{data_directory}/funding-reports-data/{datestring}-funding.csv')


    c1_1, c1_2, c1_3, c1_4 = st.beta_columns(4)
    c2_1, c2_2, c2_3, c2_4 = st.beta_columns(4)
    c3_1, c3_2, c3_3, c3_4 = st.beta_columns(4)
    #c4_1, c4_2, c4_3, c4_4 = st.beta_columns(4)


    def display_grid_val(row,column):

        val = row[column][0]

        if val <= 1:
            val = f"{int(val*100)}%"
        st.markdown(f"## {val}")

    ###### COLUMN 1: Donations
    with c1_1:
        st.markdown('### Donations')
    with c2_1:
        st.markdown('#### Number of Donations')
        display_grid_val(row, 'num_donations')
    with c3_1:
        st.markdown('#### With Contribution')
        display_grid_val(row, 'with_additional')
    ###### COLUMN 2: Projects
    with c1_2:
        st.markdown('### Projects')
    with c2_2:
        st.markdown('#### Number of Projects')
        display_grid_val(row, 'number_of_projects')
    with c3_2:
        st.markdown('#### Successfully Funded')
        display_grid_val(row, 'success_rate')

    ###### COLUMN 3: Donors
    with c1_3:
        st.markdown('### Donors')
    with c2_3:
        st.markdown('#### Total Donors')
        display_grid_val(row, 'unique_donors')
    with c3_3:
        st.markdown('#### New Donors')
        display_grid_val(row, 'new_donors')

    ###### COLUMN 4: Schools
    with c1_4:
        st.markdown('### Schools')

    with c2_4:
        st.markdown('#### Total Schools')
        display_grid_val(row, 'num_schools')

    with c3_4:
        st.markdown('#### New Schools')
        display_grid_val(row, 'proportion_schools_new')


    from chart_scripts.funding_rate_category import funding_rate_category
    #from chart_scripts.funding_rate_time import funding_rate_time


    st.markdown("## Project Success")
    st.altair_chart(funding_rate_category(funding), use_container_width=True)
if __name__=='__main__':
    app()
