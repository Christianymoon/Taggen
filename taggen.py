from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from fooconvert import footwear
from report import PDFReport
import os 

class Gen():
    def __init__(self, pdfmeasure=(13*inch, 19*inch), save_file_path="pdfgen.pdf") -> None:
        self.pagesize = pdfmeasure
        self.pdfgen = canvas.Canvas(save_file_path, pagesize=pdfmeasure)
        self.current_photo_file = ""
        self.spacedrawedx = 0
        self.spacedrawedy = 0

    def tag_clase_a(self, data, tag_measure, filepath="", barcode_path='./barcode.png', alignment=0):
        self.current_photo_file = filepath
        self.data = data
        self.pdfgen.saveState()
        separation = (0.2*cm, self.pagesize[1] - tag_measure[1] - 0.5*cm)

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0], separation[1])
        self.pdfgen.setFillColorCMYK(100, 100, 100, 100)
        self.pdfgen.setStrokeColorCMYK(0, 0, 0, 0)
        self.pdfgen.rect(10, 10, tag_measure[0], tag_measure[1], fill=1)
        self.pdfgen.setFillColorCMYK(255, 0, 0, 0)
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 1*cm, separation[1] + 4.3*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.image = ImageReader(filepath)
        self.pdfgen.drawImage(self.image, 0, 0, width=3.6*cm, height=3*cm, mask=None)
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        if alignment == 1:
            #centred string 
            self.pdfgen.translate(separation[0] +  3.9*cm, separation[1] + 6.7*cm)
            self.pdfgen.setFont("Helvetica-Bold", 18)
            self.pdfgen.rotate(90)
            self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
            self.pdfgen.scale(-1, -1)
            self.pdfgen.drawCentredString(0, 0, data["model"])
        else:
            #base string 
            self.pdfgen.translate(separation[0] + 3.9*cm, separation[1] +  9.4*cm)
            self.pdfgen.setFont("Helvetica-Bold", 18)
            self.pdfgen.rotate(90)
            self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
            self.pdfgen.scale(-1, -1)
            self.pdfgen.drawString(0, 0, data["model"])
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 1.3*cm, separation[1] + 8*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFillColorCMYK(0, 0, 0,0)
        self.pdfgen.drawCentredString(0, 0, "USA")
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 2.0*cm, separation[1] + 8.2*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFont("Helvetica-Bold", 30)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.drawCentredString(0, 0, str(footwear.if_int(data["measure"])))
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 0.7*cm, separation[1] + 6.8*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFont("Helvetica-Bold", 11)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.drawCentredString(0, 0, "CACTUSBOOTSUSA.COM")
        self.pdfgen.restoreState()



        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 4.2*cm, separation[1] + 2*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFont("Helvetica", 14)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.drawCentredString(0, 0, data["ordercode"])
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 1.3*cm, separation[1] + 5.5*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.drawCentredString(0, 0, "MEX")
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 2.0*cm, separation[1] + 5.4*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFont("Helvetica-Bold", 30)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.drawCentredString(0, 0, str(footwear.to_mex(data["measure"])))
        self.pdfgen.setFont("Helvetica-Bold", 20)
        self.pdfgen.drawString(7, 5, footwear.if_fraction(data["measure"]))
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 3.3*cm, separation[1] + 6.8*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.setFont("Helvetica", 13)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.drawCentredString(0, 0, "MEN'S")
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 0*cm, separation[1] + 10*cm)
        self.pdfgen.rotate(0)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setStrokeColorCMYK(0, 0, 0, 0)
        self.pdfgen.rect(10, 0, tag_measure[0], 2*cm, fill=1)
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.barcode_basename = barcode_path
        self.pdfgen.translate(separation[0] + 4.75*cm, separation[1] + 12*cm)
        self.pdfgen.rotate(360)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.drawImage(self.barcode_basename, 0, 0, width=4.2*cm, height=2.0*cm)
        self.pdfgen.restoreState()

        self.pdfgen.restoreState()


    def tag_clase_b(self, data, tag_measure, filepath="", barcode_path="./barcode.png", alignment=0):

        separation = (0.5*cm, self.pagesize[1] - tag_measure[1] - 0.5*cm)
        self.current_photo_file = filepath
        self.data = data
        self.pdfgen.saveState()
        self.barcode_basename = barcode_path
        #creeate tag layout
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0], separation[1])
        self.pdfgen.setFillColorCMYK(100, 100, 100, 100) # 100% BLACK
        self.pdfgen.setStrokeColorCMYK(0, 0, 0, 0) # BLACK = 0, 0, 0, 100 / WHITE = 0, 0, 0, 0
        self.pdfgen.rect( 0, 0, tag_measure[0], tag_measure[1], fill=1)
        self.pdfgen.restoreState()
        #set the barcode generated
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 1*cm, separation[1] + 5.1*cm)
        self.pdfgen.rotate(90)
        self.pdfgen.scale(-1, -1)
        self.pdfgen.drawImage(barcode_path, 0, 0, width=4.6*cm, height=2.8*cm, preserveAspectRatio=True, mask=[0,2,40,42,136,139])
        self.pdfgen.restoreState()
        #set the model
        self.pdfgen.saveState()
        if alignment == 1:
            #center string 
            #separation[0] = width
            #serparation[1] = height
            #16*cm, 5.7*cm
            self.pdfgen.translate(separation[0] + 8*cm, separation[1] + 4.5*cm)
            self.pdfgen.setFillColorCMYK(0, 0, 0, 0) #WHITE
            self.pdfgen.setFont("Helvetica-Bold", 22)
            self.pdfgen.drawCentredString(0, 0, data["model"])
        else:
            self.pdfgen.translate(separation[0] + 4.5*cm, separation[1] + 4.5*cm)
            self.pdfgen.setFillColorCMYK(0, 0, 0, 0) #WHITE
            self.pdfgen.setFont("Helvetica-Bold", 22)
            self.pdfgen.drawString(0, 0, data["model"])
        self.pdfgen.restoreState()
        #draw the boot image
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 11.5*cm, separation[1] + 0.3*cm)
        self.image = ImageReader(filepath)
        self.pdfgen.drawImage(self.current_photo_file, 0, 0, width=4*cm, height=4*cm, preserveAspectRatio=True, mask=[0, 2, 0, 2, 0, 2, ])
        self.pdfgen.restoreState()
        #draw the ordercode
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 13.5*cm, separation[1] + 4.5*cm)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 22)
        self.pdfgen.drawCentredString(0, 0, data["ordercode"])
        self.pdfgen.restoreState()
        #draw webpage
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 4.8*cm, separation[1] + 0.6*cm)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "CACTUSBOOTSUSA.COM")
        self.pdfgen.restoreState()
        #USA / MEX
        self.measurex = 1.5*cm
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 8*cm , separation[1] + self.measurex)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "MEX")
        self.pdfgen.restoreState()

        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 4.5*cm, separation[1] + self.measurex)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "USA")
        self.pdfgen.restoreState()

        #MEN'S
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 4.5*cm, separation[1] + 3.7*cm)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 12)
        self.pdfgen.drawString(0, 0, "MEN'S")
        self.pdfgen.restoreState()

        #MEASURES
        measuresy = 2.5*cm
        #USA
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 4.5*cm, separation[1] + measuresy)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 30)
        self.pdfgen.drawString(0, 0, str(footwear.if_int(data["measure"])))
        self.pdfgen.restoreState()
        #MEX
        self.pdfgen.saveState()
        self.pdfgen.translate(separation[0] + 8*cm, separation[1] + measuresy)
        self.pdfgen.setFillColorCMYK(0, 0, 0, 0)
        self.pdfgen.setFont("Helvetica-Bold", 30)
        self.pdfgen.drawString(0, 0, str(footwear.to_mex(data["measure"])))
        self.pdfgen.setFont("Helvetica-Bold", 18)
        self.pdfgen.drawString(40, 8, str(footwear.if_fraction(data["measure"])))
        self.pdfgen.restoreState()

        self.pdfgen.restoreState()
  

    def gen_recursive_tag(self, data, clase, tag_measure=(4.6*cm, 12*cm), quantity=0):
        spacedrawedx = 0
        spacedrawedy = 0
        count = 0
        while self.pagesize[1] - spacedrawedy > tag_measure[1]:
            self.pdfgen.saveState()
            while self.pagesize[0] - spacedrawedx > tag_measure[0]:
                clase(data, tag_measure, self.current_photo_file)
                self.pdfgen.translate(tag_measure[0], 0)
                spacedrawedx += tag_measure[0]
                if quantity != 0:
                    count += 1
                    if count == quantity:
                        self.pdfgen.save()
                        return
            spacedrawedx = 0
            self.pdfgen.restoreState()
            spacedrawedy += tag_measure[1]
            if self.pagesize[1] - spacedrawedy > tag_measure[1]:
                self.pdfgen.translate(0, tag_measure[1])
            else:
                if quantity == 0:
                    continue
                spacedrawedx = 0
                spacedrawedy = 0
                self.pdfgen.showPage()
        self.pdfgen.save()

    def update_progress(self, progressbar, percentage):
        progressbar.set(percentage)


    def draw(self, clase, label, tagconfig, progressbar):
        report = PDFReport(filename=f"report-{tagconfig['current_model']}.pdf")
        report.write(f"Informacion - {tagconfig['current_model']} - {tagconfig['current_ordercode']}", 100, 700, bold=True)
        report.write(f"Generacion total: {tagconfig['total_quantity']}", 100, 680, bold=True)
        report.write(f"Cantidad por medida: {tagconfig['quantitys']}", 100, 660)
        report.write(f"Medidas: {tagconfig['current_measure']}", 100, 640)
        report.write(f"Ruta de imagen: {self.current_photo_file}", 100, 620)

        tag_measure = tagconfig["measure"][tagconfig["selection"]]
        report.write(f"Medida seleccionada: {tag_measure[0] / cm} cm. x {tag_measure[1] / cm} cm.", 100, 600)
        barcodes_basenames = []
        value = 0
        iteration = 0

        for quantity, measure in zip(tagconfig["quantitys"], tagconfig["current_measure"]): # array
            label.extract_data(tagconfig["current_model"], measure, tagconfig["current_ordercode"])
            label_data = label.tagdata()
            basename = label.makebarcode(label_data) 
            for i in range(quantity):
                if (self.pagesize[0] - self.spacedrawedx) == self.pagesize[0]: # if space to width exist
                        self.pdfgen.saveState()
                try:
                    clase(label_data, 
                        tag_measure,
                        self.current_photo_file,
                        basename,
                        tagconfig["alignment"])   
                    self.pdfgen.translate(tag_measure[0], 0) #translate to width
                    self.spacedrawedx += tag_measure[0]
                    if self.pagesize[0] - self.spacedrawedx < tag_measure[0]: # if not space to width exist
                        self.pdfgen.restoreState()
                        self.spacedrawedx = 0
                        self.pdfgen.translate(0, -tag_measure[1])
                        self.spacedrawedy += tag_measure[1]
                        
                    if self.pagesize[1] - self.spacedrawedy < tag_measure[1]: # if not space to heigth exist
                        self.spacedrawedy = 0
                        self.spacedrawedx = 0
                        self.pdfgen.showPage()
                except Exception as e:
                    report.write(f"Error al generar etiqueta: {e}", 100, 100, bold=True)
                    self.pdfgen.save()
                    return
                barcodes_basenames.append(basename)
            iteration += 1
            report.write(f"Etiqueta {measure} generada {quantity} veces - Codigo: {label_data['barcode']}", 100, 580 - (iteration * 20))
            value = (iteration / len(tagconfig["quantitys"]))
            self.update_progress(progressbar, value)
        report.save()
        self.pdfgen.save()
        for file in barcodes_basenames:
            if os.path.exists(file):
                os.remove(file)





if __name__ == '__main__':
    pass

