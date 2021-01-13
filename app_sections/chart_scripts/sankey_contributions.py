
def sankey_contributions(data_directory=None):
    import altair as alt
    import pandas as pd
    import plotly.graph_objects as go
    data_directory = 'analytics-data'
    nodes = pd.read_csv(f'{data_directory}/sankey-nodes.csv', index_col=0)
    links = pd.read_csv(f'{data_directory}/sankey-links.csv', index_col=0)

    fig = go.Figure(data=[go.Sankey(arrangement = "snap",


        node = dict(
            pad = 20,
            thickness = 20,
            line = dict(color = "gray", width = 0.5),
            hovertemplate='%{customdata} <br>'+'Number of donors: %{value} <extra></extra>',
            customdata = nodes['label'],
            color = nodes.loc[:,'color']
        ),
        link = dict(
          source = links.loc[:,'index_source'], # indices correspond to labels, eg A1, A2, A1, B1, ...
          target = links.loc[:,'index_target'],

          value = links.loc[:,'Value'],
          color = links.loc[:,'color'],
            hovertemplate='%{source.customdata} <br>'+
            '%{target.customdata}<br><br>Number of donors: %{value} <extra></extra>',
      ))])

    fig.update_layout(
        margin=dict(l=0, r=5, t=10, b=30),
        width=300,
        height=200
    )




    # Add annotations for "first donation, etc"
    labels_y = -0.1
    annotation_size = 10

    fig.add_annotation(x=-0.01, y=labels_y,
                       align='center',
                       font_size=annotation_size,
                       opacity=0.7,
                       text="First",
                       showarrow=False)

    fig.add_annotation(x=.23, y=labels_y,
                       align='center',
                       font_size=annotation_size,
                       opacity=0.7,
                       text="Second",
                       showarrow=False)

    fig.add_annotation(x=.5, y=labels_y,
                       align='center',
                       font_size=annotation_size,
                       opacity=0.7,
                       text="Third",
                       showarrow=False)

    fig.add_annotation(x=.78, y=labels_y,
                       align='center',
                       font_size=annotation_size,
                       opacity=0.7,
                       text="Fourth",
                       showarrow=False)

    fig.add_annotation(x=1.01, y=labels_y,
                       align='center',
                       font_size=annotation_size,
                       opacity=0.7,
                       text="Fifth",
                       showarrow=False)



    # Add annotations for green/red bars
    '''fig.add_annotation(x=0.04, y=.8,
                       font_size=9,
                       align='left',
                       text="Donor makes an <br>optional contribution.",
                       showarrow=False)

    fig.add_annotation(x=0.04, y=0,
                       font_size=9,
                       align='left',
                       text="No contribution.",
                       showarrow=False)'''

    fig.add_annotation(x=1, y=1,
                       font_size=10,
                       align='right',
                       opacity=0.7,
                       text="Optional contributions throughout<br>a donor's first 5 donations.",
                       showarrow=False)


    return fig
