import cv2
import os

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # Resize (VERY IMPORTANT - improves accuracy)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold (better for scanned docs)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


def extract_text_from_image(image_path):
    try:
        processed = preprocess_image(image_path)

        # BETTER OCR CONFIG
        text = pytesseract.image_to_string(
            processed,
            config='--oem 3 --psm 6'
        )

        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"


# TEST
if __name__ == "__main__":
    path = input("Enter image path: ")

    if not os.path.exists(path):
        print("❌ File not found")
    else:
        print("\n⏳ Processing...\n")
        result = extract_text_from_image(path)

        print("✅ DONE\n")
        print(result)