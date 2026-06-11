---
title: Automating LinkedIn posts for my blog - Part 2
tags: programming python linkedin api automation
---

In this post, I explain how I improved my LinkedIn automation script by adding bold/italic formatting, randomized call-to-actions, and a follow‑up comment feature.

---

View the code [here](https://github.com/tiash-and-cats/tiash-and-cats.github.io/blob/master/.github/scripts/linkedin_share.py).

Plain text LinkedIn posts looked a bit flat, and could easily be missed in the midst of a doomscrolling session. So I added translation maps for bold, italic, and bold‑italic alphabets using Unicode pseudofonts. I know all you LinkedIn users used a LinkedIn Text Formatter at least once in your lifetime! I basically embedded one in my script. It makes the LinkedIn feed more eye‑catching and easier to skim.

Before, it would always show the same boring "New blog post is out!" call-to-action without any emojis or formatting or anything. Now that call to action is bold, has an emoji, and is randomized. I also emboldened the "Title:" and emboldened and randomized the "👉 Read it here:" text to either be "👉 Read it here:" or "👉 Check it out!"

Previously, the posts weren't very clear about whether they were posted by a human or not. I wanted to keep my main post clean, but still be transparent that the LinkedIn posts weren't being posted by a human, so I decided to put a comment under the post. That didn't go so well. So there's now just a note in the post that says:

> 𝙉𝙤𝙩𝙚: 𝘛𝘩𝘪𝘴 𝘱𝘰𝘴𝘵 𝘪𝘴 𝘨𝘦𝘯𝘦𝘳𝘢𝘵𝘦𝘥 𝘣𝘺 𝘢 𝘗𝘺𝘵𝘩𝘰𝘯 𝘴𝘤𝘳𝘪𝘱𝘵. 𝘠𝘰𝘶 𝘤𝘢𝘯 𝘧𝘪𝘯𝘥 𝘪𝘵 𝘩𝘦𝘳𝘦: https://github.com/tiash-and-cats/tiash-and-cats.github.io/blob/master/.github/scripts/linkedin_share.py. 𝘐𝘵 𝘴𝘪𝘮𝘱𝘭𝘺 𝘤𝘩𝘦𝘤𝘬𝘴 𝘵𝘩𝘦 𝘭𝘢𝘵𝘦𝘴𝘵 𝘣𝘭𝘰𝘨 𝘱𝘰𝘴𝘵 𝘢𝘯𝘥 𝘱𝘰𝘴𝘵𝘴 𝘢 𝘯𝘰𝘵𝘪𝘧𝘪𝘤𝘢𝘵𝘪𝘰𝘯 𝘪𝘯 𝘵𝘩𝘦 𝘧𝘰𝘳𝘮 𝘰𝘧 𝘢 𝘓𝘪𝘯𝘬𝘦𝘥𝘐𝘯 𝘱𝘰𝘴𝘵. 𝘛𝘩𝘪𝘴 𝘱𝘳𝘰𝘤𝘦𝘴𝘴 𝘥𝘰𝘦𝘴 𝘯𝘰𝘵 𝘶𝘴𝘦 𝘈𝘐.

That way, anyone curious can see how it works, without cluttering the announcement itself.

## How it works

1. The script gets the latest blog post.
2. It prepares a LinkedIn post text and the comment text.
3. It posts the blog update to LinkedIn via the `ugcPosts` API.  
4. It grabs the post ID from the response.  
5. It immediately calls the `socialActions/{postId}/comments` endpoint to add the disclaimer comment.  
6. The post front matter is updated with `post2lnkdin: false` so it won't repost.

## What did I learn?

I learnt that LinkedIn's API has multiple endpoints (`ugcPosts` vs `socialActions`), and knowing which one to use is key. Formatting with Unicode alphabets is surprisingly fun! Keeping disclaimers in comments keeps the feed polished but still transparent.

Now my blog posts show up on LinkedIn with styled text and randomized CTAs, and each one has a clear comment explaining the automation.