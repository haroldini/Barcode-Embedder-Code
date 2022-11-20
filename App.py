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


DELAY = 50
run_flag_lock = threading.Lock()

logging.basicConfig(filename="./resources/log.log",
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


class Options():
    def __init__(self):
        self.load_options()
        self.get_colors()

    def get_colors(self, theme="LIGHT"):
        ctk.set_default_color_theme("blue")
        if theme == "LIGHT":
            ctk.set_appearance_mode("Light")
            self.DARK_GREY = "#40403f"
            self.LIGHT_BLUE = "#35c2d9"
            self.DARK_BLUE = "#329dae"
            self.WHITE = "#e3e3e3"
            self.BG_COLOR = '#d1d5d8'
        elif theme == "DARK":
            ctk.set_appearance_mode("Dark")
            self.DARK_GREY = "#e3e3e3"
            self.LIGHT_BLUE = "#329dae"
            self.DARK_BLUE = "#35c2d9"
            self.WHITE = "#40403f"
            self.BG_COLOR = '#2a2d2e'

    def load_options(self):
        # Open settings.json file, read contents to embed_modes and options.
        for _ in range(2):
            try:
                with open("./resources/settings.json") as settings_file:
                    self.settings = json.load(settings_file)
                    self.embed_modes = self.settings["modes"]
                    self.options = self.settings["options"]
                # self.check_settings_file()     write this method
                break
            # If file not found, write default settings file.
            except FileNotFoundError:
                self.reset_settings_file()

        self.embed_mode_names = [key for key in self.embed_modes.keys()]
        if len(self.embed_mode_names) == 0:
            pass
            # display error

        # Create output folder for each embed mode.
        os.makedirs("./output", exist_ok=True)
        for embedModeName in self.embed_mode_names:
            os.makedirs(f"./output/{embedModeName}", exist_ok=True)


class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        Options.load_options(self)
        Options.get_colors(self, theme=self.options["theme"])

    def create_top_frame(self):
        self.frame_top = ctk.CTkFrame(master=self, corner_radius=6)
        self.frame_top.grid(row=0, column=0, columnspan=2,
                            sticky="nsew", padx=20, pady=20)
        self.frame_top.rowconfigure((0, 2, 3), minsize=20)
        self.frame_top.rowconfigure(1, minsize=80)
        self.frame_top.columnconfigure((0, 1, 2), weight=1)

    def show(self):
        self.lift()


class LeftFrame(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_logo()

        self.grid_rowconfigure((0, 1), minsize=20)
        self.grid_rowconfigure(2, minsize=self.logo_height)
        self.grid_rowconfigure((3, 4), weight=3)
        self.grid_rowconfigure((5, 6, 7), minsize=20)

        self.create_widgets()

    def read_logo(self):
        with Image.open("./icon.png").convert("RGBA") as logo:
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

        # Log button.
        self.logs_button = ctk.CTkButton(master=self,
                                         text="Logs",
                                         border_width=2,
                                         fg_color=None,
                                         hover_color=self.LIGHT_BLUE,
                                         text_color=self.DARK_GREY,
                                         height=35,
                                         width=150,
                                         corner_radius=20,
                                         text_font=(
                                             "Roboto Bold", -16))
        self.logs_button.grid(row=5, column=0, pady=(20, 20), padx=20)

        # Settings button.
        self.options_button = ctk.CTkButton(master=self,
                                            text="Options",
                                            border_width=2,
                                            fg_color=None,
                                            hover_color=self.LIGHT_BLUE,
                                            text_color=self.DARK_GREY,
                                            height=35,
                                            width=150,
                                            corner_radius=20,
                                            text_font=(
                                                 "Roboto Bold", -16))
        self.options_button.grid(row=6, column=0, pady=(0, 20), padx=20)

        self.version_label = ctk.CTkLabel(master=self,
                                          text="1.1.0",
                                          text_color=self.DARK_GREY,
                                          text_font=("Roboto Bold", -16))  # font name and size in px
        self.version_label.grid(
            row=7, column=0, pady=(0, 20), padx=20, sticky="s")


class EmbedPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(0, weight=2)
        self.create_top_frame()
        self.create_widgets()

    def create_widgets(self):

        # Screen frame title.
        self.select_pdf_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Select PDF",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto Bold", -24))
        self.select_pdf_label.grid(
            row=0, column=0, columnspan=3, pady=(15, 15), padx=20)

        # Screen frame content.
        self.select_file_label = ctk.CTkButton(master=self.frame_top,
                                               text="Drag PDF here.\nOr click to select PDF.",
                                               text_color=self.DARK_GREY,
                                               fg_color=self.WHITE,
                                               text_font=("Roboto Bold", -14),
                                               height=100,
                                               corner_radius=6,
                                               hover_color=self.LIGHT_BLUE)

        self.select_file_label.grid(
            column=0, columnspan=3, row=1, sticky="nwe", padx=20, pady=(0, 20))

        self.select_file_label.drop_target_register(DND_FILES)
        self.select_file_label.dnd_bind("<<Drop>>")

        self.embed_mode_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Select Document Type",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto Bold", -24))
        self.embed_mode_label.grid(
            row=2, column=0, columnspan=3, pady=(15, 15), padx=20)

        self.embed_mode_button = ctk.CTkOptionMenu(master=self.frame_top,
                                                   text_color=self.DARK_GREY,
                                                   dropdown_text_color=self.DARK_GREY,
                                                   fg_color=self.LIGHT_BLUE,
                                                   button_color=self.LIGHT_BLUE,
                                                   button_hover_color=self.DARK_BLUE,
                                                   dropdown_hover_color=self.LIGHT_BLUE,
                                                   height=35,
                                                   width=200,
                                                   corner_radius=20,
                                                   text_font=(
                                                       "Roboto Bold", -16),
                                                   dropdown_text_font=(
                                                       "Roboto Bold", -14))
        self.embed_mode_button.grid(
            row=3, column=0, columnspan=3, pady=(0, 20), padx=20, sticky="nswe")

        self.progresslabel = ctk.CTkLabel(master=self,
                                          text="Select a file to start",
                                          text_color=self.DARK_GREY,
                                          text_font=("Roboto Bold", -20))  # font name and size in px
        self.progresslabel.grid(
            row=4, column=0, columnspan=1, pady=(0, 5), padx=(20, 10))
        self.progressbar = ctk.CTkProgressBar(
            master=self, progress_color=self.LIGHT_BLUE, fg_color=self.DARK_GREY)
        self.progressbar.grid(row=5, column=0, columnspan=1,
                              sticky="nswe", padx=(20, 10), pady=(0, 20))
        self.progressbar.set(0.0)
        self.progressbar.configure(progress_color=self.DARK_GREY)

        self.embed_button = ctk.CTkButton(master=self,
                                          text="Embed",
                                          text_color=self.DARK_GREY,
                                          fg_color=self.LIGHT_BLUE,
                                          hover_color=self.DARK_BLUE,
                                          height=35,
                                          width=150,
                                          corner_radius=20,
                                          text_font=(
                                              "Roboto Bold", -16))
        self.embed_button.grid(row=4, rowspan=2, column=1,
                               pady=(0, 20), padx=(20, 20), sticky="swe")


class OptionsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_top_frame()
        self.frame_top.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_top.grid_rowconfigure((1, 2, 3, 4, 5), minsize=20)
        self.create_widgets()

    def create_widgets(self):
        # top frame.
        self.options_label = ctk.CTkLabel(master=self.frame_top,
                                          text="Options",
                                          text_color=self.DARK_GREY,
                                          text_font=("Roboto Bold", -24))
        self.options_label.grid(
            row=0, column=0, columnspan=3, pady=(15, 15), padx=20)

        self.dark_theme_check = ctk.CTkCheckBox(master=self.frame_top,
                                                text="Dark Mode",
                                                text_color=self.DARK_GREY,
                                                text_font=(
                                                    "Roboto", -16),
                                                hover_color=self.DARK_BLUE,
                                                fg_color=self.LIGHT_BLUE)
        self.dark_theme_check.grid(
            row=1, column=0, pady=4, padx=20, sticky="we")

        self.open_when_done_check = ctk.CTkCheckBox(master=self.frame_top,
                                                    text="Open when Done",
                                                    text_color=self.DARK_GREY,
                                                    text_font=(
                                                        "Roboto", -16),
                                                    hover_color=self.DARK_BLUE,
                                                    fg_color=self.LIGHT_BLUE)
        self.open_when_done_check.grid(
            row=2, column=0, pady=4, padx=20, sticky="we")

        self.open_with_entry = ctk.CTkEntry(master=self.frame_top,
                                            placeholder_text="Open With",
                                            placeholder_text_color=self.DARK_GREY,
                                            fg_color=self.WHITE,
                                            height=35,
                                            border_width=0,
                                            corner_radius=6,
                                            text_font=(
                                                "Roboto", -16))
        self.open_with_entry.grid(row=2, rowspan=1, column=1, columnspan=2,
                                  pady=4, padx=(0, 20), sticky="we")

        self.notify_when_done_check = ctk.CTkCheckBox(master=self.frame_top,
                                                      text="Notify when Done",
                                                      text_color=self.DARK_GREY,
                                                      text_font=(
                                                          "Roboto", -16),
                                                      hover_color=self.DARK_BLUE,
                                                      fg_color=self.LIGHT_BLUE)
        self.notify_when_done_check.grid(
            row=3, column=0, pady=4, padx=20, sticky="we")

        self.def_open_dir_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Initial Open File Directory",
                                               text_color=self.DARK_GREY,
                                               text_font=("Roboto", -16))

        self.def_open_dir_label.grid(
            row=4, column=0, pady=4, padx=20, sticky="w")

        self.def_open_dir_entry = ctk.CTkEntry(master=self.frame_top,
                                               placeholder_text="Default directory",
                                               placeholder_text_color=self.DARK_GREY,
                                               fg_color=self.WHITE,
                                               height=35,
                                               border_width=0,
                                               corner_radius=6,
                                               text_font=(
                                                   "Roboto", -16))
        self.def_open_dir_entry.grid(row=4, rowspan=1, column=1, columnspan=2,
                                     pady=4, padx=(0, 20), sticky="we")

        self.def_win_size_x = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Width",
                                           placeholder_text_color=self.DARK_GREY,
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))

        self.def_win_size_x.grid(
            row=6, column=1, pady=4, padx=0, sticky="we")

        self.def_win_size_y = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Height",
                                           placeholder_text_color=self.DARK_GREY,
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))

        self.def_win_size_y.grid(
            row=6, column=2, pady=4, padx=20, sticky="we")

        self.def_win_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Default Window Size",
                                               text_color=self.DARK_GREY,
                                               text_font=("Roboto", -16))

        self.def_win_size_label.grid(
            row=6, column=0, pady=4, padx=20, sticky="w")

        self.min_win_size_x = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Width",
                                           placeholder_text_color=self.DARK_GREY,
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))

        self.min_win_size_x.grid(
            row=7, column=1, pady=4, padx=0, sticky="we")

        self.min_win_size_y = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Height",
                                           placeholder_text_color=self.DARK_GREY,
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))

        self.min_win_size_y.grid(
            row=7, column=2, pady=4, padx=20, sticky="we")

        self.min_win_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Minimum Window Size",
                                               text_color=self.DARK_GREY,
                                               text_font=("Roboto", -16))

        self.min_win_size_label.grid(
            row=7, column=0, pady=4, padx=20, sticky="w")

        self.max_win_size_x = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Width",
                                           placeholder_text_color=self.DARK_GREY,
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))

        self.max_win_size_x.grid(
            row=9, column=1, pady=4, padx=0, sticky="we")

        self.max_win_size_y = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Height",
                                           placeholder_text_color=self.DARK_GREY,
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))

        self.max_win_size_y.grid(
            row=9, column=2, pady=4, padx=20, sticky="we")

        self.max_win_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Minimum Window Size",
                                               text_color=self.DARK_GREY,
                                               text_font=("Roboto", -16))

        self.max_win_size_label.grid(
            row=9, column=0, pady=4, padx=20, sticky="w")

        # Under top frame.
        self.cancel_button = ctk.CTkButton(master=self,
                                           text="Cancel",
                                           text_color=self.DARK_GREY,
                                           fg_color=self.LIGHT_BLUE,
                                           hover_color=self.DARK_BLUE,
                                           height=35,
                                           width=150,
                                           corner_radius=20,
                                           text_font=(
                                               "Roboto Bold", -16))
        self.cancel_button.grid(row=4, rowspan=2, column=0,
                                pady=(0, 20), padx=(20, 20), sticky="swe")

        self.save_button = ctk.CTkButton(master=self,
                                         text="Save & Return",
                                         text_color=self.DARK_GREY,
                                         fg_color=self.LIGHT_BLUE,
                                         hover_color=self.DARK_BLUE,
                                         height=35,
                                         width=150,
                                         corner_radius=20,
                                         text_font=(
                                              "Roboto Bold", -16))
        self.save_button.grid(row=4, rowspan=2, column=1,
                              pady=(0, 20), padx=(20, 20), sticky="swe")


class LogsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_top_frame()
        self.create_widgets()

    def create_widgets(self):
        # Screen frame title.
        self.logs_label = ctk.CTkLabel(master=self.frame_top,
                                       text="Logs",
                                       text_color=self.DARK_GREY,
                                       text_font=("Roboto Bold", -24))
        self.logs_label.grid(
            row=0, column=0, columnspan=3, pady=(15, 15), padx=20)

        self.filler_button = ctk.CTkButton(master=self,
                                           text="Cancel",
                                           text_color=self.DARK_GREY,
                                           fg_color=self.LIGHT_BLUE,
                                           hover_color=self.DARK_BLUE,
                                           height=35,
                                           width=150,
                                           corner_radius=20,
                                           text_font=(
                                               "Roboto Bold", -16))
        self.filler_button.grid(row=4, rowspan=2, column=0,
                                pady=(0, 20), padx=(20, 20), sticky="swe")

        self.back_button = ctk.CTkButton(master=self,
                                         text="Back",
                                         text_color=self.DARK_GREY,
                                         fg_color=self.LIGHT_BLUE,
                                         hover_color=self.DARK_BLUE,
                                         height=35,
                                         width=150,
                                         corner_radius=20,
                                         text_font=(
                                              "Roboto Bold", -16))
        self.back_button.grid(row=4, rowspan=2, column=1,
                              pady=(0, 20), padx=(20, 20), sticky="swe")


class App(TkinterDnD.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Options.load_options(self)
        Options.get_colors(self, theme=self.options["theme"])

        self.iconbitmap("./icon.ico")
        self.title("Barcode Embedder")
        self.geometry(
            f"{self.options[f'window_default_size'][0]}x" +
            f"{self.options[f'window_default_size'][1]}")
        self.minsize(self.options["window_min_size"][0],
                     self.options["window_min_size"][1])
        self.maxsize(self.options["window_max_size"]
                     [0], self.options["window_max_size"][1])
        # self.configure(bg=self.WHITE)

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

        # Returning from options page
        Options.load_options(self)
        self.embed_page.show()
        self.current_page = "embed"
        self.previous_page = "options"
        self.frame_left.options_button.configure(fg_color=None)

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
