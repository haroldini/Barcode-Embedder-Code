import customtkinter as ctk

from Page import Page


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
