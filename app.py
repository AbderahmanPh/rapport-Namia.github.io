import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Rapport"

navbar = dbc.NavbarSimple(
    [
        dbc.Button("NAMIA", href="/", color="secondary", className="me-1"),
        dbc.Button("ASMAC", href="/asmac", color="secondary"),
    ],
    brand="Rapport",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
