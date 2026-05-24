# I made a code editor using HTML, CSS and JS!

{% include linktree.md %}

<i>Feb 13, 2024 <small class="edited">edited May 23, 2025</small></i></h2>

<p>I made a code editor! It's called Morsel, <a href='https://tiashfam.w3spaces.com/sfy/?file=https://tiashdev.github.io/tiashfam-resources/sfy-examples/morsel.html'>and here is a sample.</a></p>
<p>It's very nice, isn't it? The features are:</p>
<ul>
  <li>Syntax highlighting</li>
</ul>
<p>..I couldn't think of anything else. You can access the core syntax highlighting features by making an element with one of the <code>morsel-<i>language</i></code> classes.</p>
<p>There are currently four supported languages. They are:</p>
<ul>
  <li>HTML: To make your website</li>
  <li>CSS: To style your website</li>
  <li>JavaScript or JS: To make your website functional</li>
  <li>SGML and XML: Languages that are both human and machine readable (more commonly XML).</li>
</ul>
<p>To use it, put the following in your <code>&lt;head&gt;</code>:</p>
<pre class="morsel-html">&lt;script src="https://tiashdev.github.io/tiashfam-resources/morsel/index.js"&gt;&lt;/script&gt;</pre>
<p>The features left to add are:</p>
<ul>
  <li><s>Making the tab key work as indentation</s> Some people navigate their computers by only using the tab key, not using their mouse (if they have a mouse). For those people, I am not implementing this feature.
  <br><b>Note:</b> I did end up implementing this feature, but put it behind a flag.</li>
  <li><s>Making it less of a pain to set up</s> I think I have finally made it easy to set up! To see the code to set it up, click the sample link above.</li>
</ul>
<p><b>Note:</b> If you clicked the sample link above, you might have noticed that the SFY (See For Yourself) editor has syntax highlighting. And that was done using Morsel!</p>