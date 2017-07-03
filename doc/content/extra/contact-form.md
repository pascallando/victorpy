---
title: Contact form
description: A simple no-backend contact form.
position: 100
tags:
    - contact
---

{% prog_name %} ships with a simple no-backend contact form. Feel free to use it.

This contact form is used by the present site, you can test it: [contact me](/contact/)!

## Configuration

The contact form uses [formspree](https://formspree.io/) under the wood.

The only thing you need to set is the email address to which the contact mails should be sent: this is done by setting the `email` config parameter.

#### config.yaml

```yaml
email: `mysupermail@server.com
```

Note that you can also override the route for this form (see [routes](/build-process/routes/) for more details):

#### config.yaml

```yaml
routes:
  'contact.html': "/io/contact-me-here"
```

Once your site deployed, the only thing you need to do is to submit the form once in order to confirm your email address and avoid spam.

