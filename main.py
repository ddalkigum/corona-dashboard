import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data import (
    countries_df,
    totals_df,
    dropdown_options,
    make_global_df,
    make_country_df,
)
from builders import make_table


stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = fig = px.scatter_geo(
    countries_df,
    hover_data={
        "Confirmed": True,
        "Deaths": True,
        "Recovered": True,
        "Country_Region": False,
    },
    hover_name="Country_Region",
    size="Confirmed",
    size_max=40,
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    projection="natural earth",
    title="Confirmed By Countries",
)

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total global cases",
    hover_data={"count": ":,"},
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)

bars_graph.update_traces(marker_color=["#e74c3c", "#95a5a6", "#2ecc71"])
fig.update_layout(xaxis=dict(title="Condition"), yaxis=dict(title="Count"))

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(4, 1fr)",
                "gap": 50,
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=(dcc.Graph(figure=bubble_map)),
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=html.Div(children=[dcc.Graph(figure=bars_graph)])),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": "320",
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {
                                    "label": country,
                                    "value": country,
                                }
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country_graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={
            "value": "Cases",
            "variable": "Condition",
            "confirmed:": "Confirmed",
            "deaths": "Deaths",
            "recovered": "Recoverd",
        },
        hover_data={"value": ":,", "variable": False, "date": False},
    )
    fig.update_xaxes(rangeslider_visible=True)
    fig["data"][0]["line"]["color"] = "#e74c3c"
    fig["data"][1]["line"]["color"] = "#95a5a6"
    fig["data"][2]["line"]["color"] = "#2ecc71"
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)