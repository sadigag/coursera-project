import dash
from dash import html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize the app
app = dash.Dash(__name__)

# Initial sample data
initial_data = pd.DataFrame({
    'category': ['Electronics', 'Clothing', 'Food'],
    'sales': [30000, 20000, 15000]
})

app.layout = html.Div([
    # Main container
    html.Div([
        # Header
        html.H1('Interactive Sales Dashboard',
                style={'color': '#2c3e50', 'text-align': 'center'}),

        # Input section
        html.Div([
            # Category input
            html.Div([
                html.Label('Category Name:'),
                dcc.Input(
                    id='category-input',
                    type='text',
                    placeholder='Enter category name',
                    style={'margin': '10px', 'padding': '5px'}
                ),
            ]),

            # Sales input
            html.Div([
                html.Label('Sales Amount:'),
                dcc.Input(
                    id='sales-input',
                    type='number',
                    placeholder='Enter sales amount',
                    style={'margin': '10px', 'padding': '5px'}
                ),
            ]),

            # Add button
            html.Button('Add Data',
                        id='add-button',
                        n_clicks=0,
                        style={
                            'margin': '10px',
                            'padding': '10px 20px',
                            'backgroundColor': '#3498db',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer'
                        }),

            # Reset button
            html.Button('Reset Data',
                        id='reset-button',
                        n_clicks=0,
                        style={
                            'margin': '10px',
                            'padding': '10px 20px',
                            'backgroundColor': '#e74c3c',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer'
                        }),
        ], style={'margin': '20px 0', 'textAlign': 'center'}),

        # Pie Chart
        dcc.Graph(id='pie-chart'),

        # Store component to save the data
        dcc.Store(id='data-store', data=initial_data.to_dict('records')),

        # Error message div
        html.Div(id='error-message',
                 style={'color': 'red', 'textAlign': 'center', 'margin': '10px'})

    ], style={
        'max-width': '800px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
        'borderRadius': '8px'
    })
])


# Callback to update the pie chart and handle data addition
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('data-store', 'data'),
     Output('error-message', 'children'),
     Output('category-input', 'value'),
     Output('sales-input', 'value')],
    [Input('add-button', 'n_clicks'),
     Input('reset-button', 'n_clicks')],
    [State('category-input', 'value'),
     State('sales-input', 'value'),
     State('data-store', 'data')]
)
def update_dashboard(add_clicks, reset_clicks, category, sales, data):
    # Get the button that triggered the callback
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'reset-button':
        # Reset to initial data
        return (
            create_pie_chart(initial_data.to_dict('records')),
            initial_data.to_dict('records'),
            '',
            None,
            None
        )

    elif triggered_id == 'add-button':
        # Validate inputs
        if not category or not sales:
            return (
                create_pie_chart(data),
                data,
                'Please fill in both category and sales amount',
                category,
                sales
            )

        # Add new data
        current_data = pd.DataFrame(data)
        new_row = pd.DataFrame([{'category': category, 'sales': sales}])
        updated_data = pd.concat([current_data, new_row], ignore_index=True)
        updated_records = updated_data.to_dict('records')

        return (
            create_pie_chart(updated_records),
            updated_records,
            '',
            None,
            None
        )

    # Initial load
    return (
        create_pie_chart(data),
        data,
        '',
        None,
        None
    )


def create_pie_chart(data):
    df = pd.DataFrame(data)
    fig = px.pie(
        df,
        values='sales',
        names='category',
        title='Sales Distribution',
        hole=0.3,  # Makes it a donut chart
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)