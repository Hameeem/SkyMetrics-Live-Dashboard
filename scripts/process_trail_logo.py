from PIL import Image

def process_flight_trail_logo():
    input_path = "C:/Projects/SkyMetrics/dashboard/assets/trail_logo.png"
    output_path = "C:/Projects/SkyMetrics/dashboard/assets/flight_trail_white.png"

    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # If pixel is dark silhouette airplane (R, G, B < 80), invert to pure white (255, 255, 255)
        if item[0] < 100 and item[1] < 100 and item[2] < 100 and item[3] > 30:
            new_data.append((255, 255, 255, item[3]))
        else:
            # Transparent background
            new_data.append((255, 255, 255, 0))

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print("White flight trail logo generated successfully!")

if __name__ == "__main__":
    process_flight_trail_logo()
