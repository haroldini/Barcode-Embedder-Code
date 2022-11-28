import customtkinter as ctk

from Page import Page


class LogsPage(Page):
    def __init__(self, name="Log", *args, **kwargs):
        super().__init__(name="Log", *args, **kwargs)
        self.create_title("Log")
        self.create_top_frame()
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=20)
        self.create_scrollbar()
        self.create_widgets()

    def create_widgets(self):

        self.filler_button = ctk.CTkButton(master=self,
                                           cursor="hand2",
                                           text="Cancel",
                                           text_color=self.DARK_GREY,
                                           fg_color=self.LIGHT_BLUE,
                                           hover_color=self.DARK_BLUE,
                                           height=35,
                                           width=150,
                                           corner_radius=20,
                                           text_font=(
                                               "Roboto", -16))
        self.filler_button.grid(row=4, rowspan=2, column=0,
                                pady=(20, 20), padx=(20, 20), sticky="swe")

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
        self.back_button.grid(row=4, rowspan=2, column=1,
                              pady=(20, 20), padx=(20, 20), sticky="swe")
