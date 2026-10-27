#!/usr/bin/env python3
"""src/*.txt -> index.html, guide.html, a/<slug>.html
txt format: 1行目=題, 2行目=要約, 3行目=分類, 空行, 以降は空行区切りの段落。"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "浪費ノート"
TAG = "暇と退屈の倫理学から考える、浪費の暮らし方"

def load():
    items = []
    for p in sorted(glob.glob(os.path.join(ROOT, "src", "*.txt"))):
        slug = re.sub(r"^\d+-", "", os.path.basename(p)[:-4])
        lines = open(p, encoding="utf-8").read().strip().split("\n")
        title, lede, cat = lines[0], lines[1], lines[2]
        paras = [x.strip() for x in "\n".join(lines[3:]).split("\n\n") if x.strip()]
        items.append(dict(slug=slug, title=title, lede=lede, cat=cat, paras=paras))
    return items

def page(title, body, depth, desc):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="top"><a class="brand" href="{up}index.html">{SITE}</a>
<nav><a href="{up}guide.html">考え方</a><a href="{up}index.html#articles">記事</a></nav></header>
<main>
{body}
</main>
<footer>
<p>このサイトは國分功一郎『暇と退屈の倫理学』を読んだ筆者の解釈にもとづく個人のノートです。著者・出版社とは関係がなく、本書の文章は引用していません。正確な議論は本書をお読みください。</p>
</footer>
</body>
</html>
"""

def main():
    items = load()
    guide, arts = items[0], items[1:]
    os.makedirs(os.path.join(ROOT, "a"), exist_ok=True)

    def article_html(it, depth, extra=""):
        ps = "\n".join(f"<p>{html.escape(x)}</p>" for x in it["paras"])
        return (f'<article><p class="cat">{html.escape(it["cat"])}</p>'
                f'<h1>{html.escape(it["title"])}</h1>'
                f'<p class="lede">{html.escape(it["lede"])}</p>{ps}</article>{extra}')

    # guide
    nxt = f'<p class="more"><a href="a/{arts[0]["slug"]}.html">最初の記事へ：{html.escape(arts[0]["title"])}</a></p>'
    open(os.path.join(ROOT, "guide.html"), "w", encoding="utf-8").write(
        page(f'{guide["title"]} | {SITE}', article_html(guide, 0, nxt), 0, guide["lede"]))

    # articles
    for i, it in enumerate(arts):
        nav = '<nav class="pn">'
        nav += (f'<a href="{arts[i-1]["slug"]}.html">← {html.escape(arts[i-1]["title"])}</a>' if i else "<span></span>")
        nav += (f'<a href="{arts[i+1]["slug"]}.html">{html.escape(arts[i+1]["title"])} →</a>' if i + 1 < len(arts) else "<span></span>")
        nav += "</nav>"
        open(os.path.join(ROOT, "a", it["slug"] + ".html"), "w", encoding="utf-8").write(
            page(f'{it["title"]} | {SITE}', article_html(it, 1, nav), 1, it["lede"]))

    # index
    cards = "\n".join(
        f'<a class="card" href="a/{a["slug"]}.html"><span class="cat">{html.escape(a["cat"])}</span>'
        f'<h2>{html.escape(a["title"])}</h2><p>{html.escape(a["lede"])}</p></a>' for a in arts)
    body = f"""<section class="hero">
<h1>ヒマを、ちゃんと浪費する。</h1>
<p>忙しいのに満たされないのは、時間が足りないからではなく、何を受け取っているかの問題かもしれません。國分功一郎『暇と退屈の倫理学』の考え方をもとに、料理、勉強、スポーツ、睡眠、お金、人付き合い、仕事、読書など暮らしの場面を、浪費の目で見直していくノートです。</p>
<p class="more"><a href="guide.html">まずは考え方を読む</a></p>
</section>
<section id="articles"><h2 class="sec">記事</h2>
<div class="grid">
{cards}
</div></section>"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page(f"{SITE} | {TAG}", body, 0, TAG))
    print("built", len(arts), "articles")

main()
