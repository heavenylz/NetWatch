from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

SOURCE = Path("assets/netwatch_logo.png")
OUTPUT = Path("assets/netwatch.ico")

ICON_SIZES = [
    16,
    24,
    32,
    48,
    64,
    128,
    256,
]


def prepare_source(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")

    # Transparent bounding box varsa gereksiz boşluğu kırp.
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()

    if bbox:
        image = image.crop(bbox)

    return image


def create_icon_layer(
    source: Image.Image,
    size: int,
) -> Image.Image:
    # Küçük Windows ikonlarında logonun kenarlara
    # yapışmaması için kontrollü padding.
    if size <= 24:
        padding_ratio = 0.10
    elif size <= 48:
        padding_ratio = 0.08
    else:
        padding_ratio = 0.06

    padding = max(
        1,
        round(size * padding_ratio),
    )

    available = size - (padding * 2)

    width, height = source.size

    scale = min(
        available / width,
        available / height,
    )

    target_width = max(
        1,
        round(width * scale),
    )

    target_height = max(
        1,
        round(height * scale),
    )

    resized = source.resize(
        (
            target_width,
            target_height,
        ),
        Image.Resampling.LANCZOS,
    )

    # Küçük ikonlarda detayların biraz daha okunaklı
    # kalması için hafif kontrast/keskinlik.
    if size <= 48:
        resized = ImageEnhance.Contrast(
            resized
        ).enhance(1.08)

        resized = ImageEnhance.Sharpness(
            resized
        ).enhance(1.18)

    canvas = Image.new(
        "RGBA",
        (size, size),
        (0, 0, 0, 0),
    )

    x = (
        size - target_width
    ) // 2

    y = (
        size - target_height
    ) // 2

    canvas.alpha_composite(
        resized,
        (x, y),
    )

    return canvas


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Logo not found: {SOURCE}"
        )

    source = prepare_source(
        Image.open(SOURCE)
    )

    layers = [
        create_icon_layer(
            source,
            size,
        )
        for size in ICON_SIZES
    ]

    # Pillow ICO writer stores the requested
    # Windows resolutions in one .ico file.
    largest = layers[-1]

    largest.save(
        OUTPUT,
        format="ICO",
        sizes=[
            (size, size)
            for size in ICON_SIZES
        ],
    )

    print(
        f"Created: {OUTPUT}"
    )

    print(
        "Included sizes:",
        ", ".join(
            f"{size}x{size}"
            for size in ICON_SIZES
        ),
    )


if __name__ == "__main__":
    main()