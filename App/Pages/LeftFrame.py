import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk, Image

from Page import Page


class LeftFrame(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_logo()
        self.corner_radius = 0

        self.grid_rowconfigure((0, 1), minsize=20)
        self.grid_rowconfigure(2, minsize=self.logo_height)
        self.grid_rowconfigure((3, 4), weight=3)
        self.grid_rowconfigure((5, 6, 7), minsize=20)

        self.create_widgets()

    def read_logo(self):
        with Image.open("App/resources/icon.png").convert("RGBA") as logo:
            self.image_aspect_ratio = logo.height / logo.width
            self.logo_width = 100
            self.logo_height = int(self.logo_width * self.image_aspect_ratio)
            self.logo = logo.resize(
                (self.logo_width, self.logo_height))

    def create_widgets(self):
        # Title Text
        self.title_label = ctk.CTkLabel(master=self,
                                        text="Barcode Embedder",
                                        text_color=self.DARK_GREY,
                                        text_font=("Roboto Bold", -24))  # font name and size in px
        self.title_label.grid(
            row=0, column=0, pady=(20, 0), padx=20, sticky="s")
        self.subtitle_label = ctk.CTkLabel(master=self,
                                           text="github.com/haroldini",
                                           text_color=self.DARK_GREY,
                                           text_font=("Roboto Bold", -16))  # font name and size in px
        self.subtitle_label.grid(
            row=1, column=0, pady=(0, 20), padx=20, sticky="n")

        # Logo image.
        self.bg_image = ImageTk.PhotoImage(self.logo)
        self.image_label = tk.Label(
            master=self, image=self.bg_image, bg=self.BG_COLOR)
        self.image_label.grid(row=2, column=0, pady=0, padx=20, sticky="n")

        self.error_label = ctk.CTkLabel(master=self,
                                        text="",
                                        wraplength=185,
                                        corner_radius=6,
                                        fg_color=self.LIGHT_GREY,
                                        text_color=self.ERROR,
                                        text_font=("Roboto Bold", -16))  # font name and size in px
        self.error_label.grid(
            row=4, column=0, pady=20, padx=20, ipadx=10, ipady=10, sticky="n")
        self.error_label.grid_remove()

        self.version_label = ctk.CTkLabel(master=self,
                                          text="1.1.0",
                                          text_color=self.DARK_GREY,
                                          text_font=("Roboto Bold", -16))  # font name and size in px
        self.version_label.grid(
            row=7, column=0, pady=(0, 20), padx=20, sticky="s")
