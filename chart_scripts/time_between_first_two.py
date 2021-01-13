
def time_between_first_two(filepath='analytics-data/second_donation_desc.csv'):
    import altair as alt
    import pandas as pd

    second_donation_desc = pd.read_csv(filepath, index_col=0)
    ytitle = ['⟵ Lifetime number of donations']

    chart = (alt.Chart(second_donation_desc, width=500)
     .mark_line(size=2, color='cornflowerblue')
     .encode(
         y=alt.Y('num',
                 title=ytitle,
                 sort='-y',
                 scale=alt.Scale(domain=(1, 10)),
                 axis=alt.Axis(domainOpacity=0,
                               labelOpacity=0,
                               titleAlign='right',
                               titleX=195,
                               titleY=283,
                               titleOpacity=1,
                               titleAngle=0,
                               titleFontSize=12,
                               labelFontSize=14,
                               grid=False,
                               tickOpacity=0)
                ),

         x=alt.X('median:Q',
                 title=['Median days between first two donations ⟶'],
                 axis=alt.Axis(grid=False,
                               domainOpacity=0,
                               titleColor='cornflowerblue',
                               tickCount=0,
                               titleFontSize=12,
                               titleAlign='right',
                               titleY=-29,
                               titleX=450,
                               titleOpacity=1),
                 scale=alt.Scale(domain=(60, 220))
                )
    ))



    rules2 = (alt.Chart(second_donation_desc)
              .mark_rule(orient='horizontal',
                         opacity=.5)
              .encode(
                  x='median',
                  y='num',
    ))

    rule_labels = (alt.Chart(second_donation_desc)
                   .mark_text(dy=10,
                              fontSize=12,
                              opacity=1,
                              color='cornflowerblue')

                   .encode(
                       x='dx:Q',
                       y='num',
                       text=alt.Text('median', format='.0f'))

                   .transform_calculate(dx='datum.median -10 + (10 / (sqrt(datum.num)))')
                  )


    note = '''
    The time between the first and second donation is a
    strong indicator of the number of total donations.
    If the second donation comes sooner, we expect
    high lifetime value from that donor.
    '''.split('\n')


    annotation = (alt.Chart()
                  .mark_text(
                      x=460,
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


    combined = chart + rule_labels + rules2 + annotation + y_labels

    return (combined
     .configure_view(strokeOpacity=0)
     .configure_axis(titleFontWeight='normal',
                     titleFontSize=14,
                     titlePadding=20))
