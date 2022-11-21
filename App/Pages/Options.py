import customtkinter as ctk

from Page import Page
from Options import Options


class OptionsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_top_frame()
        self.frame_top.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame_top.grid_rowconfigure((1, 2, 3, 4, 5), minsize=20)
        self.create_widgets()
        Options.load_options(self)
        print(self.options)

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
            row=5, column=0, pady=4, padx=20, sticky="w")

        self.def_open_dir_entry = ctk.CTkEntry(master=self.frame_top,
                                               placeholder_text="Default directory",
                                               placeholder_text_color=self.DARK_GREY,
                                               fg_color=self.WHITE,
                                               height=35,
                                               border_width=0,
                                               corner_radius=6,
                                               text_font=(
                                                   "Roboto", -16))
        self.def_open_dir_entry.grid(row=5, rowspan=1, column=1, columnspan=2,
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
