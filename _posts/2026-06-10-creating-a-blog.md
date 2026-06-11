---
title: Creating a blog
show_title: true
tags: programming python jekyll github linkedin api secrets
---

In this post, I explain how I used GitHub Actions, Jekyll, and the LinkedIn API to build a blog.

---

Creating just a regular blog is quite easy. Jekyll (the static site generator GitHub Pages uses) has builtin support for blogs. You just define a blog layout and put your posts in `/_posts` in the format `YEAR-MONTH-DAY-title.md`. 

But I wanted to do something else too. You see, for some time, I've been posting updates on LinkedIn. But I've quickly realized that it's not the best place for longer posts. So I decided to start a blog, but still post smaller updates on LinkedIn, and not force my followers to find my website. So I wanted to post to LinkedIn whenever I make a new blog post, and automate it because it seemed like a fun project.

## How does it work?

You can find the source code for this website [here](https://github.com/tiash-and-cats/tiash-and-cats.github.io).

Firstly, I had to create a LinkedIn app. To do that, I went to [LinkedIn Developer Solutions](https://developer.linkedin.com) and clicked on `Create app`. But to create the app, I had to input a Company Page to associate it with. Thankfully, there are some "Default Company Pages for Individual Developers" (LinkedIn provides these so you don't need a real company) that I could use. 

Then I wrote a Python script called `linkedin_secrets.py`. It uses the "Sign In with LinkedIn using OpenID Connect" product to sign in to your account. It then gets an access token which must be saved securely and the user's URN (Uniform Resource Names, basically an ID LinkedIn gives to your account) which is saved to a file. I logged in so that it could post using my account.

I wrote another Python script called `.github/scripts/linkedin_share.py`, which takes the latest blog post and posts the post's title, description (first paragraph), and link to LinkedIn. This script is automatically called by a GitHub Action that runs each time a commit is pushed to `main`.

## What did I learn?

In the end, I learned that APIs can be messy, but automation is worth the effort: now my blog and LinkedIn are in sync without me lifting a finger.