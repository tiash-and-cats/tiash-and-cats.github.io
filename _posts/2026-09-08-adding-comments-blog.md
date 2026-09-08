---
layout: post
title: Adding a comment section to my blog
tags: programming github utterances comments
---

In this post, I explain how I added a comment system to my blog using [Utterances](https://utteranc.es).

---

Static sites are great, but sometimes you want a bit of interaction. I wanted a way for readers to leave feedback or ask questions without bolting on a heavy third‑party service. Utterances turned out to be the perfect fit. It's a tiny script that connects each blog post to a GitHub Issue thread.

Under every post, there's now a comment section powered by GitHub Issues. If you have a GitHub account, you can leave a note right there. Each post gets its own thread, tied to its title, so discussions stay organized.

---

## How it works

1. I added the Utterances script to my layout.
2. It points to my `tiash-and-cats/tiash-and-cats.github.io` repo (the repo for this website).
3. Each post's title becomes the issue term.
4. Comments live as GitHub Issues with the label `comment section`.

That's all!

---

## What did I learn?

I learnt that sometimes the simplest solution is the best one. Utterances is basically a bridge between static sites and GitHub Issues, and it fits perfectly with my workflow. It keeps my site lean, consistent, and still gives readers a voice.

Now people can talk about my blog posts more easily without having to resort to LinkedIn comments.

Comments should be right below!