import json
import os
from dotenv import load_dotenv

import altair as alt
import pandas as pd
import streamlit as st
alt.renderers.set_embed_options(actions=False)

import boto3

load_dotenv()

def app():
    col_1, col_2, col_3= st.beta_columns((1,1,1))
    with col_1:
        week_box = st.selectbox(
        "Week of:",
        ['Select', 'January 6, 2017', 'January 13, 2017', 'January 20, 2017', 'January 27, 2017', 'February 3, 2017', 'February 10, 2017', 'February 17, 2017', 'February 24, 2017', 'March 3, 2017', 'March 10, 2017', 'March 17, 2017', 'March 24, 2017', 'March 31, 2017', 'April 7, 2017', 'April 14, 2017', 'April 21, 2017', 'April 28, 2017', 'May 5, 2017', 'May 12, 2017', 'May 19, 2017', 'May 26, 2017', 'June 2, 2017', 'June 9, 2017', 'June 16, 2017', 'June 23, 2017', 'June 30, 2017', 'July 7, 2017', 'July 14, 2017', 'July 21, 2017', 'July 28, 2017', 'August 4, 2017', 'August 11, 2017', 'August 18, 2017', 'August 25, 2017', 'September 1, 2017', 'September 8, 2017', 'September 15, 2017', 'September 22, 2017', 'September 29, 2017', 'October 6, 2017', 'October 13, 2017', 'October 20, 2017', 'October 27, 2017', 'November 3, 2017', 'November 10, 2017', 'November 17, 2017', 'November 24, 2017', 'December 1, 2017', 'December 8, 2017', 'December 15, 2017', 'December 22, 2017', 'December 29, 2017']
        )

    with col_2:
        expiring_box = st.selectbox(
        "Expiring within:",
        ['Select', '7 Days', '14 Days']
        #['Select', '7 Days', '14 Days']
        )

    with col_3:
        state_box = st.selectbox(
        "State:",
        ['All'] + ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        )

    if week_box != 'Select' and expiring_box != 'Select':
        date = pd.to_datetime(week_box).strftime("%Y-%m-%d")
        expiring_within = int(expiring_box.split()[0])
        data_directory  = os.environ.get("data-directory")
        fname_projects = f'{date}--at-risk-projects--{expiring_within}-days.csv'
        fname_donors = f'{date}--at-risk-donors--{expiring_within}-days.csv'

        df_ = pd.read_csv(f"{data_directory}/at-risk-projects-data/{fname_projects}")
        donors = pd.read_csv(f"{data_directory}/at-risk-projects-data/{fname_donors}", index_col=0)
        df = df_

        if state_box != "All":
            df = df_[df_['School State']==state_box]

        col_number, col_lost_revenue, col_median_remaining = st.beta_columns((1,1,1))

        with col_number:
            st.markdown('### Number of Projects')
            st.markdown(df.shape[0])

        with col_lost_revenue:
            st.markdown('### Total Cost Remaining')
            st.markdown(f"${df['Remaining Cost'].sum(): ,.2f}")

        with col_median_remaining:
            st.markdown('### Median Cost Remaining')
            st.markdown(f"${df['Remaining Cost'].median():,.2f}")

        df = df.sort_values('Remaining Cost', ascending=False)
        top_10 = df.head(10)
        display_names = list(top_10['School Name'] + ': ' + top_10['Project Title'])
        #top_box = st.selectbox("Top 10 Projects:", ['Select'] + display_names)
        top_box = st.selectbox("Top 10 Projects:", display_names)


        if top_box != "Select":
            top_index = display_names.index(top_box)
            top = top_10.iloc[top_index, :]

            fields = {}
            fields['School Name'] = top['School Name']
            fields['Project Title'] = top['Project Title']
            fields['Location'] = f"{top['School City']}, {top['School State']}"
            fields['Subject'] = top['Project Subject Category Tree']
            fields['Category'] = top['Project Resource Category']
            fields['Expires In:'] = f"{top['Days to Expiration']} Days"
            #fields['Current Progress'] = ""
            fields['Remaining'] = top['Remaining Cost']


            data  = pd.DataFrame({'Project Cost':[top['Project Cost']],
                                  'Current Progress':[top['Current Revenue']]})
            bullet = (alt
             .Chart(data, height=15,
                    width=310,
                    padding=0,
                    background='#f0f2f6')
             .mark_bar(size=15, color='steelblue',cornerRadiusBottomRight=5,cornerRadiusTopRight=5)
             .encode(x=alt.X('Current Progress:Q',
                             scale=alt.Scale(padding=0, domain=[0, top['Project Cost']]),
                             axis=None),
                    tooltip=['Project Cost', 'Current Progress']
                             )).configure_axis(grid=False).configure_view(strokeWidth=0)

            cols = st.beta_columns((1,1,1,1))
            i = 0
            for ix, (key, value) in enumerate(fields.items()):
                if ix == 4:
                    cols = st.beta_columns((1,1,2))
                    i = 0
                with cols[i]:
                    if key =="Remaining":
                        st.markdown(f"### {key}: ${value:,.2f}")
                        st.altair_chart(bullet)
                    else:
                        st.markdown(f"### {key}")

                        st.markdown(f"{value}")

                i += 1





            donor_col1, donor_col2= st.beta_columns((1,1))
            with donor_col1:
                display_button = st.button("Display Potential Donors")

            if display_button:
                st.write(f'Donors who have donated to {top["School Name"]} in the past:')

                donors_active = donors[donors['School ID'] == top['School ID']]
                donors_out = donors_active[['Donor ID', 'Donor City', 'Donor State', 'Donor Is Teacher']]

                table_col, note_col = st.beta_columns((4, 1))
                with table_col:
                    st.write(donors_out)
                with note_col:
                    st.markdown("""I'm using a very simple rule here: donors who have donated to this school in the past.

In this future, this could be replaced by a machine learning model that predicts likely donors.
                    """)

                from base64 import b64encode

                csv = donors_out.to_csv(index=False)
                b64 = b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="donors.csv">Download csv file</a>'

                with donor_col2:
                    st.markdown(href, unsafe_allow_html=True)


    #df = pd.read_csv(f'{data_directory}/{fname}')


if __name__=='__main__':
    st.title("Dashboard")
    st.sidebar.markdown("Sidebar")
    app()
    #st.write(df.shape[0])
