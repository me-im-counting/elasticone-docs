"""Generate fluid UI mockup screenshots showing LLM-driven UI evolution."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 600, 500
BG = (24, 24, 34)
PANEL = (32, 32, 48)
ACCENT = (80, 140, 220)
GREEN = (60, 180, 120)
ORANGE = (220, 140, 50)
WHITE = (240, 240, 240)
GRAY = (120, 120, 140)
DARK = (20, 20, 30)

try:
    font = ImageFont.truetype("C:/dev/graphene/assets/liberation_mono.ttf", 13)
    font_sm = ImageFont.truetype("C:/dev/graphene/assets/liberation_mono.ttf", 11)
    font_lg = ImageFont.truetype("C:/dev/graphene/assets/liberation_mono.ttf", 16)
except:
    font = ImageFont.load_default()
    font_sm = font
    font_lg = font


def rounded_rect(draw, xy, fill, r=6):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=r, fill=fill)


def draw_button(draw, x, y, w, h, text, color=ACCENT):
    rounded_rect(draw, (x, y, x+w, y+h), color)
    tw = draw.textlength(text, font=font)
    draw.text((x + (w - tw) / 2, y + (h - 16) / 2), text, fill=WHITE, font=font)


def draw_input(draw, x, y, w, h, text="", placeholder=""):
    rounded_rect(draw, (x, y, x+w, y+h), (40, 40, 56))
    draw.rectangle((x, y, x+w, y+h), outline=(60, 60, 80))
    t = text if text else placeholder
    c = WHITE if text else GRAY
    draw.text((x + 8, y + (h - 14) / 2), t, fill=c, font=font_sm)


def draw_slider(draw, x, y, w, val=0.6):
    draw.rectangle((x, y, x+w, y+4), fill=(50, 50, 70))
    px = x + int(w * val)
    draw.rectangle((x, y, px, y+4), fill=ACCENT)
    draw.ellipse((px-6, y-4, px+6, y+8), fill=ACCENT)


def draw_status_bar(draw, text, y=H-28):
    draw.rectangle((0, y, W, H), fill=(18, 18, 26))
    draw.text((12, y+6), text, fill=GRAY, font=font_sm)


def draw_label(draw, x, y, text, color=WHITE):
    draw.text((x, y), text, fill=color, font=font)


def draw_grid_label(draw, x, y, text, color=GRAY):
    draw.text((x, y), text, fill=color, font=font_sm)


# --- Mockup 1: Empty canvas, LLM starting to build ---
img1 = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img1)
draw_status_bar(d, "graphene_stream | fluid | waiting for input...")
# Terminal-style overlay showing LLM sending commands
rounded_rect(d, (40, 60, 560, 280), (16, 16, 24), r=8)
d.rectangle((40, 60, 560, 82), fill=(32, 32, 44))
d.text((50, 64), "LLM > graphene_send", fill=GRAY, font=font_sm)
lines = [
    ('feed "render_commands [];";', GRAY),
    ('feed "status_text \\"building...\\";";', GRAY),
    ('feed "btn button ( text \\"Hello\\"; x 20; y 100; );";', GREEN),
    ('feed "lbl label ( text \\"Count: 0\\"; x 20; y 160; );";', GREEN),
    ('exec', ACCENT),
    ('', None),
    ('# UI appears on device...', ORANGE),
]
yy = 92
for line, color in lines:
    if color:
        d.text((54, yy), line, fill=color, font=font_sm)
    yy += 20

draw_label(d, 40, 310, "Step 1: LLM sends UI commands via IPC", GRAY)
draw_label(d, 40, 330, "The device window starts empty.", GRAY)
img1.save(os.path.join("C:/dev/e1_assets/site", "mockup_1.png"))


# --- Mockup 2: Basic UI built by LLM ---
img2 = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img2)
draw_status_bar(d, "graphene_stream | fluid | running")

# A simple app built by the LLM
rounded_rect(d, (20, 20, 580, 56), PANEL)
draw_label(d, 30, 28, "Image Analysis", WHITE)
draw_grid_label(d, 430, 32, "connected", GREEN)

# Image placeholder
rounded_rect(d, (20, 70, 290, 280), (40, 40, 56))
d.text((110, 165), "[ image ]", fill=GRAY, font=font)

# Right side: controls
draw_label(d, 310, 75, "Model", GRAY)
draw_input(d, 310, 95, 260, 32, text="midas_v2")

draw_label(d, 310, 140, "Confidence", GRAY)
draw_slider(d, 310, 165, 260, 0.72)
draw_grid_label(d, 540, 155, "0.72", WHITE)

draw_label(d, 310, 190, "Output", GRAY)
draw_input(d, 310, 210, 260, 32, placeholder="depth_map.png")

draw_button(d, 310, 260, 120, 36, "Run")
draw_button(d, 445, 260, 120, 36, "Clear", color=(60, 60, 80))

# Results area
rounded_rect(d, (20, 300, 580, 460), PANEL)
draw_label(d, 30, 308, "Results", GRAY)
d.rectangle((20, 328, 580, 329), fill=(50, 50, 70))
draw_grid_label(d, 30, 340, "depth_min:  0.12", WHITE)
draw_grid_label(d, 30, 358, "depth_max:  0.94", WHITE)
draw_grid_label(d, 30, 376, "inference:  12.3ms", GREEN)
draw_grid_label(d, 30, 394, "resolution: 384x384", WHITE)
draw_grid_label(d, 30, 412, "backend:    directcompute", ACCENT)

img2.save(os.path.join("C:/dev/e1_assets/site", "mockup_2.png"))


# --- Mockup 3: LLM modifies the UI dynamically ---
img3 = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img3)
draw_status_bar(d, "graphene_stream | fluid | adapting...")

# Header with changed title
rounded_rect(d, (20, 20, 580, 56), PANEL)
draw_label(d, 30, 28, "Live Depth Monitor", WHITE)
draw_grid_label(d, 400, 32, "streaming", ORANGE)

# Split view: two image panels
rounded_rect(d, (20, 70, 290, 240), (40, 40, 56))
d.text((115, 148), "[ source ]", fill=GRAY, font=font_sm)
draw_grid_label(d, 30, 78, "Input", ACCENT)

rounded_rect(d, (305, 70, 580, 240), (40, 40, 56))
# Fake depth gradient
for y in range(85, 230):
    v = int((y - 85) / (230 - 85) * 80) + 30
    d.line((315, y, 570, y), fill=(v, v + 20, v + 40))
draw_grid_label(d, 315, 78, "Depth Output", GREEN)

# New: progress bars for live stats
draw_label(d, 20, 258, "FPS", GRAY)
rounded_rect(d, (80, 260, 380, 274), (40, 40, 56))
rounded_rect(d, (80, 260, 300, 274), GREEN)
draw_grid_label(d, 390, 260, "28 fps", WHITE)

draw_label(d, 20, 288, "GPU", GRAY)
rounded_rect(d, (80, 290, 380, 304), (40, 40, 56))
rounded_rect(d, (80, 290, 240, 304), ACCENT)
draw_grid_label(d, 390, 290, "54%", WHITE)

draw_label(d, 20, 318, "MEM", GRAY)
rounded_rect(d, (80, 320, 380, 334), (40, 40, 56))
rounded_rect(d, (80, 320, 200, 334), ORANGE)
draw_grid_label(d, 390, 320, "380 MB", WHITE)

# Bottom: LLM command log showing live adaptation
rounded_rect(d, (20, 360, 580, 465), (16, 16, 24), r=8)
d.rectangle((20, 360, 580, 380), fill=(28, 28, 40))
d.text((30, 363), "LLM adaptation log", fill=GRAY, font=font_sm)
log_lines = [
    ("14:23:01", "added split_view for source + depth", GREEN),
    ("14:23:02", "added progress_bar fps, gpu, mem", GREEN),
    ("14:23:03", "set streaming mode, 30fps target", ACCENT),
    ("14:23:05", "monitoring depth_min drift...", ORANGE),
]
yy = 390
for ts, msg, color in log_lines:
    d.text((30, yy), ts, fill=GRAY, font=font_sm)
    d.text((110, yy), msg, fill=color, font=font_sm)
    yy += 18

img3.save(os.path.join("C:/dev/e1_assets/site", "mockup_3.png"))

print("Generated mockup_1.png, mockup_2.png, mockup_3.png")
