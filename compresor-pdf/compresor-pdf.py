import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import platform
import sys
import webbrowser

# ================================================================
# 📄 COMPRESOR DE PDF - APLICACIÓN DE ESCRITORIO
# ------------------------------------------------
# Desarrollado por: Miguel Ramos Alarcón
# 🌐 LinkedIn: https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon
# 💻 GitHub: https://github.com/miguelramosalarcon
# 🏷 Marca personal: MRStudio (https://mrstudio.dev)
# Descripción: Compresor de archivos PDF offline, rápido y portable
# Versión: 1.0.0 - Noviembre 2025
# Licencia: MIT
# ================================================================

def ruta_recurso(relative_path):
    """Obtiene la ruta de recurso compatible con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ==== Carpeta de salida ====
OUTPUT_DIR = "pdfs-comprimidos"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def obtener_gs_path():
    """Intenta localizar Ghostscript automáticamente"""
    posibles_rutas = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gswin64c.exe'),
        r"C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe",
        r"C:\Program Files\gs\gs10.03.1\bin\gswin64c.exe",
        "gswin64c.exe",
        "gs"
    ]
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta
    return None


def comprimir_pdf(archivo, calidad, ventana_modal):
    try:
        ruta_gs = obtener_gs_path()
        if not ruta_gs:
            raise FileNotFoundError("Ghostscript no encontrado. Instálalo desde https://ghostscript.com/releases/gsdnld.html")

        archivo_salida = os.path.join(
            OUTPUT_DIR,
            os.path.basename(archivo).replace(".pdf", f"_comprimido_{calidad.lower().split()[0]}.pdf")
        )

        configuracion = {
            "Alta calidad (mayor peso)": "/prepress",
            "Media calidad": "/ebook",
            "Alta compresión (menor peso)": "/screen"
        }.get(calidad, "/ebook")

        comando = [
            ruta_gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={configuracion}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={archivo_salida}",
            archivo
        ]

        subprocess.run(comando, check=True)

        ventana_modal.destroy()
        label_estado.config(
            text=f"✅ PDF comprimido correctamente.\n📂 Guardado en: {OUTPUT_DIR}",
            fg="#F5B83A", font=("Segoe UI", 10, "bold")
        )
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(OUTPUT_DIR))

    except Exception as e:
        ventana_modal.destroy()
        messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")
    finally:
        btn_comprimir.config(state=tk.NORMAL)

def iniciar_compresion():
    archivo = entry_archivo.get()
    if not archivo or not os.path.exists(archivo):
        messagebox.showerror("Error", "Seleccione un archivo PDF válido.")
        return

    calidad = combo_calidad.get()

    modal = tk.Toplevel(ventana)
    modal.title("Comprimiendo PDF...")
    modal.geometry("360x100")
    modal.configure(bg="#003DA6")
    modal.resizable(False, False)
    centrar_ventana(modal, 360, 100)
    tk.Label(modal, text="🔄 Comprimiendo, por favor espere...",
             font=("Segoe UI", 10), fg="white", bg="#003DA6").pack(pady=10)
    barra = ttk.Progressbar(modal, mode="indeterminate", length=300)
    barra.pack(pady=5)
    barra.start(10)

    btn_comprimir.config(state=tk.DISABLED)
    label_estado.config(text="")

    threading.Thread(target=comprimir_pdf, args=(archivo, calidad, modal), daemon=True).start()

def seleccionar_pdf():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if archivo:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo)

# ==== Interfaz principal ====
ventana = tk.Tk()
ventana.title("Compresor de PDF - Miguel Ramos A. (MRStudio)")
ventana.configure(bg="#003DA6")
centrar_ventana(ventana, 650, 380)
ventana.resizable(False, False)

fuente = ("Segoe UI", 11)
fuente_boton = ("Segoe UI", 10, "bold")

tk.Label(ventana, text="📄 Seleccione un archivo PDF para comprimir:",
         font=fuente, bg="#003DA6", fg="white").pack(pady=(20, 5))

frame_input = tk.Frame(ventana, bg="#003DA6")
frame_input.pack()
entry_archivo = tk.Entry(frame_input, width=50, font=fuente, bd=2, relief="solid")
entry_archivo.pack(side=tk.LEFT, padx=(0, 5))
tk.Button(frame_input, text="Buscar", command=seleccionar_pdf, bg="white", cursor="hand2").pack(side=tk.LEFT)

tk.Label(ventana, text="📉 Seleccione el nivel de compresión:",
         font=fuente, bg="#003DA6", fg="white").pack(pady=(15, 5))

combo_calidad = ttk.Combobox(
    ventana,
    values=[
        "Alta calidad (mayor peso)",
        "Media calidad",
        "Alta compresión (menor peso)"
    ],
    state="readonly",
    font=fuente
)
combo_calidad.set("Media calidad")
combo_calidad.pack()

tk.Label(ventana, text="🛈 A menor calidad, menor peso del archivo.",
         font=("Segoe UI", 9), fg="white", bg="#003DA6").pack(pady=(5, 10))

btn_comprimir = tk.Button(ventana, text="🔽 Comprimir PDF",
                          font=fuente_boton, bg="#4A90E2", fg="white",
                          activebackground="#3c78c9", relief="flat",
                          cursor="hand2", command=iniciar_compresion)
btn_comprimir.pack(pady=(0, 10))

label_estado = tk.Label(ventana, text="", font=("Segoe UI", 10), fg="white", bg="#003DA6")
label_estado.pack()

footer = tk.Frame(ventana, bg="#003DA6")
footer.pack(fill="x", side=tk.BOTTOM, pady=(15, 5))
tk.Label(footer, text="Dev. Miguel Ramos Alarcón - MRStudio",
         font=("Segoe UI", 9), fg="#F5B83A", bg="#003DA6").pack(side=tk.LEFT, padx=10)

link = tk.Label(footer, text="GitHub", font=("Segoe UI", 9, "underline"),
                fg="white", bg="#003DA6", cursor="hand2")
link.pack(side=tk.RIGHT, padx=(0, 10))
link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/miguelramosalarcon"))

ventana.mainloop()
