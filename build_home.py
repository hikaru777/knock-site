# Builds index.html (Japanese) and en/index.html (English) from one template, in the shape
# of the NotchSwitcher site (2026-10-26, human: ノッチはこんなサイトじゃないでしょちゃんとしてよ):
# a full-width moving hero, short lines, real pictures of the app, FAQ, the film in a dialog.
#   python3 build_home.py
import pathlib

here = pathlib.Path(__file__).parent
DOWNLOAD = "https://github.com/hikaru777/knock-releases/releases/latest/download/Knock.zip"
RELEASES = "https://github.com/hikaru777/knock-releases/releases"


def page(lang):
    ja = lang == "ja"
    t = lambda j, e: j if ja else e
    r = "" if ja else "../"
    faq = [
        (t("友達も Knock が必要ですか？", "Does my friend need Knock too?"),
         t("はい。2人とも Knock を入れてサインインし、招待コードでつながります。友達がまだいなくても、お試しの相手（あお・はる）と一通り試せます。",
           "Yes. You both install Knock, sign in, and connect with an invite code. No friends on Knock yet? Try everything with the demo partners, Ao and Haru.")),
        (t("料金はかかりますか？", "Does it cost anything?"),
         t("無料です。広告もありません。", "It’s free, with no ads.")),
        (t("カーソルや画面は、どこを通りますか？", "Where do my cursor and screen go?"),
         t("2台の Mac を直接つないで、暗号化してやりとりします。ネットワークの都合で直接つながらないときだけ、サーバーがその場で中継します（保存はしません）。",
           "Straight between the two Macs, encrypted. Only when a direct connection can’t be made does the server relay them, live, without storing them.")),
        (t("どんな権限が必要ですか？", "What permissions does it need?"),
         t("画面を見せるときだけ、macOS の「画面収録」の許可を使います。見せるのは、あなたが選んだウィンドウだけです。",
           "Only when you show your screen: macOS Screen Recording. Only the window you choose is shown.")),
        (t("作業に集中したいときは？", "What if I need to focus?"),
         t("「集中する」をオンにすると、届いたノックは静かに待ちます。顔を上げて画面の端に来たときに受け取れます。",
           "Turn on Focus and knocks wait quietly until you come back to the edge.")),
    ]
    faq_html = "".join(f"<details><summary>{q}<span>＋</span></summary><p>{a}</p></details>" for q, a in faq)
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#090a0b">
<meta name="description" content="{t("画面の端を3回ノックすると、友達に届く。応じたら、2人の画面の端に小さな部屋が開く。Mac 用の無料アプリ。", "Knock three times on the edge of your screen and a friend gets it. When they answer, a small room opens on the edge of both screens. Free for Mac.")}">
<meta property="og:title" content="{t("ノック", "Knock")}"><meta property="og:image" content="https://hikaru777.github.io/knock-site/assets/poster.jpg">
<link rel="alternate" hreflang="ja" href="https://hikaru777.github.io/knock-site/"><link rel="alternate" hreflang="en" href="https://hikaru777.github.io/knock-site/en/">
<title>{t("ノック — 画面の端に、友達の部屋。", "Knock — A room for friends, on the edge of your screen.")}</title><link rel="icon" href="{r}icon.png"><link rel="stylesheet" href="{r}home.css"></head><body>
<header><a class="wordmark" href="#top"><img src="{r}icon.png" alt="">{t("ノック", "Knock")}<i></i></a><div class="header-right"><nav aria-label="{t("メインナビゲーション", "Main")}"><a href="#experience">{t("体験", "Experience")}</a><a href="#how">{t("使い方", "How it works")}</a><a href="#questions">FAQ</a><button class="nav-cta" data-open="availability">{t("ダウンロード", "Download")}</button></nav><div class="language-switch"><a href="{t("./", "../")}" lang="ja"{' aria-current="page"' if ja else ''}>JP</a><span>/</span><a href="{t("en/", "./")}" lang="en"{'' if ja else ' aria-current="page"'}>EN</a></div></div></header>
<main id="top"><section class="hero immersive-hero" id="experience"><div class="hero-motion" aria-hidden="true"><video id="background-demo" autoplay loop muted playsinline preload="auto" poster="{r}assets/poster.jpg"><source src="{r}assets/knock-zoom.mp4" type="video/mp4"></video><div class="blur-mid"></div><div class="blur-deep"></div><div class="motion-fade"></div></div><button id="background-toggle" class="motion-toggle" aria-label="{t("背景動画を一時停止", "Pause background video")}">Ⅱ <span>{t("映像を停止", "Pause video")}</span></button>
<div class="immersive-copy"><p class="eyebrow">Knock for Mac</p><h1>{t("画面の端に、<br><em>友達の部屋。</em>", "A room for friends,<br><em>on the edge.</em>")}</h1><p class="hero-description">{t("通話するほどじゃない。でも、ちょっと話したい。<br>画面の端を、3回ノックするだけ。", "Not quite a call. Just a quick word.<br>Knock three times on the edge of your screen.")}</p><div class="hero-actions"><button class="primary" data-open="availability">{t("無料でダウンロード", "Download free")}</button><button class="film-trigger" data-open="film"><span class="play-mark">▷</span> {t("動きを見る", "Watch it")}</button></div><p class="price-note">{t("無料", "Free")} <span>／</span> {t("広告なし", "No ads")} <span>／</span> macOS 26 {t("以降", "or later")}</p></div><div class="hero-foot"><span>{t("話すより軽く、チャットより近く。", "Lighter than talking. Closer than chat.")}</span><span>SCROLL TO EXPLORE <i>↓</i></span></div></section>
<section class="manifesto"><p class="section-label">01 / THE IDEA</p><div><h2>{t("通話の手前に、<br>もうひとつ。", "Something before<br>a call.")}</h2><p>{t("画面の端に、いつも友達がいる。<br>ノックすれば、すぐに小さな部屋が開く。<br>一言も、ファイルも、画面も、その部屋で。", "Your friends, always at the edge of the screen.<br>Knock, and a small room opens right there.<br>Words, files and screens, all in that room.")}</p></div><p class="side-note">{t("となりの席の、<br>「今ちょっといい？」", "The “got a sec?”<br>from the next desk.")}</p></section>
<section class="how" id="how"><div class="section-heading"><p class="section-label">02 / THREE KNOCKS</p><h2>{t("止めて。選んで。<br>3回ノック。", "Rest. Choose.<br>Knock three times.")}</h2><p>{t("画面の右端にカーソルを止めると、友達のダイヤル。<br>端に3回ぶつければ、相手に届きます。", "Rest your cursor on the right edge for a dial of friends.<br>Bump the edge three times and they get your knock.")}</p></div><div class="steps">
<article><div class="step-art"><img src="{r}assets/step-dial.jpg" alt="" loading="lazy"></div><div class="step-copy"><span>01</span><h3>{t("端に止めて、選ぶ", "Rest and choose")}</h3><p>{t("右端にカーソルを止めて、<br>スクロールで相手を選びます。", "Rest on the right edge,<br>scroll to choose a friend.")}</p></div></article>
<article><div class="step-art"><img src="{r}assets/step-room.jpg" alt="" loading="lazy"></div><div class="step-copy"><span>02</span><h3>{t("3回ノック", "Knock three times")}</h3><p>{t("端に3回ぶつけると届きます。<br>応じたら、2人の部屋が開きます。", "Bump the edge three times.<br>When they answer, a room opens.")}</p></div></article>
<article><div class="step-art"><img src="{r}assets/step-talk.jpg" alt="" loading="lazy"></div><div class="step-copy"><span>03</span><h3>{t("部屋で話す", "Talk in the room")}</h3><p>{t("一言、ファイル、画面。<br>ぜんぶ、その部屋で。", "A word, a file, a screen.<br>All in the room.")}</p></div></article>
</div></section>
<section class="detail-section"><div class="detail-image"><img src="{r}assets/room.jpg" alt="{t("あおが画面を見せている部屋", "Ao’s screen in the room")}" loading="lazy"><span class="image-tag">IN THE ROOM</span></div><div class="detail-copy"><p class="section-label">03 / IN THE ROOM</p><h2>{t("話す。渡す。<br>見せる。", "Talk. Hand over.<br>Show.")}</h2><p>{t("相手のカーソルが、名前つきで動く部屋。<br>指さすだけで伝わります。", "In the room, their cursor moves with their name on it.<br>Pointing is enough.")}</p>
<div class="detail-rule"><span>{t("一言", "Words")}</span><p>{t("打たずに返せる一言と、メッセージ。", "Quick replies without typing, and messages.")}</p></div><div class="detail-rule"><span>{t("ファイル", "Files")}</span><p>{t("フォルダごと、部屋に落とすだけ。", "Drop a whole folder into the room.")}</p></div><div class="detail-rule"><span>{t("画面", "Screens")}</span><p>{t("選んだウィンドウを見せて、ピンで指す。", "Show the window you choose, pin a spot on it.")}</p></div><div class="detail-rule"><span>{t("グループ", "Groups")}</span><p>{t("何人かでひとつの部屋。画面は並んで映ります。", "One room for several friends, their screens side by side.")}</p></div></div></section>
<section class="faq" id="questions"><div><p class="section-label">04 / GOOD TO KNOW</p><h2>{t("使い始める前に。", "Before you start.")}</h2></div><div class="questions">{faq_html}</div></section>
<section class="closing"><p>ONE KNOCK AWAY.</p><h2>{t("今、ちょっといい？", "Got a sec?")}</h2><p class="closing-price">{t("Mac 用・無料。広告なし。", "For Mac. Free. No ads.")}</p><button class="primary" data-open="film">{t("ノックの動きを見る", "Watch Knock in action")} <span>▷</span></button><button class="text-button" data-open="availability">{t("ダウンロード", "Download")}</button></section></main>
<footer><a class="wordmark" href="#top"><img src="{r}icon.png" alt="">{t("ノック", "Knock")}<i></i></a><p>{t("画面の端に、友達の部屋。", "A room for friends, on the edge of your screen.")}</p><nav class="footer-links"><a href="{r}privacy.html">{t("プライバシーポリシー", "Privacy (Japanese)")}</a><a href="{r}terms.html">{t("利用規約", "Terms (Japanese)")}</a><a href="{RELEASES}">{t("すべての版", "All versions")}</a></nav><small>© 2026 {t("ノック", "Knock")}</small></footer>
<dialog id="film"><button class="close" aria-label="{t("閉じる", "Close")}">×</button><video controls playsinline preload="none" poster="{r}assets/poster.jpg"><source src="{r}assets/knock-film.mp4" type="video/mp4"></video></dialog>
<dialog id="availability"><button class="close" aria-label="{t("閉じる", "Close")}">×</button><p class="section-label">{t("ノック", "Knock")}</p><h2>{t("ダウンロードして、はじめる", "Download and start")}</h2><p>{t("無料です。Knock.zip を開いて、Knock を「アプリケーション」フォルダに入れてください。<br>メールに届く6桁のコードでサインインし、招待コードを友達に送ればつながります。新しい版はアプリが自動で受け取ります。", "It’s free. Open Knock.zip and move Knock to your Applications folder.<br>Sign in with the six-digit code sent to your email, and send your invite code to a friend. Updates arrive automatically.")}</p><div class="download-actions"><a class="primary" href="{DOWNLOAD}">{t("Mac 版をダウンロード", "Download for Mac")}</a><a class="text-button" href="{RELEASES}">{t("すべての版", "All versions")}</a></div><p class="quiet-note">{t("対応環境：macOS 26 以降・Apple シリコン / Intel。", "Requires macOS 26 or later · Apple silicon / Intel.")}</p><button class="primary close-secondary">{t("ページに戻る", "Back to the page")}</button></dialog>
<script src="{r}home.js"></script></body></html>
"""


(here / "index.html").write_text(page("ja"))
(here / "en").mkdir(exist_ok=True)
(here / "en" / "index.html").write_text(page("en"))
print("built index.html, en/index.html")
