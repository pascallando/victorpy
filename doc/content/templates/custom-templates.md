---
title: Custom templates
description: Learn how to define your own custom templates.
position: 200
---

## Create the files

If not already done, create a `templates` directory in your site root folder (see [Configuration](/getting-started/configuration/) to change the templates directory name).

Then create one `.html` file per template in this folder. For example:

#### my_template.html

```html
<div>
    Here is my custom template!

    This site base URL is: {{ site.base_url }}.
</div>
```

## Referencing templates

One your templates created, you can reference them from your source file using the `template` front matter parameter:

```
---
title: A page
template: my_template.html
---

## We're in our own template!

{{ content }}
```
