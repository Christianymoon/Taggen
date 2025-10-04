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

    def request_data(self, model, measure, ordercode):
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
        
    def get_data(self):
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
        self.root.iconbitmap('./assets/etiqueta-de-precio.ico')

        csv_path = json.load(open('settings.json'))['configuration']['csv_path']

        # Modern menu bar
        Menubar = Menu(self.root)
        database_menu = Menu(Menubar, tearoff=0)
        database_menu.add_command(label="Abrir CSV", command=self.set_csv)
        Menubar.add_cascade(menu=database_menu, label="Archivo")
        self.root.config(menu=Menubar)

        # Modern frames
        self.imageframe = CTkFrame(self.root, fg_color="#222831", corner_radius=15)
        self.imageframe.pack_forget()

        self.mainframe = CTkFrame(self.root, fg_color="#313131", corner_radius=15)
        self.mainframe.pack(side="left", padx=20, pady=20)

        # Modern labels and entries
        self.measurelabel = CTkLabel(self.mainframe, text="Medida (USA)", font=("Segoe UI", 13, "bold"), text_color="#EEEEEE")
        self.measurelabel.grid(row=0, column=0, padx=25, sticky="W")
        self.measure_entry = CTkEntry(self.mainframe, width=250, placeholder_text="ej. 7,8.5,9", font=("Segoe UI", 12), border_width=2, corner_radius=8)
        self.measure_entry.grid(row=1, column=0, padx=25, sticky="W")

        self.modelentrylabel = CTkLabel(self.mainframe, text="Modelo", font=("Segoe UI", 13, "bold"), text_color="#EEEEEE")
        self.modelentrylabel.grid(row=2, column=0, padx=25, sticky="W")
        self.modelentry = CTkEntry(self.mainframe, width=250, placeholder_text="Modelo de calzado", font=("Segoe UI", 12), border_width=2, corner_radius=8)
        self.modelentry.grid(row=3, column=0, padx=25, sticky="W")

        self.ordercodelabel = CTkLabel(self.mainframe, text="Orden", font=("Segoe UI", 13, "bold"), text_color="#EEEEEE")
        self.ordercodelabel.grid(row=4, column=0, padx=25, sticky="W")
        self.ordercode_entry = CTkEntry(self.mainframe, width=250, placeholder_text="Codigo de orden", font=("Segoe UI", 12), border_width=2, corner_radius=8)
        self.ordercode_entry.grid(row=5, column=0, padx=25, sticky="W")

        self.pagesizelabel = CTkLabel(self.mainframe, text="Tamaño de página (pulgadas)", font=("Segoe UI", 13, "bold"), text_color="#EEEEEE")
        self.pagesizelabel.grid(row=9, column=0, padx=25, pady=10, sticky="W")

        self.pagesizelabelx = CTkLabel(self.mainframe, text="Ancho", font=("Segoe UI", 12, "bold"), text_color="#EEEEEE")
        self.pagesizelabelx_entry = CTkEntry(self.mainframe, width=50, font=("Segoe UI", 12), border_width=2, corner_radius=8)
        
        self.pagesizelabelx.grid(row=10, column=0, padx=25, sticky="W")
        self.pagesizelabelx_entry = CTkEntry(self.mainframe, width=50, font=("Segoe UI", 12), border_width=2, corner_radius=8)
        self.pagesizelabelx_entry.grid(row=10, column=0, padx=100, sticky="W")
        self.pagesizelabelx_entry.insert(0, "13")
        

        self.pagesizelabely = CTkLabel(self.mainframe, text="Alto", font=("Segoe UI", 12, "bold"), text_color="#EEEEEE")
        self.pagesizelabely.grid(row=11, column=0, padx=25, sticky="W")
        self.pagesizelabely_entry = CTkEntry(self.mainframe, width=50, font=("Segoe UI", 12), border_width=2, corner_radius=8)
        self.pagesizelabely_entry.grid(row=11, column=0, padx=100, sticky="W")
        self.pagesizelabely_entry.insert(0, "19")

        self.quantitylabel = CTkLabel(self.mainframe, text="Cantidad", font=("Segoe UI", 13, "bold"), text_color="#EEEEEE")
        self.quantitylabel.grid(row=12, column=0, padx=25, sticky="W")
        self.quantityentry = CTkEntry(self.mainframe, width=250, placeholder_text="ej. 10,20,30", font=("Segoe UI", 12), border_width=2, corner_radius=8)
        self.quantityentry.grid(row=13, column=0, padx=25, sticky="W")

        self.progressbar = CTkProgressBar(self.mainframe, mode="determinate", width=200, progress_color="#00ADB5")
        self.progressbar.set(0)
        self.progressbar.grid(row=16, column=0, padx=25, pady=15, sticky="W")

        self.draw_option_selection = IntVar()
        self.draw_option_selection.set(0)
        self.draw_option_alignment_start = CTkRadioButton(self.mainframe, text="Texto base", variable=self.draw_option_selection, value=0, font=("Segoe UI", 12), fg_color="#00ADB5")
        self.draw_option_alignment_center = CTkRadioButton(self.mainframe, text="Texto centrado", variable=self.draw_option_selection, value=1, font=("Segoe UI", 12), fg_color="#00ADB5")

        self.draw_option_alignment_start.grid(row=14, column=0, padx=25, pady=15, sticky="W")
        self.draw_option_alignment_center.grid(row=14, column=1, padx=0, pady=15, sticky="W")

        self.uploadfile = CTkButton(self.mainframe, text="Subir PNG/JPG", command=self.getimagefromuser, font=("Segoe UI", 12), fg_color="#00ADB5", hover_color="#007B7F", corner_radius=8)
        self.uploadfile.grid(row=15, column=0, padx=25, sticky="W")

        self.button = CTkButton(self.mainframe, text="Generar PDF", command=self.generate_tag_data_from_user, font=("Segoe UI", 12), fg_color="#00ADB5", hover_color="#007B7F", corner_radius=8)
        self.button.grid(row=15, column=1, padx=15, sticky="W")

        self.switch_state = customtkinter.StringVar(value="on")
        self.switch = CTkSwitch(self.mainframe, text="Dark Mode",
                    command=lambda: customtkinter.set_appearance_mode("dark" if self.switch_state.get() == "on" else "light"),
                    variable=self.switch_state,
                    onvalue="on",
                    offvalue="off",
                    font=("Segoe UI", 12),
                    fg_color="#00ADB5")
        self.switch.grid(row=17, column=0, padx=25, pady=15, sticky="W")

        self.imagelabel = CTkLabel(self.imageframe, text="", fg_color="#222831")
        self.imagelabel.pack_forget()
        self.imageinfo = CTkLabel(self.imageframe, fg_color="#222831", text_color="#EEEEEE")
        self.imageinfo.pack_forget()
        self.current_image_path = ""
        # TODO: Implementar compresión de imagen

        # self.compression_selector = customtkinter.BooleanVar(value=False)
        # self.image_compression_selector = customtkinter.CTkLabel(self.mainframe, text="Compresión de imagen", font=("Arial", 12, "bold"))
        # self.image_compression_switch = CTkSwitch(self.mainframe, text="Alta compresión", command=None, variable=self.compression_selector, onvalue=True, offvalue=False)
        # self.image_compression_selector.grid(row=18, column=0, padx=25, pady=15, sticky="W")
        # self.image_compression_switch.grid(row=18, column=1, padx=0, pady=15, sticky="W")

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
            "pdfmeasure" : (float(self.pagesizelabelx_entry.get())*inch, float(self.pagesizelabely_entry.get())*inch),
            "measure" : (13.5*cm , 5*cm),
            "alignment": int(self.draw_option_selection.get()),
            "quantitys":[int(value) for value in self.quantityentry.get().split(',')],
            "total_quantity": sum([int(value) for value in self.quantityentry.get().split(',')]),
            "image_path": self.current_image_path,
        }
        return data

    def generate_tag_info_fromuser(self):
        taginfo = self.tag_data()
        if self.current_image_path == "":
            messagebox.showerror("Error", "No has seleccionado una imagen")
            return 
        worker1 = threading.Thread(target=self.draw_multiple, args=(taginfo,))
        worker1.start()

    def draw_multiple(self, taginfo):
        save_path = self.save_as_file()
        if not save_path:
            return
        barcode_generator = Tag()
        pdf = Gen(taginfo, save_file_path=save_path)

        t1 = threading.Thread(target=pdf.draw, args=(self.progressbar, barcode_generator))
        t1.start()

        for file in glob.glob("barcode*.png"):
            os.remove(file)
        t1.join()

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
