---
title: RSS feed
description: A really simple syndication for your site
position: 200
tags:
    - syndication
---

The [RSS feed](https://en.wikipedia.org/wiki/RSS) provides a list of pages, allowing users to access updates to online content in a standardized, computer-readable format.

## Configuration

RSS feed is a no-conf feature! The default route for RSS feed is `/rss` ([try it](/rss)).

However, note that you can override the route for this feed (see [routes](/build-process/routes/) for more details):

#### config.yaml

```yaml
routes:
  'feed.html': "/my-rss-feed"
```
