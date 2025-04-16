import os
import json

def get_images(base_path="."):
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
    images = []
    folder_map = {}

    for root, _, files in os.walk(base_path):
        image_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
        if image_files:
            relative_folder = os.path.relpath(root, base_path)

            folder_map[relative_folder] = relative_folder

            # Add the relative image paths to the images list
            images.extend([os.path.join(relative_folder, f).replace("/", "\\") for f in image_files])

    return images, folder_map

def generate_html(images, folder_map, template_html):

    json_data = json.dumps({
        "images": images,
        "folders": list(set(folder_map.values()))
    }, indent=4)

    return template_html.replace("<!-- PLACEHOLDER -->", f'<script id="imagesData" type="application/json">{json_data}</script>')

def main():
    images, folder_map = get_images()

    # Read the proto.html file, we just add JSON to it so it can read the images with just a single
    #html file
    with open("proto.html", "r") as proto_file:
        template_html = proto_file.read()

    final_html = generate_html(images, folder_map, template_html)

    with open("ImageWebViewer.html", "w") as index_file:
        index_file.write(final_html)

    print("ImageWebViewer.html generated successfully.")

if __name__ == "__main__":
    main()
