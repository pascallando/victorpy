---
title: Command line
description: Learn how to use the command line tools to create/build your site.
position: 400
tags:
    - serve
    - build
---

{% prog_name %} comes with a few command line tools.

## Live server

When working on your content, you don't want to manually rebuild your site content every time you make a single change.

You may want to use the **live server**, which will:

- Serve your pages, live in the browser.
- Restart automatically when you create/update a content file.

### Starting the live server

In a terminal, make sure you are in your project root folder, and then type:

```bash
$ victorpy serve
```

{% alert type="warning" title="Shortcut" %}
You can also just type ```victorpy``` to start the live server.
{% endalert %}

{% prog_name %} should start quickly, build your site in memory, serve it and display a few messages on the console:

```bash
INFO VictorPy v0.1
INFO  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

By now, you site is live locally!

Open a browser at http://127.0.0.1:5000/ and see what you get…

## Building your site

The building process allows you to create your site HTML files, ready to upload to your server:

```bash
$ victorpy build
```

The site if built in the `public` directory (see [Configuration](/getting-started/configuration/) to change this directory).

