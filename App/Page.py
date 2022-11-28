import customtkinter as ctk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from Options import Options


class Page(ctk.CTkFrame):
    def __init__(self, name="Page", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)
        self.name = name
        Options.load_settings(self)
        Options.get_colors(self, theme=self.options["theme"])

    def create_title(self, title):
        self.title_label = ctk.CTkLabel(master=self, text_color=self.DARK_GREY,
                                        text=title,
                                        text_font=("Roboto Bold", -24))
        self.title_label.grid(row=0, column=0, padx=20,
                              pady=10, columnspan=2, sticky="new")

    def create_scrollbar(self):
        self.scrollbar = ctk.CTkScrollbar(
            self.master_frame, width=25, fg_color=self.BG_COLOR, corner_radius=25, command=self.canvas_scroll.yview)
        self.scrollbar.grid(row=0, column=1, padx=10, sticky="nsew")

        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_scroll.bind("<Configure>", lambda e: self.canvas_scroll.configure(
            scrollregion=self.canvas_scroll.bbox("all")))

    def create_top_frame(self):

        self.master_frame = ctk.CTkFrame(  # WHITE
            master=self, bg_color=self.WHITE, fg_color=self.BG_COLOR, padx=0, pady=0, corner_radius=0)
        self.master_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.master_frame.rowconfigure(0, weight=1)
        self.master_frame.columnconfigure(0, weight=1)
        self.master_frame.columnconfigure(1, minsize=20)

        self.canvas_scroll = ctk.CTkCanvas(  # BG_COLOR
            self.master_frame, bd=0, bg=self.BG_COLOR, highlightthickness=0)
        self.canvas_scroll.grid(
            row=0, column=0, sticky="nsew", padx=(20, 0), pady=0)

        self.canvas_scroll.columnconfigure(0, weight=1)
        self.canvas_scroll.columnconfigure(1, minsize=20)
        self.canvas_scroll.rowconfigure(0, weight=1)

        self.frame_top = ctk.CTkFrame(  # LIGHT_GREY
            self.canvas_scroll, corner_radius=6, fg_color=self.LIGHT_GREY)
        self.canvas_scroll.create_window(
            0, 0, window=self.frame_top, anchor="nw", tags=self.name)
        self.canvas_scroll.itemconfig(
            self.name, width=self.canvas_scroll.winfo_width())

    def onCanvasConfigure(self, e):
        if not e.height < self.frame_top.winfo_reqheight():
            self.scrollbar.grid_remove()
        else:
            self.scrollbar.grid()

        self.canvas_scroll.itemconfig(
            self.name, width=self.canvas_scroll.winfo_width())

    def _bound_to_mousewheel(self, event):
        self.canvas_scroll.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas_scroll.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_settings(self):
        Options.load_settings(self)
