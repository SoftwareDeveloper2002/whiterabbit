from src.components.navbar import Navbar
from whiterabbit.app import App  # import the main app instance

app = App()

@app.route("/")
def landing(request):
    navbar = Navbar()
    return app.render_template("index.html", {"navbar": navbar.render()})
