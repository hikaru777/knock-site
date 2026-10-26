# Builds index.html (Japanese) and en/index.html (English) from one template.
#   python3 build_home.py
import json, pathlib

here = pathlib.Path(__file__).parent
DOWNLOAD = "https://github.com/hikaru777/knock-releases/releases/latest/download/Knock.zip"
RELEASES = "https://github.com/hikaru777/knock-releases/releases"


def page(lang):
    ja = lang == "ja"
    t = lambda j, e: j if ja else e
    root = "" if ja else "../"
    demo_text = {
        "idle": t("画面の右端へ、カーソルを動かしてみてください。", "Move your cursor to the right edge of the screen."),
        "edge": t("端で上下にスクロールして相手を選び、端に3回ぶつけて（クリック3回でも）ノック。", "Scroll up or down on the edge to choose, then bump the edge three times (or click three times) to knock."),
        "knocking": t("{name}にノックしました…", "Knocking on {name}…"),
        "room": t("{name}が応じました。一言を返したり、画面を見せてもらったりできます。", "{name} answered. Send a quick reply, or ask to see their screen."),
        "closed": t("部屋を閉じました。もう一度試せます。", "Room closed. Try it again."),
        "connected": t("つながっています", "Connected"),
        "theirScreen": t("{name}の画面", "{name}’s screen"),
        "showMe": t("画面を見せてもらう", "Ask to see their screen"),
        "back": t("外をクリックか Esc で部屋に戻る", "Click outside or press Esc to go back"),
        "replies": t(["OK", "待って", "あとで"], ["OK", "Wait", "Later"]),
        "answer": t("いいよ、今見せるね", "Sure, showing you now"),
        "theirReplies": t(["了解！", "ゆっくりでいいよ", "じゃあまたあとで"], ["Got it!", "Take your time", "Talk later, then"]),
        "people": t(["ハル", "ナギ", "アオ"], ["Haru", "Nagi", "Ao"]),
        "tryClick": t("クリックで試す", "Try with a click"),
        "close": t("閉じる", "Close"),
    }
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t("ノック — 画面の端に、友達の部屋。", "Knock — A room for friends, on the edge of your screen.")}</title>
<meta name="description" content="{t("画面の端にカーソルを3回ぶつけると、友達にノックが届く。応じると、2人の画面の端に小さな部屋が開く。Mac 用の無料アプリ。", "Bump the edge of your screen three times and a friend gets a knock. When they answer, a small room opens on the edge of both screens. Free for Mac.")}">
<meta property="og:title" content="{t("ノック", "Knock")}">
<meta property="og:description" content="{t("画面の端に、友達の部屋。", "A room for friends, on the edge of your screen.")}">
<meta property="og:image" content="https://hikaru777.github.io/knock-site/icon.png">
<link rel="alternate" hreflang="ja" href="https://hikaru777.github.io/knock-site/">
<link rel="alternate" hreflang="en" href="https://hikaru777.github.io/knock-site/en/">
<link rel="icon" href="{root}icon.png">
<link rel="stylesheet" href="{root}home.css">
</head>
<body>
<main class="shell">
  <nav class="navigation">
    <a class="brand" href="./"><img src="{root}icon.png" width="36" height="36" alt="">{t("ノック", "Knock")}</a>
    <a href="{t("en/", "../")}" hreflang="{t("en", "ja")}" lang="{t("en", "ja")}">{t("English", "日本語")}</a>
  </nav>

  <header class="hero">
    <div>
      <p class="label"><span class="dot"></span>{t("Mac のための、となりの席。", "The seat next to you, for Mac.")}</p>
      <h1>{t("画面の端を、3回。", "Bump the edge, three times.")}<br><span>{t("友達が、そこにいる。", "Your friend is right there.")}</span></h1>
    </div>
    <div class="hero-aside">
      <p>{t("通話を始めるほどじゃない。でも、ちょっと話したい。", "Not quite a call. Just a quick word.")}<br>{t("画面の端にカーソルをぶつけると、友達にノックが届きます。応じたら、2人の画面の端に小さな部屋が開きます。", "Bump your cursor against the edge of the screen and a friend gets a knock. When they answer, a small room opens on the edge of both screens.")}</p>
      <a class="try-link" href="#experience">{t("触ってみる", "Give it a try")} <span aria-hidden="true">↓</span></a>
      <p class="note">{t("Mac 用・無料。", "For Mac. Free.")}</p>
    </div>
  </header>

  <section id="experience" class="experience" aria-label="{t("ノックの操作デモ", "Interactive Knock demo")}">
    <div class="desk" id="desk" data-phase="idle">
      <div class="menubar" aria-hidden="true"><span>{t("Finder　ファイル　編集　表示", "Finder　File　Edit　View")}</span><span>10:09</span></div>
      <div class="window" aria-hidden="true"><div class="lights"><i></i><i></i><i></i></div><div class="lines"><b></b><b></b><b class="short"></b><b></b><b class="short"></b></div></div>
      <div class="dial" id="dial" aria-hidden="true"></div>
      <div class="bumps" id="bumps" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="ripple" id="ripple" aria-hidden="true"></div>
      <aside class="room" id="room" aria-live="polite">
        <div class="room-head"><button class="room-close" id="roomClose" aria-label="{demo_text["close"]}">×</button><div><strong id="roomName"></strong><span>{demo_text["connected"]}</span></div><div class="avatar" id="roomAvatar"></div></div>
        <div class="room-floor" id="floor">
          <div class="tiles" id="tiles"></div>
          <div class="bubbles" id="bubbles"></div>
          <div class="cursor them" id="theirCursor"><svg viewBox="0 0 16 22" aria-hidden="true"><path d="M1 1v17l4.5-4.2 3 6.7 3-1.4-3-6.5H15z"/></svg><span id="theirLabel"></span></div>
        </div>
        <div class="room-foot"><div class="replies" id="replies"></div><button class="show" id="showMe">{demo_text["showMe"]}</button></div>
      </aside>
      <div class="edge" id="edge" aria-label="{t("画面の右端", "The right edge of the screen")}" role="button" tabindex="0"></div>
      <div class="lightbox" id="lightbox" hidden><div class="big" id="big"></div><p>{demo_text["back"]}</p></div>
    </div>
    <div class="toolbar">
      <p class="status" id="status" aria-live="polite">{demo_text["idle"]}</p>
      <button class="fallback" id="fallback">{demo_text["tryClick"]}</button>
    </div>
    <p class="disclaimer">{t("ブラウザの中のサンプルです。実際には誰にも届きません。", "A browser sample. Nobody actually receives anything.")}</p>
    <script type="application/json" id="demoText">{json.dumps(demo_text, ensure_ascii=False)}</script>
  </section>

  <section class="about">
    <p class="number">01 / {t("使い方", "HOW IT WORKS")}</p>
    <div>
      <h2>{t("端に止めて、選んで、", "Rest on the edge. Choose.")}<br>{t("3回ぶつける。", "Bump three times.")}</h2>
      <ol class="flow">
        <li><strong>{t("端に止める", "Rest")}</strong><span>{t("画面の右端にカーソルを止めると、友達を選ぶダイヤルが出ます。上下のスクロールで相手を、横のスクロールでグループを選びます。", "Rest your cursor on the right edge and a dial of friends appears. Scroll up and down to choose a person, sideways to choose a group.")}</span></li>
        <li><strong>{t("ノック", "Knock")}</strong><span>{t("端に3回ぶつけると、その人にノックが届きます。相手の画面の端に、「答える」と「ちょっと待って」が出ます。", "Bump the edge three times and they get a knock. Answer and Just a moment appear on the edge of their screen.")}</span></li>
        <li><strong>{t("部屋", "Room")}</strong><span>{t("相手が「答える」を押すと、2人の画面の端に部屋が開きます。", "When they press Answer, a room opens on the edge of both screens.")}</span></li>
      </ol>
    </div>
  </section>

  <section class="about">
    <p class="number">02 / {t("部屋でできること", "IN THE ROOM")}</p>
    <div>
      <h2>{t("話すより軽く、", "Lighter than talking.")}<br>{t("チャットより近く。", "Closer than chat.")}</h2>
      <div class="features">
        <div><h3>{t("相手のカーソル", "Their cursor")}</h3><p>{t("部屋の中では、相手のカーソルが名前つきで動きます。指さすだけで伝わります。", "In the room, their cursor moves with their name on it. Pointing is enough.")}</p></div>
        <div><h3>{t("一言の返事", "Quick replies")}</h3><p>{t("「OK」「待って」「あとで」。打たずに返せます。メッセージも送れます。", "“OK”, “Wait”, “Later” — without typing. Messages too.")}</p></div>
        <div><h3>{t("画面を見せる", "Show your screen")}</h3><p>{t("選んだウィンドウだけを見せて、ピンで場所を指せます。何人かの画面は部屋に並び、クリックで拡大、外へドラッグすると自分のウィンドウになります。", "Show just the window you choose and pin a spot on it. Several screens line up in the room: click to enlarge, drag one out to give it its own window.")}</p></div>
        <div><h3>{t("ファイルを渡す", "Hand over files")}</h3><p>{t("部屋にファイルを落とすと、相手の Mac に届きます。", "Drop a file into the room and it arrives on their Mac.")}</p></div>
        <div><h3>{t("グループ", "Groups")}</h3><p>{t("何人かでひとつの部屋を使えます。ダイヤルを横にスクロールして、グループを選びます。", "Share one room with several friends. Scroll the dial sideways to pick a group.")}</p></div>
        <div><h3>{t("集中する", "Focus")}</h3><p>{t("集中しているあいだ、届いたノックは静かに待ちます。", "While you focus, knocks wait quietly.")}</p></div>
      </div>
    </div>
  </section>

  <section class="about">
    <p class="number">03 / {t("どこを通るか", "PRIVACY")}</p>
    <div>
      <h2>{t("カーソルも画面も、", "Cursors and screens go")}<br>{t("2台の Mac のあいだで。", "between your two Macs.")}</h2>
      <p>{t("カーソル、一言の返事、見せた画面、部屋で渡すファイルは、2台の Mac を直接つないでやりとりします（暗号化されます）。ネットワークの都合で直接つながらないときだけ、サーバーがその場で中継します（保存はしません）。", "Cursors, quick replies, shared screens and files travel over a direct, encrypted connection between the two Macs. Only when a direct connection can’t be made does the server relay them, live, without storing them.")}</p>
      <p class="muted">{t("サーバーを使うのは、サインイン、ノック、メッセージ、直接つなぐための手続きと、相手がオフラインのときの受け渡しです。広告や解析のためのツールは入っていません。", "The server handles sign-in, knocks, messages, setting up the direct connection, and delivery while a friend is offline. There are no ad or analytics tools.")} <a href="{root}privacy.html">{t("プライバシーポリシー", "Privacy policy (Japanese)")}</a></p>
    </div>
  </section>

  <section id="download" class="purchase">
    <div>
      <p class="number">04 / {t("ダウンロード", "DOWNLOAD")}</p>
      <h2>{t("友達と2人で、", "Install it together")}<br>{t("入れてください。", "with a friend.")}</h2>
      <ol class="install">
        <li>{t("Knock.zip を開き、Knock を「アプリケーション」フォルダに入れます。", "Open Knock.zip and move Knock to your Applications folder.")}</li>
        <li>{t("Knock を開き、メールに届く6桁のコードでサインインします。", "Open Knock and sign in with the six-digit code sent to your email.")}</li>
        <li>{t("名前を決めて、招待コードを友達に送ります。友達がコードを入れたら、つながります。", "Choose a name and send your invite code to a friend. Once they enter it, you’re connected.")}</li>
      </ol>
      <p class="muted">{t("友達がまだいなくても、テストユーザーで一通り試せます。", "No friends on Knock yet? Try everything with a test user.")}</p>
    </div>
    <div class="price-box">
      <p class="label">{t("ノック", "Knock")}</p>
      <p class="price">{t("無料", "Free")}</p>
      <p>{t("広告なし。アカウントだけ作れば使えます。", "No ads. Just make an account.")}</p>
      <a class="download" href="{DOWNLOAD}">{t("Mac 版をダウンロード", "Download for Mac")} <span aria-hidden="true">↓</span></a>
      <p class="small">{t("macOS 26 以降 · Apple シリコン / Intel。新しい版はアプリが自動で受け取ります。", "macOS 26 or later · Apple silicon / Intel. Updates arrive automatically.")}</p>
      <p class="small"><a href="{RELEASES}">{t("すべての版", "All versions")}</a></p>
    </div>
  </section>

  <section class="notes">
    <div><h3>{t("画面を見せるには、許可を。", "Showing your screen needs permission.")}</h3><p>{t("初めて画面を見せるとき、macOS の「画面収録」の許可を求めます。見せるのは、あなたが選んだウィンドウだけです。", "The first time you share, macOS asks for Screen Recording permission. Only the window you choose is shown.")}</p></div>
    <div><h3>{t("ノックしすぎない仕組み。", "Built not to over-knock.")}</h3><p>{t("相手が集中中なら、ノックは静かに待ちます。つながっていない相手には届きません。", "If they’re focusing, your knock waits quietly. People you aren’t connected with can’t be knocked.")}</p></div>
    <div><h3>{t("困ったときは。", "Need help?")}</h3><p>{t("アプリの「アカウント」→「お問い合わせ」から送ってください。通報もここからできます。", "Use Account → Contact in the app. You can report problems there too.")}</p></div>
  </section>

  <footer>
    <a class="brand" href="./"><img src="{root}icon.png" width="30" height="30" alt="">{t("ノック", "Knock")}</a>
    <div><a href="{root}privacy.html">{t("プライバシーポリシー", "Privacy")}</a><a href="{root}terms.html">{t("利用規約", "Terms")}</a><span>© 2026 {t("ノック", "Knock")}</span></div>
  </footer>
</main>
<script src="{root}demo.js"></script>
</body>
</html>
"""


(here / "index.html").write_text(page("ja"))
(here / "en").mkdir(exist_ok=True)
(here / "en" / "index.html").write_text(page("en"))
print("built index.html, en/index.html")
