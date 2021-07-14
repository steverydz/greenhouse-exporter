from canonicalwebteam.flask_base.app import FlaskBase
from flask import render_template


app = FlaskBase(
    __name__,
    "greenhouse-exporter",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


@app.route("/")
def index():
    return render_template("index.html")