import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import ImageTk, Image
import time
import threading
import barcode
from barcode.writer import ImageWriter
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import logging
import os
import subprocess
import json

DELAY = 50
run_flag_lock = threading.Lock()


logging.basicConfig(filename="log.log",
                    encoding="utf-8",
                    format='%(levelname)s %(asctime)s  %(message)s',
                    level=logging.DEBUG)
logging.getLogger('PIL').setLevel(logging.INFO)


render_options = {
    "format": "PNG",
    "dpi": 300,
    "module_height": 5,
    "write_text": False,
    "font_size": 5,
    "text_distance": 1.5,
}


# Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("Light")
# Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")


class App(TkinterDnD.Tk):

    WIDTH = 860
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.iconbitmap("./icon.ico")
        self.title("Barcode Embedder")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Open logo.
        with Image.open("./icon.png").convert("RGBA") as logo:
            aspect_ratio = logo.height / logo.width
            self.logo_width = 200
            self.logo_height = int(self.logo_width * aspect_ratio)
            self.logo = logo.resize(
                (self.logo_width, self.logo_height))

        # Two columns.
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_left = ctk.CTkFrame(master=self,
                                       width=180,
                                       corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Right frame.
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.columnconfigure((0, 1, 2), weight=1)

        # Left frame.
        self.frame_left.grid_rowconfigure((0, 1), minsize=20)        # Title
        self.frame_left.grid_rowconfigure(
            2, minsize=self.logo_height)    # Logo
        self.frame_left.grid_rowconfigure((3, 4), weight=1)       # Settings
        self.frame_left.grid_rowconfigure((5, 6), minsize=20)

        # Screen frame.
        self.frame_screen = ctk.CTkFrame(master=self.frame_right)
        self.frame_screen.grid(row=0, column=0, columnspan=3,
                               rowspan=4, pady=20, padx=20, sticky="nsew")
        self.frame_screen.rowconfigure((0, 2, 3), minsize=20)
        self.frame_screen.rowconfigure(1, minsize=80)
        self.frame_screen.columnconfigure((0, 1, 2), weight=1)

        # Run App
        self.active_file = None
        try:
            self.load_settings()
            self.embed_mode_name = self.embed_mode_names[0]
            self.embed_mode = self.embed_modes[f"{self.embed_mode_name}"]
        except Exception as e:
            logging.critical(
                "Settings invalid. Ensure at least 1 embed mode exists.")

        self.create_widgets()
        with run_flag_lock:
            self.page = "Embed"
            self.start_run = False
        self.after(DELAY, self.update_loop)
        self.mainloop()

    def create_widgets(self):

        # Left pane
        # Title text.
        self.title_label = ctk.CTkLabel(master=self.frame_left,
                                        text="Barcode Embedder",
                                        text_color="#40403f",
                                        text_font=("Roboto Bold", -24))  # font name and size in px
        self.title_label.grid(row=0, column=0, pady=(25, 0), padx=20)
        self.subtitle_label = ctk.CTkLabel(master=self.frame_left,
                                           text="By github.com/haroldini",
                                           text_color="#40403f",
                                           text_font=("Roboto Bold", -16))  # font name and size in px
        self.subtitle_label.grid(row=1, column=0, pady=(0, 25), padx=20)

        # Logo image.
        self.bg_image = ImageTk.PhotoImage(self.logo)
        self.image_label = tk.Label(
            master=self.frame_left, image=self.bg_image, bg='#d1d5d8')
        self.image_label.grid(row=2, column=0, pady=0, padx=20)

        # Log button.
        self.log_button = ctk.CTkButton(master=self.frame_left,
                                        text="Open Logs",
                                        border_width=2,
                                        fg_color=None,
                                        hover_color="#35c2d9",
                                        text_color="#40403f",
                                        height=35,
                                        width=150,
                                        corner_radius=20,
                                        text_font=(
                                            "Roboto Bold", -16),
                                        command=self.logs_button_handler)
        self.log_button.grid(row=5, column=0, pady=(20, 20), padx=20)

        # Settings button.
        self.settings_button = ctk.CTkButton(master=self.frame_left,
                                             text="Options",
                                             border_width=2,
                                             fg_color=None,
                                             hover_color="#35c2d9",
                                             text_color="#40403f",
                                             height=35,
                                             width=150,
                                             corner_radius=20,
                                             text_font=(
                                                 "Roboto Bold", -16),
                                             command=self.options_button_handler)
        self.settings_button.grid(row=6, column=0, pady=(0, 20), padx=20)

        # Right pane
        # Screen frame title.
        self.select_pdf_label = ctk.CTkLabel(master=self.frame_screen,
                                             text="Select PDF",
                                             text_color="#40403f",
                                             text_font=("Roboto Bold", -24))
        self.select_pdf_label.grid(
            row=0, column=0, columnspan=3, pady=(15, 15), padx=20)

        # Screen frame content.
        self.select_file_label = ctk.CTkButton(master=self.frame_screen,
                                               text="Drag PDF here.\nOr click to select PDF.",
                                               text_color="#40403f",
                                               text_font=("Roboto Bold", -14),
                                               height=100,
                                               corner_radius=6,
                                               hover_color="#35c2d9",
                                               fg_color="white",
                                               command=self.select_file)

        self.select_file_label.grid(
            column=0, columnspan=3, row=1, sticky="nwe", padx=20, pady=(0, 20))

        self.select_file_label.drop_target_register(DND_FILES)
        self.select_file_label.dnd_bind("<<Drop>>", self.select_file)

        self.embed_mode_label = ctk.CTkLabel(master=self.frame_screen,
                                             text="Select Document Type",
                                             text_color="#40403f",
                                             text_font=("Roboto Bold", -24))
        self.embed_mode_label.grid(
            row=2, column=0, columnspan=3, pady=(15, 15), padx=20)

        self.embed_mode_button = ctk.CTkOptionMenu(master=self.frame_screen,
                                                   text_color="#40403f",
                                                   dropdown_text_color="#40403f",
                                                   fg_color="#35c2d9",
                                                   button_color="#35c2d9",
                                                   button_hover_color="#329dae",
                                                   dropdown_hover_color="#35c2d9",
                                                   height=35,
                                                   width=200,
                                                   corner_radius=20,
                                                   text_font=(
                                                       "Roboto Bold", -16),
                                                   dropdown_text_font=(
                                                       "Roboto Bold", -14),
                                                   values=self.embed_mode_names,
                                                   command=self.change_embed_mode)
        self.embed_mode_button.grid(
            row=3, column=0, columnspan=3, pady=(0, 20), padx=20, sticky="nwe")

        # Under screen frame.
        self.progresslabel = ctk.CTkLabel(master=self.frame_right,
                                          text="Select a file to start",
                                          text_color="#40403f",
                                          text_font=("Roboto Bold", -20))  # font name and size in px
        self.progresslabel.grid(
            row=4, column=0, columnspan=2, pady=(0, 5), padx=(20, 10))
        self.progressbar = ctk.CTkProgressBar(
            master=self.frame_right)
        self.progressbar.grid(row=5, column=0, columnspan=2,
                              sticky="ew", padx=(20, 10), pady=(0, 20))
        self.progressbar.set(0.0)
        self.progressbar.grid_remove()

        # Start button.
        self.embed_button = ctk.CTkButton(master=self.frame_right,
                                          text="Embed",
                                          text_color="#40403f",
                                          fg_color="#35c2d9",
                                          hover_color="#329dae",
                                          height=35,
                                          width=150,
                                          corner_radius=20,
                                          text_font=(
                                                   "Roboto Bold", -16),
                                          command=self.run_button_handler)
        self.embed_button.grid(row=4, rowspan=2, column=2, columnspan=1,
                               pady=(0, 20), padx=(10, 20), sticky="swe")

    def change_embed_mode(self, new_embed_mode):
        self.embed_mode_name = new_embed_mode
        self.embed_mode = self.embed_modes[f"{new_embed_mode}"]

    def change_active_file(self, filename):

        # If no file selected.
        if filename == "":
            return

        # Removes curly brackets when filename contains spaces.
        if filename.startswith("{") and filename.endswith("}"):
            filename = filename[1:-1]

        # Sets new active_file if file is a PDF.
        if filename.endswith(".pdf"):
            self.active_file = filename
            self.filename = self.active_file.split("/")[-1]
            self.select_file_label.configure(text=self.filename)
            self.embed_button.configure(state="normal")
            self.select_file_label.configure(state="normal")
            self.progresslabel.configure(text="Click Embed to continue")

        # If file is not a PDF, tell user file is invalid.
        else:
            self.active_file = None
            self.select_file_label.configure(
                text="Selected file is invalid.\nPlease select a PDF.")
            self.progresslabel.configure(text="Select a file to start")

    def select_file(self, event=None):

        # Selects file by drag event.
        try:
            if event:
                filename = event.data

            # Selects file by windows explorer popup.
            else:
                filename = tk.filedialog.askopenfilename(
                    initialdir=self.options["open_initialdir"], title="Select a PDF", filetypes=[("PDF files", ".PDF .pdf")])

            self.change_active_file(filename)
        except Exception as e:
            Embed.error = "Failed to open file."
            logging.error(e, exc_info=True)
            logging.error(
                "Failed to load PDF. Ensure settings.json is configured correctly.")

    # Main update loop.
    def update_loop(self):

        with run_flag_lock:

            # If an error has been thrown.
            if Embed.error:
                if not Embed.error_handled:
                    self.error_handler()
                Embed.error_handled = True
                self.load_settings()

            # No active file selected.
            if not self.active_file:
                self.load_settings()
                self.progressbar.grid_remove()
                self.embed_button.configure(state="disabled")

            # Active file selected but run not pressed.
            elif not Embed.running and not Embed.end_run:
                pass

            # Embed button pressed, starting run.
            elif self.start_run:
                self.progressbar.grid()
                self.progressbar.set(0.0)
                self.embed_button.configure(state="disabled")
                self.select_file_label.configure(state="disabled")
                self.embed_button.configure(text="Embedding...")
                self.start_run = False

            # Embed running.
            elif Embed.running:
                self.progresslabel.configure(text=Embed.status_text)
                self.progressbar.set(Embed.page_i/Embed.page_i_total)

            # Embed finished.
            else:
                self.progressbar.grid_remove()
                self.progresslabel.configure(text="Success")
                self.embed_button.configure(state="normal")
                self.select_file_label.configure(state="normal")
                self.embed_button.configure(text="Embed")
                self.active_file = None
                self.select_file_label.configure(
                    text="Drag PDF here.\nOr click to select PDF.")
                Embed.end_run = False

        self.after(DELAY, self.update_loop)

    def load_settings(self):
        try:
            # Open settings.json file, read contents to embed_modes and options.
            with open("settings.json") as settings_file:
                self.settings = json.load(settings_file)
                self.embed_modes = self.settings["modes"]
                self.options = self.settings["options"]
            self.embed_mode_names = [key for key in self.embed_modes.keys()]

            # Raise error if no embed modes present in settings.
            if len(self.embed_mode_names) == 0:
                Embed.error = "Failed to load settings."

        except Exception:
            Embed.error = "Failed to load settings."

        # Create output folder for each embed mode if missing.
        try:
            os.makedirs("./output", exist_ok=True)
            for embedModeName in self.embed_mode_names:
                os.makedirs(f"./output/{embedModeName}", exist_ok=True)
        except:
            logging.critical(
                "Failed to create output directories.")
            raise

    # Executes when embed button pressed.
    def run_button_handler(self):

        if not Embed.running:
            self.start_run = True
            logging.info("<----------------------------->")
            logging.info("Starting...")

            Embed(file=self.active_file,
                  embed_mode=self.embed_mode,
                  embed_mode_name=self.embed_mode_name,
                  options=self.options).start()

    # Executes when options button pressed.
    def options_button_handler(self):

        try:
            logging.info(
                f"Opening 'settings.json'")
            os.system("notepad.exe settings.json")

        except Exception as e:
            logging.error(e, exc_info=True)
            logging.error(
                f"Failed to open 'settings.json'.")

    # Executes when logs button pressed.
    def logs_button_handler(self):

        try:
            logging.info(
                f"Opening Options")
            os.system("notepad.exe log.log")

        except Exception as e:
            logging.error(e, exc_info=True)
            logging.error(
                f"Failed to open 'log.log'.")

    # Displays error message if error occurs.
    def error_handler(self):
        print("error")
        self.active_file = None
        Embed.running = False
        Embed.end_run = False
        self.load_settings()
        self.progressbar.grid_remove()
        self.progresslabel.configure(text=f"Error: {Embed.error}")
        self.embed_button.configure(state="normal")
        self.embed_button.configure(text="Embed")
        self.select_file_label.configure(state="normal")
        self.select_file_label.configure(
            text="Drag PDF here.\nOr click to select PDF.")
        Embed.error_handled = True

    def on_closing(self, event=0):
        self.destroy()


# Thread for running barcode embedder.
class Embed(threading.Thread):

    # Static variables to reference from App.
    error = None
    error_handled = False
    running = False
    end_run = False
    status_text = ""
    page_i = 0
    page_i_total = 1

    def __init__(self, file, embed_mode, embed_mode_name, options):
        super(Embed, self).__init__()
        self.daemon = True

        # Reset static variables on new Embed call.
        Embed.error = None
        Embed.error_handled = False
        Embed.running = False
        Embed.end_run = False
        Embed.status_text = ""
        Embed.page_i = 0
        Embed.page_i_total = 1

        # Store args as attributes.
        self.file = file
        self.filename = self.file.split("/")[-1]
        self.embed_mode = embed_mode
        self.embed_mode_name = embed_mode_name
        self.options = options

    def run(self):

        try:
            # Executes when embed button pressed.
            Embed.running = True

            self.output_file = f"./output/{self.embed_mode_name}/{self.filename}"
            with open(self.output_file, "wb") as output_file, open(self.file, "rb") as input_file:
                self.embed_PDF(input_file, output_file)

                # Open PDF when completed.
                try:
                    if self.options["open_on_completion"]:
                        open_with = self.options["open_with"]
                        logging.info(
                            f"Opening embedded PDF: '{self.filename}' with '{open_with}'")
                        subprocess.call(
                            [f"{open_with}", f"{os.path.abspath(self.output_file)}"])

                except Exception as e:
                    logging.error(e, exc_info=True)
                    logging.error(
                        f"Failed to open created file. 'open_with' setting may be an invalid program.")
                    Embed.error = "Failed to open created file."

            Embed.status_text = "Complete"
            logging.info("Finished.")
            if not Embed.barcodes_found:
                Embed.error = "No Barcodes Found."
            Embed.end_run = True
            Embed.running = False

        except Exception as e:
            logging.error(e, exc_info=True)
            logging.critical(
                f"Failed to embed barcodes to '{self.active_file}.'")
            Embed.error = f"Failed to embed barcodes."

    def embed_PDF(self, input_file, output_file):

        # Read file.
        input_PDF = PdfFileReader(input_file)
        output_PDF = PdfFileWriter()
        logging.info("Successfully started.")
        logging.info(f"Embedding barcodes to file '{self.filename}'")

        # Loop through pages of inputPDF.
        Embed.page_i_total = len(input_PDF.pages)
        Embed.barcodes_found = False
        for i, page in enumerate(input_PDF.pages):
            Embed.page_i = i
            Embed.status_text = f"{Embed.page_i}/{Embed.page_i_total} | {self.filename}"

            # Skip page if settings dictate.
            if i+1 < self.embed_mode["start_page"] or i+1 in self.embed_mode["skip_pages"]:
                logging.info(
                    f"Skipping page {i+1}. Check './settings.json' if this is unintended.")
            else:
                orderID = self.extractOrderID(page)
                if not orderID:
                    logging.warning(
                        f"Page: {i+1} | No OrderID found")
                else:
                    logging.info(
                        f"Page: {i+1} | OrderID found: {orderID}")
                    Embed.barcodes_found = True
                    self.embedBarcode(orderID, page)

            # Add page to output.
            output_PDF.addPage(page)

        # Write generated PDF to output file.
        logging.info("Writing embedded PDF to output file.")
        output_PDF.write(output_file)
        logging.info(
            f"Success. Barcodes embedded to file '{self.filename}'")

    def extractOrderID(self, page):

        # Extract order ID from page's text.
        pageText = page.extract_text()
        start = self.embed_mode["orderID_start"]
        length = self.embed_mode["orderID_length"]

        if start in pageText:
            orderID = (pageText.split(start)[1][:length])
            orderID = ''.join(orderID.splitlines())
            return orderID
        return False

    def embedBarcode(self, orderID, page):

        # Write Code39 object to memory. Read to image with reportlab ImageReader.
        # Write empty Canvas object to memory. Overlay barcodeImg onto barcodeCanvas.
        image_writer = ImageWriter()
        c = BytesIO()
        with BytesIO() as b:
            try:
                barcodeType = self.embed_mode["barcode_type"]
                Barcode = getattr(barcode, barcodeType)
                Barcode(orderID, writer=image_writer).write(
                    b, render_options)

            except Exception:
                logging.critical(f"Invalid barcode type given: {barcodeType}.")
                Embed.error = f"Invalid barcode type: {barcodeType}."

            barcodeImg = ImageReader(b)
            watermarkCanvas = Canvas(c)
            watermarkCanvas.drawImage(barcodeImg,
                                      self.embed_mode["barcode_location"][0],
                                      self.embed_mode["barcode_location"][1],
                                      width=self.embed_mode["barcode_size"][0],
                                      height=self.embed_mode["barcode_size"][1])

        # Commit changes to file.
        watermarkCanvas.save()
        watermark = PdfFileReader(c)
        page.mergePage(watermark.getPage(0))
        return page


if __name__ == "__main__":
    app = App()
