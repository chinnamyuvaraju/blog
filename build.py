"""Build the Markdown blog into dist/."""
import argparse
import json
import os
from collections import Counter
from datetime import date
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
import markdown
from markupsafe import Markup
import yaml


ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT / "dist"
SOCIAL = {"linkedin": ("linkedin.com", "/posts/", "/feed/update/"),
          "instagram": ("instagram.com", "/p/", "/reel/", "/reels/", "/tv/")}


def read_markdown(path):
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^---[ \t]*\r?\n", text, maxsplit=2, flags=re.M)
    if len(parts) != 3 or parts[0]:
        raise ValueError("start the file with YAML front matter enclosed by ---")
    _, metadata, body = parts
    fields = yaml.safe_load(metadata)
    if fields is None:
        fields = {}
    if not isinstance(fields, dict):
        raise ValueError("YAML front matter must contain named fields")
    fields["body"] = Markup(markdown.markdown(body, extensions=["fenced_code", "tables"]))
    return fields


def load_posts():
    posts = []
    slugs = set()
    for path in sorted((ROOT / "posts").rglob("*.md")):
        try:
            post = read_markdown(path)
            match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)", path.stem)
            if not match:
                raise ValueError("use YYYY-MM-DD-title-with-hyphens.md")
            posted, slug = match.groups()
            if slug in slugs:
                raise ValueError(f"duplicate slug: {slug}")
            for key in ("title", "summary"):
                if not isinstance(post.get(key), str) or not post[key].strip():
                    raise ValueError(f"{key} must be a non-empty string")
            tags = post.get("tags", [])
            if not isinstance(tags, list) or any(not isinstance(tag, str) or not tag.strip() for tag in tags):
                raise ValueError("tags must be a list of non-empty strings")
            section = path.parent.relative_to(ROOT / "posts").as_posix()
            if section != ".":
                tags = [*tags, section.replace("/", " / ").replace("-", " ").title()]
            post["tags"] = list(dict.fromkeys(tag.strip() for tag in tags))
            for platform in SOCIAL:
                if post.get(platform):
                    post["tags"].append(platform.title())
            post["tags"] = list(dict.fromkeys(post["tags"]))
            for platform, (domain, *prefixes) in SOCIAL.items():
                link = post.get(platform)
                if link:
                    parsed = urlsplit(link)
                    if (parsed.scheme != "https" or parsed.hostname not in {domain, f"www.{domain}", f"in.{domain}"}
                            or not any(parsed.path.startswith(prefix) and parsed.path[len(prefix):].strip("/")
                                       for prefix in prefixes)):
                        raise ValueError(f"{platform} must link to an individual post or reel")
            post.update(date=date.fromisoformat(posted), path=f"posts/{slug}/")
            posts.append(post)
            slugs.add(slug)
        except (TypeError, ValueError, AttributeError, yaml.YAMLError) as error:
            raise SystemExit(f"{path.name}: {error}") from error
    return sorted(posts, key=lambda post: (post["date"], post["path"]), reverse=True)


def build(site_url):
    site_url = site_url.rstrip("/")
    parts = urlsplit(site_url)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.query or parts.fragment:
        raise SystemExit("Use a full site URL, e.g. https://owner.github.io/blog")
    site = yaml.safe_load((ROOT / "site.yml").read_text(encoding="utf-8"))
    posts = load_posts()
    home = read_markdown(ROOT / "home.md")
    about = read_markdown(ROOT / "about.md")
    links = json.loads((ROOT / "social.json").read_text(encoding="utf-8"))
    for field in ("background", "foreground", "button"):
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", links[field]):
            raise SystemExit(f"Social {field} must be a six-digit hex color")
    for link in links["links"]:
        if urlsplit(link["url"]).scheme not in {"https", "http"}:
            raise SystemExit("Social links must use https:// or http://")
    if links.get("image") and not re.fullmatch(r"[a-zA-Z0-9._-]+", links["image"]):
        raise SystemExit("Use an uploaded image filename for the Social portrait")
    for page in [*posts, home, about]:
        page["body"] = Markup(str(page["body"]).replace('src="media:', f'src="{parts.path}/assets/uploads/'))
    topics = sorted(Counter(tag for post in posts for tag in post["tags"]).items(), key=lambda item: item[0].casefold())
    years = sorted({post["date"].year for post in posts}, reverse=True)
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals.update(
        site=site, home=home, links=links, posts=posts, topics=topics, years=years, site_url=site_url,
        url=lambda path="": f"{parts.path}/{path}",
        absolute=lambda path="": f"{site_url}/{path}",
    )

    with TemporaryDirectory(dir=ROOT) as temporary:
        output = Path(temporary) / "site"
        output.mkdir()
        shutil.copytree(ROOT / "assets", output / "assets")
        (output / ".nojekyll").touch()
        repository = os.environ.get("GITHUB_REPOSITORY", site.get("repository", "chinnamyuvaraju/yuvaraju-blog"))
        (output / "assets/admin-config.js").write_text("window.BLOG_REPOSITORY = " + json.dumps(repository) + ";", encoding="utf-8")

        def render(template, path, *, filename="index.html", **context):
            file = output / path / filename
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(env.get_template(template).render(path=path, **context), encoding="utf-8")

        render("home.html", "", title=None, active="home")
        render("archive.html", "archive/", title="Archive", active="archive")
        render("social.html", "social/", title="Social", active="social",
               social_posts=[post for post in posts if any(post.get(name) for name in SOCIAL)])
        render("about.html", "about/", title="About", active="about", about=about)
        for post in posts:
            render("post.html", post["path"], title=post["title"], active=None, post=post)
        render("404.html", "", filename="404.html", title="Page not found", active=None, missing=True)
        render("feed.xml", "", filename="feed.xml")
        if DESTINATION.exists():
            shutil.rmtree(DESTINATION)
        output.rename(DESTINATION)
    print(f"Built {len(posts)} posts in {DESTINATION}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8000", help="Full public URL, including any repository path")
    build(parser.parse_args().url)
