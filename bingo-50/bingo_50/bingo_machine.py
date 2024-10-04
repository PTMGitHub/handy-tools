import tkinter as tk
from PIL import Image, ImageTk  # Importing Pillow for image handling
import random
import os

class BingoMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Machine")

        # Set of available numbers and drawn numbers (1 to 50)
        self.available_numbers = list(range(1, 6))
        self.drawn_numbers = []

        # Dictionary mapping numbers to their assigned text and image path
        self.number_texts = {
            1: {"text": "One is the first and only.", "image": "images/image1.png"},
            2: {"text": "Two's a pair!", "image": "images/image2.png"},
            3: {"text": "Three is a magic number.", "image": "images/image1.png"},
            4: {"text": "Four seasons in a year.", "image": "images/image2.png"},
            5: {"text": "Five fingers make a hand.", "image": None},  # No image for number 5
        }

        # Frame for current number display
        self.current_number_frame = tk.Frame(self.root)
        self.current_number_frame.pack(pady=20)

        # Large label to display the current number
        self.current_number_label = tk.Label(self.current_number_frame, text="", font=("Helvetica", 48), fg="blue")
        self.current_number_label.pack()

        # Label to display the text associated with the current number
        self.current_text_label = tk.Label(self.current_number_frame, text="", font=("Helvetica", 18), fg="green")
        self.current_text_label.pack()

        # Label to display the image associated with the current number
        self.current_image_label = tk.Label(self.current_number_frame)
        self.current_image_label.pack(pady=10)

        # Button to draw the next number
        self.next_number_button = tk.Button(self.root, text="Next Number", font=("Helvetica", 24), command=self.draw_next_number)
        self.next_number_button.pack(pady=20)

        # Frame for displaying previously drawn numbers
        self.previous_numbers_frame = tk.Frame(self.root)
        self.previous_numbers_frame.pack()

        # Label to show the history of drawn numbers
        self.previous_numbers_label = tk.Label(self.previous_numbers_frame, text="Previous Numbers:", font=("Helvetica", 16))
        self.previous_numbers_label.pack()

        # Label to hold the list of previous numbers
        self.previous_numbers_list_label = tk.Label(self.previous_numbers_frame, text="", font=("Helvetica", 14))
        self.previous_numbers_list_label.pack()

    def draw_next_number(self):
        if self.available_numbers:
            # Randomly pick a number from the available list
            next_number = random.choice(self.available_numbers)
            self.available_numbers.remove(next_number)
            self.drawn_numbers.append(next_number)

            # Update the large current number display
            self.current_number_label.config(text=str(next_number))

            # Get the associated text and image for the drawn number
            number_data = self.number_texts.get(next_number, {"text": "No text assigned.", "image": None})
            number_text = number_data["text"]
            image_path = number_data["image"]

            # Update the text label with the associated text
            self.current_text_label.config(text=number_text)

            # Update the image if an image path is provided
            if image_path and os.path.exists(image_path):
                # Load the image using PIL and resize it (optional resizing to fit the label)
                image = Image.open(image_path)
                image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the image
                photo = ImageTk.PhotoImage(image)

                # Set the image to the label
                self.current_image_label.config(image=photo)
                self.current_image_label.image = photo  # Keep a reference to avoid garbage collection
            else:
                # If no image is found or the path is None, clear the image label
                self.current_image_label.config(image="", text="")

            # Update the list of previous numbers
            self.previous_numbers_list_label.config(text=", ".join(map(str, self.drawn_numbers)))
        else:
            self.current_number_label.config(text="No more numbers!")
            self.current_text_label.config(text="That's all folks")
            self.current_image_label.image = None
            self.next_number_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    bingo_machine = BingoMachine(root)
    root.mainloop()
