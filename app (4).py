import html
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.caption("A tiny app playground: personalize your name, choose a look, and add moving effects.")

# Controls
st.sidebar.header("Customize your app")
name = st.sidebar.text_input("Your name or message", value="Hello World", max_chars=80)
font_family = st.sidebar.selectbox(
    "Font type",
    ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
)
font_size = st.sidebar.slider("Font size", min_value=20, max_value=100, value=52, step=2)
font_weight = st.sidebar.selectbox("Font style", ["Bold", "Normal", "Italic", "Bold italic"])
background = st.sidebar.selectbox(
    "Background",
    ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"],
)
name_mode = st.sidebar.selectbox("Name display", ["Centered", "Smooth ticker", "Repeated"])
effect = st.sidebar.selectbox(
    "Moving effect",
    ["None", "Rain", "Snow", "Hail", "Wind gusts", "Confetti", "Tornado"],
)
speed = st.sidebar.slider(
    "Animation speed",
    min_value=1,
    max_value=10,
    value=5,
    help="1 = slower motion; 10 = faster motion.",
)
density = st.sidebar.slider("Effect density", min_value=8, max_value=60, value=28, step=4)

# Keep CSS values on an allowlist rather than using arbitrary user input.
font_css = {
    "Arial": "Arial, sans-serif",
    "Courier New": "'Courier New', monospace",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', serif",
    "Verdana": "Verdana, sans-serif",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, sans-serif",
}[font_family]

backgrounds = {
    "Light": ("#f7f8fc", "#172033", "#dfe7f4"),
    "Dark": ("#10131b", "#ffffff", "#252b3a"),
    "Ocean": ("linear-gradient(135deg, #075985, #0e7490, #164e63)", "#ffffff", "#0e7490"),
    "Sunset": ("linear-gradient(135deg, #7c2d12, #db2777, #f59e0b)", "#ffffff", "#be185d"),
    "Forest": ("linear-gradient(135deg, #052e16, #166534, #365314)", "#f0fdf4", "#166534"),
    "Lavender": ("linear-gradient(135deg, #ede9fe, #c4b5fd, #f5d0fe)", "#312e81", "#a78bfa"),
}
bg, text_color, accent = backgrounds[background]

escaped_name = html.escape(name.strip() or "Hello World")
weight = "700" if "Bold" in font_weight else "400"
italic = "italic" if "Italic" in font_weight else "normal"

if name_mode == "Repeated":
    name_markup = '<div class="repeat-grid">' + "".join(
        f'<span class="name-item">{escaped_name}</span>' for _ in range(12)
    ) + "</div>"
elif name_mode == "Smooth ticker":
    # Duplicate the message so the CSS animation loops without a visible jump.
    name_markup = (
        '<div class="ticker-window"><div class="ticker-track">'
        f'<span>{escaped_name}</span><span aria-hidden="true">{escaped_name}</span>'
        "</div></div>"
    )
else:
    name_markup = f'<div class="center-name">{escaped_name}</div>'

symbols = {
    "Rain": ["💧", "💦"],
    "Snow": ["❄️", "❅", "❆"],
    "Hail": ["🧊", "▪"],
    "Wind gusts": ["〰️", "💨", "﹏"],
    "Confetti": ["🎉", "✨", "🎊", "🟡", "🟣", "🟢"],
    "Tornado": ["🌪️", "〰️"],
}
particles = []
if effect != "None":
    for i in range(density):
        symbol = random.choice(symbols[effect])
        left = random.randint(0, 98)
        delay = random.uniform(0, 7)
        duration = random.uniform(2.8, 7.5) * (6 / speed)
        size = random.randint(14, 30) if effect != "Confetti" else random.randint(12, 24)
        drift = random.randint(-90, 90)
        if effect == "Wind gusts":
            animation = "gust"
            duration = random.uniform(2.0, 4.5) * (6 / speed)
        elif effect == "Tornado":
            animation = "twirl"
            duration = random.uniform(2.0, 4.0) * (6 / speed)
        elif effect == "Confetti":
            animation = "confetti-fall"
        else:
            animation = "fall"
        particles.append(
            f'<span class="particle {animation}" '
            f'style="left:{left}%; animation-delay:-{delay:.2f}s; '
            f'animation-duration:{duration:.2f}s; --drift:{drift}px; font-size:{size}px;">'
            f'{symbol}</span>'
        )

