import customtkinter as ctk
import json
from json_checker import Checker, Or, And
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
            self.LIGHT_GREY = "#bfc6cc"
            self.LIGHT_BLUE = "#35c2d9"
            self.DARK_BLUE = "#329dae"
            self.WHITE = "#e3e3e3"
            self.BG_COLOR = '#d1d5d8'
        elif theme == 1:
            ctk.set_appearance_mode("Dark")
            self.DARK_GREY = "#e3e3e3"
            self.LIGHT_GREY = "#343638"
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
                Options.validate_settings_file(self, settings)
                break

            # If settings not found, write default settings file.
            except FileNotFoundError as e:
                self.error = "Settings file not found."
                Options.reset_settings_file()
            except json.decoder.JSONDecodeError as e:
                self.error = "Settings file invalid JSON."
                Options.reset_settings_file()

        # Create output folder for each embed mode.
        os.makedirs("./output", exist_ok=True)
        for embed_mode in [key for key in self.embed_modes.keys()]:
            os.makedirs(f"./output/{embed_mode}", exist_ok=True)

    @staticmethod
    def reset_settings_file():
        with open("App/resources/settings_default.json", "r+") as infile:
            with open("App/resources/settings.json", "w") as outfile:
                outfile.write(json.dumps(json.load(infile), indent=4))

    @staticmethod
    def validate_settings_file(self, settings):

        settings_schema = {
            "modes": dict,
            "options": dict
        }
        options_schema = {
            "input_dir": str,
            "output_dir": str,
            "open_when_done": int,
            "notify_when_done": int,
            "open_with": str,
            "theme": int,
            "def_win_size_x": Or(int, None),
            "def_win_size_y": Or(int, None),
            "min_win_size_x": Or(int, None),
            "min_win_size_y": Or(int, None),
            "max_win_size_x": Or(int, None),
            "max_win_size_y": Or(int, None)
        }
        modes_schema = {
            "orderID_start": str,
            "orderID_length": int,
            "start_page": int,
            "skip_pages": list,
            "barcode_type": str,
            "barcode_size": list,
            "barcode_location": list
        }
        Checker(settings_schema, soft=True).validate(settings)
        Checker(options_schema, soft=True).validate(settings["options"])
        for mode in settings["modes"]:
            Checker(modes_schema, soft=True).validate(
                settings["modes"][mode])

        # Check length of modes > 0:
        if len(settings["modes"]) == 0:
            self.error = "Settings file missing document types."
            # Require user to add new document type.

        self.embed_modes = settings["modes"]
        self.options = settings["options"]
        self.settings = settings

    @staticmethod
    def create_new_settings(self, settings):
        checkbox_keys = ["theme", "open_when_done", "notify_when_done"]
        directory_keys = ["open_with", "input_dir", "output_dir"]
        win_size_keys = ["def_win_size_x", "def_win_size_y",
                         "min_win_size_x", "min_win_size_y",
                         "max_win_size_x", "max_win_size_y"]

        # Create checkbox settings.
        for checkbox_key in checkbox_keys:
            settings["options"][checkbox_key] = self.options_page.__getattribute__(
                f"{checkbox_key}_field").get()

        # Create directory settings.
        for directory_key in directory_keys:
            settings["options"][directory_key] = self.options_page.__getattribute__(
                f"{directory_key}_field").get()

        # Create window size settings
        for win_size_key in win_size_keys:
            win_size_value = self.options_page.__getattribute__(
                f"{win_size_key}_field").get()
            Options.validate_win_size_setting(
                self, settings, win_size_key, win_size_value)

        Options.validate_new_settings(
            self, settings, checkbox_keys, directory_keys)
        return settings

    @staticmethod
    def validate_new_settings(self, settings, checkbox_keys, directory_keys):
        options = settings["options"]

        # Ensure window sizes adhere to min<def<max.
        prevent_these = ["def_win_size_x", "def_win_size_y", "max_win_size_x",
                         "max_win_size_y", "max_win_size_x", "max_win_size_x"]
        less_than_these = ["min_win_size_x", "min_win_size_y", "min_win_size_x",
                           "min_win_size_y", "def_win_size_x", "def_win_size_y"]

        for i, prevent_this in enumerate(prevent_these):
            if type(options[prevent_this]) == int and type(options[less_than_these[i]]) == int:
                if options[prevent_this] < options[less_than_these[i]]:
                    self.error = "Window size settings must adhere to 'minimum < default < maximum'."

        # Ensure checkboxes have value 0 or 1.
        for checkbox_key in checkbox_keys:
            if not self.options_page.__getattribute__(f"{checkbox_key}_field").get() in [0, 1]:
                self.error = "Checkbox entries invalid."

        # Ensure directories exist.
        for directory_key in directory_keys:
            if not os.path.exists(options[directory_key]):
                self.error = f"{directory_key} is not a valid directory."
                break

        # Ensure directories are correct files
        else:
            if not options["open_with"].endswith(".exe"):
                self.error = f"Open with must be a valid .exe file."
            if not os.path.isdir(options["input_dir"]):
                self.error = "Default input folder must be a folder, not a file."

    @staticmethod
    def validate_win_size_setting(self, settings, win_size_key, win_size_value):
        options = settings["options"]

        # If input can be converted to int type, set it as setting.
        try:
            win_size_value = int(win_size_value)
            options[win_size_key] = win_size_value

        # If input cannot be converted to int, it is either "none" or invalid.
        except ValueError:
            if win_size_value == "" or win_size_value.lower() == "none":
                options[win_size_key] = None
            else:
                self.error = "Window size fields should contain only numbers or 'None'."

        # Ensure window size settings between min and max value.
        if options[win_size_key] is not None:
            if options[win_size_key] < 100 or options[win_size_key] > 2000:
                self.error = "Window size settings must be between 100 and 2000, or 'None'."
