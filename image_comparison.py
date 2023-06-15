from skimage.metrics import structural_similarity as ssim
from skimage import img_as_ubyte
from PIL import Image

def are_images_identical(image_path1, image_path2):
    # print(f"Comparing {image_path1} and {image_path2}")

    # Load the images
    image1 = Image.open(image_path1).convert("L")
    image2 = Image.open(image_path2).convert("L")

    # Check if aspect ratios differ significantly
    aspect_ratio_threshold = 0.1  # Adjust this threshold based on your needs

    aspect_ratio_diff = get_min_aspect_ratio_diff(image1, image2)

    if aspect_ratio_diff > aspect_ratio_threshold:
        # print(f"Aspect ratio doesn't match: aspect_ratio_diff {aspect_ratio_diff:.4f}")
        return False

    # Resize the images to have the same width while preserving aspect ratio
    target_width = 100

    if (abs(calculate_aspect_ratio(image1) - calculate_aspect_ratio(image2)) > 0.1):
        image1 = image1.rotate(90, expand=True)

    new_height1 = int(image1.height * target_width / image1.width)
    new_height2 = int(image2.height * target_width / image2.width)
    resized1 = image1.resize((target_width, new_height1))
    resized2 = image2.resize((target_width, new_height2))

    for _ in range(3):
        if not resized1.height == resized2.height:
            # print(f"image1.height: {image1.height:.4f}, image2.height: {image2.height:.4f}")
            continue

        # Convert images to uint8
        grey1 = img_as_ubyte(resized1)
        grey2 = img_as_ubyte(resized2)

        # Calculate SSIM and MSE scores
        ssim_score = ssim(grey1, grey2)
        mse_score = ((grey1 - grey2) ** 2).mean()

        similarity_threshold = 0.9  # Adjust this threshold based on your needs
        mse_threshold = 20  # Adjust this threshold based on your needs

        if ssim_score > similarity_threshold and mse_score < mse_threshold:
            print(f"Dupe found! {image_path1} and {image_path2} are equal. Metrics: SSIM: {ssim_score:.4f}, MSE: {mse_score:.4f}")
            return True  # Images are considered identical or similar
        #else:
        #    print(f"SSIM: {ssim_score:.4f}, MSE: {mse_score:.4f}")

        resized1 = resized1.rotate(90, expand=True)
        # width, height = resized1.size
        # print(f"Rotating image1: width: {width:.4f}, height: {height:.4f}")

    return False  # Images are different

def get_min_aspect_ratio_diff(image1, image2):
    aspect_ratio1 = calculate_aspect_ratio(image1)
    aspect_ratio2 = calculate_aspect_ratio(image2)

    return min([abs(aspect_ratio1 - aspect_ratio2), abs(aspect_ratio1 - (1 / aspect_ratio2))])

def calculate_aspect_ratio(image):
    width, height = image.size
    return width / height

