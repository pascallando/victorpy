---
title: Default templates
description: List of default templates included.
position: 100
---

## What's included?

{% prog_name %} comes with a bunch of overridable default templates:

- `base.html`: a simple base template use by all default templates (based on [Bootstrap](http://getbootstrap.com/) + [Bootswatch](https://bootswatch.com/)).
- `page.html`: the content page template.
- `tags.html`: a simple template to display a list of tags.
- `tag.html`: a simple template to display a list of pages related to a tag.
- `contact.html`: a default no-backend [contact form](/extra/contact-form/), based on [formspree.io](http://formspree.io).
- `feed.html`: RSS feed template.

## Overriding

You can override on or several default template:

1. Create a `templates` directory in your site root folder (see [Configuration](/getting-started/configuration/) to change the templates directory name).
2. Create files with the exact same name.

For example, to override the `page.html` template, you'll want to create a file like this at `your_site/templates/page.html`:

```html
<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        Oh, it's my own page template…

        My page content rendered:

        {{ content }}
    </body>
</html>
```