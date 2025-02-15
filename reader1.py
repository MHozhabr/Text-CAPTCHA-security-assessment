import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import os

#
#
# text extractor using tesseract model to extract captchas
#
#

#locate tesseract from path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class CaptchaOCRApp:
    #make the window
    def __init__(self, root):
        self.root = root
        self.root.title("Captcha OCR")
        self.root.geometry("400x200")

        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.pack()

        self.open_button = tk.Button(root, text="Open Captcha", command=self.open_captcha)
        self.open_button.pack()

    def open_captcha(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.process_captcha(file_path)

    # use OCR to detect captcha and extract the written text
    def process_captcha(self, file_path):
        captcha_image = Image.open(file_path)
        captcha_image_tk = ImageTk.PhotoImage(captcha_image)
        self.image_label.config(image=captcha_image_tk)
        self.image_label.image = captcha_image_tk

        extracted_text = self.extract_text(captcha_image, file_path)
        self.result_label.config(text=f"Result: {extracted_text}")

    def extract_text(self, image, file_path):
        preprocessed_image = self.preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed_image, config='--psm 8').strip()

        filename = os.path.basename(file_path)
        if filename.startswith("c") or filename.startswith("g") or filename.startswith("C"):
            return self.process_letter_captcha(text)
        elif filename.startswith("e") or filename.startswith("n"):
            return self.process_equation_captcha(text)
        elif filename.startswith("h") or filename.startswith("H"):
            return self.process_hybrid_captcha(text)

    def preprocess_image(self, image):
        # Convert the image to grayscale
        gray_image = image.convert('L')
        # Apply threshold to get a binary image
        binary_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
        return binary_image

    def process_letter_captcha(self, text):
        # Extract exactly 5 letters (handling OCR errors or noise)
        letters = ''.join(filter(str.isalpha, text))
        if len(letters) == 5:
            return letters
        else:
            return f"{letters}\nInvalid Captcha"

    def process_equation_captcha(self, text):
        # Extract the numbers and the addition result
        numbers = list(map(int, filter(str.isdigit, text)))
        if len(numbers) == 2 and numbers[0] + numbers[1] <= 18:
            return f"{numbers[0]} + {numbers[1]} = {numbers[0] + numbers[1]}"
        else:
            return f"{text}\nInvalid Equation Captcha"

    def process_hybrid_captcha(self, text):
        # Split the text to separate the 5-letter word and the equation
        parts = text.split()
        if len(parts) < 2:
            return f"{text}\nInvalid Hybrid Captcha"

        # Process the 5-letter word
        letters = ''.join(filter(str.isalpha, parts[0]))
        if len(letters) != 5:
            return f"{letters}\nInvalid 5-letter part"

        # Process the equation part
        equation_part = ' '.join(parts[1:])
        numbers = list(map(int, filter(str.isdigit, equation_part)))
        if len(numbers) == 2 and numbers[0] + numbers[1] <= 18:
            equation_result = f"{numbers[0]} + {numbers[1]} = {numbers[0] + numbers[1]}"
            return f"{letters} {equation_result}"
        else:
            return f"{text}\nInvalid Equation part"

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaOCRApp(root)
    root.mainloop()
