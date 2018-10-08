# canonicalwebteam.yaml-responses

[![CircleCI build status](https://circleci.com/gh/canonical-webteam/yaml-responses.svg?style=svg)][circleci] [![Code coverage](https://codecov.io/gh/canonical-webteam/yaml-responses/branch/master/graph/badge.svg)][codecov]

Easily serve `302` and `410` responses with simple YAML files.

This module contains Django and Flask helpers to serve ["302 Found"](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#301) redirect and ["410 Gone"](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#410) deleted responses from lists read from `redirects.yaml` and `deleted.yaml` files contained in the app directory.

## File format

**redirects.yaml**

``` yaml
hello: /world  # A simple redirect
example-(?P<name>.*): http://example.com/{name}  # A redirect with a regex replacement
```

**deleted.yaml**

``` yaml
deleted:
deleted/.*/regex:  # This will match "/deleted/{anything}/regex"
deleted/with/message:
  message: "Gone, gone, gone"  # This context data is passed directly to the template
```

## Usage

You can use this library with either Django or Flask.

### Django

Install the packege for Django as follows:

``` bash
pip install canonicalwebteam.yaml_responses[django]  # For Django helpers
```

Here's how to add URL patterns for redirects and deleted endpoints to Django:

#### `create_redirect_views` and `create_deleted_views` basic usage

This will read `redirects.yaml` and `deleted.yaml` pages in the project root.

For the "deleted" responses, it will look for a template called `410.html` in the default `templates/` directory.

``` python
# urls.py
from django.conf.urls import url
from canonicalwebteam.yaml_responses.django import (
    create_redirect_views,
    create_deleted_views
)

urlpatterns = django.create_redirect_views()  # Read redirects.yaml
urlpatterns += django.create_deleted_views()  # Read deleted.yaml

urlpatterns += ...  # The rest of your views
```

#### Options for `create_redirect_views`

- `path`: The path to the YAML file
- `permanent`: Return ["301 Moved Permanently"](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#301) statuses instead of 302

E.g.:

``` python
urlpatterns = create_redirect_views(
    path="config/permanent-redirects.yaml",
    permanent=True
)
urlpatterns += ...  # The rest of the views
```

#### Options for `create_deleted_views`

- `path`: The path to the YAML file
- `view_callback`: An alternative function to process Deleted responses

E.g.:

``` python
def deleted_callback(request, url_mapping, settings, *args, **kwargs):
    return render(request, "errors/410.html", url_mapping, status=410)

urlpatterns = create_deleted_views(
    path="config/deleted-paths.yaml",
    view_callback=deleted_callback
)
```

### Flask

Install the package for Flask as follows:

``` bash
pip install canonicalwebteam.yaml_responses[flask]  # For Flask helpers
```

Here's how to process redirects and deleted before other views are processed in Flask:

#### `prepare_redirects` and `prepare_deleted` basic usage

This will read `redirects.yaml` and `deleted.yaml` pages in the project root.

For the "deleted" responses, it will look for a template called `410.html` in the default `templates/` directory.

``` python
# app.py
from flask import Flask
from canonicalwebteam.yaml_responses.flask import (
    prepare_deleted,
    prepare_redirects,
)

app = Flask()

app.before_request(prepare_redirects())  # Read redirects.yaml
app.before_request(prepare_deleted())  # Read deleted.yaml
```

#### Options for `prepare_redirects`

- `path`: The path to the YAML file
- `permanent`: Return ["301 Moved Permanently"](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#301) statuses instead of 302

E.g.:

``` python
app.before_request(
    prepare_redirects(
        path=f"{parent_dir}/redirects.yaml",
        permanent=True
    )
)
```

#### Options for `prepare_deleted`

- `path`: The path to the YAML file
- `view_callback`: An alternative function to process Deleted responses

E.g.:

``` python
def deleted_callback(context):
    return render_template("errors/410.html"), 410

app.before_request(
    path=prepare_deleted(path="config/deleted-paths.yaml",
    view_callback=deleted_callback)
)
```

## Notes

This package has evolved from, and is intended to replace, the following projects:

- [canonicalwebteam.yaml-redirects](https://github.com/canonical-webteam/yaml-redirects)
- [canonicalwebteam.yaml-deleted-paths](https://github.com/canonical-webteam/yaml-deleted-paths)
- [canonicalwebteam.views-from-yaml](https://github.com/canonical-webteam/views-from-yaml)


[circleci]: https://circleci.com/gh/canonical-webteam/yaml-responses "CircleCI build status"
[codecov]: https://codecov.io/gh/canonical-webteam/yaml-responses "Code coverage"
