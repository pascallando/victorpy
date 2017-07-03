---
title: Shortcodes
description: Shorcodes allow you to extend your markdown vocabulary.
position: 400
tags:
    - advanced
    - customization
---

Shortcodes are simple snippets that you can include in your [markdown content files](/content/content-pages/). {% prog_name %} will render it using a predefined template.

{% alert type="warning" title="Performance" %}
Shortcode processing is enabled by default. Thus, shortcodes have a performance cost when rendering/building your site: you can disable shortcodes processing by setting the site [configuration parameter](/getting-started/configuration/) `enable_shortcodes` to `False`.
{% endalert %}

## Shortcode usage syntax

You can include shortcodes in your content using the following syntax:

```
{% the_shortcode_name %}
```

## Built-in shortcodes

{% prog_name %} ships with a set of predefined shorcodes:

### sectionpages

Generates a list of links to the pages of current section (useful for section's index page).

#### Example

```
{% sectionpages %}
```

For example, this shortcode used in the current page outputs the following:

{% sectionpages %}

---

### figure

Allow you to show complete figure as a one-liner.

#### Parameters

- `src`: The address of the resource (may be something like "/static/images/my-image.jpg")
- `alt`: An alternative text for the resource (think [accessibility](https://www.w3.org/WAI/intro/accessibility.php)…)
- `caption`: A descriptive text to show under the figure. If not provided, `alt` value will be used.

#### Example

```
{% figure src="//blog.lamaisondelamontagne.org/public/images/2011/Victor_Hugo_001.jpg" alt="Victor Hugo" %}
```

{% figure src="//blog.lamaisondelamontagne.org/public/images/2011/Victor_Hugo_001.jpg" alt="Victor Hugo" %}

---

### amazon

Generate ready-to-fly Amazon products links.

#### Parameters

- `code_type`: "url", "image" or "snippet"
- `asin`: The [Amazon Standard Identification Number](https://en.wikipedia.org/wiki/Amazon_Standard_Identification_Number) of the product to show.
- `title`: A title to display under the product (only for _snippet_).

{% alert type="info" title="Associate ID" %}
The shortcode can include your Amazon associate ID in the links. Just make sure to have the `amazon_id` parameter defined in your [configuration file](/getting-started/configuration/).
{% endalert %}

#### Example

```
{% amazon image B072QZZDV7 %}
```

…outputs this:

{% amazon image B072QZZDV7 %}

---

### tweet

Display a tweet.

#### Parameters

- `id`: The Twitter tweet id.

#### Example

```
{% tweet 860599072234844160 %}
```

{% tweet 860599072234844160 %}

---

### alert […] endalert

To be documented.

### row […] endrow

To be documented.

### col […] endcol

To be documented.

### pull […] endpull

To be documented.

## User defined shortcodes

You can create your own shortcodes in order to extend existing {% prog_name %} features:

1. Create a new file called `shortcodes.py` in your project directory.
2. Add one function per shortcode to process (the function name is the shortcode name).
3. Use your shortcode in whatever content page you want!

### The context parameter

Every shortcode function gets a special `context` parameter, which contains the full context on the page using the shortcode.

#### shortcodes.py

```py
def hello(context):
    return "Hello, we're on {page_title}!".format(page_title=context['page']['title'])
```

#### my-page.md
```
{% hello %}
```

Here is the result, when used on the current page:

{% alert type="info" %}
{% hello %}
{% endalert %}


### Extra parameters

You can specify other parameters to customize your shortcodes behaviour.

Let's say we want to create a shortcode to display the factorial of a number. We'd like to use it this way, with a **custom parameters** to get the number to factorialize:

```
The factorial of number 4 is {% factorial 4 %}.
```

Let's go ahead and create the factorial function in our `shortcodes.py` file:

#### shortcodes.py

```py
def factorial(context, n):
    num = 1
    n = int(n)
    while n >= 1:
        num = num * n
        n = n - 1
    return str(num)
```

#### my-page.md
```
The factorial of number 4 is {% factorial 4 %}.
```

Here is the result:

{% alert type="info" %}
The factorial of number 4 is {% factorial 4 %}.
{% endalert %}







