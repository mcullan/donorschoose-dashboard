def count_percentile_chart(count_percentiles):
    import altair as alt
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['index'], empty='none')

    line = (alt.Chart(count_percentiles, width=300, height=150)
     .mark_line(clip=True)
     .encode(
         x=alt.Y('index', title="Percentile", axis=alt.Axis(format='%')),
         y=alt.Y('count', title="Number of Donations",
                 scale=alt.Scale(domain=(0, 50))
                )
     ))


    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(count_percentiles).mark_point().encode(
        x='index:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point(clip=True).encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text =line.mark_text(clip=True, align='left', dx=-70, dy=-20).encode(
        text=alt.condition(nearest, 't:N', alt.value(' '))
    ).transform_calculate(t='join(["Donations:", datum.count], " ")')

    # Draw a rule at the location of the selection
    rules = alt.Chart(count_percentiles).mark_rule(color='gray').encode(
        x='index:Q',
    ).transform_filter(
        nearest
    )

    return line + selectors + rules + text + points

def donation_percentile_chart(donation_percentiles):
    import altair as alt
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['index'], empty='none')

    line = (alt.Chart(donation_percentiles, width=300, height=150)
     .mark_line(clip=True)
     .encode(
         x=alt.Y('index', title="Percentile", axis=alt.Axis(format='%')),
         y=alt.Y('sum', title="Total Donation Value",
                 scale=alt.Scale(domain=(0, 1000))
                )
     ))


    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(donation_percentiles).mark_point().encode(
        x='index:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point(clip=True).encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text =line.mark_text(clip=True, align='left', dx=-60, dy=-20).encode(
        text=alt.condition(nearest, 't:N', alt.value(' '))
    ).transform_calculate(t='join(["Total: $", datum.sum], "")')

    # Draw a rule at the location of the selection
    rules = alt.Chart(donation_percentiles).mark_rule(color='gray').encode(
        x='index:Q',
    ).transform_filter(
        nearest
    )

    return line + selectors + rules + text + points



