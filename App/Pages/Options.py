import customtkinter as ctk
import tkinter as tk
import os

from Page import Page


class OptionsPage(Page):
    def __init__(self, name="Options", *args, **kwargs):
        super().__init__(name="Options", *args, **kwargs)

        self.create_top_frame()
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=20)
        self.frame_top.grid_columnconfigure(0, minsize=80)
        self.frame_top.grid_columnconfigure((1, 2), weight=1)
        self.frame_top.grid_rowconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), minsize=20)
        self.create_title("Options")
        self.create_widgets()
        self.create_scrollbar()
        self.fill_fields()

    def create_widgets(self):

        self.edit_mode_field = ctk.CTkOptionMenu(master=self.frame_top,

                                                 text_color=self.DARK_GREY,
                                                 dropdown_text_color=self.DARK_GREY,
                                                 fg_color=self.WHITE,
                                                 button_color=self.LIGHT_BLUE,
                                                 button_hover_color=self.DARK_BLUE,
                                                 dropdown_hover_color=self.LIGHT_BLUE,
                                                 height=35,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16),
                                                 dropdown_text_font=(
                                                     "Roboto", -14))
        self.edit_mode_field.grid(
            row=0, column=0, columnspan=3, pady=(20, 18), padx=(20, 20), sticky="we")

        self.theme_field = ctk.CTkCheckBox(master=self.frame_top,
                                           text="Dark Mode",
                                           text_color=self.DARK_GREY,
                                           text_font=(
                                               "Roboto", -16),
                                           hover_color=self.DARK_BLUE,
                                           fg_color=self.LIGHT_BLUE)
        self.theme_field.grid(
            row=1, column=0, pady=4, padx=20, sticky="we")

        self.open_with_label = ctk.CTkLabel(master=self.frame_top,
                                            text="Open With",
                                            text_color=self.DARK_GREY,
                                            text_font=("Roboto", -16))

        self.open_with_label.grid(
            row=1, column=1, columnspan=2, pady=0, padx=20, sticky="we")

        self.open_when_done_field = ctk.CTkCheckBox(master=self.frame_top,
                                                    text="Open when Done",
                                                    text_color=self.DARK_GREY,
                                                    text_font=(
                                                        "Roboto", -16),
                                                    hover_color=self.DARK_BLUE,
                                                    fg_color=self.LIGHT_BLUE,
                                                    command=self.toggle_open_with_field)
        self.open_when_done_field.grid(
            row=2, column=0, pady=4, padx=20, sticky="we")

        self.open_with_field = ctk.CTkButton(master=self.frame_top,
                                             fg_color=self.WHITE,
                                             hover_color=self.LIGHT_BLUE,
                                             height=35,
                                             border_width=0,
                                             corner_radius=6,
                                             text_font=(
                                                 "Roboto", -16),
                                             command=lambda: self.select_file(type="open_with"))
        self.open_with_field.text_label.configure(anchor="e")
        self.open_with_field.grid(row=2, rowspan=1, column=1, columnspan=2,
                                  pady=4, padx=(0, 20), sticky="we")

        if not self.options["open_when_done"]:
            self.open_with_field.grid_remove()
            self.open_with_label.grid_remove()

        self.notify_when_done_field = ctk.CTkCheckBox(master=self.frame_top,
                                                      text="Notify when Done",
                                                      text_color=self.DARK_GREY,
                                                      text_font=(
                                                          "Roboto", -16),
                                                      hover_color=self.DARK_BLUE,
                                                      fg_color=self.LIGHT_BLUE)
        self.notify_when_done_field.grid(
            row=3, column=0, pady=4, padx=20, sticky="we")

        self.output_dir_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Output Folder",
                                             anchor="w",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto", -16))

        self.output_dir_label.grid(
            row=4, column=0, pady=(18, 4), padx=20, sticky="w")

        self.output_dir_field = ctk.CTkButton(master=self.frame_top,
                                              fg_color=self.WHITE,
                                              hover_color=self.LIGHT_BLUE,
                                              height=35,
                                              border_width=0,
                                              corner_radius=6,
                                              text_font=(
                                                  "Roboto", -16),
                                              command=lambda: self.select_file(type="output_dir"))
        self.output_dir_field.text_label.configure(anchor="e")
        self.output_dir_field.grid(row=4, rowspan=1, column=1, columnspan=2,
                                   pady=(18, 4), padx=(0, 20), sticky="we")

        self.input_dir_label = ctk.CTkLabel(master=self.frame_top,
                                            text="Input Folder",
                                            anchor="w",
                                            text_color=self.DARK_GREY,
                                            text_font=("Roboto", -16))
        self.input_dir_label.grid(
            row=5, column=0, pady=(4, 18), padx=20, sticky="w")

        self.input_dir_field = ctk.CTkButton(master=self.frame_top,
                                             fg_color=self.WHITE,
                                             hover_color=self.LIGHT_BLUE,
                                             height=35,
                                             border_width=0,
                                             corner_radius=6,
                                             text_font=(
                                                 "Roboto", -16),
                                             command=lambda: self.select_file(type="input_dir"))
        self.input_dir_field.text_label.configure(anchor="e")
        self.input_dir_field.grid(row=5, rowspan=1, column=1, columnspan=2,
                                  pady=(4, 18), padx=(0, 20), sticky="we")

        self.def_win_size_x_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="px",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.def_win_size_x_field.grid(
            row=6, column=1, pady=4, padx=0, sticky="we")

        self.def_win_size_y_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="px",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.def_win_size_y_field.grid(
            row=6, column=2, pady=4, padx=20, sticky="we")

        self.def_win_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Default Window Size",
                                               text_color=self.DARK_GREY,
                                               anchor="w",
                                               text_font=("Roboto", -16))

        self.def_win_size_label.grid(
            row=6, column=0, pady=4, padx=20, sticky="w")

        self.min_win_size_x_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="Blank to ignore",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.min_win_size_x_field.grid(
            row=7, column=1, pady=4, padx=0, sticky="we")

        self.min_win_size_y_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="Blank to ignore",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.min_win_size_y_field.grid(
            row=7, column=2, pady=4, padx=20, sticky="we")

        self.min_win_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Minimum Window Size",
                                               text_color=self.DARK_GREY,
                                               anchor="w",
                                               text_font=("Roboto", -16))

        self.min_win_size_label.grid(
            row=7, column=0, pady=4, padx=20, sticky="w")

        self.max_win_size_x_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="Blank to ignore",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.max_win_size_x_field.grid(
            row=8, column=1, pady=(4, 18), padx=0, sticky="we")

        self.max_win_size_y_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="Blank to ignore",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.max_win_size_y_field.grid(
            row=8, column=2, pady=(4, 18), padx=20, sticky="we")

        self.max_win_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Maximum Window Size",
                                               text_color=self.DARK_GREY,
                                               anchor="w",
                                               text_font=("Roboto", -16))

        self.max_win_size_label.grid(
            row=8, column=0, pady=(4, 18), padx=20, sticky="we")

        # Restore defaults buttons. Frame needed to ignore parent frame columnconfigure.
        self.reset_buttons_frame = ctk.CTkFrame(
            master=self.frame_top, fg_color=self.LIGHT_GREY)
        self.reset_buttons_frame.grid(
            row=9, column=0, columnspan=3, sticky="nswe")
        self.reset_buttons_frame.grid_columnconfigure((0, 1), weight=1)
        self.reset_buttons_frame.grid_rowconfigure(1, weight=1)

        self.restore_settings_button = ctk.CTkButton(master=self.reset_buttons_frame,
                                                     cursor="hand2",
                                                     text="Restore Default Settings",
                                                     text_color=self.DARK_GREY,
                                                     fg_color=self.WHITE,
                                                     hover_color=self.LIGHT_BLUE,
                                                     height=35,
                                                     corner_radius=6,
                                                     text_font=(
                                                         "Roboto", -16))
        self.restore_settings_button.grid(row=0, column=0,
                                          pady=(4, 0), padx=(20, 10), sticky="nswe")

        self.restore_presets_button = ctk.CTkButton(master=self.reset_buttons_frame,
                                                    cursor="hand2",
                                                    text="Restore Default Presets",
                                                    text_color=self.DARK_GREY,
                                                    fg_color=self.WHITE,
                                                    hover_color=self.LIGHT_BLUE,
                                                    height=35,
                                                    corner_radius=6,
                                                    text_font=(
                                                         "Roboto", -16))
        self.restore_presets_button.grid(row=0, column=1,
                                         pady=(4, 0), padx=(10, 20), sticky="nswe")

        # Under top frame.
        self.back_button = ctk.CTkButton(master=self,
                                         cursor="hand2",
                                         text="Back",
                                         text_color=self.DARK_GREY,
                                         fg_color=self.LIGHT_BLUE,
                                         hover_color=self.DARK_BLUE,
                                         height=35,
                                         width=150,
                                         corner_radius=20,
                                         text_font=(
                                             "Roboto", -16))
        self.back_button.grid(row=4, rowspan=2, column=0,
                              pady=(20, 20), padx=(20, 20), sticky="swe")

        self.save_button = ctk.CTkButton(master=self,
                                         cursor="hand2",
                                         text="Save & Return",
                                         text_color=self.DARK_GREY,
                                         fg_color=self.LIGHT_BLUE,
                                         hover_color=self.DARK_BLUE,
                                         height=35,
                                         width=150,
                                         corner_radius=20,
                                         text_font=(
                                              "Roboto", -16))
        self.save_button.grid(row=4, rowspan=2, column=1,
                              pady=(20, 20), padx=(20, 20), sticky="swe")

    def toggle_open_with_field(self):
        if self.open_when_done_field.get():
            self.open_with_field.grid(row=2, rowspan=1, column=1, columnspan=2,
                                      pady=4, padx=(0, 20), sticky="we")
            self.open_with_label.grid(row=1, column=1, columnspan=2,
                                      pady=0, padx=20, sticky="we")
        else:
            self.open_with_field.grid_remove()
            self.open_with_label.grid_remove()

    def fill_fields(self):
        self.load_settings()
        check_fields = [
            "theme", "open_when_done", "notify_when_done"]
        button_fields = [
            "input_dir", "output_dir", "open_with"]
        numeric_fields = [
            "def_win_size_x", "def_win_size_y",
            "min_win_size_x", "min_win_size_y",
            "max_win_size_x", "max_win_size_y"]

        for field in numeric_fields:
            self.__getattribute__(f"{field}_field").delete(
                0, ctk.END)
            if self.options[field] is None:
                self.__getattribute__(f"{field}_field").insert(
                    0, "None")
            else:
                self.__getattribute__(f"{field}_field").insert(
                    0, self.options[field])

        for field in button_fields:
            self.__getattribute__(f"{field}_field").configure(
                text=self.options[field]
            )

        for field in check_fields:
            if self.options[field]:
                self.__getattribute__(f"{field}_field").select()
            else:
                self.__getattribute__(f"{field}_field").deselect()

        self.edit_mode_field.configure(
            values=list(self.settings["modes"].keys())+["Add New"])
        self.edit_mode_field.text_label["text"] = "Edit Document Preset"

    def select_file(self, type):
        currentdir = self.__getattribute__(f"{type}_field").text_label["text"]
        print(currentdir)
        if type == "open_with":
            currentdir = os.path.dirname(currentdir)
            directory = tk.filedialog.askopenfilename(
                initialdir=currentdir if currentdir else "./",
                title=f"Select an 'Open With' file.",
                filetypes=[("EXE files", ".EXE .exe")])
        elif type == "output_dir" or type == "input_dir":
            directory = tk.filedialog.askdirectory(
                initialdir=currentdir if currentdir is not None else "./",
                title=f"Select an '{type}'."
            )

        if directory != "":
            self.__getattribute__(f"{type}_field").configure(
                text=directory)
        print(directory)
