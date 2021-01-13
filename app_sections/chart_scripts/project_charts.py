import pandas as pd
import altair as alt


def funding_rate_category(filepath='data/funding.csv'):
    funding = filepath


    minimal_axis = alt.Axis(grid=False, ticks=False,labels=False)


    median_sort = alt.EncodingSortField('median:Q', order='descending')

    base = (
        alt.Chart(funding, width=200, title='Project funding rates')
        .mark_bar()
        .encode(
            x=alt.X('funded_rate:Q', title=''),

            y=alt.Y('median:O',
                    title='',
                    axis=None,
                    sort=median_sort)
        )
    )

    bars = (base
            .encode(
                color=alt.Color('threshold:N',
                                sort=alt.EncodingSortField('median:Q', order='descending'),

                                    scale=alt.Scale(range=['#556c5b', '#f36a5d']),
                                legend=None))
           )

    labels = base.mark_text(
        align='right',
        baseline='middle',
        dx=-21,
        color='white',
        fontSize=13
    ).encode(
        text='Project Resource Category:N'
    )

    values = base.mark_text(
        align='left',
        baseline='middle',
        dx=5,
        fontSize=13
    ).encode(
        text=alt.Text('funded_rate:Q', format='.1%'),
    )

    prop_funded_category = ((bars + labels + values).
                            configure_view(strokeWidth=0)
                            .configure_title(color='dimgray'))

    return prop_funded_category





def funding_rate_time(filepath='data/window.csv'):
    # Create a selection that chooses the nearest point & selects based on x-value



    chart_height=100
    chart_width=600


    window = filepath
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

     .mark_line(size=3,
                color='cornflowerblue')

     .encode(
        x=alt.X('posted:T',
                title='',
                axis=alt.Axis(grid=False,
                              bandPosition=0.5,
                              tickCount=5,
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
                      color='lightslategray',
                      opacity=0.1,
                      clip=True)

                  .encode(
                      x=alt.X('posted:T',
                              axis=alt.Axis(
                                  title='',
                                  domainOpacity=0,
                                  grid=False,
                                  tickOpacity=0,
                                  labelFontSize=12,
                                  labelOpacity=0.2,
                                  tickCount=4,
                                  labelPadding=-0.2 * chart_height,
                                  tickOffset=(60))),

                      y=alt.Y('even_year:Q', title='',
                              scale=alt.Scale(domain=(0, 1)))
                  ))


    #===============================================================================
    #===============================================================================
    #===============================================================================
    # Draw a rule at the location of the selection
    rules = alt.Chart(window).mark_rule(color='gray', opacity=0.7, y=0, y2=chart_height/2,  strokeDash=[6,5]).encode(
        x='posted:T',
    ).transform_filter(
        nearest
    )

    #===============================================================================
    #===============================================================================
    #===============================================================================
    # Draw text labels near the points, and highlight based on selection
    text = (alt.Chart(window)
            .mark_text(align='center', y=.65*chart_height, size=12, opacity=0.1)
            .encode(
                x='posted:T',
                text=alt.Text('s:O'),
                opacity=alt.condition(nearest, alt.value(.4), alt.value(0))
    )
            .transform_calculate(s='join([timeFormat(datum.posted, "%b %d"),format(datum.funded, ".1%")], ": ")')
           )

    #===============================================================================
    #===============================================================================
    #===============================================================================
    funding_rate_date_chart = ((year_rects + selectors + funding_rate_chart +  rules + text)
                               .properties(title='Project funding rates by posting date')
                               .configure_title(color='dimgray'))


    return funding_rate_date_chart



__all__ = ['funding_rate_category', 'funding_rate_date']
