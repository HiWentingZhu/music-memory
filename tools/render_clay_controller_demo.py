from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(r"C:\Users\zhuwt\OneDrive\000 - Side Projects\01 - Music")
OUT = ROOT / "output" / "control-clay-reference-style-v7.png"
FONT_DIR = ROOT / "fonts"
WIN_FONT_DIR = Path(r"C:\Windows\Fonts")


def load_font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except Exception:
        return ImageFont.load_default()


F = {
    "title": load_font(FONT_DIR / "oxanium-700.ttf", 34),
    "note": load_font(FONT_DIR / "rajdhani-600.ttf", 18),
    "year": load_font(FONT_DIR / "oxanium-700.ttf", 21),
    "label": load_font(FONT_DIR / "oxanium-700.ttf", 18),
    "list": load_font(FONT_DIR / "space-grotesk-600.ttf", 18),
    "small": load_font(FONT_DIR / "space-grotesk-600.ttf", 15),
    "song_en": load_font(FONT_DIR / "oxanium-700.ttf", 27),
    "song_small": load_font(FONT_DIR / "oxanium-700.ttf", 23),
    "cn": load_font(WIN_FONT_DIR / "msyhbd.ttc", 24),
    "cn_small": load_font(WIN_FONT_DIR / "msyhbd.ttc", 18),
    "lyric": load_font(FONT_DIR / "space-grotesk-600.ttf", 17),
    "time": load_font(FONT_DIR / "oxanium-700.ttf", 18),
    "mode": load_font(FONT_DIR / "oxanium-700.ttf", 16),
    "name_cn": load_font(WIN_FONT_DIR / "msyhbd.ttc", 22),
    "name_en": load_font(FONT_DIR / "oxanium-700.ttf", 16),
}


def u(text):
    return text.encode("ascii").decode("unicode_escape")


def rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def light(c, t):
    return mix(c, (255, 255, 255), t)


def dark(c, t):
    return mix(c, (0, 0, 0), t)


def rgba(c, a=255):
    return (c[0], c[1], c[2], a)


def clamp(v):
    return max(0, min(255, int(v)))


def shadow(size, box, radius, blur=18, offset=(0, 10), opacity=90):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(
        (
            box[0] + offset[0],
            box[1] + offset[1],
            box[2] + offset[0],
            box[3] + offset[1],
        ),
        radius=radius,
        fill=(0, 0, 0, opacity),
    )
    return layer.filter(ImageFilter.GaussianBlur(blur))


def rounded_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=rgba(fill) if len(fill) == 3 else fill,
        outline=rgba(outline) if outline and len(outline) == 3 else outline,
        width=width,
    )


def clay_panel(image, box, radius, fill, shadow_scale=1.0):
    image.alpha_composite(
        shadow(
            image.size,
            box,
            radius,
            int(15 * shadow_scale),
            (0, int(9 * shadow_scale)),
            int(75 * shadow_scale),
        )
    )
    draw = ImageDraw.Draw(image)
    rounded_rect(draw, box, radius, fill, dark(fill, 0.24), 2)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(
        (x1 + 4, y1 + 4, x2 - 4, y2 - 4),
        radius=max(1, radius - 4),
        outline=rgba(light(fill, 0.42), 145),
        width=2,
    )
    draw.line((x1 + radius, y1 + 8, x2 - radius, y1 + 8), fill=rgba(light(fill, 0.58), 140), width=2)
    draw.line((x1 + radius, y2 - 7, x2 - radius, y2 - 7), fill=rgba(dark(fill, 0.28), 92), width=2)


def inset_panel(image, box, radius, fill):
    draw = ImageDraw.Draw(image)
    x1, y1, x2, y2 = box
    rounded_rect(draw, box, radius, dark(fill, 0.04), dark(fill, 0.35), 2)
    draw.rounded_rectangle(
        (x1 + 4, y1 + 4, x2 - 4, y2 - 4),
        radius=max(1, radius - 4),
        outline=rgba(dark(fill, 0.18), 90),
        width=2,
    )
    draw.line((x1 + radius, y1 + 6, x2 - radius, y1 + 6), fill=rgba(light(fill, 0.45), 140), width=2)


