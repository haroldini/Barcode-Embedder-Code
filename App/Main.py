import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import ImageTk, Image
import time
import threading
import barcode
from barcode.writer import ImageWriter
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import logging
import os
import subprocess
import json

from Page import Page
from Options import Options
from Pages.Options import OptionsPage
from Pages.Embed import EmbedPage
from Pages.Log import LogsPage
from Pages.LeftFrame import LeftFrame

DELAY = 50
run_flag_lock = threading.Lock()

logging.basicConfig(filename="App/resources/log.log",
                    encoding="utf-8",
                    format='%(levelname)s %(asctime)s  %(message)s',
                    level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.INFO)


render_options = {
    "format": "PNG",
    "dpi": 300,
    "module_height": 5,
    "write_text": False,
    "font_size": 5,
    "text_distance": 1.5,
}


class App(TkinterDnD.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Options.load_options(self)
        Options.get_colors(self, theme=self.options["theme"])

        self.iconbitmap("App/resources/icon.ico")
        self.title("Barcode Embedder")
        self.geometry(
            f"{self.options[f'window_default_size'][0]}x" +
            f"{self.options[f'window_default_size'][1]}")
        self.minsize(self.options["window_min_size"][0],
                     self.options["window_min_size"][1])
        self.maxsize(self.options["window_max_size"]
                     [0], self.options["window_max_size"][1])
        self.configure(bg=self.WHITE)

        self.create_gui()
        self.create_navigation_handlers()
        self.after(DELAY, self.update_app)

        self.mainloop()

    def update_app(self):
        # update things here
        self.after(DELAY, self.update_app)

    def create_gui(self):

        self.current_page = "embed"
        self.previous_page = "embed"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.options_page = OptionsPage(self)
        self.embed_page = EmbedPage(self)
        self.logs_page = LogsPage(self)
        self.frame_left = LeftFrame(self)

        self.embed_page.grid(row=0, column=1,
                             rowspan=3, padx=20, pady=20, sticky="nsew")
        self.options_page.grid(row=0, column=1, padx=20,
                               pady=20, sticky="nsew")
        self.logs_page.grid(row=0, column=1, padx=20,
                            pady=20, sticky="nsew")
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

        self.embed_page.show()

    def create_navigation_handlers(self):
        self.frame_left.options_button.configure(
            command=self.options_button_handler)
        self.frame_left.logs_button.configure(
            command=self.logs_button_handler)
        self.options_page.cancel_button.configure(
            command=self.options_cancel_button_handler)
        self.options_page.save_button.configure(
            command=self.options_save_button_handler)
        self.logs_page.back_button.configure(
            command=self.logs_back_button_handler)

    def options_button_handler(self):
        if self.current_page != "options":
            Options.load_options(self)
            self.options_page.show()
            self.previous_page = self.current_page
            self.current_page = "options"
            self.frame_left.options_button.configure(fg_color=self.LIGHT_BLUE)
            self.frame_left.options_button.configure(state="disabled")
            self.frame_left.logs_button.configure(state="disabled")
            self.frame_left.logs_button.configure(fg_color=None)
            return

    def logs_button_handler(self):
        if self.current_page != "logs":
            self.logs_page.show()
            self.previous_page = self.current_page
            self.current_page = "logs"
            self.frame_left.logs_button.configure(fg_color=self.LIGHT_BLUE)
            self.frame_left.options_button.configure(fg_color=None)
            return

        self.embed_page.show()
        self.current_page = "embed"
        self.previous_page = "logs"
        self.frame_left.logs_button.configure(fg_color=None)

    def options_cancel_button_handler(self):
        if self.current_page == "options":
            self.previous_page = self.current_page
            self.current_page = "embed"
            self.frame_left.options_button.configure(fg_color=None)
            self.frame_left.options_button.configure(state="normal")
            self.frame_left.logs_button.configure(state="normal")
            Options.load_options(self)
            self.embed_page.show()

    def options_save_button_handler(self):
        if self.current_page == "options":
            self.previous_page = self.current_page
            self.current_page = "embed"
            self.frame_left.options_button.configure(fg_color=None)
            self.frame_left.options_button.configure(state="normal")
            self.frame_left.logs_button.configure(state="normal")
            Options.load_options(self)
            self.embed_page.show()

    def logs_back_button_handler(self):
        if self.current_page == "logs":
            self.previous_page = self.current_page
            self.current_page = "embed"
            self.frame_left.logs_button.configure(fg_color=None)
            self.embed_page.show()

    def reset_settings_file(self):
        with open("./resources/settings_default.json", "r") as infile:
            with open("./resources/settings.json", "w") as outfile:
                outfile.write(json.dumps(json.load(infile), indent=4))


if __name__ == "__main__":
    app = App()
