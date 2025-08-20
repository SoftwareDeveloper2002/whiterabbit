from whiterabbit import App
from src.routes.landing import landing
from src.routes.docs import docs

# Initialize the app
app = App()

# Register routes
app.route("/")(landing)
app.route("/docs")(docs)

# Run the server
if __name__ == "__main__":
    app.run()
