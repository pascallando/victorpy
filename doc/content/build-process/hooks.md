---
title: Hooks
description: Hooks are a way to plug extra features to the generator.
position: 400
tags:
    - hook
    - action
    - customization
---

Hooks are a way to plug extra features (called **actions**) to {% prog_name %} at some pre-defined points. Common hooks use cases are: copying files, transpiling [some language] to JS/CSS/whatever, pinging some external service…

{% prog_name %} includes the fallowing hooks:

- `after_render`: when the pages rendering process is completed.
- `affet_build`: when the site building process is completed.

## Configuring hooks

Configuring hook is generally two steps process:

1. Linking an action to a hook (i.e. _when_ to do _what_…).
2. Cufiguring each action.

For example, if you want to transpile your Less files to CSS each time your site has been rendered, you will have to say that you want to trigger the Less to CSS transpiling process after rendering **and** to tell {% prog_name %} where your Less source files are located andwhere you want to create the CSS files.

Linking actions to hooks is done using the `hooks` [config](/getting-started/configuration/) parameter:

```yaml
hooks:
    after_render:              # the hook
        - compile_less_files   # the action to launch
        # ...
```

{% alert type="info" title="Processing order" %}
The actions list is ordered: actions on top will be processed first.
{% endalert %}

Action related configuration should be done in a dedicated config parameters (every action defines its own configuration structure). For example:

```yaml
less:
    files:
        - 'app/less/main.less': "static/css/main.min.css"
```


## Built-in actions

{% prog_name %} ships with a set of predefined actions:

### compile_less_files

[Less](http://lesscss.org/) is a CSS pre-processor. The `compile_less_files` takes your Less files and transpile it into plain CSS files.

#### config.yaml

```yaml
hooks:
    after_render:
        - copy_files(front)

less:
    files:
        - 'app/less/regular.less': "static/css/regular.css"
        - 'app/less/home.less': "static/css/home.css"
        - 'app/less/other.less': "static/css/other.css"
```

---

### copy_files

This action allow you to collect static files (inspired by the [Django collectstatic](https://docs.djangoproject.com/fr/1.11/ref/contrib/staticfiles/) command).

#### config.yaml

```yaml
hooks:
    after_render:
        - copy_files(front)
        - copy_files(static)

copy_files:
    front:
        'app/__javascript__/main.js': "static/js/main.js"
        'app/__javascript__/other.js': "static/js/other.js"
    static:
        '/toto': 'tata'
```

---


### minify_html

Delete spaces in HTML files. Operates on files located in [build_path](/getting-started/configuration/).

#### config.yaml

```yaml
hooks:
    after_build:
        - minify_html
```

---

### create_lunr_index

This hook creates an index file for using with the [Lunr search engine](https://lunrjs.com/).

#### config.yaml

```yaml
hooks:
    after_render:
        - create_lunr_index

```


## User-defined hooks

Todo.
