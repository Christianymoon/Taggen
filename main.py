from __future__ import absolute_import, division, print_function, unicode_literals
from tkinter.ttk import Progressbar
from upcean import *
from tkinter import *
import pandas as pd
from taggen import *
from reportlab.lib.units import cm, inch
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import threading
import cProfile
import os

class Extract():
    def __init__(self, filepath) -> None:
        self.df = pd.read_csv(filepath)

    def barcode(self, measure: int, model):
        barcode = self.df.loc[self.df["measure"] == measure, model]
        barcode = barcode.astype('Int64').values[0]
        return barcode


class Tag():
    def __init__(self, model, measure, ordercode):
        
        data = Extract("./allbarcodes.csv")
        self.model = model
        self.measure = measure
        self.ordercode = ordercode
        self.barcode = data.barcode(self.measure, self.model)
        self.last_basename = "./barcode.png"
        self.filenumber = 1
        
    def tagdata(self):
        tag_metadata = {
            "model": self.model,
            "measure": self.measure,
            "ordercode": self.ordercode,
            "barcode": self.barcode,
        }
        return tag_metadata

    def makebarcode(self, data):
        while os.path.exists(self.last_basename):
            self.last_basename = f'./barcode{self.filenumber}.png'
            self.filenumber += 1

        barcode = upcean.oopfuncs.barcode('upca', str(data["barcode"]))
        if not barcode.validate_checksum():
            return None
        barcode.validate_create_barcode(self.last_basename, 8)
        return self.last_basename


class TagGUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("TagGen")
        self.root.resizable(False, False)
        self.root.iconbitmap('./assets/etiqueta-de-precio.ico') #route of bitmap

        self.imageframe = Frame()
        self.imageframe.config(bg="grey", width="400", height="400")
        self.imageframe.pack_forget()
        # principal frame
        self.mainframe = Frame(self.root)
        self.mainframe.config()
        self.mainframe.pack(side="left")

        # Entrys
        self.modelentrylabel = Label(self.mainframe, text="Modelo")
        self.modelentrylabel.grid(row=1, column=1, padx=5, pady=5)
        self.modelentry = Entry(self.mainframe, text="Modelo")
        self.modelentry.grid(row=1, column=2, padx=5, pady=5)

        self.measurelabel = Label(self.mainframe, text="Medida (USA)")
        self.measurelabel.grid(row=0, column=1, padx=5, pady=5)
        self.measure_entry = Entry(self.mainframe)
        self.measure_entry.grid(row=0, column=2, padx=5, pady=5)

        self.ordercodelabel = Label(self.mainframe, text="Orden")
        self.ordercodelabel.grid(row=2, column=1, padx=5, pady=5)
        self.ordercode_entry = Entry(self.mainframe)
        self.ordercode_entry.grid(row=2, column=2, padx=5, pady=5)

        self.measureselection = Label(self.mainframe, text="Medida clase")
        self.measureselection.grid(row=3, column=1, padx=5, pady=5)

        self.currentselection = IntVar()
        self.currentselection.set(0)
        self.radiobutton_clase1 = Radiobutton(self.mainframe, text="4.6 x 12 cm clase A", padx=20, variable=self.currentselection, value=0)
        self.radiobutton_clase1.grid(row=3, column=2, padx=5, pady=5)

        self.radiobutton_claseb = Radiobutton(self.mainframe, text="16 x 5.7 cm clase B", variable=self.currentselection, value=1)
        self.radiobutton_claseb.grid(row=4, column=2, padx=5, pady=5)

        self.pagesizelabelx = Label(self.mainframe, text="Ancho lienzo x (inch)")
        self.pagesizelabelx.grid(row=5, column=1, padx=5, pady=5)
        self.pagesizelabelx_entry = Entry(self.mainframe)
        self.pagesizelabelx_entry.grid(row=5, column=2, padx=5, pady=5)

        self.pagesizelabely = Label(self.mainframe, text="Alto lienzo y (inch)")
        self.pagesizelabely.grid(row=6, column=1, padx=5, pady=5)
        self.pagesizelabely_entry = Entry(self.mainframe)
        self.pagesizelabely_entry.grid(row=6, column=2, padx=5, pady=5)

        self.quantitylabel = Label(self.mainframe, text="Cantidad")
        self.quantitylabel.grid(row=7, column=1, padx=5, pady=5)
        self.quantityentry = Entry(self.mainframe)
        self.quantityentry.grid(row=7, column=2, padx=5, pady=5)

        self.progressbar = Progressbar(self.mainframe, orient="horizontal", length=100, mode="determinate")
        self.progressbar.grid(row=8, column=1, padx=5, pady=5)

        self.percentage_label = Label(self.mainframe, text="% 0")
        self.percentage_label.grid(row=8, column=2, padx=5, pady=5)

        self.draw_option_selection = IntVar()
        self.draw_option_selection.set(0)
        self.draw_option_alignment_start = Radiobutton(self.mainframe, text="Texto base", padx=20, variable=self.draw_option_selection, value=0)
        self.draw_option_alignment_center = Radiobutton(self.mainframe, text="Texto centrado", padx=20, variable=self.draw_option_selection, value=1)

        self.draw_option_alignment_start.grid(row=9, column=1, padx=5, pady=5)
        self.draw_option_alignment_center.grid(row=9, column=2, padx=5, pady=5)

        self.uploadfile = Button(self.mainframe, text="Subir PNG/JPG", command=self.getimagefromuser)
        self.uploadfile.grid(row=10, column=1, padx=10, pady=10)

        self.button = Button(self.mainframe, text="Generar PDF", command=self.generate_tag_data_from_user)
        self.button.grid(row=11, column=1, padx=10, pady=10)

        self.imagelabel = Label(self.imageframe)
        self.imagelabel.pack_forget()

        self.current_image_path = ""

    def update_percentage(self, percentage):
        self.percentage_label.config(text=f"% {round(percentage)}")

    def update_progress(self, progress):
        if progress <= 100:
            self.progressbar["value"] = progress
            self.update_percentage(progress)
        else:
            self.progressbar["value"] = 100
            self.update_percentage(100)


    def getimagefromuser(self):
        self.filepath = filedialog.askopenfilename(initialdir="./", title="Selecciona una imagen", filetypes=(("JPG Files", "*jpg"), ("PNG Files", "*.png")))
        self.image = Image.open(self.filepath)
        self.current_image_path = self.filepath
        self.include_image_inframe(self.image)

    def include_image_inframe(self, image):
        self.resized_image = ImageTk.PhotoImage(image.resize((350, 300)))
        self.imagelabel.config(image=self.resized_image)
        self.imagelabel.pack()
        self.imageframe.pack()

    def tag_data(self):
        data = {
            "current_model" : str(self.modelentry.get()),
            "current_measure" : [float(measure) for measure in self.measure_entry.get().split(',')], ## comma delimiters
            "current_ordercode" : str(self.ordercode_entry.get()),
            "selection" : self.currentselection.get(),
            "pdfmeasure" : (float(self.pagesizelabelx_entry.get())*inch, float(self.pagesizelabely_entry.get())*inch),
            "measure" : [(4.6*cm, 12*cm), (16*cm , 5.7*cm)],
            "alignment": int(self.draw_option_selection.get()),
        }
        return data

    def generate_tag_info_fromuser(self):
        taginfo = self.tag_data()
        if self.current_image_path == "":
            messagebox.showerror("Error", "Imagen no seleccionada")
            return       
        if len(taginfo["current_measure"]) > 1: # if more than 1 measures exist
            worker1 = threading.Thread(target=self.draw_recursive_multiple_types, args=(taginfo,))
            worker1.start()
        else:
            worker2 = threading.Thread(target=self.draw_recursive_one_type, args=(taginfo,))
            worker2.start()

    def draw_recursive_one_type(self, taginfo):
        pdf_path_save = self.save_as_file()
        if not pdf_path_save:
            return
        try:
            label = Tag(taginfo["current_model"], taginfo["current_measure"][0], taginfo["current_ordercode"])
            basename = label.makebarcode(label.tagdata())
            pdf = Gen(taginfo["pdfmeasure"], save_file_path=pdf_path_save)
        except:
            messagebox.showerror("Error", "Dato no encontrado")
            return 
        if taginfo["selection"] == 0:
            t1 = threading.Thread(target=pdf.tag_clase_a(label.tagdata(), taginfo["measure"][taginfo["selection"]], self.current_image_path))
            t1.start()
            if self.quantityentry.get() != '':
                t2 = threading.Thread(target=pdf.gen_recursive_tag(label.tagdata(), pdf.tag_clase_a, taginfo["measure"][taginfo["selection"]], int(self.quantityentry.get())))
            else:
                t2 = threading.Thread(target=pdf.gen_recursive_tag(label.tagdata(), pdf.tag_clase_a, taginfo["measure"][taginfo["selection"]]))
            t2.start()

        if taginfo["selection"] == 1:
            t1 = threading.Thread(target=pdf.tag_clase_b(label.tagdata(), taginfo["measure"][taginfo["selection"]], self.current_image_path))
            t1.start()
            if self.quantityentry.get() != '':
                t2 = threading.Thread(target=pdf.gen_recursive_tag(label.tagdata(), pdf.tag_clase_b, taginfo["measure"][taginfo["selection"]], int(self.quantityentry.get())))
            else:
                t2 = threading.Thread(target=pdf.gen_recursive_tag(label.tagdata(), pdf.tag_clase_b, taginfo["measure"][taginfo["selection"]]))
            t2.start()
        self.update_progress(100)
        os.remove(basename)

    def draw_recursive_multiple_types(self, taginfo):
        pdf_path_save = self.save_as_file()
        if not pdf_path_save:
            return 
        pdf = Gen(taginfo["pdfmeasure"], save_file_path=pdf_path_save)
        quantitys = [int(value) for value in self.quantityentry.get().split(',')]
        total_quantity = sum(quantitys)
        current_percentage = []
        listof_barcodes = []
        for quantity, current_measure in zip(quantitys, taginfo["current_measure"]):
            try:
                label = Tag(taginfo["current_model"], current_measure, taginfo["current_ordercode"])
                basename = label.makebarcode(label.tagdata())
            except:
                messagebox.showerror("Error", "Dato no coincidente")
                return
            # CLASE A 
            if taginfo["selection"] == 0:
                t1 = threading.Thread(target=pdf.tag_clase_a(label.tagdata(), 
                    taginfo["measure"][taginfo["selection"]],
                    filepath=self.current_image_path,
                    barcode_path=basename,
                    alignment=taginfo["alignment"]))
                t1.start()
                # the drawing function clase A
                t2 = threading.Thread(target=pdf.draw_multiple_recursive, 
                    args=(label.tagdata(), 
                    pdf.tag_clase_a, 
                    taginfo["measure"][taginfo["selection"]], 
                    quantity, taginfo["alignment"]))
                t2.start()
            # CLASE B
            if taginfo["selection"] == 1:
                t1 = threading.Thread(target=pdf.tag_clase_b(label.tagdata(), 
                    taginfo["measure"][taginfo["selection"]], 
                    self.current_image_path, 
                    barcode_path=basename,
                    alignment=taginfo["alignment"]))
                t1.start()
                # the drawing funcion clase B
                t2 = threading.Thread(target=pdf.draw_multiple_recursive(label.tagdata(), 
                    pdf.tag_clase_b, 
                    taginfo["measure"][taginfo["selection"]], 
                    quantity, taginfo["alignment"]))
                t2.start()          
            t1.join()
            t2.join()           
            listof_barcodes.append(basename)
            percentage = (quantity / total_quantity) * 100
            current_percentage.append(percentage)
            self.update_progress(sum(current_percentage))
        pdf.pdfgen.save()
        self.delete_barcodes(listof_barcodes)


    def save_as_file(self):
        savefile = filedialog.asksaveasfile(title="Guardar PDF", mode="w", defaultextension=".pdf")
        if savefile is not None:
            return savefile.name
        return False

    def generate_tag_data_from_user(self):
        try:
            self.generate_tag_info_fromuser()
        except ValueError:
            messagebox.showerror("Error de valor", "Solo valores numericos")

    def delete_barcodes(self, filebase):
        for file in filebase:
            if os.path.exists(file):
                os.remove(file)

if __name__ == "__main__":
    app = TagGUI()
    app.root.mainloop()
