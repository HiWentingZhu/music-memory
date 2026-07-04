from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(r"C:\Users\zhuwt\OneDrive\000 - Side Projects\01 - Music")
OUT = ROOT / "output" / "control-clay-2026-focus-v1.png"
FONT_DIR = ROOT / "fonts"
WIN_FONT_DIR = Path(r"C:\Windows\Fonts")


def font(path, size):
    try:
        return ImageFont.truetype(str(path), size)
    except Exception:
        return ImageFont.load_default()


F = {
    "label": font(FONT_DIR / "oxanium-700.ttf", 28),
    "list": font(FONT_DIR / "space-grotesk-700.ttf", 28),
    "list_num": font(FONT_DIR / "oxanium-700.ttf", 25),
    "song": font(WIN_FONT_DIR / "msyhbd.ttc", 42),
    "song_en": font(FONT_DIR / "oxanium-700.ttf", 38),
    "mode": font(FONT_DIR / "oxanium-700.ttf", 25),
    "time": font(FONT_DIR / "oxanium-700.ttf", 28),
    "lyric": font(WIN_FONT_DIR / "msyhbd.ttc", 29),
    "lyric_en": font(FONT_DIR / "space-grotesk-700.ttf", 28),
    "name_cn": font(WIN_FONT_DIR / "msyhbd.ttc", 37),
    "name_en": font(FONT_DIR / "oxanium-700.ttf", 28),
}


def u(text):
    return text.encode("ascii").decode("unicode_escape")


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


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


def soft_shadow(size, box, radius, blur=22, offset=(0, 14), opacity=90):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle(
        (box[0] + offset[0], box[1] + offset[1], box[2] + offset[0], box[3] + offset[1]),
        radius=radius,
        fill=(41, 27, 13, opacity),
    )
    return layer.filter(ImageFilter.GaussianBlur(blur))


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(
        box,
        radius=radius,
        fill=rgba(fill) if len(fill) == 3 else fill,
        outline=rgba(outline) if outline and len(outline) == 3 else outline,
        width=width,
    )


def clay(image, box, radius, fill, shadow=1.0):
    image.alpha_composite(soft_shadow(image.size, box, radius, int(24 * shadow), (0, int(16 * shadow)), int(85 * shadow)))
    draw = ImageDraw.Draw(image)
    rounded(draw, box, radius, fill, dark(fill, 0.18), 2)
    x1, y1, x2, y2 = box

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle((x1 + 4, y1 + 4, x2 - 4, y2 - 4), radius=radius - 4, outline=rgba(light(fill, 0.46), 165), width=3)
    od.line((x1 + radius, y1 + 10, x2 - radius, y1 + 10), fill=rgba(light(fill, 0.62), 130), width=3)
    od.line((x1 + radius, y2 - 9, x2 - radius, y2 - 9), fill=rgba(dark(fill, 0.22), 90), width=3)
    image.alpha_composite(overlay)


def inset(image, box, radius, fill):
    draw = ImageDraw.Draw(image)
    rounded(draw, box, radius, light(fill, 0.02), dark(fill, 0.22), 2)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 5, y1 + 5, x2 - 5, y2 - 5), radius=radius - 5, outline=rgba(dark(fill, 0.12), 120), width=2)
    draw.line((x1 + radius, y1 + 8, x2 - radius, y1 + 8), fill=rgba(light(fill, 0.4), 155), width=2)


def draw_text_shadow(draw, xy, text, font_obj, fill, shadow_fill=(53, 37, 23), offset=(3, 4)):
    draw.text((xy[0] + offset[0], xy[1] + offset[1]), text, font=font_obj, fill=rgba(shadow_fill, 120))
    draw.text(xy, text, font=font_obj, fill=rgba(fill))


