from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFReport:
    def __init__(self, filename="report.pdf"):
        self.filename = filename
        self.canva = canvas.Canvas(self.filename, pagesize=letter)
        self.canva.setTitle("Print Report")
        self.canva.setFont("Helvetica", 12)

    def write(self, text, x, y, bold=False):
        if bold:
            self.canva.setFont("Helvetica-Bold", 12)
            self.canva.drawString(x, y, text)
            return
        self.canva.setFont("Helvetica", 12)
        self.canva.drawString(x, y, text)
        

    def save(self):
        self.canva.save()