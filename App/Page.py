import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
from Options import Options


class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        Options.load_settings(self)
        Options.get_colors(self, theme=self.options["theme"])

    def create_top_frame(self):

        # self.frame_top = ctk.CTkFrame(
        #     master=self, corner_radius=6)
        # self.frame_top.grid(row=0, column=0, columnspan=2,
        #                     sticky="nsew", padx=20, pady=20)

        # self.frame_top.rowconfigure((1, 2, 3, 4, 5, 6, 7), minsize=20)
        # self.frame_top.rowconfigure(0, minsize=80)
        # self.frame_top.columnconfigure((0, 1, 2), weight=1)

        self.frame_scroll = ScrolledText(self, state="disable")
        self.frame_scroll.grid(row=0, column=0,
                               columnspan=2, sticky="nsew", padx=20, pady=20)

        self.frame_top = ctk.CTkFrame(self.frame_scroll, corner_radius=6)
        self.frame_scroll.window_create("1.0", window=self.frame_top)

    def load_settings(self):
        Options.load_settings(self)
