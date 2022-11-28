import customtkinter as ctk
import tkinter as tk

from Page import Page


class ModeEditPage(Page):
    def __init__(self, name="ModeEdit", *args, **kwargs):
        super().__init__(name="ModeEdit", *args, **kwargs)
        self.create_top_frame()
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=20)
        self.frame_top.grid_columnconfigure(0, minsize=80)
        self.frame_top.grid_columnconfigure((1, 2), weight=1)
        self.frame_top.grid_rowconfigure(
            (0, 1, 2, 3, 4, 5, 6, 7), minsize=20)

        self.create_title("Edit Preset")
        self.mode = None
        self.create_widgets()
        self.create_scrollbar()

    def show(self, mode):
        self.mode = mode
        self.canvas_scroll.yview_moveto(0)
        if self.mode == "Add New":
            self.title_label.configure(text="New Preset")
        else:
            self.title_label.configure(text="Edit Preset")
        self.fill_fields()
        self.lift()

    def create_widgets(self):

        self.name_label = ctk.CTkLabel(master=self.frame_top,
                                       text="Preset Name",
                                       anchor="w",
                                       text_color=self.DARK_GREY,
                                       text_font=("Roboto", -16))
        self.name_label.grid(
            row=0, column=0, pady=(20, 18), padx=20, sticky="w")

        self.name_field = ctk.CTkEntry(master=self.frame_top,
                                       placeholder_text="Name of Document Preset",
                                       fg_color=self.WHITE,
                                       height=35,
                                       border_width=0,
                                       corner_radius=6,
                                       text_font=(
                                           "Roboto", -16))
        self.name_field.grid(row=0, rowspan=1, column=1, columnspan=2,
                             pady=(20, 18), padx=20, sticky="we")

        self.ID_start_label = ctk.CTkLabel(master=self.frame_top,
                                           text="ID Identifier",
                                           anchor="w",
                                           text_color=self.DARK_GREY,
                                           text_font=("Roboto", -16))
        self.ID_start_label.grid(
            row=1, column=0, pady=4, padx=20, sticky="w")

        self.ID_start_field = ctk.CTkEntry(master=self.frame_top,
                                           placeholder_text="Precedes ID. eg: 'Order ID: '",
                                           fg_color=self.WHITE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))
        self.ID_start_field.grid(row=1, rowspan=1, column=1, columnspan=2,
                                 pady=4, padx=20, sticky="we")

        self.ID_length_label = ctk.CTkLabel(master=self.frame_top,
                                            text="ID Length",
                                            anchor="w",
                                            text_color=self.DARK_GREY,
                                            text_font=("Roboto", -16))
        self.ID_length_label.grid(
            row=2, column=0, pady=(4, 18), padx=20, sticky="w")

        self.ID_length_field = ctk.CTkEntry(master=self.frame_top,
                                            placeholder_text="Length of ID",
                                            fg_color=self.WHITE,
                                            height=35,
                                            border_width=0,
                                            corner_radius=6,
                                            text_font=(
                                                "Roboto", -16))
        self.ID_length_field.grid(row=2, rowspan=1, column=1, columnspan=2,
                                  pady=(4, 18), padx=20, sticky="we")

        self.start_page_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Start Page",
                                             anchor="w",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto", -16))
        self.start_page_label.grid(
            row=3, column=0, pady=4, padx=20, sticky="w")

        self.start_page_field = ctk.CTkEntry(master=self.frame_top,
                                             placeholder_text="Ignore pages before this",
                                             fg_color=self.WHITE,
                                             height=35,
                                             border_width=0,
                                             corner_radius=6,
                                             text_font=(
                                                 "Roboto", -16))
        self.start_page_field.grid(row=3, rowspan=1, column=1, columnspan=2,
                                   pady=4, padx=20, sticky="we")

        self.skip_pages_label = ctk.CTkLabel(master=self.frame_top,
                                             text="Skip Pages",
                                             anchor="w",
                                             text_color=self.DARK_GREY,
                                             text_font=("Roboto", -16))
        self.skip_pages_label.grid(
            row=4, column=0, pady=(4, 18), padx=20, sticky="w")

        self.skip_pages_field = ctk.CTkEntry(master=self.frame_top,
                                             placeholder_text="Blank or list. eg: '2, 3, 7' ",
                                             fg_color=self.WHITE,
                                             height=35,
                                             border_width=0,
                                             corner_radius=6,
                                             text_font=(
                                                 "Roboto", -16))
        self.skip_pages_field.grid(row=4, rowspan=1, column=1, columnspan=2,
                                   pady=(4, 18), padx=20, sticky="we")

        self.barcode_type_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Barcode Type",
                                               anchor="w",
                                               text_color=self.DARK_GREY,
                                               text_font=("Roboto", -16))
        self.barcode_type_label.grid(
            row=5, column=0, pady=4, padx=20, sticky="w")

        self.barcode_type_field = ctk.CTkEntry(master=self.frame_top,
                                               placeholder_text="eg: 'Code128'",
                                               fg_color=self.WHITE,
                                               height=35,
                                               border_width=0,
                                               corner_radius=6,
                                               text_font=(
                                                   "Roboto", -16))
        self.barcode_type_field.grid(row=5, rowspan=1, column=1, columnspan=2,
                                     pady=4, padx=20, sticky="we")

        self.barcode_size_x_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="px",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.barcode_size_x_field.grid(
            row=6, column=1, pady=4, padx=(20, 0), sticky="we")

        self.barcode_size_y_field = ctk.CTkEntry(master=self.frame_top,
                                                 placeholder_text="px",
                                                 fg_color=self.WHITE,
                                                 height=35,
                                                 border_width=0,
                                                 corner_radius=6,
                                                 text_font=(
                                                     "Roboto", -16))

        self.barcode_size_y_field.grid(
            row=6, column=2, pady=4, padx=20, sticky="we")

        self.barcode_size_label = ctk.CTkLabel(master=self.frame_top,
                                               text="Barcode Size",
                                               text_color=self.DARK_GREY,
                                               anchor="w",
                                               text_font=("Roboto", -16))

        self.barcode_size_label.grid(
            row=6, column=0, pady=4, padx=20, sticky="w")

        self.barcode_location_x_field = ctk.CTkEntry(master=self.frame_top,
                                                     placeholder_text="px",
                                                     fg_color=self.WHITE,
                                                     height=35,
                                                     border_width=0,
                                                     corner_radius=6,
                                                     text_font=(
                                                         "Roboto", -16))

        self.barcode_location_x_field.grid(
            row=7, column=1, pady=(4, 18), padx=(20, 0), sticky="we")

        self.barcode_location_y_field = ctk.CTkEntry(master=self.frame_top,
                                                     placeholder_text="px",
                                                     fg_color=self.WHITE,
                                                     height=35,
                                                     border_width=0,
                                                     corner_radius=6,
                                                     text_font=(
                                                         "Roboto", -16))

        self.barcode_location_y_field.grid(
            row=7, column=2, pady=(4, 18), padx=20, sticky="we")

        self.barcode_location_label = ctk.CTkLabel(master=self.frame_top,
                                                   text="Barcode Location",
                                                   text_color=self.DARK_GREY,
                                                   anchor="w",
                                                   text_font=("Roboto", -16))

        self.barcode_location_label.grid(
            row=7, column=0, pady=(4, 18), padx=20, sticky="w")

        self.delete_button = ctk.CTkButton(master=self.frame_top,
                                           cursor="hand2",
                                           text="Delete Preset",
                                           fg_color=self.WHITE,
                                           hover_color=self.LIGHT_BLUE,
                                           height=35,
                                           border_width=0,
                                           corner_radius=6,
                                           text_font=(
                                               "Roboto", -16))
        self.delete_button.grid(row=8, rowspan=1, column=0, columnspan=3,
                                pady=(4, 20), padx=20, sticky="we")

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

    def fill_fields(self):
        self.load_settings()
        fields = [
            "ID_start", "ID_length",
            "start_page", "skip_pages",
            "barcode_type", "barcode_size_x", "barcode_size_y",
            "barcode_location_x", "barcode_location_y"]

        if self.mode == "Add New":
            self.name_field.delete(0, ctk.END)
            self.delete_button.grid_remove()
            for field in fields:
                self.__getattribute__(f"{field}_field").delete(
                    0, ctk.END)
        else:
            mode = self.settings["modes"][self.mode]
            self.name_field.delete(0, ctk.END)
            self.name_field.insert(0, self.mode)
            self.delete_button.grid()

            for field in fields:
                self.__getattribute__(f"{field}_field").delete(
                    0, ctk.END)
                if mode[field] != []:
                    self.__getattribute__(f"{field}_field").insert(
                        0, mode[field])
