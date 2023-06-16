import os
from os import sys
from image_comparison import are_images_identical
import time
import shutil

import os
from PIL import Image

def scale_images(input_folder, output_folder, target_size):

    if os.path.exists(output_folder):
        user_input = input(f"${output_folder} already exist. Should we override it (Y/n): ")

        if user_input.lower() != "y":
            print("Omitting scaling!")
            return

    # Clear the output folder
    shutil.rmtree(output_folder, ignore_errors=True)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)


    for root, dirs, files in os.walk(input_folder):
        # Create corresponding directory structure in the output folder
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        os.makedirs(output_subfolder, exist_ok=True)

        for file in files:
            # Check if the file is an image
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_subfolder, file)

                # Open the image and calculate the new dimensions
                image = Image.open(input_path)
                width, height = image.size

                # Calculate the scaling factor
                if width < height:
                    scale_factor = target_size / width
                    new_width = target_size
                    new_height = int(height * scale_factor)
                else:
                    scale_factor = target_size / height
                    new_width = int(width * scale_factor)
                    new_height = target_size

                # Resize the image while maintaining aspect ratio
                scaled_image = image.resize((new_width, new_height))

                # Save the scaled image to the output folder
                scaled_image.save(output_path)

def compare_folders(folder1, folder2):
    # Collect all image paths from folder1
    image_paths1 = collect_image_paths(folder1)

    # Collect all image paths from folder2
    image_paths2 = collect_image_paths(folder2)

    # Compare images in both folders
    only_in_folder1 = []
    only_in_folder2 = []
    duplicates = []

    for image_path1 in image_paths1:
        # Record the start time
        start_time = time.time()
        print(f"Starting to compare {image_path1} against all images in {folder2}")
        found_duplicate = False

        for image_path2 in image_paths2:
            if are_images_identical(image_path1, image_path2):
                duplicates.append((image_path1, image_path2))
                found_duplicate = True
                break

        if not found_duplicate:
            only_in_folder1.append(image_path1)

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        print(f"That took {elapsed_time} seconds")

    for image_path2 in image_paths2:
        found = False
        for duple in duplicates:
            for element in duple:
                if image_path2 == element:
                    found = True
        if not found:
            only_in_folder2.append(image_path2)

    return only_in_folder1, only_in_folder2, duplicates

def collect_image_paths(folder):
    image_paths = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(root, file)
                image_paths.append(image_path)
    return image_paths


if len(sys.argv) != 3:
    print("Usage: python image_comparison.py <folder_path1> <folder_path2>")
    sys.exit(1)

folder1 = sys.argv[1]
folder2 = sys.argv[2]

output_folder1 = f"./scaled/{os.path.basename(folder1)}"
output_folder2 = f"./scaled/{os.path.basename(folder2)}"

print(f"Scaling images in {folder1}")
scale_images(folder1, output_folder1, 100)
print(f"Scaling images in {folder2}")
scale_images(folder2, output_folder2, 100)

only_in_folder1, only_in_folder2, duplicates = compare_folders(output_folder1, output_folder2)

def change_prefixes(strings, old_prefix, new_prefix):
    new_strings = []
    for string in strings:
        new_string = string.replace(old_prefix, new_prefix, 1)
        new_strings.append(new_string)
    return new_strings

def save_list_to_file(lst, filename):
    with open(filename, 'w') as file:
        for item in lst:
            file.write(item + '\n')

os.makedirs('results', exist_ok=True)

# Output the results
images_folder1 = []
for image_path in change_prefixes(only_in_folder1, output_folder1, folder1):
    images_folder1.append(image_path)

save_list_to_file(images_folder1, 'results/folder1.txt')

images_folder2 = []
for image_path in change_prefixes(only_in_folder2, output_folder2, folder2):
    images_folder2.append(image_path)

save_list_to_file(images_folder2, 'results/folder2.txt')

images_duplicated = []
for image_path1, image_path2 in duplicates:
    images_duplicated.append((f"{image_path1.replace(output_folder1, folder1, 1)} - {image_path2.replace(output_folder1, folder2, 1)}"))

save_list_to_file(images_duplicated, 'results/duplicates.txt')


