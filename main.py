from __future__ import absolute_import, division, print_function, unicode_literals
import customtkinter
from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkRadioButton, CTkProgressBar, CTkImage, CTkSwitch
from upcean import *
import pandas as pd
from taggen import *
from reportlab.lib.units import cm, inch
from tkinter import messagebox, filedialog, Menu, IntVar
from PIL import Image
import threading
import glob
import os
import json

customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("system")
csv_path = "./allbarcodes.csv"

class Extract():
    def __init__(self, filepath) -> None:
        self.df = pd.read_csv(filepath)

    def barcode(self, measure: int, model):
        barcode = self.df.loc[self.df["measure"] == measure, model]
        barcode = barcode.astype('Int64').values[0]
        return barcode


class Tag():
    def __init__(self):
        self.data = Extract(csv_path)
        self.model = None
        self.measure = None
        self.ordercode = None
        self.barcode = None

    def extract_data(self, model, measure, ordercode):
        self.model = model
        self.measure = measure
        self.ordercode = ordercode
        try:    
            self.barcode = self.data.barcode(self.measure, self.model)
        except:
            messagebox.showerror("Error", "Dato no encontrado")
            return
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
        self.root = customtkinter.CTk()
        self.root.title("TagGen")
        self.root.geometry("1000x600")
        self.root.resizable(True, False)
        self.root.iconbitmap('./assets/etiqueta-de-precio.ico') #route of bitmap

        csv_path = json.load(open('settings.json'))['configuration']['csv_path']

        Menubar = Menu(self.root)
        database_menu = Menu(Menubar, tearoff=0)
        database_menu.add_command(label="Abrir CSV", command=self.set_csv)
        Menubar.add_cascade(menu=database_menu, label="Archivo")
        self.root.config(menu=Menubar)

        self.imageframe = CTkFrame(self.root)
        self.imageframe.configure()
        self.imageframe.pack_forget()

        # principal frame
        self.mainframe = CTkFrame(self.root, fg_color="transparent")
        self.mainframe.configure()
        self.mainframe.pack(side="left")

        # Entrys
        self.measurelabel = CTkLabel(self.mainframe, text="Medida (USA)", font=("Arial", 12, "bold"))
        self.measurelabel.grid(row=0, column=0, padx=25, sticky="W")
        self.measure_entry = CTkEntry(self.mainframe, width=250, placeholder_text="Numero de calzado")
        self.measure_entry.grid(row=1, column=0, padx=25, sticky="W")

        self.modelentrylabel = CTkLabel(self.mainframe, text="Modelo", font=("Arial", 12, "bold"))
        self.modelentrylabel.grid(row=2, column=0, padx=25, sticky="W")
        self.modelentry = CTkEntry(self.mainframe, width=250, placeholder_text="Modelo de calzado (MAYUSCULAS)")
        self.modelentry.grid(row=3, column=0, padx=25, sticky="W")

        self.ordercodelabel = CTkLabel(self.mainframe, text="Orden", font=("Arial", 12, "bold"))
        self.ordercodelabel.grid(row=4, column=0, padx=25, sticky="W")
        self.ordercode_entry = CTkEntry(self.mainframe, width=250, placeholder_text="Codigo de orden")
        self.ordercode_entry.grid(row=5, column=0, padx=25, sticky="W")

        self.measureselection = CTkLabel(self.mainframe, text="Selecciona clase de medida", font=("Arial", 12, "bold"))
        self.measureselection.grid(row=6, column=0, padx=25, sticky="W")

        self.currentselection = IntVar()
        self.currentselection.set(0)
        self.radiobutton_clasea = CTkRadioButton(self.mainframe, text="4.6 x 12 cm clase A", variable=self.currentselection, value=0)
        self.radiobutton_clasea.grid(row=7, column=0, padx=25, pady=7.5, sticky="W")

        self.radiobutton_claseb = CTkRadioButton(self.mainframe, text="16 x 5.7 cm clase B", variable=self.currentselection, value=1)
        self.radiobutton_claseb.grid(row=8, column=0, padx=25, pady=7.5, sticky="W")

        self.pagesizelabel = CTkLabel(self.mainframe, text="Tamaño de página (inch)", font=("Arial", 12, "bold"))
        self.pagesizelabel.grid(row=9, column=0, padx=25, sticky="W")

        self.pagesizelabelx = CTkLabel(self.mainframe, text="Ancho", font=("Arial", 12, "bold"))
        self.pagesizelabelx.grid(row=10, column=0, padx=25, sticky="W")
        self.pagesizelabelx_entry = CTkEntry(self.mainframe, width=50)
        self.pagesizelabelx_entry.grid(row=10, column=0, padx=100, sticky="W")

        self.pagesizelabely = CTkLabel(self.mainframe, text="Alto", font=("Arial", 12, "bold"))
        self.pagesizelabely.grid(row=11, column=0, padx=25, sticky="W")
        self.pagesizelabely_entry = CTkEntry(self.mainframe, width=50)
        self.pagesizelabely_entry.grid(row=11, column=0, padx=100, sticky="W")

        self.quantitylabel = CTkLabel(self.mainframe, text="Cantidad", font=("Arial", 12, "bold"))
        self.quantitylabel.grid(row=12, column=0, padx=25, sticky="W")
        self.quantityentry = CTkEntry(self.mainframe)
        self.quantityentry.grid(row=13, column=0, padx=25, sticky="W")

        self.progressbar = CTkProgressBar(self.mainframe, mode="determinate", width=200)
        self.progressbar.set(0)
        self.progressbar.grid(row=16, column=0, padx=25, pady=15, sticky="W")

        self.draw_option_selection = IntVar()
        self.draw_option_selection.set(0)
        self.draw_option_alignment_start = CTkRadioButton(self.mainframe, text="Texto base", variable=self.draw_option_selection, value=0)
        self.draw_option_alignment_center = CTkRadioButton(self.mainframe, text="Texto centrado", variable=self.draw_option_selection, value=1)

        self.draw_option_alignment_start.grid(row=14, column=0, padx=25, pady=15, sticky="W")
        self.draw_option_alignment_center.grid(row=14, column=1, padx=0, pady=15, sticky="W")

        self.uploadfile = CTkButton(self.mainframe, text="Subir PNG/JPG", command=self.getimagefromuser)
        self.uploadfile.grid(row=15, column=0, padx=25, sticky="W")

        self.button = CTkButton(self.mainframe, text="Generar PDF", command=self.generate_tag_data_from_user)
        self.button.grid(row=15, column=1, padx=0, sticky="W")

        self.switch_state = customtkinter.StringVar(value="on")
        self.switch = CTkSwitch(self.mainframe, text="Dark Mode", 
                                command= lambda: customtkinter.set_appearance_mode("dark" if self.switch_state.get() == "on" else "light"), 
                                variable=self.switch_state, 
                                onvalue="on", 
                                offvalue="off")
        self.switch.grid(row=17, column=0, padx=25, pady=15, sticky="W")
        self.imagelabel = CTkLabel(self.imageframe)
        self.imagelabel.configure(text="")
        self.imagelabel.pack_forget()
        self.imageinfo = CTkLabel(self.imageframe)
        self.imageinfo.pack_forget()
        self.current_image_path = ""

    def set_csv(self):
        csv_path = filedialog.askopenfilename(
            initialdir="/", title="Selecciona un archivo CSV",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        if csv_path:
            with open('settings.json', 'w') as f:
                json.dump({"configuration": {"csv_path": csv_path}}, f, indent=4)
            messagebox.showinfo("Configuración", "Archivo CSV configurado correctamente.")
        else:
            messagebox.showerror("Error", "No se seleccionó ningún archivo CSV.")


    def update_percentage(self, percentage):
        self.percentage_label.config(text=f"% {round(percentage)}")

    def update_progress(self, progress):
        if progress <= 100:
            self.progressbar.set(progress)
            self.update_percentage(progress * 100)
        else:
            self.progressbar.set(1)
            self.update_percentage(100)

    def getimagefromuser(self):
        self.filepath = filedialog.askopenfilename(initialdir="./", title="Selecciona una imagen", filetypes=(("JPG Files", "*jpg"), ("PNG Files", "*.png")))
        self.current_image_path = self.filepath
        self.image = CTkImage(light_image=Image.open(self.filepath), size=(600, 600))
        self.include_image_inframe(self.image)

    def include_image_inframe(self, image):
        self.imagelabel.configure(image=image)
        self.imageinfo.configure(text=f"Imagen: {self.current_image_path}")
        self.imageinfo.pack(side="bottom")
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
            "quantitys":[int(value) for value in self.quantityentry.get().split(',')],
            "total_quantity": sum([int(value) for value in self.quantityentry.get().split(',')]),
        }
        return data

    def generate_tag_info_fromuser(self):
        taginfo = self.tag_data()
        if self.current_image_path == "":
            messagebox.showerror("Error", "Imagen no seleccionada")
            return       
        if len(taginfo["current_measure"]) > 1: # if more than 1 measures exist
            # worker1 = threading.Thread(target=self.draw_recursive_multiple_types, args=(taginfo,))
            worker1 = threading.Thread(target=self.draw_multiple, args=(taginfo,))
            worker1.start()
        else:
            worker2 = threading.Thread(target=self.draw_recursive_one_type, args=(taginfo,))
            # worker2 = threading.Thread(target=self.draw_mutliple, args=(taginfo,))
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

    def draw_multiple(self, taginfo):

        ''' taginfo son las configuraciones de entrada del usuario 
        por medio de estas se obtiene el modelo ingresado (string), la medidas ingresadas (array)
        el codigo de orden (int), la seleccion de tipo (int), el alineamiento (int),
        y la medida de la tarjeta (array) '''

        save_path = self.save_as_file()
        if not save_path:
            return
        pdf = Gen(taginfo["pdfmeasure"], save_file_path=save_path)

        # crea un atributo tag que construye el modelo de una etiqueta con sus respecitvos 
        # nombres, modelo y medida 

        if taginfo["selection"] == 0:
            # Clase A 
            label = Tag()
            label.extract_data(taginfo["current_model"], taginfo["current_measure"][0], taginfo["current_ordercode"])
            basename = label.makebarcode(label.tagdata())
            if basename == None:
                messagebox.showerror("Error", "Codigo de barras no valido verifique la base de datos")
                return 
            # Dibuja la tarjeta una sola vez y retorna 
            t1 = threading.Thread(target=pdf.tag_clase_a(label.tagdata(), 
                    taginfo["measure"][taginfo["selection"]], 
                    self.current_image_path, 
                    barcode_path=basename,
                    alignment=taginfo["alignment"]))
            t1.start()

            # dibuja la tarjeta recursivamente 
            t2 = threading.Thread(target=pdf.draw(
                pdf.tag_clase_a, label, taginfo, self.progressbar))
            t2.start() 
            for file in glob.glob("barcode*.png"):
                os.remove(file)


        if taginfo["selection"] == 1:
            # Clase B
            label = Tag()
            label.extract_data(taginfo["current_model"], taginfo["current_measure"][1], taginfo["current_ordercode"])
            basename = label.makebarcode(label.tagdata())

            # Dibuja la tarjeta una sola vez y retorna 
            t1 = threading.Thread(target=pdf.tag_clase_b(label.tagdata(), 
                    taginfo["measure"][taginfo["selection"]], 
                    self.current_image_path, 
                    barcode_path=basename,
                    alignment=taginfo["alignment"]))
            t1.start()

            # dibuja la tarjeta recursivamente 
            t2 = threading.Thread(target=pdf.draw(
                pdf.tag_clase_b, label, taginfo, self.progressbar))
            t2.start() 
            for file in glob.glob("barcode*.png"):
                os.remove(file)

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
