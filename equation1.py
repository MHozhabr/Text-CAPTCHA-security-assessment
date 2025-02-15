import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
import time

#
#
# equation captcha with a simple addition of 1-digit numbers, the answer is the result of the equation.
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

        # Generate the initial captcha
        self.generate_captcha()

    def generate_captcha(self):
        self.captcha_text, self.solution = self.generate_equation()
        self.captcha_image = self.generate_captcha_image(self.captcha_text)
        self.captcha_image_tk = ImageTk.PhotoImage(self.captcha_image)
        self.captcha_label.config(image=self.captcha_image_tk)
        self.entry.delete(0, tk.END)
        self.start_time = time.time()

    def generate_equation(self):
        # Generate a simple addition equation with two random numbers
        while True:
            num1 = random.randint(0, 9)
            num2 = random.randint(0, 9)

            if num1 + num2 <= 18:
                equation = f"{num1} + {num2}"
                solution = num1 + num2
                return equation, solution

    def generate_captcha_image(self, text):
        # Create a blank image for the captcha
        width, height = 200, 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        fonts = ["arial.ttf", "times.ttf", "courbd.ttf", "calibri.ttf"]

        # Draw each character of the captcha text on the image
        x_offset = 10
        for char in text:
            font_path = random.choice(fonts)
            font_size = random.randint(30, 36)
            font = ImageFont.truetype(font_path, font_size)
            x = x_offset
            y = random.randint(0, 20)
            char_image = Image.new('RGBA', (font_size, font_size), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_image)
            char_draw.text((0, 0), char, font=font, fill=self.random_color())

            # Rotate and place the character image onto the main image
            char_image = char_image.rotate(random.randint(-30, 30), expand=1)
            image.paste(char_image, (x, y), char_image)
            x_offset += font_size

        # Add random noise
        for _ in range(50):
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.point((x, y), fill=self.random_color())

        # Add random lines
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
        # Check if the entered captcha solution is correct
        end_time = time.time()
        elapsed_time = (end_time - self.start_time) * 1000
        user_input = self.entry.get()
        try:
            user_solution = int(user_input)
            if user_solution == self.solution:
                messagebox.showinfo("Success", "Captcha entered correctly!")
            else:
                messagebox.showerror("Error", "Incorrect captcha, please try again.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
        self.timer_label.config(text=f"Time: {int(elapsed_time)} ms")

    def save_captcha(self):
        # Save the generated captcha image to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.captcha_image.save(file_path)
            messagebox.showinfo("Saved", f"Captcha saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptchaApp(root)
    root.mainloop()
