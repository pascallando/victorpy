---
title: Routes
description: Routes are paths to resources.
position: 400
tags:
    - path
    - customization
---

Routes are paths to resources.

When rendering/building your site, {% prog_name %} automatically creates routes to your pages, using a simple mapping _file path &rarr; resource path_.

For example, if you create a file `cat.md` in a directory called `animals` at the root of your site content (`/content/animals/cat.md`), then you will be able to access the following URL: `http://127.0.0.1:5000/animals/cat/` and see your rendered cat page.

Thus, you will sometimes need to define extra-routes to non content resources.

## Builtin routes

{% prog_name %} ships with a set of predefined extra-routes:

- `/tags`: a route to the page listing the site tags.
- `/tags/*`: a route to a specific page for each tag.
- `/contact`: a route to a prebuilt contact page.
- `/rss`: a route to a prebuilt RSS feed resource listing the site pages.

## Defining routes

To define your own routes, you have to set your paths in the `routes` [config parameter](/getting-started/configuration/).

Every routes associates an URL pattern to a template.

### Custom route example

Let's say you want to create a survey form for your site.

You want this survey to be accessible from the `/survey/` URL.


First, define the route in the config file `routes` parameter:

#### config.yaml

```yaml
routes:
  'survey.html': '/survey'
```

Then, create a template called `survey.html` in the `templates` directory:

#### templates/survey.html

```html
{% extends "base.html" %}

{% block title %}Survey{% endblock %}

{% block before_endbody %}
<script src="https://surveyjs.azureedge.net/0.12.18/survey.jquery.js"></script>

<script>
    Survey.Survey.cssType = "bootstrap";
    Survey.defaultBootstrapCss.navigationButton = "btn btn-green";

    window.survey = new Survey.Model({ questions: [
        { type: "radiogroup", name: "car", title: "What car are you driving?", isRequired: true,
         colCount: 4, choices: ["None", "Ford", "Vauxhall", "Volkswagen", "Nissan", "Audi", "Mercedes-Benz", "BMW", "Peugeot", "Toyota", "Citroen"] }
    ]});
    survey.onComplete.add(function(result) {
        document.querySelector('#surveyResult').innerHTML = "result: " + JSON.stringify(result.data);
    });


    $("#surveyElement").Survey({model:survey});
</script>
{% endblock before_endbody %}


{% block main %}
    <div id="surveyElement"></div>
    <div id="surveyResult"></div>
{% endblock main %}
```

OK! Our new route is now available: [/survey/](/survey/).

{% alert type="info" title="Note" %}
You can extend whatever template you need when defining a new route template (we just extended the `base.html` template in this example).
{% endalert %}