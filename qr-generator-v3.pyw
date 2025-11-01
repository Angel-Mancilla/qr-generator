import sys, os, csv, qrcode

if sys.version_info < (3, 6):
    raise Exception("Este script requiere Python 3.6 o superior.")

import tkinter as tk
from tkinter import filedialog, messagebox

class UI(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.save_dir_var = tk.StringVar(value="No se ha seleccionado una carpeta")
        self.csv_file_var = tk.StringVar(value="No se ha seleccionado un archivo")
        self.csv_file = ""
        self.save_dir = ""
        self.init_ui()

    def init_ui(self):
        
        self.parent.title("Generador de codigos qr")
        self.parent.configure(background="#C1C5CC")

        tk.Label(
            self.parent,
            text="Generador de Códigos QR",
            font=("Arial", 16, "bold"),
            bg="#C1C5CC",
            fg="black"
        ).pack(pady=(20, 10))

         # Obtener ruta absoluta de la imagen que sera el icono oficial
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_dir, "public", "excel-icon.png")

        try:
            self.image_tk = tk.PhotoImage(file=img_path)
            
            
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            self.image_tk = None

        if self.image_tk:
            tk.Label(
                self.parent,
                image=self.image_tk,
                # bg="#C1C5CC"
                ).pack(pady=20)
        

        
        #APARTADO SELECCION DE DIRECTORIO
        tk.Label(
            self.parent,
            text="Seleccione la carpeta donde guardará sus códigos QR:",
            font=("Font", 10),
            bg="#9BABC2",
            fg="white",
        ).pack(side="top", anchor="w", padx=30, pady=(20, 5))

        tk.Label(
            self.parent, 
            textvariable=self.save_dir_var,
            bg="#C1C5CC",
            fg="black",
            wraplength=400,
            anchor="w",
            justify="left"
        ).pack(side="top", anchor="w", padx=30, pady=(5, 10))

        btn1 = tk.Button(
            self.parent, 
            text="Seleccionar directorio", 
            command=self.select_save_directory
            ).pack(side="top", anchor="w", padx=30)
        
        

        #APARTADO SELECCION DE ARCHIVO
        tk.Label(
            self.parent,
            text="Seleccione el archivo con extension csv donde tiene sus codigos QR:",
            font=("Font", 10),
            bg="#9BABC2",
            fg="white"
        ).pack(side="top", anchor="w", padx=30, pady=(20, 5))

        tk.Label(
            self.parent, 
            textvariable=self.csv_file_var,
            bg="#C1C5CC",
            fg="black",
            wraplength=400,
            anchor="w",
            justify="left"
        ).pack(side="top", anchor="w", padx=30, pady=(5, 10))

        btn2 = tk.Button(
            self.parent, 
            text="Seleccionar archivo",
            command=self.select_csv
            ).pack(side="top", anchor="w", padx=30)
        

        #APARTADO GENERAR QR
        btn3 = tk.Button(
            self.parent, 
            text="Generar codigos",
            font=("Arial", 9, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",        
            activeforeground="white",
            relief="raised",                    
            bd=3,                   
            command=self.generate_qr
            ).pack(side="top", anchor="center", padx=30, pady=(40,10))

        #DERECHOS DE AUTOR
        tk.Label(
            self.parent,
            text="© 2024 AM. All rights reserved.",
            bg="#C1C5CC",
            fg="black",
            font=("Arial", 8)
            ).pack(side="bottom", anchor="e", padx=10, pady=5)



    #SELECCIONAR DIRECTORIO
    def select_save_directory(self):
        saveDirectory = filedialog.askdirectory(title="Seleccione el directorio donde desea guardar los codigos QR");
        if not (saveDirectory):
            messagebox.showwarning("Aviso", "No selecciono una carpeta.")
            return

        os.chdir(saveDirectory)
        self.save_dir = saveDirectory  
        self.save_dir_var.set(f"Carpeta seleccionada:\n{saveDirectory}")
    


    #SELECCIONAR ARCHIVO
    def select_csv(self):    
        archivo_csv = filedialog.askopenfilename(
            title="Seleccione el archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        );

        if not archivo_csv:
            messagebox.showwarning("Aviso", "No selecciono ningun archivo.")
            return
        
        self.csv_file_var.set(f"Archivo seleccionado:\n {archivo_csv}")
        self.csv_file = archivo_csv
       
    
    def generate_qr(self):

        if not hasattr(self, "save_dir") or not self.save_dir:
            messagebox.showwarning("Aviso", "Debe seleccionar la carpeta donde se guardarán los códigos QR.")
            return

        if not self.csv_file:
            messagebox.showwarning("Aviso", "Debe seleccionar un archivo CSV primero.")
            return
        try:
            self.read_csv(self.csv_file);
            messagebox.showinfo("Exito", "Codigos QR generados exitosamente.")
        except Exception as e: 
            messagebox.showerror("Error", f"Ocurrio un error: {str(e)}")
            


    #LEER ARCHIVO CSV
    def read_csv(self, archivo_csv):
        with open(archivo_csv, "r", newline='', encoding='utf-8') as csvfile:
            lector_csv = csv.reader(csvfile)
            next(lector_csv)

            for i, fila in enumerate(lector_csv):
                cadena = fila[0]  # Primera columna
                nombre_archivo = fila[1] + ".png"  # Segunda columna
                self.create_qr(cadena, nombre_archivo)
                


    #CREAR CODIGOS QR
    def create_qr(self,cadena, nombre_archivo):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(cadena)
        qr.make(fit=True)
        imagen = qr.make_image(fill_color="#E163EC", back_color="white")
        imagen.save(nombre_archivo)

if __name__ == "__main__":
    ROOT = tk.Tk()              #crea la ventana principal (objeto widget)
    ROOT.geometry("600x600")    #dimension de la ventana
    APP = UI(parent=ROOT)       #crea una instancia de la clase UI
    APP.mainloop()              #ejecuta el bucle de eventos principal de la aplicacion el cual gestiona las entradas del raton y del teclado y se comunica con el SO