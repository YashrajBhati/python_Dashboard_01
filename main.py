import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("student_depression.data_2000.csv")

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Student Depression Dashboard", style={'textAlign': 'center', 'color': 'white', 'backgroundColor': '#222'}),

    # Dropdown for selecting the city
    html.Label("Select a City:", style={'color': 'white'}),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in df['City'].unique()],
        value=df['City'].unique()[0],  # Default to the first city
        clearable=False,
        style={'color': '#000'}  # Dropdown text color
    ),

    html.Br(),

    # Scatter Plot
    html.Div([
        html.H3("Scatter Plot: Degree vs CGPA", style={'color': 'white'}),
        dcc.Graph(id='scatter-plot')
    ]),

    # Bar Graph
    html.Div([
        html.H3("Bar Graph: Academic Pressure by Degree", style={'color': 'white'}),
        dcc.Graph(id='bar-graph')
    ]),

    # Pie Chart
    html.Div([
        html.H3("Pie Chart: Sleep Duration Distribution", style={'color': 'white'}),
        dcc.Graph(id='pie-chart')
    ])
], style={'backgroundColor': '#222', 'padding': '20px'})  # Dark background color for the entire layout

# Callback to update the graphs based on the selected city
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('bar-graph', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('city-dropdown', 'value')]
)
def update_graphs(selected_city):
    # Filter data for the selected city
    filtered_df = df[df['City'] == selected_city]

    # Scatter Plot: Degree vs CGPA
    scatter_fig = px.scatter(
        filtered_df,
        x='Degree',
        y='CGPA',
        title=f'Degree vs CGPA in {selected_city}',
        labels={'Degree': 'Degree', 'CGPA': 'CGPA'},
        color='Degree',
        size='CGPA',
        hover_data=['Degree', 'CGPA']
    )
    scatter_fig.update_layout(
        title_font=dict(color='white'),  # Title color
        paper_bgcolor='#222',           # Background color
        plot_bgcolor='#444',            # Plot area background color
        font=dict(color='white')        # General font color
    )

    # Bar Graph: Academic Pressure by Degree
    bar_fig = px.bar(
        filtered_df,
        x='Degree',
        y='Academic Pressure',
        title=f'Academic Pressure by Degree in {selected_city}',
        labels={'Degree': 'Degree', 'Academic Pressure': 'Academic Pressure'},
        color='Degree'
    )
    bar_fig.update_layout(
        title_font=dict(color='white'),
        paper_bgcolor='#222',
        plot_bgcolor='#444',
        font=dict(color='white')
    )

    # Pie Chart: Sleep Duration Distribution
    pie_fig = px.pie(
        filtered_df,
        names='Sleep Duration',
        title=f'Sleep Duration Distribution in {selected_city}',
        hole=0.4
    )
    pie_fig.update_layout(
        title_font=dict(color='white'),
        paper_bgcolor='#222',
        font=dict(color='white')
    )

    return scatter_fig, bar_fig, pie_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
 