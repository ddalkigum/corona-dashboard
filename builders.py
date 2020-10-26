import dash_html_components as html


def make_table(df):
    return html.Table(
        children=[
            html.Thead(
                children=[
                    html.Tr(
                        children=[
                            html.Th(column_name.replace("_", " "))
                            for column_name in df.columns
                        ]
                    )
                ]
            ),
            html.Tbody(
                children=[
                    html.Tr(children=[html.Td(value_column) for value_column in value])
                    for value in df.values
                ]
            ),
        ]
    )
