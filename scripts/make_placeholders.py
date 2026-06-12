"""
Generate placeholder brand + property images for New Beginnings DSC.

Run:  python scripts/make_placeholders.py

Outputs (under public/):
  favicon.png, apple-touch-icon.png, og-share.png
  images/properties/<slug>-<n>.jpg

Refined "boutique residence" treatment: emerald + champagne gold + ivory.
Placeholders are refined monogram placards. When real photos arrive,
overwrite the JPGs at the same paths and update data/properties.json.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PROPS_DIR = PUBLIC / "images" / "properties"
PROPS_DIR.mkdir(parents=True, exist_ok=True)

# Palette: emerald + champagne gold + ivory + charcoal.
EMERALD_LIGHT = (20, 86, 63)     # #14563f
EMERALD = (10, 61, 46)            # #0a3d2e
EMERALD_DEEP = (6, 41, 32)        # #062920
GOLD = (201, 169, 110)            # #c9a96e
GOLD_BRIGHT = (224, 195, 137)     # #e0c389
IVORY = (247, 243, 235)           # #f7f3eb
IVORY_MUTED = (210, 204, 188)
INK = (26, 31, 28)                # #1a1f1c

PROPERTIES = [
    ("sunny-cottage", "The Sunny Cottage", ["Living Room", "Kitchen", "Porch"]),
    ("mint-hill-bungalow", "Mint Hill Bungalow", ["Bedroom", "Kitchenette", "Patio"]),
    ("lakeside-loft", "Lakeside Loft", ["Great Room", "Lake View", "Deck"]),
]


def font(size, bold=False, serif=False, italic=False):
    if serif:
        candidates = (
            ["georgiabi.ttf", "georgiab.ttf"] if (bold or italic)
            else ["georgia.ttf", "constantia.ttf"]
        )
    elif bold:
        candidates = ["arialbd.ttf", "segoeuib.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            try:
                return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)
            except OSError:
                continue
    return ImageFont.load_default()


def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def tracked_text(draw, text, x, y, font_obj, fill, spacing=4):
    """Draw text with letter-spacing (Pillow has no native tracking)."""
    chars = list(text)
    widths = [draw.textbbox((0, 0), c, font=font_obj)[2] for c in chars]
    total = sum(widths) + spacing * (len(chars) - 1)
    cx = x - total / 2
    for c, w in zip(chars, widths):
        draw.text((cx, y), c, font=font_obj, fill=fill, anchor="lm")
        cx += w + spacing


def brand_icon(size):
    """Refined house monogram on emerald gradient. Transparent rounded corners."""
    s = size
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    grad = vgrad(s, s, EMERALD_LIGHT, EMERALD_DEEP).convert("RGBA")
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=255)
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    # walls
    d.rounded_rectangle([s * 0.25, s * 0.52, s * 0.75, s * 0.80], radius=int(s * 0.03), fill=IVORY)
    # roof in gold
    d.polygon([(s * 0.18, s * 0.56), (s * 0.50, s * 0.28), (s * 0.82, s * 0.56)], fill=GOLD)
    # door in deep emerald
    d.rounded_rectangle([s * 0.44, s * 0.62, s * 0.56, s * 0.80], radius=int(s * 0.02), fill=EMERALD_DEEP)
    return img


def save_icon(size, name):
    brand_icon(size).save(PUBLIC / name)
    print("  wrote", name)


def make_og():
    w, h = 1200, 630
    img = vgrad(w, h, EMERALD_LIGHT, EMERALD_DEEP)
    d = ImageDraw.Draw(img)
    # double gold border (boutique-hotel placard feel)
    d.rectangle([56, 56, w - 56, h - 56], outline=GOLD, width=2)
    d.rectangle([72, 72, w - 72, h - 72], outline=GOLD, width=1)
    tracked_text(d, "EST. 2026", w / 2, 168, font(24, bold=True), GOLD, spacing=6)
    # NB monogram in serif
    d.text((w / 2, 290), "New Beginnings", font=font(78, serif=True), fill=IVORY, anchor="mm")
    d.text((w / 2, 360), "DSC", font=font(64, serif=True, italic=True), fill=GOLD, anchor="mm")
    # ornate rule
    d.line([(w / 2 - 220, 422), (w / 2 - 20, 422)], fill=GOLD, width=1)
    d.polygon([(w / 2, 415), (w / 2 + 10, 422), (w / 2, 429), (w / 2 - 10, 422)], fill=GOLD)
    d.line([(w / 2 + 20, 422), (w / 2 + 220, 422)], fill=GOLD, width=1)
    tracked_text(d, "BOUTIQUE SHORT-TERM RESIDENCES", w / 2, 462, font(20, bold=True), IVORY, spacing=4)
    tracked_text(d, "MISSOURI", w / 2, 498, font(16, bold=True), GOLD, spacing=6)
    img.save(PUBLIC / "og-share.png")
    print("  wrote og-share.png")


def make_property_tile(path, name, label):
    w, h = 1200, 800
    img = vgrad(w, h, EMERALD_LIGHT, EMERALD_DEEP)
    d = ImageDraw.Draw(img)
    # double gold border
    d.rectangle([60, 60, w - 60, h - 60], outline=GOLD, width=2)
    d.rectangle([76, 76, w - 76, h - 76], outline=GOLD, width=1)
    tracked_text(d, "NEW BEGINNINGS", w / 2, 210, font(20, bold=True), GOLD, spacing=5)
    # name in large serif
    d.text((w / 2, 340), name, font=font(80, serif=True), fill=IVORY, anchor="mm")
    # ornate rule
    d.line([(w / 2 - 240, 412), (w / 2 - 20, 412)], fill=GOLD, width=1)
    d.polygon([(w / 2, 404), (w / 2 + 11, 412), (w / 2, 420), (w / 2 - 11, 412)], fill=GOLD)
    d.line([(w / 2 + 20, 412), (w / 2 + 240, 412)], fill=GOLD, width=1)
    # label
    tracked_text(d, label.upper(), w / 2, 462, font(28, bold=True), GOLD, spacing=6)
    tracked_text(d, "PHOTO TO FOLLOW", w / 2, 600, font(16, bold=True), IVORY_MUTED, spacing=5)
    img.save(path, quality=88)
    print("  wrote", path.relative_to(PUBLIC))


if __name__ == "__main__":
    print("Brand icons:")
    save_icon(64, "favicon.png")
    save_icon(180, "apple-touch-icon.png")
    print("Social card:")
    make_og()
    print("Property tiles:")
    for slug, name, labels in PROPERTIES:
        for i, label in enumerate(labels, start=1):
            make_property_tile(PROPS_DIR / f"{slug}-{i}.jpg", name, label)
    print("Done.")
