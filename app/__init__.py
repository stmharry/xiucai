import re

from flask import Blueprint, Flask, render_template, request
from flask_bootstrap import Bootstrap4
from linkpreview import link_preview

blueprint = Blueprint("main", __name__)


@blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    url = request.form["url"]
    preview = link_preview(url)

    title = preview.title
    title = re.compile("[-|｜]", re.UNICODE).split(title)[0].strip()

    desc = preview.description
    desc = re.compile("（[^（）]*報導）", re.UNICODE).sub("", desc)

    print("")
    print("site:", preview.site_name)
    print("title:", preview.title)
    print("description:", preview.description)
    print("image:", preview.image)

    return render_template(
        "index.html",
        form=request.form,
        site=preview.site_name,
        title=title,
        title_width=80,
        title_font_size=28,
        desc=desc,
        desc_width=85,
        desc_font_size=24,
        image_url=preview.image,
        image_height=25,
        image_width=100,
    )


def create_app(configfile=None):
    app = Flask(__name__)

    _ = Bootstrap4(app)
    app.register_blueprint(blueprint)

    return app


application = create_app()
