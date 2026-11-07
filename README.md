# Dr. Yuvaraju Chinnam’s blog

A personal academic blog inspired by [S Anand’s site](https://www.s-anand.net/). The home page has an author introduction and recent posts. The archive filters by topic, year, and keyword. The Social page lists notes with links to individual LinkedIn or Instagram posts.

## Publish on GitHub Pages

1. Create an empty GitHub repository named `yuvaraju-blog` (or choose another name). Use a public repository for GitHub Pages on GitHub Free.
2. From this folder, push the `main` branch to that repository. Substitute your GitHub username and repository name.

   ```sh
   git remote add origin https://github.com/YOUR-USERNAME/yuvaraju-blog.git
   git push -u origin main
   ```

   If you downloaded the source ZIP, first run `git init -b main`, `git add .`, and `git commit -m "Create academic blog"` from the extracted folder.

3. In **Settings → Pages**, under **Build and deployment**, choose **GitHub Actions**.
4. In **Actions**, open **Deploy blog to GitHub Pages** and select **Run workflow**. Subsequent pushes to `main` deploy automatically.
5. Open the URL shown in **Settings → Pages**. For a project repository it is usually `https://YOUR-USERNAME.github.io/yuvaraju-blog/`.

GitHub supplies the deployed URL to the build so links, styles, and the feed work under a repository path or on a custom domain.

## Use a custom domain

In the repository’s **Settings → Pages**, enter your hostname under **Custom domain**. Follow [GitHub’s DNS setup instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) for the domain you choose. For a subdomain such as `blog.example.com`, create a DNS CNAME record pointing to `YOUR-USERNAME.github.io`. Enable **Enforce HTTPS** once GitHub offers it, then run the deployment workflow again so the feed and canonical URLs use the new domain.

To use a different static host, build with `python build.py --url https://blog.example.com` and publish the contents of `dist/`.

## Add or edit a post

You can edit directly in the GitHub web interface. Copy [_drafts/post-template.md](_drafts/post-template.md) into `posts/` as, for example, `2026-11-07-my-new-post.md`. The filename gives the post its displayed date and a link at `/posts/my-new-post/`. Keep the slug unchanged after sharing the link.

Write the article after the second `---`. Above it, fill in the title and summary, and list any topics under `tags`. To add a social post or reel, use the individual **Copy link** URL from LinkedIn or Instagram. Add either or both fields to the front matter:

```yaml
linkedin: <paste an individual LinkedIn post URL>
instagram: <paste an individual Instagram reel or post URL>
```

Remove unused lines and replace the placeholders with real links. These fields add outbound links to the article and automatically list it on the **Social** page. They also work for short, link-first entries with a few lines of context. The site uses plain links so visitors can read it without loading social widgets.

To publish a blog note first and share it later, add your script or caption to the note, share the article’s URL, then return and add the social permalink. Two lesson notes include sample reel scripts, and the survey note has a LinkedIn caption draft. Review those before publishing. Keep private drafts outside any public repository. The `_drafts/` folder is skipped by the website build but its contents can still be read in a public repository.

Edit `about.md` for the biography and `site.yml` for the name, affiliation, and profile links. Put article images in `assets/` and link to them from a post with `../../assets/your-image.jpg` and descriptive alt text.

## Preview locally

Use Python 3.11 or later. On macOS or Linux, run:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python -m http.server 8000 --directory dist
```

Open <http://localhost:8000>. Rerun `python build.py` after editing Markdown and refresh the browser.
