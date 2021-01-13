def app():


    import streamlit as st

    from chart_scripts.sankey_contributions import sankey_contributions
    #from chart_scripts.time_between_first_two import time_between_first_two

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


    st.markdown("## Defining *high-value* donors")
    col_1, col_2 = st.beta_columns((1,1))
    with col_1:
        st.markdown("### Total Spend")
        st.markdown("""
* What does an average donor spend?
    * Do a slider with the percentiles
    * Also zoom in on the top 1% and do it again
* How many of those donors are only donating once?
        """)
    with col_2:
        st.markdown("### Number of Donations")
        st.markdown("""
* Distribution of number of donations
* How many donors come back a second time?
* How frequently are repeat donations made?
* Why do frequency and retention matter?
    * We need a growing donor base to support a growing school / project base
        """)

    st.sidebar.markdown("## Placeholder")


    st.write("## Identifying Repeat Donors")
    st.write('### What the first two donations tell us')

    col_1, col_2 = st.beta_columns((1,1))
    with col_2:

        st.markdown("""
lk;ajsd;lfkasdflkj
asd;foasd;lfkjasd;lfkasdflkjasd


asdlfkjasd;lfalsdf


as;ldkfja;sldkfja


as/dlkfja;lsdfj


asdlfkjas;dlfjadsf


asdf;lkjasd;lfj
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
