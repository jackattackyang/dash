import pandas as pd
import plotly_express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)
server = app.server

df = px.data.gapminder()

app.layout = html.Div(children=[
    html.Div(
        dash_table.DataTable(
                            id='table',
                            columns=[
                                {"name": i, "id": i, "selectable": True, 'hideable': True} for i in df.columns
                            ],
                            data=df.to_dict('records'),
                            editable=True,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable="single",
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            fixed_rows={'headers': True},
                            page_size=20,
                            style_table={'height': '500px', 'overflowY': 'auto'},
                            style_cell={
                                'width': '35px',
                                'maxWidth': '35px',
                                'minWidth': '35px',
                            }

        )
    ),
    html.Div(html.Div(id='bar-container'))
], style={'width': '100%', 'display': 'flex'})

@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='table', component_property='derived_virtual_data')]
)
def update_bar(data):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

    dff = df if data is None else pd.DataFrame(data)
    dff = (dff.value_counts(['continent']).reset_index(name='count_')
           .assign(pct_=lambda x: x.count_ / x.count_.sum() * 100))
    return [
        dcc.Graph(id='barplot',
                  figure=(px.bar(dff,
                                 x='continent', y='count_', text='pct_',
                                 hover_data={'continent': False, 'pct_': False})
                          .update_layout(
                              xaxis={'categoryorder': 'total descending'},
                              title='Gapminder Barplot',
                              xaxis_title='Continent',
                              yaxis_title='Count')
                          .update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                          ),
            style={'width': '400'}
                      )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
