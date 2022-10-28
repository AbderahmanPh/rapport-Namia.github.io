import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Rapport"

app.index_string = """<!DOCTYPE html>
    <html>
        <head>
            <style>
                .hidden {
                opacity: 0;
                }

                .visible {
                opacity: 1;
                transition: opacity 2s ease-out;
                }
            </style>
            
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-NK3SH0SRM6"></script>
            <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-NK3SH0SRM6');
            </script>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
         
        </head>
        <body>
            <script>
                document.body.className = 'hidden';
            </script>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
            <script>
                document.body.className = 'visible';
            </script>
        </body>
</html> """


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
