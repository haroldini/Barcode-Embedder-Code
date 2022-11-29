import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk, Image

from Page import Page


class LeftFrame(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_logo()
        self.corner_radius = 0

        self.grid_rowconfigure((0, 1), minsize=25)
        self.grid_rowconfigure(2, minsize=self.logo_height)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, minsize=25)

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
                                        height=25,
                                        text_font=("Roboto", -24))  # font name and size in px
        self.title_label.grid(
            row=0, column=0, pady=(20, 0), padx=20, sticky="nwe")
        self.subtitle_label = ctk.CTkLabel(master=self,
                                           text="github.com/haroldini",
                                           height=25,
                                           text_color=self.DARK_GREY,
                                           text_font=("Roboto", -16))  # font name and size in px
        self.subtitle_label.grid(
            row=1, column=0, pady=(0, 20), padx=20, sticky="nwe")

        # Logo image.
        self.bg_image = ImageTk.PhotoImage(self.logo)
        self.image_label = ctk.CTkLabel(
            master=self, image=self.bg_image, bg=self.BG_COLOR, anchor="n")
        self.image_label.grid(
            row=2, column=0, pady=0, padx=20, sticky="nwe")

        # Error frame
        self.error_frame = ctk.CTkFrame(
            master=self, corner_radius=6, fg_color=self.LIGHT_GREY, height=120)
        self.error_frame.grid(row=4, column=0, padx=20, pady=20, sticky="swe")
        self.error_frame.grid_rowconfigure(0, weight=1)
        self.error_frame.grid_columnconfigure(0, weight=1)
        self.error_frame.grid_remove()

        # Error label
        self.error_label = ctk.CTkLabel(master=self.error_frame,
                                        text="",
                                        wraplength=185,
                                        anchor="center",
                                        text_color=self.ERROR,
                                        text_font=("Roboto Bold", -16))  # font name and size in px
        self.error_label.grid(
            row=0, column=0, pady=10, padx=10, sticky="nswe")

        self.version_label = ctk.CTkLabel(master=self,
                                          text="2.0.1",
                                          text_color=self.DARK_GREY,
                                          text_font=("Roboto Bold", -16))  # font name and size in px
        self.version_label.grid(
            row=5, column=0, pady=(0, 20), padx=20, sticky="s")
