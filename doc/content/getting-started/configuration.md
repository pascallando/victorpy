---
title: Configuration
description: Configuring your first site.
position: 200
tags:
    - config.yaml
    - debug
    - Yaml
---

Bootstrapping a {% prog_name %} site is very easy:

1. Create a directory for your site.
2. Create a `config.yaml` file in it.
3. Ready to write content!

## The config file

All your static site configuration is held by the `config.yaml` file.

{% alert type="info" title="Yaml format" %}
    The config file is written using Yaml formating language. See [Yaml official doc](http://yaml.org/) for further informations.
{% endalert %}

#### config.yaml

```yaml
title: "My site"
base_url: "http://mysite.com"
```

### Parameters

{% prog_name %} uses a bunch of default parameters to build your site:

| Name                 | Type    | Default                         | Notes                                                                                     |
|:---------------------|:--------|:--------------------------------|:------------------------------------------------------------------------------------------|
| `actions_dir_name`   | String  | "actions"                       | The directory containing custom actions to trigger via [hooks](/build-process/hooks/).                              |
| `amazon_id`          | String  | None                            | If defined, used by the [amazon shortcode](/templates/shortcodes/#amazon).                |
| `base_url`           | String  | ""                              |                                                                                           |
| `build_dir_name`     | String  | "public"                        | The directory where generated files should be written                                     |
| `content_dir_name`   | String  | "content"                       | The directory containing your source markdown content files.                              |
| `debug`              | Boolean | False                           | When True, adds page context infos in the browser console and source file opening button. |
| `enable_shortcodes`  | Boolean | True                            |                                                                                           |
| `enable_headers_id`  | Boolean | True                            |                                                                                           |
| `hooks`              | Dict    | {}                              | A hash of hooks. See [Hooks](/build-process/hooks/) doc.                                  |
| `image`              | String  | "default.jpg"                   | A default image illustrating your site. File should be located in `/static/images/`.      |
| `port`               | Number  | 5000                            | The port number of the live server.                                                       |
| `routes`             | Dict    | [{...}](/build-process/routes/) | A hash containing some special routes. See [Routes](/build-process/routes/) doc.          |
| `static_dir_name`    | String  | "static"                        | Your CSS/JS… files directory.                                                             |
| `templates_dir_name` | String  | "templates"                     | The directory where {% prog_name %} should find user defined templates.                   |
| `title`              | String  | ""                              |                                                                                           |


### Additional parameters

In addition, you can provide extra parameters.

Each parameter will be added to every [page context](/templates/data/), allowing you to use it within your [templates](/templates/) and [shortcodes](/templates/shortcodes/).


#### config.yaml

```yaml
title: "My site"
base_url: "http://mysite.com"

my_param: "Yeah!"
another_one: 123
```
