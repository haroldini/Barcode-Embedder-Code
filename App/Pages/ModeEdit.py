import customtkinter as ctk
import tkinter as tk

from Page import Page


class ModeEditPage(Page):
    def __init__(self, name="ModeEdit", *args, **kwargs):
        super().__init__(name="ModeEdit", *args, **kwargs)
        self.create_top_frame()
        self.frame_top.grid_columnconfigure(0, minsize=80)
        self.frame_top.grid_columnconfigure((1, 2), weight=1)
        self.frame_top.grid_rowconfigure(0, weight=1)
        self.create_title("ModeEdit")
        self.mode = None
        self.create_widgets()
        self.create_scrollbar()

    def show(self, mode):
        self.mode = mode
        self.title_label.configure(text=mode)
        self.fill_fields()
        self.lift()
        print(self)
        print("hei", mode)

    def create_widgets(self):
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
                                             "Roboto Bold", -16))
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
                                              "Roboto Bold", -16))
        self.save_button.grid(row=4, rowspan=2, column=1,
                              pady=(20, 20), padx=(20, 20), sticky="swe")

    def fill_fields(self):
        self.load_settings()
        mode = self.settings["modes"][self.mode]
        print(mode)
