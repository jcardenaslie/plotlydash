import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd

df = pd.read_excel('cotizaciones_all.xlsx')

def generate_table(dataframe, proyecto='Todos los Proyectos', max_rows=10):
    if filter != 'Todos los Proyectos':
            dataframe = dataframe[dataframe['Proyecto'] == proyecto]

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr(
            [
                html.Td(dataframe.iloc[i][col]) 
                for col in dataframe.columns
            ]) 
        for i in range(min(len(dataframe), max_rows))]
    )


#  Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)

proyectos = df.Proyecto.unique()
options = []

map_data = df

for p in proyectos:
    options.append({'label':p, 'value': p})
options.append({'label':'Todos los Proyectos', 'value': 'TP'})

app = dash.Dash()

app.layout = html.Div(children=[
    html.Label('Proyectos'),
    dcc.Dropdown(
        id='dropdown_b',
        options=options,
        value='TP',
        multi=True,
    ),
   
    html.Div(id='output-b'),
    
    html.Div(id='output-a'),
    html.Label('Cantidad de Filas a ver'),

    dcc.Slider(
        id='slider_filas',
        min=0,
        max=map_data.shape[0],
        step=50,
        # marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
    html.Div(id='slider_output'),
    
    html.H4(children='Cotizaciones'),
    # generate_table(df)
    html.Div(
             [
                dt.DataTable(
                    rows=map_data[:10].to_dict('records'),
                    columns=map_data.columns,
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    id='datatable'),
                ],
            style = layout_table,
            className="six columns"
        ),
])

#Callback a elemento: output-b
@app.callback(
    Output('output-b', 'children'),
    [dash.dependencies.Input('dropdown_b', 'value')])
def callback_proyecto_selected(dropdown_value):
    return 'Proyectos seleccionados "{}"'.format(dropdown_value)

#Callback a elemento: output-a
@app.callback(
    Output('output-a', 'children'),
    [dash.dependencies.Input('dropdown_b', 'value')])
def callback_cantidad_filas(dropdown_value):
    map_aux = map_data.copy()
    if 'TP' not in dropdown_value:
        map_aux = map_aux[map_aux['Proyecto'].isin(dropdown_value)]
    
    q = map_aux.shape[0]
    print(1)
    return 'Filas: {}'.format(q)

@app.callback(
    Output('slider_output', 'children'),
    [Input('slider_filas', 'value')])
def callback_slider_cantidad_filas(slider_value):
    print(slider_value)
    return 'Viendo {} filas de {}'.format(slider_value, map_data.shape[0])
    # return 'Proyectos seleccionados "{}"'.format(dropdown_value)


#Callback a elemento: datatable
@app.callback(
   Output('datatable', 'rows'),
    [Input('dropdown_b', 'value'),
    Input('slider_filas', 'value')
    ])
def update_selected_row_indices(dropdown_b, slider_filas):
    map_aux = map_data.copy()
    
    if 'TP' not in dropdown_b:
        map_aux = map_aux[map_aux['Proyecto'].isin(dropdown_b)]
    
    # Type filter
    # Boroughs filter
    rows = map_aux[:10].to_dict('records')
    return rows


if __name__ == '__main__':
    app.run_server(debug=True)