# Core
import os

# Packages
from flask import Flask, render_template

# Local
from canonicalwebteam.yaml_responses.flask_helpers import (
    prepare_deleted,
    prepare_redirects,
)


def callback(context):
    return render_template("410.html", message="custom callback"), 410


this_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(this_dir)

app_redirects = Flask("redirects", template_folder=f"{this_dir}/templates")
app_permanent_redirects = Flask(
    "redirects", template_folder=f"{this_dir}/templates"
)
app_empty_redirects = Flask(
    "empty_redirects", template_folder=f"{this_dir}/templates"
)
app_deleted = Flask("deleted", template_folder=f"{this_dir}/templates")
app_empty_deleted = Flask(
    "empty_deleted", template_folder=f"{this_dir}/templates"
)
app_deleted_callback = Flask(
    "deleted_callback", template_folder=f"{this_dir}/templates"
)

app_redirects.before_request(
    prepare_redirects(path=f"{parent_dir}/redirects.yaml")
)
app_permanent_redirects.before_request(
    prepare_redirects(path=f"{parent_dir}/redirects.yaml", permanent=True)
)
app_deleted.before_request(prepare_deleted(path=f"{parent_dir}/deleted.yaml"))
app_deleted_callback.before_request(
    prepare_deleted(path=f"{parent_dir}/deleted.yaml", view_callback=callback)
)
app_empty_redirects.before_request(
    prepare_redirects(path=f"{parent_dir}/empty.yaml")
)
app_empty_deleted.before_request(
    prepare_deleted(path=f"{parent_dir}/empty.yaml")
)


@app_redirects.route("/homepage")
@app_deleted.route("/homepage")
def homepage():
    return "hello world"
