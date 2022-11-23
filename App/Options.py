import customtkinter as ctk
import json
import os


class Options():
    def __init__(self):
        self.error = None
        self.load_settings()
        self.get_colors()

    def get_colors(self, theme=0):
        ctk.set_default_color_theme("blue")
        if theme == 0:
            ctk.set_appearance_mode("Light")
            self.DARK_GREY = "#40403f"
            self.LIGHT_BLUE = "#35c2d9"
            self.DARK_BLUE = "#329dae"
            self.WHITE = "#e3e3e3"
            self.BG_COLOR = '#d1d5d8'
        elif theme == 1:
            ctk.set_appearance_mode("Dark")
            self.DARK_GREY = "#e3e3e3"
            self.LIGHT_BLUE = "#329dae"
            self.DARK_BLUE = "#35c2d9"
            self.WHITE = "#40403f"
            self.BG_COLOR = '#2a2d2e'

    def load_settings(self):

        for _ in range(2):
            try:
                with open("App/resources/settings.json") as settings_file:
                    settings = json.load(settings_file)
                    with open("App/resources/settings_default.json", "r") as defaults_file:
                        defaults = json.load(defaults_file)
                Options.validate_settings(self, settings, defaults)
                break

            # If settings not found, write default settings file.
            except FileNotFoundError as e:
                self.error = "Settings file not found."
                Options.reset_settings_file()
            except json.decoder.JSONDecodeError as e:
                self.error = "Settings file invalid JSON."
                Options.reset_settings_file()

        self.embed_mode_names = [key for key in self.embed_modes.keys()]

        # Create output folder for each embed mode.
        os.makedirs("./output", exist_ok=True)
        for embedModeName in self.embed_mode_names:
            os.makedirs(f"./output/{embedModeName}", exist_ok=True)

    @staticmethod
    def reset_settings_file(self):
        with open("App/resources/settings_default.json", "r+") as infile:
            with open("App/resources/settings.json", "w") as outfile:
                outfile.write(json.dumps(json.load(infile), indent=4))

    @staticmethod
    def validate_settings(self, settings, defaults):
        # Check options and modes exists.
        if not all(x in settings for x in ["options", "modes"]):
            self.error = "Settings file invalid structure."
            Options.reset_settings_file()

        # Check all options are present.
        if not sorted(defaults["options"].keys()) == sorted(settings["options"].keys()):
            self.error = "Settings file missing options."
            Options.reset_settings_file()

        # Check length of modes > 0:
        if len(settings["modes"]) == 0:
            self.error = "Settings file missing document types."
            # Require user to add new document type.

        self.embed_modes = settings["modes"]
        self.options = settings["options"]
        self.settings = settings
