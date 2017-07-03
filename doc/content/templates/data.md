---
title: Data available in templates
description: A list of available values in your templates.
position: 300
tags:
    - context
    - mini-context
---

## Preamble

In every template, {% prog_name %} provides you with a lot of data about:

- The page
- The site

This dataset is called the **page context**.

Every parameters you defined in a content page [front matter](/content/content-pages/) is available in the page context.

For example, let say we have a content page `my_page.md`:

#### content/my_page.md

```
---
title: My page title
something: This is something!
---

Some **content** here…
```

In the template, you have an access to every parameter, so you can do:

#### templates/page.html

```html
The title of this page is {{ title }}, and here is something: {{ something }}

{{ content }}
```

When rendering, you should get:

```html
The title of this page is My page title, and here is something: This is something!

Some <strong>content</strong> here…
```

## The page dict

In addition to your own parameters, {% prog_name %} will populate you context with some extra stuff:

| Name               | Type       | Notes                                                                                                                                          |
|:-------------------|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| `unique_id`        | Number     | A unique identifier for the page.                                                                                                              |
| `shortest_title`   | String     | The shortest title between `title` and `short_title`.                                                                                          |
| `longest_title`    | String     | The longest title between `title` and `long_title`.                                                                                            |
| `breadcrumb`       | List[Dict] | A list of mini-contexts of the pages in this page breadcrumb path.                                                                             |
| `content`          | String     | The HTML rendered version of your markdown source.                                                                                             |
| `permalink`        | String     |                                                                                                                                                |
| `url`              | String     | Relative URL of the page.                                                                                                                      |
| `slug`             | String     |                                                                                                                                                |
| `section_pages`    | List[Dict] | A list of mini-contexts of all the pages of current section (ordered by `position`).                                                           |
| `section_page`     | Dict       | The mini-context of the index of this page's section index.                                                                                    |
| `section_sections` | List[Dict] | A list of mini-contexts of all the subsections of this page section parent, i.e. a list of this page section brothers (ordered by `position`). |
| `sub_sections`     | List[Dict] | A list of mini-contexts of all the subsections of this page (ordered by `position`).                                                           |
| `is_section_index` | Boolean    |                                                                                                                                                |
| `site`             | Dict       | The site dict: see [below](#the-site-dict).                                                                                                                      |

{% alert type="warning" title="Mini-context" %}
A mini-context is a dict containing a restricted set of a page context. It is used in the list of pages (i.e. `section_pages`, `sub_sections`…).
{% endalert %}



### The site dict

In addition to page data, you can access site wide data in every template.

| Name                 | Type          | Notes                                                                        |
|:---------------------|:--------------|:-----------------------------------------------------------------------------|
| `site.title`         | String        |                                                                              |
| `site.baseUrl`       | String        |                                                                              |
| `site.render_id`     | String        | A unique id, refreshed every time the site is rendered.                      |
| `site.root_sections` | List[Section] | A list of all root sections of this site, i.e. sections which has no parent. |


Note: your can define other site constants in the [config file](/getting-started/configuration/) to make them available in every page.

