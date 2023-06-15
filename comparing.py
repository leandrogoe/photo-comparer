from image_comparison import are_images_identical
from os import sys

if len(sys.argv) != 3:
    print("Usage: python image_comparison.py <image_path1> <image_path2>")
    sys.exit(1)

image_path1 = sys.argv[1]
image_path2 = sys.argv[2]

result = are_images_identical(image_path1, image_path2)
print("Images are identical:", result)