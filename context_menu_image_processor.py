import os
import sys
import cv2
import concurrent.futures

def process_image(full_path):
    try:
        # Read the image using OpenCV
        img = cv2.imread(full_path)

        # Save the image with reduced quality
        save_path = os.path.join(os.path.dirname(full_path), f"{os.path.splitext(os.path.basename(full_path))[0]}_70.jpeg")
        cv2.imwrite(save_path, img, [cv2.IMWRITE_JPEG_QUALITY, 70])

        # If saved successfully, remove the old image
        os.remove(full_path)
        return None
    except Exception as e:
        return f"Error processing '{full_path}': {e}"

def process_images_in_directory(directory):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        image_paths = [os.path.join(root, filename) for root, _, files in os.walk(directory) for filename in files if filename.lower().endswith(('.jpg', '.jpeg')) and not filename.endswith('_70.jpeg')]
        list(executor.map(process_image, image_paths))
        

def main():
    if len(sys.argv) != 2:
        print("Usage: context_menu_image_processor.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)

    process_images_in_directory(directory)

if __name__ == "__main__":
    main()
