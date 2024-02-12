import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go


# Function to generate layout and callback for each graph
def generate_graph_layout(csv_file_path, graph_id):
    # Read CSV file with custom column names
    column_names = ["timestamp", "value", "diff", "pcr", "opinion"]
    df = pd.read_csv(csv_file_path, names=column_names)

    # Convert the timestamp column to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d-%b-%Y %H:%M:%S")

    # Define the layout of the Dash application
    graph_layout = html.Div(
        [
            dcc.Graph(id=graph_id),
            dcc.Interval(id=f"interval-{graph_id}", interval=1 * 1000, n_intervals=0),
        ]
    )

    # Define callback to update the graph
    @app.callback(
        Output(graph_id, "figure"), [Input(f"interval-{graph_id}", "n_intervals")]
    )
    def update_graph_live(n):
        # Reload the CSV file at each update
        df = pd.read_csv(csv_file_path, names=column_names)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d-%b-%Y %H:%M:%S")

        # Create a Plotly figure
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"], y=df["diff"], mode="lines+markers", name="PCR Diff"
            )
        )
        fig.update_layout(
            title=f"{graph_id}",
            xaxis=dict(title="Timestamp"),
            yaxis=dict(title="Change in OI"),
        )

        return fig

    return graph_layout


# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the Dash application
app.layout = html.Div(
    [
        generate_graph_layout(
            "D:\\trading\\weekly_options\\data\\output_nifty.csv", "NIFTY"
        ),
        generate_graph_layout(
            "D:\\trading\\weekly_options\\data\\output_banknifty.csv", "BANKNIFTY"
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
