import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from Page import Page


class EmbedPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure(0, weight=2)
        self.create_top_frame()
        self.create_widgets()

    def create_widgets(self):

        # Screen frame title.
        self.select_pdf_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Select PDF",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto Bold", -24))
        self.select_pdf_label.grid(
            row=0, column=0, columnspan=3, pady=(15, 15), padx=20)

        # Screen frame content.
        self.select_file_label = ctk.CTkButton(master=self.frame_top,
                                               text="Drag PDF here.\nOr click to select PDF.",
                                               text_color=self.DARK_GREY,
                                               fg_color=self.WHITE,
                                               text_font=("Roboto Bold", -14),
                                               height=100,
                                               corner_radius=6,
                                               hover_color=self.LIGHT_BLUE)

        self.select_file_label.grid(
            column=0, columnspan=3, row=1, sticky="nwe", padx=20, pady=(0, 20))

        self.select_file_label.drop_target_register(DND_FILES)
        self.select_file_label.dnd_bind("<<Drop>>")

        self.embed_mode_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Select Document Type",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto Bold", -24))
        self.embed_mode_label.grid(
            row=2, column=0, columnspan=3, pady=(15, 15), padx=20)

        self.embed_mode_button = ctk.CTkOptionMenu(master=self.frame_top,
                                                   text_color=self.DARK_GREY,
                                                   dropdown_text_color=self.DARK_GREY,
                                                   fg_color=self.LIGHT_BLUE,
                                                   button_color=self.LIGHT_BLUE,
                                                   button_hover_color=self.DARK_BLUE,
                                                   dropdown_hover_color=self.LIGHT_BLUE,
                                                   height=35,
                                                   width=200,
                                                   corner_radius=20,
                                                   text_font=(
                                                       "Roboto Bold", -16),
                                                   dropdown_text_font=(
                                                       "Roboto Bold", -14))
        self.embed_mode_button.grid(
            row=3, column=0, columnspan=3, pady=(0, 20), padx=20, sticky="nswe")

        self.progresslabel = ctk.CTkLabel(master=self,
                                          text="Select a file to start",
                                          text_color=self.DARK_GREY,
                                          text_font=("Roboto Bold", -20))  # font name and size in px
        self.progresslabel.grid(
            row=4, column=0, columnspan=1, pady=(0, 5), padx=(20, 10))
        self.progressbar = ctk.CTkProgressBar(
            master=self, progress_color=self.LIGHT_BLUE, fg_color=self.DARK_GREY)
        self.progressbar.grid(row=5, column=0, columnspan=1,
                              sticky="nswe", padx=(20, 10), pady=(0, 20))
        self.progressbar.set(0.0)
        self.progressbar.configure(progress_color=self.DARK_GREY)

        self.embed_button = ctk.CTkButton(master=self,
                                          text="Embed",
                                          text_color=self.DARK_GREY,
                                          fg_color=self.LIGHT_BLUE,
                                          hover_color=self.DARK_BLUE,
                                          height=35,
                                          width=150,
                                          corner_radius=20,
                                          text_font=(
                                              "Roboto Bold", -16))
        self.embed_button.grid(row=4, rowspan=2, column=1,
                               pady=(0, 20), padx=(20, 20), sticky="swe")