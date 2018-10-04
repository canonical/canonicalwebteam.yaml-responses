# Core
import os

# Packages
from django.http import HttpResponseGone
from canonicalwebteam.yaml_responses import django


parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Add redirects
urlpatterns = django.create_deleted_views(
    path=f"{parent_dir}/deleted.yaml",
    view_callback=lambda request, context, settings: HttpResponseGone(
        "custom callback"
    ),
)
