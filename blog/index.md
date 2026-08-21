# Blog

Suprise! I have a blog now. Here are the posts that there currently are:

<ul>
{% for post in site.posts %}
  <li>
    <a href="{{ post.url }}">{{ post.title }}</a><br>
    <time datetime="{{ post.date | date_to_xmlschema }}">
      {{ post.date | date: "%B %d, %Y" }}
    </time><br>
    <p><blockquote>{{ post.excerpt }}</blockquote></p>
  </li>
{% endfor %}
</ul>

There's also [an RSS feed](/feed.xml).

Most blog posts also have a synopsis cross-posted to LinkedIn, so you can follow me there too.

The following is the blog I used to maintain at my old website. It is kept for archival purposes. The earliest and cringiest posts have not been archived, for I want to make this site somewhat professional.

- [I made a code editor using HTML, CSS and JS!](/oldblog/i-made-a-code-editor.html)
- [I made my own programming language!](/oldblog/i-made-my-own-language.html)
- [I made my own browser!](/oldblog/i-made-my-own-browser.html)
- [I made my own image format!](/oldblog/i-made-my-own-image-fmt.html)