effect_markup = "".join(particles)
html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{ font-family: {font_css}; }}
  .stage {{
    position: relative; isolation: isolate; overflow: hidden;
    width: 100%; height: 620px; border-radius: 22px;
    background: {bg}; color: {text_color};
    box-shadow: 0 10px 35px rgba(0,0,0,.15);
  }}
  .soft-glow {{
    position: absolute; inset: 0; z-index: -2; pointer-events: none;
    background: radial-gradient(circle at 50% 45%, {accent}55, transparent 55%);
  }}
  .effect-layer {{ position: absolute; inset: 0; z-index: 1; overflow: hidden; pointer-events: none; }}
  .particle {{
    position: absolute; top: -12%; display: block; opacity: .85;
    user-select: none; will-change: transform;
    text-shadow: 0 2px 5px rgba(0,0,0,.12);
  }}
  .fall {{ animation-name: fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes fall {{
    0% {{ transform: translate3d(0,-10vh,0) rotate(0deg); }}
    100% {{ transform: translate3d(var(--drift), 125vh,0) rotate(360deg); }}
  }}
  .confetti-fall {{ animation-name: confetti-fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes confetti-fall {{
    0% {{ transform: translate3d(0,-10vh,0) rotate(0deg); }}
    100% {{ transform: translate3d(var(--drift), 125vh,0) rotate(900deg); }}
  }}
  .gust {{ top: auto; left: -15%; animation-name: gust; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }}
  @keyframes gust {{
    0% {{ transform: translateX(-20vw) translateY(0) rotate(0deg); opacity: 0; }}
    15% {{ opacity: .9; }}
    50% {{ transform: translateX(65vw) translateY(-35px) rotate(12deg); }}
    100% {{ transform: translateX(125vw) translateY(20px) rotate(-10deg); opacity: 0; }}
  }}
  .twirl {{ animation-name: twirl; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes twirl {{
    0% {{ transform: translate3d(0,-10vh,0) rotate(0deg) scale(.7); }}
    50% {{ transform: translate3d(calc(var(--drift) * -1), 55vh,0) rotate(360deg) scale(1.35); }}
    100% {{ transform: translate3d(var(--drift), 125vh,0) rotate(720deg) scale(.7); }}
  }}
  .name-layer {{
    position: absolute; z-index: 2; inset: 0; display: flex;
    align-items: center; justify-content: center; padding: 30px;
    font-size: {font_size}px; font-weight: {weight}; font-style: {italic};
    text-align: center; overflow: hidden; overflow-wrap: anywhere;
    text-shadow: 0 3px 14px rgba(0,0,0,.15);
  }}
  .center-name {{ max-width: 100%; }}
  .ticker-window {{ width: 100%; overflow: hidden; white-space: nowrap; }}
  .ticker-track {{ display: flex; width: max-content; animation: ticker {max(5, 32 - speed * 2)}s linear infinite; }}
  .ticker-track span {{ flex: 0 0 auto; padding-right: 1.5em; }}
  @keyframes ticker {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
  .repeat-grid {{ width: 100%; display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 22px; }}
  .name-item {{ overflow-wrap: anywhere; }}
  .hint {{ position: absolute; z-index: 3; bottom: 15px; left: 0; right: 0; text-align: center; font-size: 13px; opacity: .72; }}
  @media (max-width: 600px) {{
    .stage {{ height: 520px; border-radius: 14px; }}
    .name-layer {{ padding: 18px; }}
    .repeat-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); gap: 14px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, .ticker-track {{ animation-duration: 30s !important; }}
  }}
</style>
</head>
<body>
  <main class="stage" aria-label="Animated name display">
    <div class="soft-glow"></div>
    <div class="effect-layer" aria-hidden="true">{effect_markup}</div>
    <div class="name-layer">{name_markup}</div>
    <div class="hint">HELLO WORLD MOTION LAB · Try changing the controls</div>
  </main>
</body>
</html>"""

components.html(html_doc, height=635, scrolling=False)
st.caption("Tip: the animation runs inside the preview, so it loops smoothly without repeatedly refreshing the whole Streamlit page.")
