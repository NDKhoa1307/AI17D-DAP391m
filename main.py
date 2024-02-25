from app.utils import Data
import datetime as dt
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

# Set variables for plots
start_date = dt.datetime(2018, 1, 1)
end_date = dt.datetime(2020, 1, 1)
company = 'FB'

# Get dataset
data = Data(company, start_date, end_date).getModifedDataset()

# Variables for candlestick chart
fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'])])

fig.update_layout(title='Candlestick Chart',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=False)

# Variables for Closing Prices and Moving Average plot
window = 30
moving_average = data['Close'].rolling(window=window).mean()

# Main app 
app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(children="Facebook Stock Price Analytics"),
        html.P(
            children=(
                "Analyze the stock price of Facebook"
                f" in the US between {start_date.year} and {end_date.year}"
            ),
        ),

        dcc.DatePickerRange(
            id='date-range-picker',
            min_date_allowed=data["Date"].min().date(),
            max_date_allowed=data["Date"].max().date(),
            start_date=data["Date"].min().date(),
            end_date=data["Date"].max().date(),
        ),

        dcc.Graph(
            id = "line-graph",
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Close"],
                        "mode": "lines+markers",  # Include markers
                        "marker": {"color": "blue", "size": 4},  # Marker properties
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Closing Prices Over Time"},
            },
        ),

        dcc.Graph(
            id = "candlestick-chart",
            figure = fig
        ),

        dcc.Graph(
            id = 'moving-closing-average',
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Close"],
                        "type": "scatter",
                        "mode": "lines",
                        "name": "Closing Price",
                    },
                    {
                        "x": data["Date"],
                        "y": moving_average,
                        "type": "scatter",
                        "mode": "lines",
                        "name": f"{window}-Day Moving Average",
                    },
                ],
                "layout": {"title": f'Closing Prices and {window}-Day Moving Average'},
            },
        ),
    ]
)

@app.callback(
    [Output('line-graph', 'figure'),
    Output('candlestick-chart', 'figure'),
    Output('moving-closing-average', 'figure')],
    [Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')]
)
def update_figure(start_date, end_date):
    # company = 'FB'

    # Get dataset
    data = Data(company, start_date, end_date).getModifedDataset()

    # Variables for candlestick chart
    candlestick_fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'])])

    candlestick_fig.update_layout(title='Candlestick Chart',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False)

    # Variables for Closing Prices and Moving Average plot
    window = 30
    moving_average = data['Close'].rolling(window=window).mean()

    line_fig = {
        "data": [
            {
                "x": data["Date"],
                "y": data["Close"],
                "mode": "lines+markers",  # Include markers
                "marker": {"color": "blue", "size": 4},  # Marker properties
                "type": "lines",
            },
        ],
        "layout": {"title": "Closing Prices Over Time"},
    }

    moving_average_fig = {
        "data": [
            {
                "x": data["Date"],
                "y": data["Close"],
                "type": "scatter",
                "mode": "lines",
                "name": "Closing Price",
            },
            {
                "x": data["Date"],
                "y": moving_average,
                "type": "scatter",
                "mode": "lines",
                "name": f"{window}-Day Moving Average",
            },
        ],
        "layout": {"title": f'Closing Prices and {window}-Day Moving Average'},
    }

    return line_fig, candlestick_fig, moving_average_fig
    

if __name__ == "__main__":
    app.run_server(debug=True)