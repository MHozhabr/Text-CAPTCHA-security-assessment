import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import time

#
#
# Simple addition equation captcha generator with no particular distortion, just a background noise to test the OCR
#
#
class CaptchaApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Captcha Verification")

        # Initialize variables to store captcha text and timer
        self.captcha_text = ''
        self.start_time = 0

        self.captcha_label = tk.Label(root)
        self.captcha_label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.enter_button = tk.Button(root, text="Enter", command=self.check_captcha)
        self.enter_button.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.generate_captcha)
        self.reset_button.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_captcha)
        self.save_button.pack()

        self.timer_label = tk.Label(root, text="Time: 0 ms")
        self.timer_label.pack()

        self.generate_captcha()

    def generate_captcha(self):
        # Generate a new captcha text and image
        self.captcha_text = self.generate_random_equation()
        self.captcha_image = self.generate_captcha_image(self.captcha_text)
        self.captcha_image_tk = ImageTk.PhotoImage(self.captcha_image)
        self.captcha_label.config(image=self.captcha_image_tk)
        self.entry.delete(0, tk.END)
        self.start_time = time.time()

    def generate_random_equation(self):
        # Generate a random addition equation where the sum does not exceed 18
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
        while num1 + num2 > 18:
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
        return f"{num1} + {num2}"

    def generate_captcha_image(self, text):
        # Create a blank image for the captcha and draw the text on it
        width, height = 200, 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font_path = "courbd.ttf"
        font = ImageFont.truetype(font_path, 36)

        # Draw the text
        draw.text((10, 10), text, font=font, fill='black')

        # Add background noise
        noise_amount = 700
        for _ in range(noise_amount):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            draw.point((x, y), fill='black')

        return image

    def check_captcha(self):
        # Check if the entered captcha matches the generated captcha
        end_time = time.time()
        elapsed_time = (end_time - self.start_time) * 1000
        user_input = self.entry.get()
        correct_answer = eval(self.captcha_text)
        if user_input == str(correct_answer):
            messagebox.showinfo("Success", "Captcha entered correctly!")
        else:
            messagebox.showerror("Error", "Incorrect captcha, please try again.")
        self.timer_label.config(text=f"Time: {int(elapsed_time)} ms")

    def save_captcha(self):
        # Save the generated captcha
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.captcha_image.save(file_path)
            messagebox.showinfo("Saved", f"Captcha saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaApp(root)
    root.mainloop()
