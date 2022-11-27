import threading
import subprocess
import os
import barcode

from barcode.writer import ImageWriter
from PyPDF2 import PdfFileReader, PdfFileWriter
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

    def __init__(self, file, mode):
        super(Embed, self).__init__()
        self.daemon = True

        Options.load_settings(self)

        # Save attributes
        self.file = file
        self.filename = self.file.split("/")[-1]
        self.mode = mode
        self.mode_settings = self.settings["modes"][f"{self.mode}"]
        print(self.mode)

    def run(self):
        # Executes when embed button pressed.
        output_dir = self.options["output_dir"]
        self.output_file = f"{output_dir}/{self.mode}/{self.filename}"
        with open(self.output_file, "wb") as output_file, open(self.file, "rb") as input_file:
            self.embed_PDF(input_file, output_file)

            # Open PDF when completed.
            if self.options["open_when_done"]:
                open_with = self.options["open_with"]
                subprocess.call(
                    [f"{open_with}", f"{os.path.abspath(self.output_file)}"])

    def embed_PDF(self, input_file, output_file):
        input_PDF = PdfFileReader(input_file)
        output_PDF = PdfFileWriter()

        # Loop through pages of inputPDF.
        for i, page in enumerate(input_PDF.pages):

            # Skip page if settings dictate.
            if i+1 < self.mode_settings["start_page"] or i+1 in self.mode_settings["skip_pages"]:
                pass
            else:
                orderID = self.extract_order_ID(page)
                if not orderID:
                    pass  # no order id found
                else:
                    self.embed_barcode(orderID, page)

            # Add page to output.
            output_PDF.addPage(page)

        # Write generated PDF to output file.
        output_PDF.write(output_file)

    def extract_order_ID(self, page):
        # Extract order ID from page's text.
        pageText = page.extract_text()
        start = self.mode_settings["ID_start"]
        length = self.mode_settings["ID_length"]

        if start in pageText:
            orderID = (pageText.split(start)[1][:length])
            orderID = ''.join(orderID.splitlines())
            return orderID
        return False

    def embed_barcode(self, orderID, page):

        # Write Code39 object to memory. Read to image with reportlab ImageReader.
        # Write empty Canvas object to memory. Overlay barcodeImg onto barcodeCanvas.
        image_writer = ImageWriter()
        c = BytesIO()
        with BytesIO() as b:
            barcodeType = self.mode_settings["barcode_type"]
            Barcode = getattr(barcode, barcodeType)
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
