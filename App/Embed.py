import threading
import subprocess
import os
import barcode

from barcode.writer import ImageWriter
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.errors import PdfReadError
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

from Options import Options


render_options = {
    "format": "PNG",
    "dpi": 300,
    "module_height": 5,
    "write_text": False,
    "font_size": 5,
    "text_distance": 1.5,
}


class Embed(threading.Thread):
    complete = False
    running = False
    error = None
    current_page = 0
    total_pages = 1
    current_status = None
    IDs_found = 0

    def __init__(self, file, mode):
        super(Embed, self).__init__()
        self.daemon = True
        self._stop_event = threading.Event()

        Options.load_settings(self)

        # Reset class variables
        Embed.complete = False
        Embed.running = True
        Embed.error = None
        Embed.current_page = 0
        Embed.total_pages = 1
        Embed.current_status = None
        Embed.IDs_found = 0

        # Save attributes
        self.file = file
        self.filename = self.file.split("/")[-1]
        self.mode = mode
        self.mode_settings = self.settings["modes"][f"{self.mode}"]

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        # Executes when embed button pressed.
        try:
            foldername = "Barcode Embedder Output"
            output_dir = self.options["output_dir"]
            self.output_file = f"{output_dir}/{foldername}/{self.mode}/{self.filename}"
            with open(self.output_file, "wb") as output_file, open(self.file, "rb") as input_file:
                cont = self.embed_PDF(input_file, output_file)
                if cont == False:
                    self.end()

                # Open PDF when completed.
                if self.options["open_when_done"]:
                    open_with = self.options["open_with"]
                    subprocess.call(
                        [f"{open_with}", f"{os.path.abspath(self.output_file)}"])

            if Embed.IDs_found == 0 and not Embed.error:
                Embed.error = "No valid IDs found. Check your barcode type and input file."
            self.end()
        # Catches any uncaught errors.
        except Exception and not Embed.error:
            Embed.error = "An unknown error occurred while embedding."
            self.end()

    def end(self):
        Embed.complete = True
        Embed.running = False

    def embed_PDF(self, input_file, output_file):
        try:
            input_PDF = PdfFileReader(input_file)
        except PdfReadError:
            Embed.error = "Failed to read PDF. File may be corrupted."
            return False

        output_PDF = PdfFileWriter()

        # Loop through pages of inputPDF.
        Embed.total_pages = len(input_PDF.pages)
        for i, page in enumerate(input_PDF.pages):
            Embed.current_page = i

            # Skip page if settings dictate.
            if i+1 < self.mode_settings["start_page"] or i+1 in self.mode_settings["skip_pages"]:
                pass
            else:
                orderID = self.extract_order_ID(page)
                print(orderID)
                if not orderID:
                    pass  # no order id found
                else:
                    try:
                        self.embed_barcode(orderID, page)
                        Embed.IDs_found += 1
                    except:
                        Embed.error = "One or more barcodes failed to embed. Check preset settings."

            # Add page to output.
            output_PDF.addPage(page)

        # Write generated PDF to output file.
        output_PDF.write(output_file)

    def extract_order_ID(self, page):
        # Extract order ID from page's text.
        pageText = page.extract_text().replace(" ", "")
        start = self.mode_settings["ID_start"].replace(" ", "")
        length = self.mode_settings["ID_length"]
        if start in pageText:
            orderID = (pageText.split(start)[1][:length])
            orderID = ''.join(orderID.splitlines())
            return orderID
        return None

    def embed_barcode(self, orderID, page):

        categories = {"codex": ["Code39", "Code128", "PZN", "Gs1_128"],
                      "ean": ["EuropeanArticleNumber13", "EuropeanArticleNumber8",
                              "JapanArticleNumber", "EuropeanArticleNumber14"],
                      "isxn": ["InternationalStandardBookNumber10",
                               "InternationalStandardSerialNumber", "InternationalStandardBookNumber13"],
                      "upc": ["UniversalProductCodeA"]
                      }

        image_writer = ImageWriter()
        c = BytesIO()
        with BytesIO() as b:
            barcode_type = self.mode_settings["barcode_type"]
            barcode_category = [
                key for (key, val) in categories.items() if barcode_type in val][0]

            mod = getattr(barcode, barcode_category)
            Barcode = getattr(mod, barcode_type)
            Barcode(orderID, writer=image_writer).write(
                b, render_options)

            barcodeImg = ImageReader(b)
            watermarkCanvas = Canvas(c)
            watermarkCanvas.drawImage(barcodeImg,
                                      self.mode_settings["barcode_location_x"],
                                      self.mode_settings["barcode_location_y"],
                                      width=self.mode_settings["barcode_size_x"],
                                      height=self.mode_settings["barcode_size_y"])

        # Commit changes to file.
        watermarkCanvas.save()
        watermark = PdfFileReader(c)
        page.mergePage(watermark.getPage(0))
        return page
