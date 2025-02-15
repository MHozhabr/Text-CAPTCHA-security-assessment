import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import string
import time

#
# Hybrid captcha using 5-letter text and equation captchas.
# The user must correctly enter the text and solve the equation to pass the captcha test
#

class CombinedCaptchaApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Combined Captcha Verification")
        self.root.geometry("450x200")

        # Initialize variables to store captcha text, equation, solution, and timer
        self.captcha_text = ''
        self.equation_text = ''
        self.solution = 0
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
        # Generate a new captcha text and equation
        self.captcha_text = self.generate_random_text()
        self.equation_text, self.solution = self.generate_equation()
        combined_text = f"{self.captcha_text} {self.equation_text}"
        self.captcha_image = self.generate_captcha_image(combined_text)
        self.captcha_image_tk = ImageTk.PhotoImage(self.captcha_image)
        self.captcha_label.config(image=self.captcha_image_tk)
        self.entry.delete(0, tk.END)
        self.start_time = time.time()

    def generate_random_text(self):
        # Generate a random string of 5 characters, ensuring no consecutive characters are the same
        characters = string.ascii_letters
        while True:
            captcha_text = ''.join(random.choice(characters) for _ in range(5))
            if not any(captcha_text[i] == captcha_text[i + 1] for i in range(4)):
                return captcha_text

    def generate_equation(self):
        # Generate a simple addition equation with a sum <= 18
        while True:
            num1 = random.randint(0, 9)
            num2 = random.randint(0, 9)
            if num1 + num2 <= 18:
                equation = f"{num1} + {num2}"
                solution = num1 + num2
                return equation, solution

    def generate_captcha_image(self, text):
        # Create a blank image for the captcha and draw the combined text (5-letter word and equation) on it
        width, height = 400, 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        fonts = ["arial.ttf", "times.ttf", "courbd.ttf", "calibri.ttf"]

        x_offset = 10
        for char in text:
            font_path = random.choice(fonts)
            if char.islower():
                font_size = random.randint(20, 24)  # Smaller font size for lowercase letters
            else:
                font_size = random.randint(30, 36)  # Larger font size for uppercase letters and digits
            font = ImageFont.truetype(font_path, font_size)
            x = x_offset
            y = random.randint(0, 20)
            char_image = Image.new('RGBA', (font_size, font_size), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_image)
            char_draw.text((0, 0), char, font=font, fill=self.random_color())

            # Rotate and place character image onto main image
            char_image = char_image.rotate(random.randint(-30, 30), expand=1)
            image.paste(char_image, (x, y), char_image)
            x_offset += font_size

        # Add noise
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=self.random_color())

        # Add lines
        for _ in range(5):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=self.random_color())

        return image

    def random_color(self):
        # Generate a random color
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def check_captcha(self):
        # Check if the entered captcha matches the generated captcha (both text and equation solution)
        end_time = time.time()
        elapsed_time = (end_time - self.start_time) * 1000
        user_input = self.entry.get()

        if ' ' not in user_input:
            messagebox.showerror("Error", "Please enter both the 5-letter word and the equation solution.")
            return

        user_word, user_solution = user_input.split()

        if user_word != self.captcha_text and int(user_solution) != self.solution:
            messagebox.showerror("Error", "Both the 5-letter word and the equation solution are incorrect.")
        elif user_word != self.captcha_text:
            messagebox.showerror("Error", "The 5-letter word is incorrect.")
        elif int(user_solution) != self.solution:
            messagebox.showerror("Error", "The equation solution is incorrect.")
        else:
            messagebox.showinfo("Success", "Captcha entered correctly!")

        self.timer_label.config(text=f"Time: {int(elapsed_time)} ms")

    def save_captcha(self):
        # Save the generated captcha image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.captcha_image.save(file_path)
            messagebox.showinfo("Saved", f"Captcha saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedCaptchaApp(root)
    root.mainloop()
