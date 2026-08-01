import os
from PIL import Image, ImageDraw


def create_crisp_plane_logo():
    # Create 256x256 RGBA image
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw plane body (white with black outline)
    # Fuselage
    fuselage_points = [
        (40, 160), (90, 130), (190, 95), (230, 90), (240, 105),
        (220, 125), (140, 150), (90, 175), (55, 185)
    ]
    draw.polygon(fuselage_points, fill=(255, 255, 255, 255), outline=(15, 23, 42, 255))

    # Tail fin
    tail_points = [(40, 160), (15, 100), (55, 115), (90, 130)]
    draw.polygon(tail_points, fill=(3, 105, 161, 255), outline=(15, 23, 42, 255))

    # Main Wing
    wing_points = [(100, 140), (150, 220), (190, 200), (150, 125)]
    draw.polygon(wing_points, fill=(240, 249, 255, 255), outline=(15, 23, 42, 255))

    # Top wing
    top_wing = [(110, 110), (70, 40), (110, 48), (145, 95)]
    draw.polygon(top_wing, fill=(240, 249, 255, 255), outline=(15, 23, 42, 255))

    # Underbelly blue accent
    belly_points = [(90, 175), (140, 150), (220, 125), (200, 140), (130, 165)]
    draw.polygon(belly_points, fill=(2, 132, 199, 255))

    # Cockpit window
    draw.ellipse([215, 96, 230, 104], fill=(15, 23, 42, 255))

    # Windows
    for x in [120, 140, 160, 180, 200]:
        y = 118 - int((x - 120) * 0.15)
        draw.ellipse([x, y, x+6, y+6], fill=(15, 23, 42, 255))

    os.makedirs("C:/Projects/SkyMetrics/dashboard/assets", exist_ok=True)
    img.save("C:/Projects/SkyMetrics/dashboard/assets/plane_logo.png", "PNG")
    print("Crisp plane logo created successfully!")

if __name__ == "__main__":
    create_crisp_plane_logo()
