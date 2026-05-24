# Tiash's website!

{% include linktree.md %}

Hello, I'm Ridwan Bin Mohammad. Please don't call me Ridwan, instead call me Tiash. I'm a young (<span id="age"></span> year old) developer. This is my little spot in the web.

I have many [projects](projects.md), such as an [image format](https://tiash-and-cats.github.io/nvgif/) and an [operating system](https://github.com/PopcornOS/popcorn-os). I've also written some [stories](stories.md).

## Why did I get redirected here?

If you got redirected from https://tiashfam.w3spaces.com/, then it's because that was my old website. It has been shut down because: 

1. It's too hard to write raw HTML, CSS and JavaScript. This new site is written in Markdown with the static site generator Jekyll.
2. Without W3Schools Pro, W3Schools Spaces has a limit on how many visits your site gets.
3. It also has a limit on how many files your site can have.

All important stuff has been moved (for example, my now-defunct [blog](oldblog/), previously News, and my [stories](stories.md), previously Books).

<script>
function getAge(birthDateStr) {
  const birthDate = new Date(birthDateStr);
  const today = new Date();

  let age = today.getFullYear() - birthDate.getFullYear();
  const hasHadBirthdayThisYear =
    today.getMonth() > birthDate.getMonth() ||
    (today.getMonth() === birthDate.getMonth() &&
     today.getDate() >= birthDate.getDate());

  if (!hasHadBirthdayThisYear) {
    age--;
  }
  return age;
}

const age = getAge("2014-22-09");
document.getElementById("age").textContent = age;
</script>