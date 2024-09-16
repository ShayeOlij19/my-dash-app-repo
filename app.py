import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy.stats import gaussian_kde

# Initialize the Dash app
app = dash.Dash(__name__)

# Function to generate payouts
def generate_payouts(allocation_a, n=1000):
    fund_a_return = 105
    fund_b_mean = 120
    fund_b_std = 20
    allocation_b = 1 - allocation_a / 100
    fund_b_returns = np.random.normal(fund_b_mean, fund_b_std, n)
    total_payouts = allocation_a / 100 * fund_a_return + allocation_b * fund_b_returns
    return total_payouts

# Function to calculate the density (smooth line) of the payouts
def calculate_density(payouts):
    kde = gaussian_kde(payouts, bw_method='scott')
    x = np.linspace(min(payouts), max(payouts), 1000)
    y = kde(x)
    return x, y

# Layout of the app
app.layout = html.Div([
    html.H1("Fund Allocation Payout Simulation", style={'textAlign': 'center'}),
    dcc.Slider(
        id='fund-a-slider',
        min=0,
        max=100,
        step=5,
        value=50,
        marks={i: f'{i}' for i in range(0, 101, 10)}
    ),
    dcc.Graph(id='payout-graph'),
    html.Div(id='fund-a-label', style={'marginTop': 20}),
    html.Div(id='fund-b-label', style={'marginBottom': 40}),
])

@app.callback(
    [Output('payout-graph', 'figure'),
     Output('fund-a-label', 'children'),
     Output('fund-b-label', 'children')],
    [Input('fund-a-slider', 'value')]
)
def update_chart(allocation_a):
    payouts = generate_payouts(allocation_a)
    fund_a_return = 105
    fund_b_mean = 120
    fund_b_std = 20
    fund_b_returns = np.random.normal(fund_b_mean, fund_b_std, 100000)
    expected_return = allocation_a / 100 * fund_a_return + (1 - allocation_a / 100) * np.mean(fund_b_returns)
    x_density, y_density = calculate_density(payouts)
    payout_density_line = go.Scatter(x=x_density, y=y_density, mode='lines', name='Payout Density', line=dict(color='lightblue', width=3), fill='tozeroy')
    expected_line = go.Scatter(x=[expected_return, expected_return], y=[0, max(y_density) * 1.05], mode='lines', line=dict(color='red', width=3), name=f'Expected Return: {expected_return:.2f}')
    annotation = dict(x=expected_return, y=max(y_density) * 1.05, xref='x', yref='y', text=f'Expected return: {expected_return:.2f}', showarrow=False, font=dict(color='red'))
    arrow_annotation = dict(x=100, y=0, xref='x', yref='y', text='Investment capital', showarrow=True, arrowhead=2, ax=0, ay=-40, font=dict(color='black', size=14))
    layout = go.Layout(title=f'Fund Allocation: {allocation_a}% in Fund A and {100 - allocation_a}% in Fund B', xaxis=dict(title='Payout', range=[50, 180]), yaxis=dict(title='Frequency', range=[0, max(y_density) * 1.2], showgrid=False), annotations=[annotation, arrow_annotation], shapes=[{'type': 'rect', 'x0': 95, 'x1': 105, 'y0': -0.005, 'y1': 0.004, 'line': dict(color='black', width=1), 'fillcolor': 'white'}])
    figure = go.Figure(data=[payout_density_line, expected_line], layout=layout)
    fund_a_text = f'Amount invested in Fund A: €{allocation_a}'
    fund_b_text = f'Amount invested in Fund B: €{100 - allocation_a}'
    return figure, fund_a_text, fund_b_text

if __name__ == '__main__':
    app.run_server(debug=True)
