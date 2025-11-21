from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from fooconvert import footwear
from report import PDFReport
import os 

class Gen():
    def __init__(self, taginfo, save_file_path="pdfgen.pdf") -> None:
        self.taginfo = taginfo
        self.pagesize = self.taginfo["pdfmeasure"]
        self.pdfgen = canvas.Canvas(save_file_path, pagesize=self.pagesize)
        self.current_photo_file = self.taginfo["image_path"]
        
        self.spacedrawedx = 0
        self.spacedrawedy = 0

    def draw_tag(self, data, basename=""):

        separation = (0.5*cm, self.pagesize[1] - self.taginfo["measure"][1] - 0.5*cm)
        self.pdfgen.saveState()
        #creeate tag layout
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0], separation[1])
        self.pdfgen.setFillColorCMYK(100, 100, 100, 100) # 100% BLACK
        self.pdfgen.setStrokeColorCMYK(0, 0, 0, 0) # BLACK = 0, 0, 0, 100 / WHITE = 0, 0, 0, 0
        self.pdfgen.rect( 0, 0, self.taginfo["measure"][0], self.taginfo["measure"][1], fill=1)
        self.pdfgen.restoreState()
        #set the barcode generated
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 0*cm, separation[1] + 4.5*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.drawImage(basename, 0, 0, width=4*cm, height=3*cm, preserveAspectRatio=True, mask=[0,2,40,42,136,139])
        self.pdfgen.restoreState()
        #set the model
        self.pdfgen.saveState()
        if self.taginfo["alignment"] == 1:
            self.pdfgen.translate(separation[0] + 6.75*cm, separation[1] + 4.0*cm)
            self.pdfgen.setFillColorCMYK(0, 0, 0, 0) #WHITE
            self.pdfgen.setFont("Helvetica-Bold", 22)
            self.pdfgen.drawCentredString(0, 0, data["model"])
        else:
            self.pdfgen.translate(separation[0] + 3*cm, separation[1] + 4.0*cm)
            self.pdfgen.setFillColorCMYK(0, 0, 0, 0) #WHITE
            self.pdfgen.setFont("Helvetica-Bold", 18)
            self.pdfgen.drawString(0, 0, data["model"])
        self.pdfgen.restoreState()
        #draw the boot image
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 9.5*cm, separation[1] + 0.5*cm)
        self.image = ImageReader(self.current_photo_file)
        self.pdfgen.drawImage(self.current_photo_file, 0, 0, width=3.0*cm, height=3.0*cm, preserveAspectRatio=True, mask=[0, 2, 0, 2, 0, 2, ])
        self.pdfgen.restoreState()
        #draw the ordercode
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 11.0*cm, separation[1] + 4.0*cm)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 18)
        self.pdfgen.drawCentredString(0, 0, data["ordercode"])
        self.pdfgen.restoreState()
        #draw webpage
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 3.0*cm, separation[1] + 0.5*cm)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "CACTUSBOOTSUSA.COM")
        self.pdfgen.restoreState()
        #USA / MEX
        self.measurex = 1.4*cm
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 6.5*cm , separation[1] + self.measurex)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "MEX")
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 3*cm, separation[1] + self.measurex)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "USA")
        self.pdfgen.restoreState()

        #MEN'S
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 3*cm, separation[1] + 3.4*cm)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "MEN'S")
        self.pdfgen.restoreState()

        #MEASURES
        measuresy = 2.3*cm
        #USA
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 3*cm, separation[1] + measuresy)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 30)
        self.pdfgen.drawString(0, 0, str(footwear.if_int(data["measure"])))
        self.pdfgen.restoreState()
        #MEX
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 6.5*cm, separation[1] + measuresy)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 30)
        self.pdfgen.drawString(0, 0, str(footwear.to_mex(data["measure"])))
        self.pdfgen.setFont("Helvetica-Bold", 18)
        self.pdfgen.drawString(40, 8, str(footwear.if_fraction(data["measure"])))
        self.pdfgen.restoreState()

        self.pdfgen.restoreState()
  

    def update_progress(self, progressbar, percentage):
        progressbar.set(percentage)


    def draw(self, progressbar, barcode_generator):
        report = PDFReport(filename=f"report-{self.taginfo['current_model']}.pdf")
        report.write(f"Informacion - {self.taginfo['current_model']} - {self.taginfo['current_ordercode']}", 100, 700, bold=True)
        report.write(f"Generacion total: {self.taginfo['total_quantity']}", 100, 680, bold=True)
        report.write(f"Cantidad por medida: {self.taginfo['quantitys']}", 100, 660)
        report.write(f"Medidas: {self.taginfo['current_measure']}", 100, 640)
        report.write(f"Ruta de imagen: {self.current_photo_file}", 100, 620)
        report.write(f"Medida seleccionada: {self.taginfo['measure'][0] / cm} cm. x {self.taginfo['measure'][1] / cm} cm.", 100, 600)

        barcodes_basenames = []
        value = 0
        iteration = 0

        for quantity, measure in zip(self.taginfo["quantitys"], self.taginfo["current_measure"]): # array
            barcode_generator.request_data(self.taginfo["current_model"], measure, self.taginfo["current_ordercode"])
            barcode_data = barcode_generator.get_data()
            basename = barcode_generator.makebarcode(barcode_data) 
            for i in range(quantity):
                if (self.pagesize[0] - self.spacedrawedx) == self.pagesize[0]: # if space to width exist
                        self.pdfgen.saveState()
                try:
                    self.draw_tag(barcode_data, basename=basename)   
                    self.pdfgen.translate(self.taginfo["measure"][0], 0) #translate to width
                    self.spacedrawedx += self.taginfo["measure"][0]
                    if self.pagesize[0] - self.spacedrawedx < self.taginfo["measure"][0]: # if not space to width exist
                        self.pdfgen.restoreState()
                        self.spacedrawedx = 0
                        self.pdfgen.translate(0, -self.taginfo["measure"][1])
                        self.spacedrawedy += self.taginfo["measure"][1]
                        
                    if self.pagesize[1] - self.spacedrawedy < self.taginfo["measure"][1]: # if not space to heigth exist
                        self.spacedrawedy = 0
                        self.spacedrawedx = 0
                        self.pdfgen.showPage()
                except Exception as e:
                    report.write(f"Error al generar etiqueta: {e}", 100, 100, bold=True)
                    self.pdfgen.save()
                    return
                barcodes_basenames.append(basename)
            iteration += 1
            report.write(f"Etiqueta {measure} generada {quantity} veces - Codigo: {barcode_data['barcode']}", 100, 580 - (iteration * 20))
            value = (iteration / len(self.taginfo["quantitys"]))
            self.update_progress(progressbar, value)
        report.save()
        self.pdfgen.save()
        for file in barcodes_basenames:
            if os.path.exists(file):
                os.remove(file)





if __name__ == '__main__':
    pass

