import os
from pathlib import Path
import pytesseract
import cv2
import nltk
from fpdf import FPDF

nltk.download("punkt")

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Location of tesseract.eve file
)


def read_text(image):
    print("converting")
    custom_config = r"--oem 3 kor+chi_sim+eng+jpn+vie --psm 6"
    text = pytesseract.image_to_string(image, lang="eng+kor+vie+jap+sun_chi")
    return text


def image_to_text(image_file):
    image = cv2.imread(image_file)
    if input("(RECOMMENDED) apply grayscole y/n:").lower() == "y":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    if input("(OPTIONAL) apply thresholding y/n:").lower() == "y":
        if input("Is the text closer to black or white? B/W:").lower() == "b":
            ret, thresh_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        else:
            ret, thresh_image = cv2.threshold(
                gray_image, 127, 255, cv2.THRESH_BINARY_INV
            )
    else:
        thresh_image = image
    text = read_text(thresh_image)
    return text


def main():
    print("starting process...")
    BASE_DIR = Path(__file__).resolve().parent
    images_folder = os.path.join(BASE_DIR, "images")

    i = 0
    image_text = ""

    text_file = open('text_file.txt', 'a+')

    for f in os.listdir(images_folder):
        try:
            i += 1
            print(f"FILE {i}...")
            image_file = os.path.join(images_folder, f)
            image_text = image_to_text(image_file)
            print(f"TEXT: {image_text}")
            text_file.write(f"DATA FROM FILE {f}\n\n{image_text}\n\n\n\n")
            print(f"FILE {i} complete")
        except:
            print ("could not convert file")

    text_file.close()

    print(image_text)


main()
