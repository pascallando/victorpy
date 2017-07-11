---
title: Site structure
description: Your site lives in a directory. See how to structure it.
position: 300
tags:
    - structure
---

{% prog_name %} sites are fully stored in a single directory.

This directory should have the following structure:

```
my-site/
    config.yaml
    shortcodes.py
    content/
        index.md
        a-section/
            index.md
            a-page.md
        another_section/
            index.md
    static/
        images/
        js/
        css/
    templates/
        page.html
```

## Minimal site

A minimal site should have this structure:

```
my-site/
    config.yaml
    content/
        index.md
```

## Run it!

Once created this folder, you could launch a test server to see your site content by typing `victorpy` from your site directory (for example: `my-site`), and then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

{% alert type="info" title="Command line" %}
More details about how to use the command line tools are provided in the [Command line](/build-process/command-line/) section.
{% endalert %}