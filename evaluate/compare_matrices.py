# compare_matrices.py

from PIL import Image

def combine_images(img1_path, img2_path, output_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Resize to match height
    img1 = img1.resize((img1.width, img2.height))
    total_width = img1.width + img2.width
    result = Image.new('RGB', (total_width, img2.height))

    result.paste(img1, (0, 0))
    result.paste(img2, (img1.width, 0))

    result.save(output_path)
    print(f"Combined side-by-side image saved to: {output_path}")

if __name__ == "__main__":
    combine_images(
        "./output/confusion_matrix.png", 
        "./output/confusion_matrix_knn.png", 
        "./output/comparison_matrix.png"
        )
