import os
import sys
import glob
import frontmatter  # Parses and rewrites YAML front matter safely
import requests

# configuration
ACCESS_TOKEN = os.environ.get("LNKDIN_ACCESS_TOKEN")
with open("linkedin_urn.config.txt"):
    AUTHOR_URN = f.read()
SITE_URL = "https://tiash-and-cats.github.io"

if not ACCESS_TOKEN:
    print("\x1b[1;31mError: Missing LINKEDIN_ACCESS_TOKEN in Environment Secrets.\x1b[0m")
    sys.exit(1)

# look for all blog posts
post_files = glob.glob("_posts/*.md") + glob.glob("_posts/*.markdown")
if not post_files:
    print("No posts found in _posts/ directory.")
    sys.exit(0)

# find the newest markdown post by file creation/modification time
latest_post_path = max(post_files, key=os.path.getmtime)
print(f"Checking front matter for: {latest_post_path}")

# load the file layout
with open(latest_post_path, "r", encoding="utf-8") as f:
    post = frontmatter.load(f)

# conditional check: skip if explicitly marked false
# note: if the key is entirely missing, it defaults to True and executes
if post.get("post2lnkdin") is False:
    print(f"\x1b[23m>> Skipping. 'post2lnkdin: false' found in frontmatter.\x1b[0m")
    sys.exit(0)

print("\x1b[1mNew post discovered! Preparing LinkedIn broadcast...\x1b[0m")

title = post.get("title", "New Blog Update")
description = post.get("description", post.content.split("\n\n", 1)[0])

# derive custom Jekyll permalink structure from file name
filename = os.path.basename(latest_post_path)
date_part = "-".join(filename.split("-")[:3])  # Extracts YYYY-MM-DD
title_part = "-".join(filename.split("-")[3:]).split(".")[0]
post_date_path = date_part.replace("-", "/")

# construct production hyperlink path
permalink = f"{SITE_URL}/{post_date_path}/{title_part}.html"
formatted_text = f"{title}\n\n{description}\n\nRead it here: {permalink}"

# execute LinkedIn REST API Request
url = "https://api.linkedin.com/v2/ugcPosts"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "LinkedIn-Version": "202605",
    "X-Restli-Protocol-Version": "2.0.0",
    "Content-Type": "application/json",
}

payload = {
    "author": AUTHOR_URN,
    "commentary": formatted_text,
    "visibility": "PUBLIC",
    "distribution": {"feedDistribution": "MAIN_FEED"},
    "lifecycleState": "PUBLISHED",
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 201:
    print(f"\x1b[1;22mSuccessfully posted to LinkedIn! URN ID: {response.headers.get('x-restli-id')}\x1b[0m")
    
    # modify frontmatter and overwrite file to prevent duplicate triggers
    post["post2lnkdin"] = False
    with open(latest_post_path, "w", encoding="utf-8") as f:
        frontmatter.dump(post, f, sort_keys=False)  # preserves structure alignment
    print(f"\x1b[1mAppended 'post2lnkdin: false' to {filename} natively.\x1b[0m")
else:
    print(f"\x1b[1;31mAPI Rejected Request: {response.status_code}\n{response.json()}\x1b[0m")
    sys.exit(1)