YEARS = [
    {
        "year": "2022",
        "theme": "Rain Archive Amber",
        "base": "#d8b98e",
        "panel": "#f2dfbd",
        "center": "#3a281b",
        "accent": "#d9962e",
        "text": "#f6dfad",
        "muted": "#33788a",
        "cn": u("\\u6768\\u5b97\\u7eac"),
        "en": "Aska Yang",
        "image": "singer-image-demo-2022-aska-yang.png",
        "song": u("\\u65c5\\u884c\\u4e2d\\u5fd8\\u8bb0"),
        "artist": u("\\u8881\\u5a05\\u7ef4 TIA RAY"),
        "list": ["Rain Replay", "Ticket Stub", "Archive Boss", "Loop Ring"],
        "lyrics": [
            u("\\u6211\\u60f3\\u8981 (Live)"),
            u("\\u8bf4\\u7ed9\\u4f60\\u542c"),
            u("\\u60f3\\u5bf9\\u4f60\\u8bf4"),
            u("\\u521d\\u8877"),
            u("\\u90a3\\u4e2a\\u7537\\u4eba"),
        ],
    },
    {
        "year": "2023",
        "theme": "Encore Stage Navy",
        "base": "#121b2c",
        "panel": "#1e283d",
        "center": "#111622",
        "accent": "#f05b3f",
        "text": "#ffd79a",
        "muted": "#f29b45",
        "cn": u("\\u6768\\u5b97\\u7eac"),
        "en": "Aska Yang",
        "image": "singer-image-demo-2023-aska-yang.png",
        "song": "MASCARA",
        "artist": "XG",
        "list": ["Encore Memory", "Mic Cable Mood", "Duet Drama", "Stage Light"],
        "lyrics": [
            u("\\u5343\\u91d1\\u6563\\u5c3d"),
            u("\\u5927\\u96e8 (Live)"),
            u("\\u5fc3\\u5b89\\u7684\\u9b54\\u50cf"),
            u("\\u5bf9\\u7684\\u4eba"),
            u("\\u5e73\\u51e1\\u7684\\u6211"),
        ],
    },
    {
        "year": "2024",
        "theme": "Quiet Sage Cream",
        "base": "#ddd6c7",
        "panel": "#f6efdf",
        "center": "#e8ecdc",
        "accent": "#bda36a",
        "text": "#263e35",
        "muted": "#7e9888",
        "cn": u("\\u6613\\u70ca\\u5343\\u73ba"),
        "en": "Jackson Yee",
        "image": "singer-image-demo-2024-jackson-yee.png",
        "song": u("\\u4e00\\u591c"),
        "artist": u("\\u9648\\u695a\\u751f"),
        "list": ["Soft Album Panel", "Folded Note", "Making Peace", "Quiet Room"],
        "lyrics": [
            u("\\u5979\\u9a91\\u5728\\u5348\\u591c\\u524d"),
            u("\\u610f\\u6e21"),
            u("\\u4f60\\u597d\\uff0c\\u6211\\u662f___"),
            u("\\u4e94\\u5149\\u5341\\u8272"),
            u("\\u4e5d\\u91cc\\u5e84\\u4eba\\u624d\\u4e2d\\u5fc3"),
        ],
    },
    {
        "year": "2025",
        "theme": "Neon Kinetic Club",
        "base": "#0e111a",
        "panel": "#202432",
        "center": "#181b28",
        "accent": "#ff3f9d",
        "text": "#f8f0fb",
        "muted": "#00d9f2",
        "cn": u("\\u67e5\\u8389 XCX"),
        "en": "Charli xcx",
        "image": "singer-image-demo-2025-charli.png",
        "song": "Everything Is Romantic",
        "artist": "Charli xcx",
        "list": ["Neon Feelings", "Bass Feelings", "Glow Up", "Kinetic Crisis"],
        "lyrics": ["Rewind", "Everything is romantic", "Talk talk", "Sympathy is a knife", "Von dutch"],
    },
    {
        "year": "2026",
        "theme": "Open Horizon Teal",
        "base": "#ead9b7",
        "panel": "#fff0cf",
        "center": "#e8f3e8",
        "accent": "#e2b94f",
        "text": "#1f6f70",
        "muted": "#49a5a3",
        "cn": u("\\u5f90\\u4f73\\u83b9"),
        "en": "Lala Hsu",
        "image": "singer-image-demo-2026-lala-hsu.png",
        "song": u("\\u4fee\\u70bc\\u7231\\u60c5 (Live)"),
        "artist": u("\\u5f90\\u4f73\\u83b9"),
        "list": ["Open Horizon", "Free Replay", "Wind Path", "Galaxy Repeat"],
        "lyrics": [
            u("\\u4fee\\u70bc\\u7231\\u60c5 (Live)"),
            u("\\u8389\\u8389\\u5b89 (Live)"),
            u("\\u6d6a\\u8d39 (Live)"),
            u("\\u76f8\\u7231\\u540e\\u52a8\\u7269\\u611f\\u4f24"),
            u("\\u5495\\u53fd\\u5495\\u53fd (Live)"),
        ],
    },
]


