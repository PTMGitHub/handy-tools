import tkinter as tk
from PIL import Image, ImageTk  # Importing Pillow for image handling
import random
import os

class BingoMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Bingo Machine")
        self.root.configure(bg="black")

        # Set of available numbers and drawn numbers (1 to 50)
        self.available_numbers = list(range(1, 51))
        self.drawn_numbers = []

        # Dictionary mapping numbers to their assigned text and image path
        self.number_texts = {
            1: {"text": "Yearly Flu Jab", "image": None},
            2: {"text": "Percipio Training platform", "image": None},
            3: {"text": "Hybrid working", "image": None},
            4: {"text": "Flexi Time", "image": None},
            5: {"text": "Free Specsavers Corporate Eyecare", "image": None},
            6: {"text": "5 days for training a year", "image": None},
            7: {"text": "10% additional learning time (EO/HEO) ", "image": None},
            8: {"text": "Paid Membership to Bcs", "image": None},
            9: {"text": "Cycle to work scheme (edenred.uk.com)", "image": None},
            10: {"text": "Government Campus learn.civilservice.gov.uk", "image": None},
            11: {"text": "Apprenticeships", "image": None},
            12: {"text": "MyLifestyle discounts (edenred.uk.com)", "image": None},
            13: {"text": "Coaching and Mentorship (Government Campus learn.civilservice.gov.uk)", "image": None},
            14: {"text": "Employee Assistance Programme (Vita Health", "image": None},
            15: {"text": "Discounted Dental insurance (edenred.uk.com)", "image": None},
            16: {"text": "MyGymDiscounts (edenred.uk.com)", "image": None},
            17: {"text": "myrecognition (Thank you vouchers)", "image": None},
            18: {"text": "Selling holidays", "image": None},
            19: {"text": "1 additional day's holiday a year (untill you reach 30 days holiday a year)", "image": None},
            20: {"text": "A decent Pension contribution", "image": None},
            21: {"text": "Professions learning catalogue", "image": None},
            22: {"text": "Get Cloud Certified this Autumn! (https: //digitalpeople.blog.gov.uk/2024/09/17/get-cloud-certified-this-autumn/)", "image": None},
            23: {"text": "Community Slack channels", "image": None},
            24: {"text": "Cross Gov Slack", "image": None},
            25: {"text": "HMRC Networks (e.g. LGBT+)", "image": None},
            26: {"text": "PAM Assist", "image": None},
            27: {"text": "Community of Practices ", "image": None},
            28: {"text": "HMRC Digital Academy", "image": None},
            29: {"text": "Freedom to make decisions within your team", "image": None},
            30: {"text": "Unmanaged devices to allow a greater degree of freedom to use the tools you want to to carry out your job", "image": None},
            31: {"text": "3 Glass Wharf events", "image": None},
            32: {"text": "Woman in Tech", "image": None},
            33: {"text": "Woman's Mental Health Forum", "image": None},
            34: {"text": "3WG Running Group", "image": None},
            35: {"text": "Mental Health Discussion Forum", "image": None},
            36: {"text": "3WG Showers available", "image": None},
            37: {"text": "3WG Lockers available", "image": None},
            38: {"text": "Getting to work with Holly Hughes ", "image": "images/HollyHughes.jpeg"},
            39: {"text": "4 days a year volunteering leave ", "image": None},
            40: {"text": "Cafe - it might not be the best but believe me there are muuuuuuuch worse", "image": None},
            41: {"text": "Higher rate of pay compared to some other departments (& regional)", "image": None},
            42: {"text": "No blame culture ", "image": None},
            43: {"text": "Platform Demos ", "image": None},
            44: {"text": "Unions available to join", "image": None},
            45: {"text": "Fortnightly anonymous (if desired) Permies Drop in Q&A", "image": None},
            46: {"text": "The work we do is part of making a difference to the lives of the general public ", "image": None},
            47: {"text": "Working in an environment that cares about diverisity and inclusion", "image": None},
            48: {"text": "An always warm and toasty 3GW Office", "image": None},
            49: {"text": "Easy access to Small Goods doughnuts from 3GW Office", "image": "images/SmallGoods.png"},
            50: {"text": "3GW Office workplace adjustment, such as ergonomic chairs ", "image": None},
        }
        # Button to draw the next number
        self.next_number_button = tk.Button(self.root, text="Next Number", font=("Helvetica", 24), command=self.draw_next_number, fg="black", bg="Orange")
        self.next_number_button.pack(pady=20)


        # Frame for current number display
        self.current_number_frame = tk.Frame(self.root, bg="black")
        self.current_number_frame.pack(pady=20)

        # Large label to display the current number
        self.current_number_label = tk.Label(self.current_number_frame, text="", font=("Helvetica", 250), fg="Orange", bg="black")
        self.current_number_label.pack()

        # Label to display the text associated with the current number
        self.current_text_label = tk.Label(self.current_number_frame, text="", font=("Helvetica", 40), fg="white", bg="black", wraplength=1000)
        self.current_text_label.pack(side="bottom", fill="x")

        # Label to display the image associated with the current number
        self.current_image_label = tk.Label(self.current_number_frame, bg="black")
        self.current_image_label.pack(pady=10)


        # Frame for displaying previously drawn numbers
        self.previous_numbers_frame = tk.Frame(self.root, bg="black")
        self.previous_numbers_frame.pack()

        # Label to show the history of drawn numbers
        self.previous_numbers_label = tk.Label(self.previous_numbers_frame, text="Previous Numbers:", font=("Helvetica", 14), fg="light grey", bg="black")
        self.previous_numbers_label.pack()

        # Label to hold the list of previous numbers
        self.previous_numbers_list_label = tk.Label(self.previous_numbers_frame, text="", font=("Helvetica", 25), fg="light grey", bg="black", wraplength=1000)
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
            self.current_number_label.config(text="No more numbers!", font=("Helvetica", 80))
            self.current_text_label.config(text="That's all folks")
            self.current_image_label.image = None
            self.next_number_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    bingo_machine = BingoMachine(root)
    root.mainloop()
