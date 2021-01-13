def funding_rate_time(data_directory=None):
    # Create a selection that chooses the nearest point & selects based on x-value
    import altair as alt
    import pandas as pd
    import os

    if data_directory is None:
        data_directory = os.environ.get("data-directory")


    chart_height=200
    chart_width=800


    window = pd.read_csv(f'{data_directory}/window.csv')
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single',
                            nearest=True,
                            on='mouseover',
                            encodings=['x'],
                            empty='none')




    selectors = alt.Chart(window).mark_point().encode(
        x='posted:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    #===============================================================================
    #===============================================================================
    #===============================================================================
    funding_rate_chart = (alt.Chart(window,
               height=chart_height,
               width=chart_width)

     .mark_area(size=3,
                color='cornflowerblue')

     .encode(
        x=alt.X('posted:T',
                title='',
                axis=alt.Axis(grid=False,
                              bandPosition=0.5,
                              tickCount=5,
                              labelColor='black',
                              labelFontSize=12,
                              format='%Y')),

        y=alt.Y('funded:Q',
                title='',
                axis=alt.Axis(tickCount=3, format='%'),
                scale=alt.Scale(domain=(0.0, 1)),
               )))

    #===============================================================================
    #===============================================================================
    #===============================================================================

    year_rects = (alt.Chart(window,height=chart_height,
               width=chart_width)

                  .mark_area(
                      color='white',
                      opacity=0.2,
                      clip=True)

                  .encode(
                      x=alt.X('posted:T',
                              axis=alt.Axis(
                                  title='',
                                  domainOpacity=0,
                                  grid=False,
                                  format='%Y',
                                  tickOpacity=0,
                                  labelFontSize=12,
                                  labelOpacity=1,
                                  tickCount=4)),

                      y=alt.Y('even:Q', title='',
                              scale=alt.Scale(domain=(0, 1)))
                  ).transform_calculate(even='datum.even_year * datum.funded')
                 )


    #===============================================================================
    #===============================================================================
    #===============================================================================
    # Draw a rule at the location of the selection
    rules = alt.Chart(window).mark_rule( strokeDash=[6,5]).encode(
        x='posted:T'
    ).transform_filter(
        nearest
    )

    #===============================================================================
    #===============================================================================
    #===============================================================================
    # Draw text labels near the points, and highlight based on selection
    text = (alt.Chart(window)
            .mark_text(align='center', y=1.15*chart_height, size=12, opacity=0.1)
            .encode(
                x='posted:T',
                text=alt.Text('s:O'),
                opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
            .transform_calculate(s='join([timeFormat(datum.posted, "%b %d"),format(datum.funded, ".1%")], ": ")')
           )

    #===============================================================================
    #===============================================================================
    #===============================================================================
    funding_rate_date_chart = ((funding_rate_chart + selectors   + year_rects + rules + text)
                               .properties(title='Project funding rates by posting date')
                               .configure_title(color='dimgray'))


    return funding_rate_date_chart

funding_rate_time()
