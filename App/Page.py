import customtkinter as ctk

from Options import Options


class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        Options.load_options(self)
        Options.get_colors(self, theme=self.options["theme"])

    def create_top_frame(self):
        self.frame_top = ctk.CTkFrame(master=self, corner_radius=6)
        self.frame_top.grid(row=0, column=0, columnspan=2,
                            sticky="nsew", padx=20, pady=20)
        self.frame_top.rowconfigure((0, 2, 3), minsize=20)
        self.frame_top.rowconfigure(1, minsize=80)
        self.frame_top.columnconfigure((0, 1, 2), weight=1)

    def show(self):
        self.lift()
