from whiterabbit import App
from src.components.navbar import Navbar

app = App()

@app.route("/")
def home(request):
    navbar = Navbar().render()
    return app.render_template("index.html", {"navbar": navbar})

@app.route("/docs")
def docs(request):
    navbar = Navbar().render()
    return app.render_template("docs.html", {"navbar": navbar})
