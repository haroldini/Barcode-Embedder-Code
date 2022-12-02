import customtkinter as ctk
import json
from json_checker import Checker, Or, And
import os


class Options():
    def __init__(self):
        self.error = None
        self.load_settings()
        self.get_colors()

    @staticmethod
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
            self.ERROR = "#d92d02"
        elif theme == 1:
            ctk.set_appearance_mode("Dark")
            self.DARK_GREY = "#e3e3e3"
            self.LIGHT_GREY = "#343638"
            self.LIGHT_BLUE = "#329dae"
            self.DARK_BLUE = "#35c2d9"
            self.WHITE = "#40403f"
            self.BG_COLOR = '#2a2d2e'
            self.ERROR = "#d92d02"

    @staticmethod
    def load_settings(self):
        error = None

        # Attempts: reset options, reset modes, reset all, final attempt
        for _ in range(2):
            try:
                with open("App/resources/settings.json") as settings_file:
                    settings = json.load(settings_file)
                validate = Options.validate_settings_file(self, settings)
                if not error:
                    error = validate
                break

            # If settings not found, write default settings file.
            except FileNotFoundError as e:
                error = "Settings file not found. Default settings restored."
                Options.reset_settings_file("both")

            except json.decoder.JSONDecodeError as e:
                error = "Settings file invalid. Default settings restored."
                Options.reset_settings_file("both")

        # Create output folder for each embed mode.
        output = settings["options"]["output_dir"]
        foldername = "Barcode Embedder Output"
        os.makedirs(f"{output}/{foldername}", exist_ok=True)
        for embed_mode in [key for key in self.embed_modes.keys()]:
            os.makedirs(f"{output}/{foldername}/{embed_mode}", exist_ok=True)

        return error

    @staticmethod
    def reset_settings_file(to_reset="both"):
        with open("App/resources/settings_default.json", "r") as default_file:
            if to_reset == "both":
                with open("App/resources/settings.json", "w") as outfile:
                    outfile.write(json.dumps(
                        json.load(default_file), indent=4))
            elif to_reset == "modes" or to_reset == "options":
                with open("App/resources/settings.json", "r") as current_file:
                    settings = json.load(current_file)
                    default = json.load(default_file)
                    settings[to_reset] = default[to_reset]
                    with open("App/resources/settings.json", "w") as outfile:
                        outfile.write(json.dumps(settings, indent=4))

    @staticmethod
    def validate_settings_file(self, settings):
        error = None

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
            "ID_start": str,
            "ID_length": int,
            "start_page": int,
            "skip_pages": list,
            "barcode_type": str,
            "barcode_size_x": int,
            "barcode_size_y": int,
            "barcode_location_x": int,
            "barcode_location_y": int,
        }
        Checker(settings_schema, soft=True).validate(settings)
        Checker(options_schema, soft=True).validate(settings["options"])
        for mode in settings["modes"]:
            Checker(modes_schema, soft=True).validate(
                settings["modes"][mode])

        # Check length of modes > 0:
        if len(settings["modes"]) == 0:
            error = "Settings file missing document presets. Default settings restored."
            Options.reset_settings_file(to_reset="modes")
            with open("App/resources/settings.json") as settings_file:
                settings = json.load(settings_file)
            validate = Options.validate_settings_file(self, settings)
            if not error:
                error = validate

        self.embed_modes = settings["modes"]
        self.options = settings["options"]
        self.settings = settings
        return error

    @staticmethod
    def create_new_options(self, settings):
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
                f"{directory_key}_field").text_label["text"]

        # Create window size settings
        for win_size_key in win_size_keys:
            win_size_value = self.options_page.__getattribute__(
                f"{win_size_key}_field").get()
            Options.validate_win_size_options(
                self, settings, win_size_key, win_size_value)

        Options.validate_new_options(
            self, settings, checkbox_keys, directory_keys)
        return settings

    @staticmethod
    def validate_new_options(self, settings, checkbox_keys, directory_keys):
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
            if not os.path.isdir(options["input_dir"]) or not os.path.isdir(options["output_dir"]):
                self.error = "Input/output folders must be a folders, not files."

    @staticmethod
    def validate_win_size_options(self, settings, win_size_key, win_size_value):
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

    @staticmethod
    def create_new_modes(self, settings, mode):
        fields = ["ID_start", "ID_length",
                  "start_page", "skip_pages",
                  "barcode_type", "barcode_size_x", "barcode_size_y",
                  "barcode_location_x", "barcode_location_y"]
        numeric_fields = ["barcode_location_x", "barcode_location_y",
                          "barcode_size_x", "barcode_size_y",
                          "ID_length", "start_page"]

        new_mode_options = {}

        # Loop fields to validate they are filled.
        for field in fields:
            field_value = self.mode_edit_page.__getattribute__(
                f"{field}_field").get()
            if field_value == "" and field != "skip_pages":
                self.error = "All fields except 'Skip Pages', are required to create a document preset."
                return

        # Loop fields to validate their content.
        for field in fields:
            field_value = self.mode_edit_page.__getattribute__(
                f"{field}_field").get()

            Options.validate_new_mode_field(self, field, field_value)
            print("x", self.error)
            if self.error:
                return

            if field in numeric_fields:
                new_mode_options[field] = int(field_value)
            elif field == "skip_pages":
                if field_value == "":
                    new_mode_options[field] = []
                else:
                    sp_list = [int(val)
                               for val in field_value.replace(" ", "").split(",")]
                    new_mode_options[field] = sp_list
            else:  # field = string
                new_mode_options[field] = field_value

        # Validate name.
        new_mode_name = self.mode_edit_page.name_field.get()
        if len(new_mode_name) < 1 or len(new_mode_name) > 60:
            self.error = "Preset name must be between 1 and 60 characters."
            return

        # Prevent duplicate presets
        if mode == "Add New":
            if new_mode_name in settings["modes"]:
                self.error = "That preset name is already in use."
                return
        elif mode != new_mode_name:
            if new_mode_name in settings["modes"]:
                self.error = "That preset name is already in use."
                return

        return new_mode_name, new_mode_options

    @staticmethod
    def validate_new_mode_field(self, field, field_value):
        locations = ["barcode_location_x", "barcode_location_y"]
        numeric_fields = ["barcode_location_x", "barcode_location_y",
                          "barcode_size_x", "barcode_size_y",
                          "ID_length", "start_page"]

        # Validate string fields.
        if field == "barcode_type" or field == "ID_start":
            field_name = field.replace("_", " ").title()
            if len(field_value) > 100:
                self.error = f"{field_name} cannot contain more than 100 characters"
                return

        # Valid barcode types.
        if field == "barcode_type":
            valid_barcodes = ["Code39", "Code128", "PZN",
                              "EuropeanArticleNumber13", "EuropeanArticleNumber8",
                              "JapanArticleNumber", "InternationalStandardBookNumber13",
                              "InternationalStandardBookNumber10",
                              "InternationalStandardSerialNumber",
                              "UniversalProductCodeA", "EuropeanArticleNumber14",
                              "Gs1_128"]
            if field_value not in valid_barcodes:
                self.error = f"{field_value} is not a valid barcode type."

        # Validate that numeric fields have numeric input.
        if field in numeric_fields:
            try:
                field_value = int(field_value)
            except ValueError:
                field_name = field.replace("_", " ").title()
                self.error = f"{field_name} requires numeric input"
                return

        # Numeric fields validation
        if field == "ID_length":
            if field_value > 128 or field_value < 1:
                self.error = "ID Length must be between 1 and 128"

        if field == "barcode_size_x":
            if field_value > 2000 or field_value < 50:
                self.error = "Barcode width must be between 50 and 2000"
                return
        if field == "barcode_size_y":
            if field_value > 1000 or field_value < 10:
                self.error = "Barcode height must be between 10 and 1000"
                return
        if field in locations:
            if field_value > 10000 or field_value < 1:
                self.error = "Barcode location must be between 0 and 10,000"
                return
        if field == "start_page":
            if field_value < 1:
                self.error = "Start page cannot be less than 1"
                return
            if field_value > 10000:
                self.error = "Start page cannot be greater than 10,000"
                return

        # List field validation
        if field == "skip_pages":
            field_values = field_value.replace(" ", "").split(",")

            # Skip none.
            if field_value == "":
                return

            # Ensure less than 100 items in list.
            if len(field_values) > 100:
                self.error = "Cannot skip more than 100 pages"
                return

            # Ensure skipped pages are valid numbers.
            for val in field_values:
                try:
                    val = int(val)
                except ValueError:
                    self.error = "Skipped pages must be numbers"
                    return
                if val < 1:
                    self.error = "Skipped pages cannot be less than 1"
                    return
                if val > 10000:
                    self.error = "Skipped pages cannot be greater than 10,000"
                    return
