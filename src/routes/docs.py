from src.components.navbar import Navbar
from whiterabbit.app import App  # import the main app instance

app = App()

@app.route("/docs")
def docs(request):
    navbar = Navbar()
    return app.render_template("docs.html", {"navbar": navbar.render()})
