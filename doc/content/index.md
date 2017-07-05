---
title: VictorPy documentation site
description: This site is the reference manual for the Python static site generator.
---

{% prog_name %} is a **simple yet powerful static site generator**.

It is inspired by [Steve Francia](http://spf13.com/)'s _[Hugo](https://gohugo.io/)_, with less talent but some pythonic sugar :)

Features:

- Jinja2 templating.
- Shortcodes.
- Hooks.
- Action pipeline (collecting files, compiling Less/Transcrypt…).
- Live server/debug.
- Easy customization.
- Pretty fast.

## Why a new static site generator?

After having tested many awesome static generator, if you're not totally convinced, check this.

### ☺ Python.

{% prog_name %} is **[Python 3](https://www.python.org/) powered**.

You will write [shortcodes](/templates/shortcodes/) as Python functions, as well as [hook actions](/build-process/hooks/), taking advantage of the amazing Python libs ecosystem.

### ☺ Content driven

Static site generators usually make some funky assumptions about how to map the content tree to site URLs.

{% prog_name %} has a simple rule: **strict content to URL mapping**. Folders become sections. Sub-folders become sub-sections. Files become pages.

Custom [routing](/build-process/routes/) available for no-content "direct to template" URLs.

### ☺ Want something really simple?

For every Python lover, **syntax and readability matters**.

{% row %}

{% col 6 %}
#### Hugo

```go
{{ if isset .Params "title" }}
    <h4>{{ index .Params "title" }}</h4>
{{ end }}
```
{% endcol %}

{% col 6 %}
#### {% prog_name %}

```jinja
{% if params.title %}
    <h4>{{ params.title }}</h4>
{% endif %}
```

{% endcol %}

{% endrow %}

### ☺ Full stack

{% prog_name %} covers the **static site building process from A to Z**: render pages, build site and execute all the tasks you need thank to hooks, without requirering other frameworks/languages. No Grunt/Gulp/Webpack needed.