def draw_ecg(draw, x, y, width, color):
    points = [
        (x, y),
        (x + 70, y),
        (x + 78, y - 7),
        (x + 88, y + 17),
        (x + 99, y - 21),
        (x + 111, y + 8),
        (x + 195, y + 8),
        (x + 210, y),
        (x + 220, y + 5),
        (x + 235, y - 4),
        (x + 315, y - 4),
        (x + 330, y + 10),
        (x + 343, y - 12),
        (x + 356, y),
        (x + width, y),
    ]
    draw.line(points, fill=rgba(color), width=4, joint="curve")


def draw_triangle(draw, cx, cy, size, color, direction="right"):
    if direction == "right":
        points = [(cx - size * 0.35, cy - size * 0.55), (cx - size * 0.35, cy + size * 0.55), (cx + size * 0.45, cy)]
    else:
        points = [(cx + size * 0.35, cy - size * 0.55), (cx + size * 0.35, cy + size * 0.55), (cx - size * 0.45, cy)]
    draw.polygon(points, fill=rgba(color))


def draw_button(draw, cx, cy, radius, fill, text, kind):
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=rgba(fill), outline=rgba(dark(fill, 0.4)), width=2)
    draw.arc((cx - radius + 4, cy - radius + 4, cx + radius - 4, cy + radius - 4), 210, 330, fill=rgba(light(fill, 0.58)), width=2)
    icon = dark(text, 0.12)
    if kind == "play":
        draw_triangle(draw, cx + 2, cy, radius * 1.1, icon, "right")
    elif kind == "prev":
        draw_triangle(draw, cx - 3, cy, radius * 0.86, icon, "left")
        draw.line((cx + 8, cy - radius * 0.42, cx + 8, cy + radius * 0.42), fill=rgba(icon), width=3)
    elif kind == "next":
        draw_triangle(draw, cx + 3, cy, radius * 0.86, icon, "right")
        draw.line((cx - 8, cy - radius * 0.42, cx - 8, cy + radius * 0.42), fill=rgba(icon), width=3)


