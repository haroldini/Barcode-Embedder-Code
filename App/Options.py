import customtkinter as ctk
import json
import os


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
                with open("App/resources/settings.json") as settings_file:
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