def app():
    import altair as alt
    import os
    import pandas as pd
    def revenue_by_revenue_chart(df):
        import altair as alt
        chart = (alt.Chart(df, width=400)
         .mark_bar()
         .encode(x=alt.X('sum:Q', title='Proportion of Total Revenue'),
                 y=alt.Y('label:O', title='', sort=alt.EncodingSortField(field='binstart', order='descending'))
                ))

        return chart

    def revenue_by_count_chart(df):
        import altair as alt

        chart = (alt.Chart(df, width=320)
         .mark_bar()
         .encode(x=alt.X('sum:Q', title='Proportion of Total Revenue'),
                 y=alt.Y('label:O', title='', sort=alt.EncodingSortField(field='binstart', order='descending'))
                ))

        return chart

    import streamlit as st

    from chart_scripts.sankey_contributions import sankey_contributions
    #from chart_scripts.time_between_first_two import time_between_first_two
    data_directory = os.environ.get("data-directory")



    def time_between_first_two(data_directory=None):
        import altair as alt
        import pandas as pd
        import os

        if data_directory is None:
            data_directory = os.environ.get("data-directory")

        second_donation_desc = pd.read_csv(f'{data_directory}/second_donation_desc.csv', index_col=0)
        second_donation_desc['lift'] = [-1.5,0,0,0,1,0,1,0,1]

        ytitle = 'Total number of donations ' #⟵⟶
        chart_width = 300
        chart_height = 250
        chart = (alt.Chart(second_donation_desc, height=chart_height, width=chart_width)
         .mark_line(size=2, color='cornflowerblue')
         .encode(
             y=alt.Y('num',
                     title=ytitle,
                     sort='-y',
                     scale=alt.Scale(domain=(2, 10)),
                     axis=alt.Axis(domainOpacity=0,
                                   labelOpacity=0,
                                   tickCount=10,
                                   titleColor='cornflowerblue',
                                   titleAlign='center',
                                   #titleX=chart_width//2.5,
                                   #titleY=chart_height//3,
                                   titleOpacity=1,
                                   titleAngle=-90,
                                   titlePadding=2,
                                   titleFontSize=12,
                                   labelFontSize=10,
                                   grid=False,
                                   tickOpacity=0)
                    ),

             x=alt.X('median:Q',
                     title=['Days between first two donations'],
                     axis=alt.Axis(grid=False,
                                   domainOpacity=0,
                                   tickCount=0,
                                   tickOpacity=0,
                                   titleFontSize=12,
                                   titleAlign='center',
                                   titleOpacity=1),
                     scale=alt.Scale(domain=(90, 220))
                    )
        ))



        rules2 = (alt.Chart(second_donation_desc)
                  .mark_rule(orient='horizontal',
                             opacity=.5,
                             strokeDash=(3,3))
                  .encode(
                      x='median',
                      y='num',
        ))

        rules_2 = (alt.Chart(second_donation_desc[second_donation_desc['num']>2])
                  .mark_rule(orient='vertical',
                             opacity=.25,
                             strokeDash=(3,3))
                  .encode(
                      y='h:Q',
                      y2='dy:Q',
                      x='median',
        ).transform_calculate(h='datum.num - .3', dy='2.2+datum.lift/3')
                  )

        rule_labels = (alt.Chart(second_donation_desc)
                       .mark_text(dy=0,
                                  fontSize=12,
                                  opacity=1,
                                  color='cornflowerblue')

                       .encode(
                           x='dx:Q',
                           y='num',
                           text=alt.Text('num', format='.0f'))

                       .transform_calculate(dx='datum.median')
                      )

        rule_labels_x = (alt.Chart(second_donation_desc)
                       .mark_text(
                                  fontSize=8,
                                  opacity=1,
                                  y=chart_height)

                       .encode(
                           x='median:Q',
                           y='dy:Q',
                           text=alt.Text('median', format='.0f'))

                       .transform_calculate(dy='2+datum.lift/3')
                      )


        rule_labels_ = (alt.Chart(second_donation_desc)
                       .mark_point(dy=-10,
                                   size=300,
                                  fontSize=12,
                                   filled=True,
                                  opacity=1,
                                  color='white')

                       .encode(
                           x='dx:Q',
                           y='num',
                           text=alt.Text('num', format='.0f'))

                       .transform_calculate(dx='datum.median - 1')
                      )



        note = '''
        The time between the first and second donation is a
        strong indicator of the number of total donations.
        If the second donation comes sooner, we expect
        high lifetime value from that donor.
        '''.split('\n')


        annotation = (alt.Chart()
                      .mark_text(
                          x=chart_width//4,
                          y=20,
                          fontSize=12,
                          text=note,
                          opacity=0.1,
                          align='right'
                      )
                     )

        y_labels = (alt
                    .Chart(second_donation_desc)
                    .mark_text(dy=10, fontSize=12,x=10, opacity=1,  align='center')
                    .encode(
                        y='num',
                        text=alt.Text('num', format='.0f')
                    )
                   )


        combined = chart  +  rule_labels_ + rules_2 +rule_labels + rule_labels_x

        return (combined
         .configure_view(strokeOpacity=0)
         .configure_axis(titleFontWeight='normal',
                         titleFontSize=14,
                         titlePadding=20))


    st.markdown("## Donor characteristics and revenue")
    col_1, col_2 = st.beta_columns((1,1))
    with col_1:
        st.markdown("### Total Spend")
        st.markdown("""
* Over 25% of all revenue is generated by donors with total donations under $100.
        """)
        df1 = pd.read_csv(f"{data_directory}/bin_revenue_plot_sum.csv")
        chart1 = revenue_by_count_chart(df1)

        st.altair_chart(chart1)


    with col_2:
        st.markdown("### Number of Donations")

        df2 = pd.read_csv(f"{data_directory}/bin_revenue_plot_count.csv")
        chart2 = revenue_by_count_chart(df2)

        st.altair_chart(chart2)
        st.markdown("""
* Over 25% of revenue comes from donors with only one donation.
* Over 50% of revenue comes from donors with 1-5 donations.
        """)

    st.markdown("## Defining high-value")
    st.markdown('''
While "small donors" capture a great deal of revenue, this is because they comprise a greater share of our base.
Mouse over the plots below to view the percentiles of donors according to number of donations and total donation value.
''')
    count_percentiles = pd.read_csv(f"{data_directory}/count_percentiles.csv")
    donation_percentiles = pd.read_csv(f"{data_directory}/donation-percentiles.csv")

    ch1, ch2 = st.beta_columns((1,1))
    with ch1:
        st.altair_chart(count_percentile_chart(count_percentiles))
    with ch2:
        st.altair_chart(donation_percentile_chart(donation_percentiles))

    st.markdown('''
It turns out that 72% of our donors have only donated once!
However, donors with between 2-5 donations also contribute a great share to revenue,
despite being a much smaller group.

I'm recommending that we focus on boosting repeat donations among low-count donors.
''')

    st.sidebar.markdown("## Placeholder")


    st.write("""## Identifying Repeat Donors

This is a very limited data set, since it only consists of actual transactions.
We don't have much information if we want to predict repeat donors based on a single donation. In a real-world setting, we would bolster this data with email clicks and other marketing data.

However, we still get a fair amount of signal and a clear story if we focus on donors with 2 donations.

    """)

    st.write("""### What the first two donations tell us
    """)

    col_1, col_2 = st.beta_columns((1,1))
    with col_2:

        st.markdown("""We'll look at the **number of days** between the first and second donation.
What can this value tell us about the number of times someone will donate in their lifetime?

On the left, I've plotted the median duration between a donor's first and second donation,
grouped by total lifetime donation count. For example, donors with 3 lifetime donations took 164 days,
on average, between their first and second donation.
        """)

    st.markdown("""This result might not be surprising. Shorter gaps means a higher frequency of donations.
But because we can observe the pattern so quickly, we can more aptly identify donors to may be convinced to make, for example, quarterly donations.
In other words, the time between donations presents a compelling **lookalike** for high-value, high-donation donors.

This is only a brief investigation, but it points to opportunity. We have some signal now, and
with more detailed activity data, a machine learning approach could make a serious impact.
""")


    with col_1:
        st.write('')
        st.altair_chart(time_between_first_two())






if __name__=='__main__':
    from dotenv import load_dotenv
    import streamlit as st
    st.title("Dashboard")
    load_dotenv()
    app()