def ecg(draw, x, y, width, color):
    points = [
        (x, y),
        (x + 70, y),
        (x + 82, y - 8),
        (x + 95, y + 20),
        (x + 110, y - 27),
        (x + 127, y + 8),
        (x + 245, y + 8),
        (x + 258, y),
        (x + 270, y + 5),
        (x + 286, y - 5),
        (x + 425, y - 5),
        (x + 438, y + 13),
        (x + 454, y - 16),
        (x + 471, y),
        (x + width, y),
    ]
    draw.line(points, fill=rgba(color), width=6, joint="curve")


def triangle(draw, cx, cy, size, color, direction="right"):
    if direction == "right":
        points = [(cx - size * 0.36, cy - size * 0.55), (cx - size * 0.36, cy + size * 0.55), (cx + size * 0.46, cy)]
    else:
        points = [(cx + size * 0.36, cy - size * 0.55), (cx + size * 0.36, cy + size * 0.55), (cx - size * 0.46, cy)]
    draw.polygon(points, fill=rgba(color))


def round_button(image, cx, cy, radius, fill, text_color, kind):
    draw = ImageDraw.Draw(image)
    image.alpha_composite(soft_shadow(image.size, (cx - radius, cy - radius, cx + radius, cy + radius), radius, 14, (0, 8), 55))
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=rgba(fill), outline=rgba(dark(fill, 0.3)), width=2)
    draw.arc((cx - radius + 6, cy - radius + 6, cx + radius - 6, cy + radius - 6), 210, 330, fill=rgba(light(fill, 0.5)), width=3)
    icon = dark(text_color, 0.12)
    if kind == "play":
        triangle(draw, cx + 3, cy, radius * 1.06, icon, "right")
    elif kind == "prev":
        triangle(draw, cx - 4, cy, radius * 0.88, icon, "left")
        draw.line((cx + 9, cy - radius * 0.42, cx + 9, cy + radius * 0.42), fill=rgba(icon), width=4)
    elif kind == "next":
        triangle(draw, cx + 4, cy, radius * 0.88, icon, "right")
        draw.line((cx - 9, cy - radius * 0.42, cx - 9, cy + radius * 0.42), fill=rgba(icon), width=4)


def add_paper_texture(image, strength=0.004):
    pixels = image.load()
    random.seed(26)
    width, height = image.size
    for y in range(height):
        for x in range(width):
            if random.random() < strength:
                r, g, b, a = pixels[x, y]
                delta = random.choice([-9, -6, 5, 7])
                pixels[x, y] = (clamp(r + delta), clamp(g + delta), clamp(b + delta), a)


