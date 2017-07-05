---
title: Content pages edition
description: This page provides informations of how to write and format your content pages.
position: 100
tags:
    - Markdown
    - front matter
    - Yaml
    - tags
    - draft
---


## Anatomy of a content page

Every page has two parts:

- The **front matter**
- The **content**

### Front matter

Your pages should begin with a **front matter header**, containing meta-data in [YAML](http://yaml.org/) format, surrounded by `---`.

```
---
title: My page title
description: This is my page description!
tags:
    - cool
    - site
---

## Some headings

And some content here...
```

### Markdown content

Page content should be written in [Markdown](https://daringfireball.net/projects/markdown/).


## Front matter parameters

| Name          | Type    | Default     | Notes                                                                            |
|:--------------|:--------|:------------|:---------------------------------------------------------------------------------|
| `title`       | String  | None        |                                                                                  |
| `short_title` | String  | None        | A short version of the title (useful for menus…)                                 |
| `long_title`  | String  | None        | A long version of the title (SEO?)                                               |
| `description` | String  | None        | A few words about the page. Typically used for HTML `<meta name="description">`. |
| `keywords`    | List    | None        | Typically used for HTML `<meta name="keywords">`.                                |
| `template`    | String  | "page.html" | The [template](/templates/) {% prog_name %} should use to render the page.       |
| `tags`        | String  | []          | A list of tags, used to generate the site tags index.                            |
| `draft`       | Boolean | False       | If True, the page will be skipped when generating the site.                      |
| `position`    | Number  | 0           | The position of the page in it's section menu.                                   |
| `date`        | Date    | None        |                                                                                  |
