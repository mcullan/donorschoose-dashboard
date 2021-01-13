def funding_rate_category(funding):

    import altair as alt
    import pandas as pd
    import os

    #if data_directory is None:
    #    data_directory = os.environ.get("data-directory")


    #funding=pd.read_csv(f'{data_directory}/funding.csv', index_col=0)
    #funding = filepath

    minimal_axis = alt.Axis(grid=False, ticks=False,labels=False)

    base = (
        alt.Chart(funding, width=300, height=420, title='')
        .mark_bar()
        .encode(
            x=alt.X('funded_rate:Q', title='',axis=None),

            y=alt.Y('category:N',
                    axis=None,
                    sort='-x',
                    title='')
        )
    )




    selector = alt.selection_single(encodings=['x', 'y'], nearest=True, on='mouseover',empty='none')

    bars = (base
            .encode(
                color=alt.Color('threshold:N',
                                scale=alt.Scale(domain=[0,1], range=['#039590', '#f36a5d']),
                                legend=None),
                opacity=alt.condition(selector, alt.value(.8), alt.value(1))
            )


           ).add_selection(selector)


    labels = base.mark_text(
        align='right',
        baseline='middle',
        dx=-21,
        color='white',
        fontSize=13
    ).encode(
        text='category:N'
    )

    values = base.mark_text(
        align='left',
        baseline='middle',
        dx=5,
        fontSize=13
    ).encode(
        text=alt.Text('funded_rate:Q', format='.1%'),
    )

    prop_funded_category = ((bars + labels + values))




    points_ = (alt.Chart(funding, width=200, height=150,
                         title=''
                        )
     .mark_point(filled=True,
                 size=700

                )
     .encode(
         x=alt.X('median:Q',
                 axis=alt.Axis(grid=False,
                               title='Median project cost (by category)',
                               format='$.0f',
                               tickCount=1)),

         y=alt.Y('funded_rate:Q',
                 axis=alt.Axis(grid=False,
                               title='',
                               format='%',
                               tickCount=1,

                              ),
                 scale=alt.Scale(domain=[.5, 1]))
     )
    )

    points = (points_
              .encode(
         color=alt.Color('threshold:N',
                                scale=alt.Scale(range=['#556c5b', '#ffa27a'])),
         opacity=alt.condition(selector, alt.value(1), alt.value(0.4))
     )
    )




    text_template = (alt.Chart(funding)
            .mark_text(
            )
            .encode(
                text='out:N',
                opacity=alt.condition(selector, alt.value(1), alt.value(0))
            ))


    text_category = (text_template
                     .mark_text(size = 24, dx=-10, align='left')
                     .transform_calculate(
                out=('join([datum.category])')
            ))

    text_median = (text_template.mark_text(size = 14, dy=30, align='left')
                     .transform_calculate(
                         out=('join(["Median project cost", format(datum.median, "$.2f")], ":   ")')))


    text_rate = (text_template.mark_text(size = 14, dy=50, align='left')
                     .transform_calculate(
                         out=('join(["Percent of projects funded", format(datum.funded_rate, ".1%")], ":   ")')))




    out  =  prop_funded_category | ((points  ) & (text_category + text_median + text_rate) )




    return out.configure_view(strokeWidth=0).configure_title(color='gray')
