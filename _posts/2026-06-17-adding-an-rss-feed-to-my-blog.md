---
title: Adding an RSS feed to my blog
show_title: true
tags: programming jekyll rss automation
post2lnkdin: false
---

In this post, I explain how I added an RSS feed to my blog.

---

## Why?

RSS is one of those old‑school web standards that never really died. It lets you subscribe to updates from a site in your feed reader, so you don't have to keep checking manually. Since I've been automating LinkedIn posts, it made sense to also expose a feed for anyone who prefers a reader (such as myself).

## How?

I created a `feed.xml` template in Jekyll that loops through all posts and outputs them in RSS 2.0 format. It includes:

- Title
- Link
- Publication date
- GUID (permalink)

Here's the snippet:

{% raw %}
``` xml
---
layout: null
---
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{{ site.title | xml_escape }}</title>
    <link>{{ site.url }}{{ site.baseurl }}/</link>
    <description>{{ site.description | xml_escape }}</description>
    <atom:link href="{{ "/feed.xml" | prepend: site.baseurl | prepend: site.url }}" rel="self" type="application/rss+xml"/>
    {% for post in site.posts %}
    <item>
      <title>{{ post.title | xml_escape }}</title>
      <link>{{ post.url | prepend: site.baseurl | prepend: site.url }}</link>
      <pubDate>{{ post.date | date_to_rfc822 }}</pubDate>
      <guid isPermaLink="true">{{ post.url | prepend: site.baseurl | prepend: site.url }}</guid>
    </item>
    {% endfor %}
  </channel>
</rss>
```
{% endraw %}

The `layout: null` is important, as it prevents Jekyll from trying to put the RSS inside an HTML layout.

---

Now you can subscribe to [my feed](/feed.xml) in any RSS reader and get updates whenever I publish a new post. Between LinkedIn automation and RSS, my blog is starting to feel like a proper publishing pipeline.

That's it: a small addition, but one that makes the blog more accessible. Now I can put my site in my RSS reader (Opera, by the way) and subscribe to it like just another news site!