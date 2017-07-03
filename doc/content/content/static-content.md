---
title: Static content
description: Learn how VictorPy deals with your static files (CSS, JS, images…)
position: 200
tags:
    - images
    - CSS
    - JS
    - assets
---

## Storing static

Your static content should be stored in the `static_dir_name` path (see [site configuration](/getting-started/configuration/) for more informations about how to customize this).

## Accessing in content files

In your content files, you can access you static files this way `/static/images/hello.jpg`. For example : `![My hello image](/static/images/hello.jpg)`.
