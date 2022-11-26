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
from copy import deepcopy

from Page import Page
from Options import Options
from Pages.Options import OptionsPage
from Pages.Embed import EmbedPage
from Pages.Log import LogsPage
from Pages.ModeEdit import ModeEditPage
from Pages.LeftFrame import LeftFrame

DELAY = 500
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

        # Load options.
        Options.load_settings(self)
        Options.get_colors(self, theme=self.options["theme"])
        self.iconbitmap("App/resources/icon.ico")
        self.title("Barcode Embedder")
        self.bind_all("<Button>", self.reset_focus)

        # Set window size.
        self.geometry(f"{self.options[f'def_win_size_x'] if self.options[f'def_win_size_x'] is not None else 880}x" +
                      f"{self.options[f'def_win_size_y'] if self.options[f'def_win_size_y'] is not None else 520}")
        self.configure_app()

        # Prep gui.
        self.current_page = "embed"
        self.previous_page = "embed"
        self.error = None

        # Create gui
        self.create_pages()
        self.embed_page.lift()
        self.create_button_handlers()

        # Prep embedder
        self.active_file = None
        self.active_mode = None

        # Run app.
        self.after(DELAY, self.update_app)
        self.mainloop()

    def update_app(self):
        print(self.error)
        print(self.active_mode)
        print(self.active_file)
        self.after(DELAY, self.update_app)

    def configure_app(self):
        self.configure(bg=self.WHITE)
        self.minsize(self.options["min_win_size_x"] if self.options["min_win_size_x"] is not None else 0,
                     self.options["min_win_size_y"] if self.options["min_win_size_y"] is not None else 0)
        self.maxsize(self.options["max_win_size_x"] if self.options["max_win_size_x"] is not None else 0,
                     self.options["max_win_size_y"] if self.options["max_win_size_y"] is not None else 0)

    def create_pages(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.options_page = OptionsPage(self)
        self.mode_edit_page = ModeEditPage(self)
        self.embed_page = EmbedPage(self)
        self.logs_page = LogsPage(self)
        self.frame_left = LeftFrame(self)

        self.embed_page.grid(row=0, column=1,
                             rowspan=3, padx=20, pady=20, sticky="nsew")
        self.options_page.grid(row=0, column=1, padx=20,
                               pady=20, sticky="nsew")
        self.mode_edit_page.grid(row=0, column=1, sticky="nsew",
                                 padx=20, pady=20)
        self.logs_page.grid(row=0, column=1, padx=20,
                            pady=20, sticky="nsew")
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nswe")

        self.pages = [self.options_page, self.embed_page,
                      self.logs_page, self.mode_edit_page]

        # Make scrollable regions of the pages change size with window resize.
        for page in self.pages:
            page.frame_top.bind('<Enter>', page._bound_to_mousewheel)
            page.frame_top.bind('<Leave>', page._unbound_to_mousewheel)
            page.canvas_scroll.bind("<Configure>", page.onCanvasConfigure)
            page.canvas_scroll.configure(
                scrollregion=page.canvas_scroll.bbox('all'))

    def create_button_handlers(self):
        self.frame_left.options_button.configure(
            command=self.options_button_handler)
        self.frame_left.logs_button.configure(
            command=self.logs_button_handler)

        self.embed_page.embed_button.configure(
            command=self.embed_button_handler)
        self.embed_page.embed_mode_button.configure(
            command=self.embed_mode_button_handler)
        self.embed_page.select_pdf_button.configure(
            command=self.select_pdf_button_handler)
        self.embed_page.select_pdf_button.drop_target_register(DND_FILES)
        self.embed_page.select_pdf_button.dnd_bind(
            "<<Drop>>", self.select_pdf_button_handler)

        self.logs_page.back_button.configure(
            command=self.logs_back_button_handler)

        self.options_page.back_button.configure(
            command=self.options_back_button_handler)
        self.options_page.save_button.configure(
            command=self.options_save_button_handler)
        self.options_page.edit_mode_field.configure(
            command=lambda mode: self.mode_edit_page.show(mode))
        self.options_page.restore_presets_button.configure(
            command=self.options_restore_presets_button_handler)
        self.options_page.restore_settings_button.configure(
            command=self.options_restore_settings_button_handler)

        self.mode_edit_page.back_button.configure(
            command=self.edit_mode_back_button_handler)
        self.mode_edit_page.save_button.configure(
            command=self.edit_mode_save_button_handler)
        self.mode_edit_page.delete_button.configure(
            command=self.edit_mode_delete_button_handler)

    def embed_mode_button_handler(self, event):
        self.active_mode = event

        if self.active_file is not None:
            self.embed_page.embed_button.configure(state="normal")
            self.embed_page.progresslabel.configure(
                text="Click Embed to continue")
        else:
            self.embed_page.embed_button.configure(state="disabled")
            self.embed_page.progresslabel.configure(
                text="Select a file to start")

    def select_pdf_button_handler(self, event=None):
        print("select file")
        if event:
            file = event.data
        else:
            file = tk.filedialog.askopenfilename(
                initialdir=self.options["input_dir"], title="Select a PDF", filetypes=[("PDF files", ".PDF .pdf")])
        self.change_active_file(file)

    def change_active_file(self, file):
        # If no file selected.
        if file == "":
            return
        # Removes curly brackets when filename contains spaces.
        if file.startswith("{") and file.endswith("}"):
            file = file[1:-1]
        if file.endswith(".pdf"):
            self.active_file = file
            self.active_file_name = self.active_file.split("/")[-1]
            self.embed_page.select_pdf_button.configure(
                text=self.active_file_name)

            if self.active_mode is not None:
                self.embed_page.embed_button.configure(state="normal")
                self.embed_page.progresslabel.configure(
                    text="Click Embed to continue")
            else:
                self.embed_page.embed_button.configure(state="disabled")
                self.embed_page.progresslabel.configure(
                    text="Select a preset to continue")

    def embed_button_handler(self):
        print("embed button pressed")
        print(self.active_file)
        print(self.active_mode)

    def options_restore_presets_button_handler(self):
        Options.reset_settings_file("modes")
        Options.load_settings(self)
        self.embed_page.embed_mode_button.configure(
            values=list(self.settings["modes"].keys()))
        self.options_page.edit_mode_field.configure(
            values=list(list(self.settings["modes"].keys())+["Add New"]))

    def options_restore_settings_button_handler(self):
        Options.reset_settings_file("options")
        Options.load_settings(self)
        Options.get_colors(self, theme=self.options["theme"])
        self.configure_app()
        self.create_pages()
        self.create_button_handlers()

        self.frame_left.options_button.configure(fg_color=self.LIGHT_BLUE)
        self.frame_left.options_button.configure(state="disabled")
        self.frame_left.logs_button.configure(state="disabled")
        self.frame_left.logs_button.configure(fg_color=None)
        self.options_page.lift()

    def options_button_handler(self):
        if self.current_page != "options":
            Options.load_settings(self)
            self.options_page.fill_fields()
            self.options_page.lift()
            self.previous_page = self.current_page
            self.current_page = "options"
            self.frame_left.options_button.configure(fg_color=self.LIGHT_BLUE)
            self.frame_left.options_button.configure(state="disabled")
            self.frame_left.logs_button.configure(state="disabled")
            self.frame_left.logs_button.configure(fg_color=None)

    def logs_button_handler(self):
        if self.current_page != "logs":
            self.logs_page.lift()
            self.previous_page = self.current_page
            self.current_page = "logs"
            self.frame_left.logs_button.configure(fg_color=self.LIGHT_BLUE)
            self.frame_left.options_button.configure(fg_color=None)
            return

        self.embed_page.lift()
        self.current_page = "embed"
        self.previous_page = "logs"
        self.frame_left.logs_button.configure(fg_color=None)

    def options_back_button_handler(self):
        if self.current_page == "options":
            self.previous_page = self.current_page
            self.current_page = "embed"
            self.error = None
            self.frame_left.options_button.configure(fg_color=None)
            self.frame_left.options_button.configure(state="normal")
            self.frame_left.logs_button.configure(state="normal")
            self.embed_page.embed_mode_button.configure(
                values=list(self.settings["modes"].keys()))
            self.embed_page.embed_mode_button.text_label["text"] = "Select Document Preset"
            self.active_mode = None
            self.active_file = None
            self.embed_page.lift()

    def options_save_button_handler(self):
        if self.current_page == "options":

            # Create new settings dict from options form.
            self.error = None
            with open("App/resources/settings.json", "r") as settings_file:
                settings = json.load(settings_file)
            prev_settings = deepcopy(settings)
            settings = Options.create_new_options(self, settings)
            # ensure both directories are valid directories somehow.

            # Save new settings dictionary.
            if self.error is None:
                with open("App/resources/settings.json", "w") as settings_file:
                    settings_file.write(json.dumps(settings, indent=4))

                # Reload settings and colours.
                Options.load_settings(self)
                if prev_settings["options"]["theme"] != self.settings["options"]["theme"]:
                    Options.get_colors(self, theme=self.options["theme"])
                    self.create_pages()
                    self.create_button_handlers()
                self.configure_app()
                self.frame_left.options_button.configure(fg_color=None)
                self.frame_left.options_button.configure(state="normal")
                self.frame_left.logs_button.configure(state="normal")
                self.embed_page.embed_mode_button.configure(
                    values=list(self.settings["modes"].keys()))
                self.embed_page.embed_mode_button.text_label["text"] = "Select Document Preset"

                # Navigate to embed page.
                self.previous_page = self.current_page
                self.current_page = "embed"
                self.active_mode = None
                self.active_file = None
                self.embed_page.lift()

    def edit_mode_back_button_handler(self):
        self.error = None
        self.options_page.edit_mode_field.text_label["text"] = "Edit Document Preset"
        self.options_page.lift()

    def edit_mode_save_button_handler(self):
        if self.current_page == "options":

            self.error = None
            with open("App/resources/settings.json", "r") as settings_file:
                settings = json.load(settings_file)

            new_mode = Options.create_new_modes(self)
            # Save new mode.
            if self.error is None:
                new_mode_name, new_mode_options = new_mode
                old_mode_name = self.mode_edit_page.mode

                # If not "Add New", delete old mode.
                if old_mode_name != "Add New":
                    settings["modes"].pop(old_mode_name)
                settings["modes"][new_mode_name] = new_mode_options

                with open("App/resources/settings.json", "w") as settings_file:
                    settings_file.write(json.dumps(settings, indent=4))

                # Apply mode changes to mode dropdowns, navigate to options page.
                self.nav_from_mode_to_options()

    def nav_from_mode_to_options(self):
        Options.load_settings(self)
        self.embed_page.embed_mode_button.configure(
            values=list(self.settings["modes"].keys()))
        self.options_page.edit_mode_field.configure(
            values=list(list(self.settings["modes"].keys())+["Add New"]))
        self.options_page.edit_mode_field.text_label["text"] = "Edit Document Preset"
        self.options_page.lift()

    def edit_mode_delete_button_handler(self):
        with open("App/resources/settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            if len(settings["modes"]) > 1:
                settings["modes"].pop(self.mode_edit_page.mode)
                with open("App/resources/settings.json", "w") as settings_file:
                    settings_file.write(json.dumps(settings, indent=4))
                self.nav_from_mode_to_options()
            else:
                self.error = "Cannot delete only preset. Create a new preset first."

    def logs_back_button_handler(self):
        if self.current_page == "logs":
            self.previous_page = self.current_page
            self.current_page = "embed"
            self.frame_left.logs_button.configure(fg_color=None)
            self.embed_page.lift()

    def reset_focus(self, event):
        event.widget.focus_set()


if __name__ == "__main__":
    app = App()
