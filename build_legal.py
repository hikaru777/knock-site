# Builds privacy.html and terms.html from the app repo's docs/legal/*.md (the source of truth).
#   uv run --with markdown python3 build_legal.py ~/app/knock-v1-chat-20261012T1921Z/docs/legal
import pathlib, re, sys
import markdown

src = pathlib.Path(sys.argv[1]).expanduser()
here = pathlib.Path(__file__).parent
page = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — ノック</title>
<link rel="icon" href="icon.png">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="wrap">
  <header class="site"><img src="icon.png" alt=""><a href="./">ノック</a></header>
  <main><article class="doc">
{body}
  </article></main>
  <footer>
    <nav><a href="./">トップ</a><a href="privacy.html">プライバシーポリシー</a><a href="terms.html">利用規約</a></nav>
    <div>© 2026 ノック</div>
  </footer>
</div>
</body>
</html>
"""
for name, title in [("privacy", "プライバシーポリシー"), ("terms", "利用規約")]:
    text = (src / f"{name}.md").read_text()
    body = markdown.markdown(text, extensions=["tables"])
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    body = re.sub(r"(https://[^\s<）]+)", r'<a href="\1">\1</a>', body)
    (here / f"{name}.html").write_text(page.format(title=title, body=body))
    print("wrote", name)
