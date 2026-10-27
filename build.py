#!/usr/bin/env python3
"""src/*.txt -> index.html, guide.html, a/<slug>.html
txt format: 1行目=題, 2行目=要約, 3行目=分類, 空行, 以降は空行区切りの段落。"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://kaitoinoue0921.github.io/rouhi-note/"
SITE = "浪費ノート"
TAG = "暇と退屈の倫理学から考える、浪費の暮らし方"


WEEK = [
 ("一日目", "何も変えずに、閉じたきっかけだけを書く", "phone", "今日は、いつもどおりスマホを使ってください。ただし、動画やSNSを閉じるたびに、何がきっかけで閉じたかを一言だけ書きます。満足したから、眠くなったから、電池が切れたから、誰かに呼ばれたから。自分で閉じたのか、外から閉じさせられたのかが分かれば十分です。"),
 ("二日目", "開く前に、本数か時間を決める", "phone", "動画を開く前に、今日は三本まで、あるいは十分までと決めます。守れたかどうかより、決めたことで見え方が変わるかを確かめます。終わりを自分で作ると、一本ごとの重さが変わります。"),
 ("三日目", "寝床にスマホを持ち込まない", "sleep", "寝る一時間前から、スマホを寝床から離します。充電器を部屋の反対側に置くのが簡単です。睡眠は、勉強したことを記憶に定着させる時間でもあります。眠れない夜の最初の十分は、天井を眺めて過ごします。"),
 ("四日目", "待ち時間の最初の三分を、何もせずに過ごす", "walk", "電車やレジの待ち時間に、最初の三分だけスマホを出しません。退屈を一度通ってから、気晴らしを選びます。三分たって見たくなったなら、見ていいのです。"),
 ("五日目", "動画を一本選んで、浪費として最後まで味わう", "phone", "今日は、見たい動画を一本だけ、先に選びます。ほかの画面は閉じて、その一本だけを最後まで見ます。見終わったら、すぐに次へ行かず、少し余韻を置きます。満足して止まれたなら、それは浪費です。"),
 ("六日目", "誰にも言わないつもりで、本を十ページ読む", "reading", "読んだ冊数にも、人に話せる要約にもならないつもりで、十ページだけ読みます。引っかかった一文を、そのまま書き写します。要約ではなく、本の言葉のままで残します。"),
 ("七日目", "満足して止まれた回数を、一日目と比べる", "money", "一週間の最後に、満足して自分で止まれた回数を、一日目と比べます。増えていなくてもかまいません。どの日がいちばん楽で、どの日が難しかったかが、これからの暮らし方の手がかりになります。"),
]

def load():
    items = []
    for p in sorted(glob.glob(os.path.join(ROOT, "src", "*.txt"))):
        slug = re.sub(r"^\d+-", "", os.path.basename(p)[:-4])
        lines = open(p, encoding="utf-8").read().strip().split("\n")
        title, lede, cat = lines[0], lines[1], lines[2]
        paras = [x.strip() for x in "\n".join(lines[3:]).split("\n\n") if x.strip()]
        items.append(dict(slug=slug, title=title, lede=lede, cat=cat, paras=paras))
    return items

def page(title, body, depth, desc, path=""):
    up = "../" * depth
    url = BASE + path
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE}">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="top"><a class="brand" href="{up}index.html">{SITE}</a>
<nav><a href="{up}guide.html">考え方</a><a href="{up}index.html#articles">記事</a><a href="{up}week.html">一週間</a></nav></header>
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
        page(f'{guide["title"]} | {SITE}', article_html(guide, 0, nxt), 0, guide["lede"], "guide.html"))

    # articles
    for i, it in enumerate(arts):
        nav = '<nav class="pn">'
        nav += (f'<a href="{arts[i-1]["slug"]}.html">← {html.escape(arts[i-1]["title"])}</a>' if i else "<span></span>")
        nav += (f'<a href="{arts[i+1]["slug"]}.html">{html.escape(arts[i+1]["title"])} →</a>' if i + 1 < len(arts) else "<span></span>")
        nav += "</nav>"
        rel = [a for j, a in enumerate(arts) if j not in (i, i-1, (i+1) % len(arts))]
        rel = (rel[i % len(rel):] + rel[:i % len(rel)])[:3]
        nav += '<section class="rel"><h2 class="sec">ほかの記事</h2>' + "".join(
            f'<a href="{a["slug"]}.html"><span class="cat">{html.escape(a["cat"])}</span> {html.escape(a["title"])}</a>' for a in rel) + "</section>"
        open(os.path.join(ROOT, "a", it["slug"] + ".html"), "w", encoding="utf-8").write(
            page(f'{it["title"]} | {SITE}', article_html(it, 1, nav), 1, it["lede"], "a/" + it["slug"] + ".html"))

    # index
    cards = "\n".join(
        f'<a class="card" href="a/{a["slug"]}.html"><span class="cat">{html.escape(a["cat"])}</span>'
        f'<h2>{html.escape(a["title"])}</h2><p>{html.escape(a["lede"])}</p></a>' for a in arts)
    body = f"""<section class="hero">
<h1>ヒマを、ちゃんと浪費する。</h1>
<p>忙しいのに満たされないのは、時間が足りないからではなく、何を受け取っているかの問題かもしれません。國分功一郎『暇と退屈の倫理学』の考え方をもとに、料理、勉強、スポーツ、睡眠、お金、人付き合い、仕事、読書など暮らしの場面を、浪費の目で見直していくノートです。</p>
<p class="more"><a href="guide.html">まずは考え方を読む</a>　<a href="week.html">いきなり一週間試す</a></p>
</section>
<section id="articles"><h2 class="sec">記事</h2>
<div class="grid">
{cards}
</div></section>"""
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page(f"{SITE} | {TAG}", body, 0, TAG, ""))
    ti = {a["slug"]: a["title"] for a in arts}
    ds = "".join(f'<p class="cat">{d}</p><h2 class="day">{html.escape(h)}</h2><p>{html.escape(t)}</p><p class="more"><a href="a/{sl}.html">関連：{html.escape(ti[sl])}</a></p>' for d, h, sl, t in WEEK)
    wb = ('<article><p class="cat">一週間</p><h1>一週間、浪費を試す</h1><p class="lede">読むだけで終わらせず、七日間で気晴らしとの付き合い方を試す小さな実験です。</p>'
          '<p>やめることを目標にはしません。毎日、やることを一つだけ変えて、満足して自分で止まれたかを見ます。紙やメモ帳に、日付と一言だけ書けば足ります。途中で一日抜けても、そのまま続けてください。</p>' + ds + '</article>')
    open(os.path.join(ROOT, "week.html"), "w", encoding="utf-8").write(
        page(f"一週間、浪費を試す | {SITE}", wb, 0, "気晴らしとの付き合い方を七日間で試す小さな実験。", "week.html"))
    print("built", len(arts), "articles")

main()