def main():
    width, row_h, gap, top = 1700, 320, 50, 145
    height = top + len(YEARS) * row_h + (len(YEARS) - 1) * gap + 70
    image = Image.new("RGBA", (width, height), (242, 232, 216, 255))

    pixels = image.load()
    random.seed(14)
    for y in range(height):
        for x in range(width):
            if random.random() < 0.0025:
                r, g, b, a = pixels[x, y]
                delta = random.choice([-8, -5, 6, 8])
                pixels[x, y] = (clamp(r + delta), clamp(g + delta), clamp(b + delta), a)

    draw = ImageDraw.Draw(image)
    draw.text((58, 34), "Clay / Soft-Look Controller Style", fill="#3f3126", font=F["title"])
    draw.text((58, 78), "Demo only. Same structure for every year; colors shift by the approved yearly palettes.", fill="#7b6856", font=F["note"])

    for index, item in enumerate(YEARS):
        y = top + index * (row_h + gap)
        base = rgb(item["base"])
        panel = rgb(item["panel"])
        center = rgb(item["center"])
        accent = rgb(item["accent"])
        text = rgb(item["text"])
        muted = rgb(item["muted"])
        dark_theme = sum(base) < 170

        draw.text((64, y - 32), f"{item['year']} / {item['theme']}", fill="#756454", font=F["year"])
        shell = (58, y, 1642, y + row_h)
        clay_panel(image, shell, 38, base, 1.05)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((76, y + 14, 1624, y + row_h - 14), radius=29, outline=rgba(light(base, 0.45), 170), width=2)

        list_box = (90, y + 46, 430, y + row_h - 46)
        portrait_box = (460, y + 38, 640, y + row_h - 38)
        center_box = (675, y + 42, 1235, y + row_h - 42)
        lyric_box = (1268, y + 46, 1605, y + row_h - 46)

        inset_panel(image, list_box, 24, panel)
        clay_panel(image, portrait_box, 21, panel, 0.78)
        clay_panel(image, center_box, 24, center, 0.9)
        inset_panel(image, lyric_box, 24, panel)
        draw = ImageDraw.Draw(image)

        title_color = dark(panel, 0.65) if not dark_theme else light(panel, 0.68)
        draw.text((list_box[0] + 64, list_box[1] + 23), "YEAR MUSIC LIST", fill=rgba(title_color), font=F["label"])
        draw.line((list_box[0] + 28, list_box[1] + 36, list_box[0] + 52, list_box[1] + 36), fill=rgba(accent), width=2)
        draw.line((list_box[2] - 52, list_box[1] + 36, list_box[2] - 28, list_box[1] + 36), fill=rgba(accent), width=2)

        for list_index, name in enumerate(item["list"]):
            row_y = list_box[1] + 76 + list_index * 47
            active = list_index == 0
            fill = muted if active else light(panel, 0.05)
            rounded_rect(draw, (list_box[0] + 24, row_y, list_box[2] - 24, row_y + 33), 16, fill, dark(fill, 0.34), 1)
            draw.ellipse((list_box[0] + 35, row_y + 5, list_box[0] + 60, row_y + 30), fill=rgba(light(fill, 0.23)), outline=rgba(dark(fill, 0.25)))
            draw.text((list_box[0] + 43, row_y + 6), str(list_index + 1), fill=rgba(text if active and dark_theme else dark(text, 0.15)), font=F["small"])
            row_text = (255, 244, 216) if active and dark_theme else (dark(text, 0.08) if not dark_theme else light(text, 0.05))
            draw.text((list_box[0] + 76, row_y + 6), name, fill=rgba(row_text), font=F["list"])
            if active:
                bar_x = list_box[2] - 58
                for bar, bar_h in enumerate([9, 17, 23]):
                    draw.rectangle((bar_x + bar * 7, row_y + 28 - bar_h, bar_x + bar * 7 + 4, row_y + 28), fill=rgba(light(accent, 0.2)))

        try:
            portrait = Image.open(ROOT / "output" / item["image"]).convert("RGB").resize(
                (portrait_box[2] - portrait_box[0] - 12, portrait_box[3] - portrait_box[1] - 12),
                Image.Resampling.LANCZOS,
            )
            mask = Image.new("L", portrait.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle((0, 0, portrait.size[0], portrait.size[1]), radius=17, fill=255)
            image.paste(portrait, (portrait_box[0] + 6, portrait_box[1] + 6), mask)
        except Exception:
            pass

        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((portrait_box[0] + 13, portrait_box[3] - 66, portrait_box[2] - 13, portrait_box[3] - 12), radius=14, fill=rgba(dark(muted, 0.22), 215))
        draw.text((portrait_box[0] + 28, portrait_box[3] - 62), item["cn"], fill="#fff4d8", font=F["name_cn"])
        draw.text((portrait_box[0] + 29, portrait_box[3] - 32), item["en"], fill="#fff4d8", font=F["name_en"])

        cx1, cy1, cx2, cy2 = center_box
        draw_ecg(draw, cx1 + 44, cy1 + 38, cx2 - cx1 - 88, muted if not dark_theme else accent)
        song_line = f"{item['song']} - {item['artist']}"
        song_font = F["cn"] if any(ord(ch) > 127 for ch in song_line) else (F["song_small"] if len(song_line) > 33 else F["song_en"])
        draw.text((cx1 + 44, cy1 + 96), song_line, fill=rgba(text), font=song_font)

        control_y = cy1 + 165
        pill = (cx1 + 44, control_y - 19, cx1 + 205, control_y + 19)
        clay_panel(image, pill, 19, light(base, 0.2) if not dark_theme else light(center, 0.12), 0.32)
        draw = ImageDraw.Draw(image)
        draw.text((pill[0] + 18, pill[1] + 8), "LIST LOOP", fill=rgba(text if dark_theme else dark(text, 0.12)), font=F["mode"])
        draw.arc((pill[2] - 45, pill[1] + 10, pill[2] - 20, pill[1] + 31), 40, 300, fill=rgba(muted), width=3)
        draw.arc((pill[2] - 40, pill[1] + 8, pill[2] - 15, pill[1] + 29), 220, 120, fill=rgba(muted), width=3)
        draw_button(draw, cx1 + 245, control_y, 23, light(base, 0.2), text, "prev")
        draw_button(draw, cx1 + 302, control_y, 31, muted, text, "play")
        draw_button(draw, cx1 + 360, control_y, 23, light(base, 0.2), text, "next")
        draw.text((cx1 + 404, control_y - 10), "VOL", fill=rgba(text), font=F["mode"])
        draw.rounded_rectangle((cx1 + 458, control_y - 8, cx1 + 575, control_y + 9), radius=9, fill=rgba(dark(center, 0.38)), outline=rgba(accent), width=2)
        draw.rounded_rectangle((cx1 + 463, control_y - 4, cx1 + 529, control_y + 5), radius=5, fill=rgba(muted))
        draw.ellipse((cx1 + 520, control_y - 14, cx1 + 544, control_y + 14), fill=rgba(light(panel, 0.08)), outline=rgba(dark(panel, 0.42)))

        progress_y = cy1 + 225
        draw.text((cx1 + 44, progress_y - 11), "1:26", fill=rgba(text), font=F["time"])
        draw.rounded_rectangle((cx1 + 124, progress_y - 8, cx2 - 130, progress_y + 9), radius=9, fill=rgba(dark(center, 0.42)), outline=rgba(dark(center, 0.63)), width=2)
        draw.rounded_rectangle((cx1 + 124, progress_y - 8, cx1 + 330, progress_y + 9), radius=9, fill=rgba(muted))
        draw.ellipse((cx1 + 306, progress_y - 20, cx1 + 338, progress_y + 20), fill=rgba(light(panel, 0.08)), outline=rgba(dark(panel, 0.42)))
        draw.text((cx2 - 110, progress_y - 11), "4:46", fill=rgba(text), font=F["time"])

        for lyric_index, lyric in enumerate(item["lyrics"][:5]):
            lyric_y = lyric_box[1] + 34 + lyric_index * 43
            if lyric_index == 0:
                rounded_rect(draw, (lyric_box[0] + 22, lyric_y - 8, lyric_box[2] - 22, lyric_y + 27), 16, muted, dark(muted, 0.35), 1)
                line_color = text if dark_theme else dark(text, 0.08)
            else:
                line_color = dark(text, 0.05) if not dark_theme else light(text, 0.1)
            draw.ellipse((lyric_box[0] + 33, lyric_y + 2, lyric_box[0] + 48, lyric_y + 17), fill=rgba(light(panel, 0.05)), outline=rgba(dark(panel, 0.25)))
            lyric_font = F["cn_small"] if any(ord(ch) > 127 for ch in lyric) else F["lyric"]
            draw.text((lyric_box[0] + 64, lyric_y - 3), lyric, fill=rgba(line_color), font=lyric_font)
            if lyric_index > 0:
                draw.line((lyric_box[0] + 60, lyric_y + 31, lyric_box[2] - 36, lyric_y + 31), fill=rgba(dark(panel, 0.18)), width=1)
        draw.arc((lyric_box[0] + 28, lyric_box[3] - 42, lyric_box[0] + 52, lyric_box[3] - 18), 25, 325, fill=rgba(accent), width=3)
        draw.text((lyric_box[0] + 64, lyric_box[3] - 41), "Auto-scrolls / syncs with song", fill=rgba(title_color), font=F["small"])

    image.convert("RGB").save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
