import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from Page import Page


class EmbedPage(Page):
    def __init__(self, name="Embed", *args, **kwargs):
        super().__init__(name="Embed", *args, **kwargs)
        self.create_top_frame()
        self.create_widgets()
        self.create_scrollbar()
        self.frame_top.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=20)
        self.frame_top.grid_rowconfigure(0, minsize=120)
        self.frame_top.grid_rowconfigure((1, 2, 3), minsize=20)
        self.frame_top.grid_rowconfigure(4, minsize=40)

    def create_widgets(self):

        # Screen frame content.
        self.select_pdf_button = ctk.CTkButton(master=self.frame_top,
                                               cursor="hand2",
                                               text="Drag PDF here.\nOr click to select PDF.",
                                               text_color=self.DARK_GREY,
                                               fg_color=self.WHITE,
                                               text_font=("Roboto", -14),
                                               height=100,
                                               corner_radius=6,
                                               hover_color=self.LIGHT_BLUE)

        self.select_pdf_button.grid(
            column=0, columnspan=3, row=0, sticky="nwe", padx=20, pady=(20, 0))

        self.embed_mode_button = ctk.CTkOptionMenu(master=self.frame_top,
                                                   dropdown_text_color=self.DARK_GREY,
                                                   text_color=self.DARK_GREY,
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
        self.embed_mode_button.grid(
            row=1, column=0, columnspan=3, pady=20, padx=20, sticky="nswe")

        self.embed_mode_button.configure(
            values=list(self.settings["modes"].keys()))
        self.embed_mode_button.text_label["text"] = "Select Document Preset"

        self.embed_button = ctk.CTkButton(master=self.frame_top,
                                          state="disabled",
                                          text="Embed",
                                          text_color=self.DARK_GREY,
                                          fg_color=self.WHITE,
                                          hover_color=self.DARK_BLUE,
                                          height=35,
                                          corner_radius=6,
                                          text_font=(
                                               "Roboto", -16))
        self.embed_button.grid(row=2, rowspan=1, column=0, columnspan=2,
                               pady=(0, 20), padx=20, sticky="swe")

        self.progress_label = ctk.CTkLabel(master=self.frame_top,
                                           text="Select a file to start.",
                                           text_color=self.DARK_GREY,
                                           text_font=("Roboto", -24))  # font name and size in px
        self.progress_label.grid(
            row=3, column=0, columnspan=3, pady=(20, 0), padx=20)
        self.progress_bar = ctk.CTkProgressBar(
            master=self.frame_top, progress_color=self.LIGHT_BLUE, fg_color=self.DARK_GREY)
        self.progress_bar.grid(row=4, column=0, columnspan=3,
                               sticky="nswe", padx=20, pady=20)
        self.progress_bar.set(0.0)
        self.progress_bar.grid_remove()

        # Under frame
        # Log button.
        self.exit_button = ctk.CTkButton(master=self,
                                         text="Exit",
                                         text_color=self.DARK_GREY,
                                         fg_color=self.LIGHT_BLUE,
                                         hover_color=self.DARK_BLUE,
                                         height=35,
                                         corner_radius=20,
                                         text_font=(
                                             "Roboto", -16))
        self.exit_button.grid(row=2, column=1, pady=20, padx=20, sticky="nswe")

        # Settings button.
        self.options_button = ctk.CTkButton(master=self,
                                            text="Options",
                                            text_color=self.DARK_GREY,
                                            fg_color=self.LIGHT_BLUE,
                                            hover_color=self.DARK_BLUE,
                                            height=35,
                                            corner_radius=20,
                                            text_font=(
                                                 "Roboto", -16))
        self.options_button.grid(
            row=2, column=0, pady=20, padx=20, sticky="nswe")