def main():
    base = hex_to_rgb("#ead9b7")
    cream = hex_to_rgb("#fff0cf")
    teal = hex_to_rgb("#49a5a3")
    deep_teal = hex_to_rgb("#1f6f70")
    gold = hex_to_rgb("#e2b94f")
    wood = hex_to_rgb("#6b5540")
    center = hex_to_rgb("#5f4a37")
    text = hex_to_rgb("#fff3d2")

    width, height = 1880, 970
    image = Image.new("RGBA", (width, height), (245, 233, 214, 255))
    add_paper_texture(image)

    draw = ImageDraw.Draw(image)
    # warm vignette
    vignette = Image.new("L", (width, height), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-280, -330, width + 280, height + 560), fill=180)
    vignette = ImageOps.invert(vignette.filter(ImageFilter.GaussianBlur(130)))
    shade = Image.new("RGBA", (width, height), (92, 56, 18, 42))
    image.alpha_composite(Image.composite(shade, Image.new("RGBA", (width, height), (0, 0, 0, 0)), vignette))

    shell = (55, 175, 1825, 730)
    clay(image, shell, 54, base, 1.25)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((86, 208, 1794, 698), radius=42, outline=rgba(light(base, 0.48), 170), width=3)

    list_box = (88, 210, 440, 695)
    portrait_box = (464, 210, 680, 695)
    center_box = (704, 210, 1386, 695)
    lyric_box = (1412, 210, 1792, 695)

    inset(image, list_box, 32, cream)
    clay(image, portrait_box, 30, light(base, 0.08), 0.7)
    clay(image, center_box, 31, center, 1.0)
    inset(image, lyric_box, 32, cream)
    draw = ImageDraw.Draw(image)

    # Music list.
    draw.line((list_box[0] + 36, list_box[1] + 66, list_box[0] + 62, list_box[1] + 66), fill=rgba(gold), width=3)
    draw.line((list_box[2] - 62, list_box[1] + 66, list_box[2] - 36, list_box[1] + 66), fill=rgba(gold), width=3)
    draw.text((list_box[0] + 75, list_box[1] + 47), "YEAR MUSIC LIST", font=F["label"], fill=rgba(dark(wood, 0.1)))

    songs = ["Open Horizon", "Free Replay", "Wind Path", "Galaxy Repeat"]
    for index, song in enumerate(songs):
        y = list_box[1] + 116 + index * 78
        active = index == 0
        row_fill = teal if active else light(base, 0.17)
        clay(image, (list_box[0] + 28, y, list_box[2] - 28, y + 55), 24, row_fill, 0.35)
        draw = ImageDraw.Draw(image)
        draw.ellipse((list_box[0] + 48, y + 11, list_box[0] + 82, y + 45), fill=rgba(light(row_fill, 0.22)), outline=rgba(dark(row_fill, 0.28)), width=2)
        draw.text((list_box[0] + 58, y + 14), str(index + 1), font=F["list_num"], fill=rgba(dark(deep_teal, 0.05) if active else dark(wood, 0.02)))
        draw.text((list_box[0] + 100, y + 12), song, font=F["list"], fill=rgba(text if active else dark(wood, 0.05)))
        if active:
            bx = list_box[2] - 72
            for bar, bar_h in enumerate([13, 22, 31]):
                draw.rounded_rectangle((bx + bar * 10, y + 43 - bar_h, bx + bar * 10 + 6, y + 43), radius=3, fill=rgba(light(gold, 0.15)))

    # Singer image card.
    portrait_path = ROOT / "output" / "singer-image-demo-2026-lala-hsu.png"
    portrait = Image.open(portrait_path).convert("RGB").resize((portrait_box[2] - portrait_box[0] - 12, portrait_box[3] - portrait_box[1] - 12), Image.Resampling.LANCZOS)
    warm = Image.new("RGB", portrait.size, (255, 224, 178))
    portrait = Image.blend(portrait, warm, 0.16)
    mask = Image.new("L", portrait.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, portrait.size[0], portrait.size[1]), radius=24, fill=255)
    image.paste(portrait, (portrait_box[0] + 6, portrait_box[1] + 6), mask)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((portrait_box[0] + 12, portrait_box[3] - 96, portrait_box[2] - 12, portrait_box[3] - 14), radius=22, fill=rgba(dark(teal, 0.18), 220))
    draw_text_shadow(draw, (portrait_box[0] + 50, portrait_box[3] - 91), u("\\u5f90\\u4f73\\u83b9"), F["name_cn"], text)
    draw.text((portrait_box[0] + 51, portrait_box[3] - 45), "Lala Hsu", font=F["name_en"], fill=rgba(text))

    # Center display.
    cx1, cy1, cx2, cy2 = center_box
    ecg(draw, cx1 + 55, cy1 + 78, cx2 - cx1 - 110, teal)
    draw_text_shadow(draw, (cx1 + 80, cy1 + 150), u("\\u4fee\\u70bc\\u7231\\u60c5 (Live) - \\u5f90\\u4f73\\u83b9"), F["song"], text)

    control_y = cy1 + 285
    pill = (cx1 + 60, control_y - 35, cx1 + 235, control_y + 35)
    clay(image, pill, 32, light(cream, 0.03), 0.55)
    draw = ImageDraw.Draw(image)
    draw.text((pill[0] + 23, pill[1] + 20), "LIST LOOP", font=F["mode"], fill=rgba(dark(wood, 0.03)))
    draw.arc((pill[2] - 52, pill[1] + 21, pill[2] - 18, pill[1] + 52), 35, 305, fill=rgba(teal), width=4)
    draw.arc((pill[2] - 45, pill[1] + 17, pill[2] - 11, pill[1] + 48), 220, 120, fill=rgba(teal), width=4)

    round_button(image, cx1 + 292, control_y, 34, light(cream, 0.03), wood, "prev")
    round_button(image, cx1 + 373, control_y, 50, light(teal, 0.12), wood, "play")
    round_button(image, cx1 + 456, control_y, 34, light(cream, 0.03), wood, "next")
    draw = ImageDraw.Draw(image)
    draw.text((cx1 + 530, control_y - 18), "VOL", font=F["mode"], fill=rgba(text))
    draw.rounded_rectangle((cx1 + 600, control_y - 13, cx1 + 720, control_y + 13), radius=12, fill=rgba(dark(center, 0.44)), outline=rgba(dark(wood, 0.2)), width=2)
    draw.rounded_rectangle((cx1 + 604, control_y - 9, cx1 + 674, control_y + 9), radius=9, fill=rgba(teal))
    draw.ellipse((cx1 + 661, control_y - 20, cx1 + 701, control_y + 20), fill=rgba(light(cream, 0.03)), outline=rgba(dark(wood, 0.15)), width=2)

    progress_y = cy1 + 405
    draw.text((cx1 + 60, progress_y - 18), "1:26", font=F["time"], fill=rgba(text))
    draw.rounded_rectangle((cx1 + 132, progress_y - 13, cx2 - 112, progress_y + 13), radius=12, fill=rgba(dark(center, 0.46)), outline=rgba(dark(wood, 0.24)), width=2)
    draw.rounded_rectangle((cx1 + 132, progress_y - 13, cx1 + 345, progress_y + 13), radius=12, fill=rgba(teal))
    draw.ellipse((cx1 + 320, progress_y - 23, cx1 + 366, progress_y + 23), fill=rgba(light(cream, 0.03)), outline=rgba(dark(wood, 0.15)), width=2)
    draw.text((cx2 - 96, progress_y - 18), "4:46", font=F["time"], fill=rgba(text))

    # Lyrics.
    lyrics = [
        u("\\u4fee\\u70bc\\u7231\\u60c5 (Live)"),
        u("\\u8389\\u8389\\u5b89 (Live)"),
        u("\\u6d6a\\u8d39 (Live)"),
        u("\\u76f8\\u7231\\u540e\\u52a8\\u7269\\u611f\\u4f24"),
        u("\\u5495\\u53fd\\u5495\\u53fd (Live)"),
    ]
    for index, lyric in enumerate(lyrics):
        y = lyric_box[1] + 68 + index * 73
        if index == 0:
            clay(image, (lyric_box[0] + 28, y - 17, lyric_box[2] - 28, y + 35), 22, light(teal, 0.22), 0.4)
            draw = ImageDraw.Draw(image)
            color = deep_teal
        else:
            color = dark(wood, 0.03)
        draw.ellipse((lyric_box[0] + 47, y - 4, lyric_box[0] + 63, y + 12), fill=rgba(light(base, 0.15)), outline=rgba(dark(base, 0.2)), width=2)
        draw.text((lyric_box[0] + 80, y - 16), lyric, font=F["lyric"], fill=rgba(color))
        if index > 0:
            draw.line((lyric_box[0] + 80, y + 36, lyric_box[2] - 40, y + 36), fill=rgba(dark(base, 0.15)), width=2)
    draw.arc((lyric_box[0] + 44, lyric_box[3] - 65, lyric_box[0] + 72, lyric_box[3] - 37), 25, 325, fill=rgba(gold), width=4)
    draw.text((lyric_box[0] + 90, lyric_box[3] - 66), "Auto-scrolls with song", font=F["mode"], fill=rgba(dark(wood, 0.02)))

    image.convert("RGB").save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
