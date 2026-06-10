# I made my own image format!

<i>Apr 6, 2025</i>

<p>Well, of course I did. It's called NVGIF (Not Very Good Image Format), and it works!</p>
<p>AirSquirrel now supports viewing NVGIF pictures, just like PNGs!</p>
<p>NVGIFv1 worked like this:</p>
<ul>
   <li><b>Magic bytes:</b> "NVG"<br>
       Every NVGIF image starts with these three bytes.</li>
   <li><b>Version:</b> The byte <code>\x01</code> (<code>00000001</code> in binary) for v1.</li>
   <li><b>Width:</b> 2-byte big-endian number.<br>
   "Big-endian" just means that 200 is <code>00 C8</code> instead of <code>C8 00</code>. Kind of like if we wrote 2578 as 7825.</li>
   <li><b>Height:</b> 2-byte big-endian number.</li>
   <li>Then, for each row in the image:
      <ul>
         <li>A two-byte, big-endian header with the length of the row.</li>
         <li>For each pixel in the row:
            <ul>
               <li>One byte for red</li>
               <li>One byte for blue</li>
               <li>One byte for green</li>
            </ul>
         </li>
      </ul>
   </li>
</ul>
<p>More info can be found <a href="https://tiashdev.github.io/tiashfam-resources/nvgif/specs/">here</a>.