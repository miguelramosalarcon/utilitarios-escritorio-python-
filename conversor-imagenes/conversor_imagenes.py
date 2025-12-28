import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import threading
import platform
import sys
import webbrowser

# ================================================================
# 🖼️ CONVERSOR DE IMÁGENES A WEBP/AVIF - APLICACIÓN DE ESCRITORIO
# ----------------------------------------------------------------
# Desarrollado por: Miguel Ramos Alarcón
# 🌐 LinkedIn: https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon
# 💻 GitHub: https://github.com/miguelramosalarcon
# 🏷 Marca personal: MRStudio (https://mrstudio.dev)
# Descripción: Conversor de imágenes a formatos web modernos (WebP/AVIF)
#              Optimizado para performance web y Core Web Vitals
# Versión: 1.0.0 - Diciembre 2025
# Licencia: MIT
# ================================================================

def ruta_recurso(relative_path):
    """Obtiene la ruta de recurso compatible con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ==== Carpeta de salida ====
OUTPUT_DIR = "imagenes-convertidas"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def centrar_ventana(ventana, ancho, alto):
    """Centra la ventana en la pantalla"""
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def obtener_tamaño_archivo(ruta):
    """Retorna el tamaño del archivo en KB o MB"""
    tamaño = os.path.getsize(ruta)
    if tamaño < 1024 * 1024:
        return f"{tamaño / 1024:.1f} KB"
    return f"{tamaño / (1024 * 1024):.1f} MB"

def convertir_imagen(archivo, formato_salida, calidad, ventana_modal):
    """Convierte una imagen al formato seleccionado"""
    try:
        # Validar archivo
        if not os.path.exists(archivo):
            raise FileNotFoundError("El archivo no existe")
        
        # Obtener información del archivo original
        tamaño_original = obtener_tamaño_archivo(archivo)
        
        # Abrir imagen
        img = Image.open(archivo)
        
        # Convertir RGBA a RGB si es necesario para JPEG o formatos sin transparencia
        if img.mode in ('RGBA', 'LA', 'P') and formato_salida.lower() in ['jpg', 'jpeg']:
            fondo = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            fondo.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = fondo
        
        # Generar nombre de archivo de salida
        nombre_base = os.path.splitext(os.path.basename(archivo))[0]
        extension_salida = formato_salida.lower()
        archivo_salida = os.path.join(OUTPUT_DIR, f"{nombre_base}_converted.{extension_salida}")
        
        # Configuración según formato
        if formato_salida.upper() == "WEBP":
            img.save(archivo_salida, "WEBP", quality=calidad, method=6)
        elif formato_salida.upper() == "AVIF":
            img.save(archivo_salida, "AVIF", quality=calidad)
        elif formato_salida.upper() == "PNG":
            img.save(archivo_salida, "PNG", optimize=True)
        elif formato_salida.upper() in ["JPG", "JPEG"]:
            img.save(archivo_salida, "JPEG", quality=calidad, optimize=True)
        
        # Obtener información del archivo convertido
        tamaño_convertido = obtener_tamaño_archivo(archivo_salida)
        reduccion = ((os.path.getsize(archivo) - os.path.getsize(archivo_salida)) / os.path.getsize(archivo)) * 100
        
        ventana_modal.destroy()
        
        # Mostrar resultado
        mensaje_resultado = f"✅ Imagen convertida exitosamente\n\n"
        mensaje_resultado += f"📊 Original: {tamaño_original}\n"
        mensaje_resultado += f"📊 Convertida: {tamaño_convertido}\n"
        mensaje_resultado += f"💾 Reducción: {reduccion:.1f}%\n\n"
        mensaje_resultado += f"📂 Guardado en: {OUTPUT_DIR}"
        
        label_estado.config(
            text=mensaje_resultado,
            fg="#F5B83A", 
            font=("Segoe UI", 9, "bold")
        )
        
        # Abrir carpeta de salida
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(OUTPUT_DIR))
        elif platform.system() == "Darwin":  # macOS
            os.system(f'open "{os.path.abspath(OUTPUT_DIR)}"')
        else:  # Linux
            os.system(f'xdg-open "{os.path.abspath(OUTPUT_DIR)}"')

    except Exception as e:
        ventana_modal.destroy()
        messagebox.showerror("Error", f"Ocurrió un problema al convertir:\n{str(e)}")
    finally:
        btn_convertir.config(state=tk.NORMAL)

def iniciar_conversion():
    """Inicia el proceso de conversión en un hilo separado"""
    archivo = entry_archivo.get()
    
    # Validaciones
    if not archivo or not os.path.exists(archivo):
        messagebox.showerror("Error", "Seleccione un archivo de imagen válido.")
        return
    
    # Validar extensión
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
    extension = os.path.splitext(archivo)[1].lower()
    if extension not in extensiones_validas:
        messagebox.showerror("Error", "Formato de imagen no soportado.\nFormatos válidos: JPG, PNG, BMP, GIF, TIFF, WebP")
        return
    
    formato_salida = combo_formato.get()
    calidad = int(slider_calidad.get())
    
    # Ventana modal de progreso
    modal = tk.Toplevel(ventana)
    modal.title("Convirtiendo imagen...")
    modal.geometry("360x120")
    modal.configure(bg="#003DA6")
    modal.resizable(False, False)
    centrar_ventana(modal, 360, 120)
    
    tk.Label(modal, text="🔄 Convirtiendo imagen, por favor espere...",
             font=("Segoe UI", 10), fg="white", bg="#003DA6").pack(pady=10)
    
    tk.Label(modal, text=f"Formato destino: {formato_salida} | Calidad: {calidad}%",
             font=("Segoe UI", 9), fg="#F5B83A", bg="#003DA6").pack(pady=5)
    
    barra = ttk.Progressbar(modal, mode="indeterminate", length=300)
    barra.pack(pady=10)
    barra.start(10)
    
    btn_convertir.config(state=tk.DISABLED)
    label_estado.config(text="")
    
    # Iniciar conversión en hilo separado
    threading.Thread(
        target=convertir_imagen, 
        args=(archivo, formato_salida, calidad, modal), 
        daemon=True
    ).start()

def seleccionar_imagen():
    """Abre el diálogo para seleccionar una imagen"""
    archivo = filedialog.askopenfilename(
        filetypes=[
            ("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("WebP", "*.webp"),
            ("Todos los archivos", "*.*")
        ]
    )
    if archivo:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo)
        # Mostrar información del archivo
        tamaño = obtener_tamaño_archivo(archivo)
        label_info_archivo.config(text=f"📊 Tamaño actual: {tamaño}")

def actualizar_label_calidad(valor):
    """Actualiza el label de calidad al mover el slider"""
    label_calidad_valor.config(text=f"{int(float(valor))}%")

# ==== Interfaz principal ====
ventana = tk.Tk()
ventana.title("Conversor de Imágenes WebP/AVIF - Miguel Ramos A. (MRStudio)")
ventana.configure(bg="#003DA6")
centrar_ventana(ventana, 680, 520)
ventana.resizable(False, False)

fuente = ("Segoe UI", 11)
fuente_boton = ("Segoe UI", 10, "bold")
fuente_small = ("Segoe UI", 9)

# ==== Título ====
tk.Label(
    ventana, 
    text="🖼️ Conversor de Imágenes a Formatos Web Modernos",
    font=("Segoe UI", 12, "bold"), 
    bg="#003DA6", 
    fg="white"
).pack(pady=(15, 5))

# ==== Selección de archivo ====
tk.Label(
    ventana, 
    text="📁 Seleccione una imagen para convertir:",
    font=fuente, 
    bg="#003DA6", 
    fg="white"
).pack(pady=(15, 5))

frame_input = tk.Frame(ventana, bg="#003DA6")
frame_input.pack()

entry_archivo = tk.Entry(frame_input, width=50, font=fuente, bd=2, relief="solid")
entry_archivo.pack(side=tk.LEFT, padx=(0, 5))

tk.Button(
    frame_input, 
    text="Buscar", 
    command=seleccionar_imagen, 
    bg="white", 
    fg="#003DA6",
    font=fuente_small,
    cursor="hand2",
    relief="flat",
    padx=15
).pack(side=tk.LEFT)

# Label info archivo
label_info_archivo = tk.Label(
    ventana, 
    text="", 
    font=fuente_small, 
    fg="#F5B83A", 
    bg="#003DA6"
)
label_info_archivo.pack(pady=(5, 0))

# ==== Formato de salida ====
tk.Label(
    ventana, 
    text="🎯 Seleccione el formato de salida:",
    font=fuente, 
    bg="#003DA6", 
    fg="white"
).pack(pady=(15, 5))

combo_formato = ttk.Combobox(
    ventana,
    values=["WEBP", "AVIF", "PNG", "JPG"],
    state="readonly",
    font=fuente,
    width=20
)
combo_formato.set("WEBP")
combo_formato.pack()

# Descripción de formatos
frame_info = tk.Frame(ventana, bg="#003DA6")
frame_info.pack(pady=(5, 0))

info_text = "💡 WebP: Mejor compatibilidad | AVIF: Mayor compresión | PNG: Sin pérdida"
tk.Label(
    frame_info, 
    text=info_text,
    font=("Segoe UI", 8), 
    fg="white", 
    bg="#003DA6"
).pack()

# ==== Control de calidad ====
tk.Label(
    ventana, 
    text="⚙️ Ajuste la calidad de conversión:",
    font=fuente, 
    bg="#003DA6", 
    fg="white"
).pack(pady=(15, 5))

frame_calidad = tk.Frame(ventana, bg="#003DA6")
frame_calidad.pack()

slider_calidad = tk.Scale(
    frame_calidad,
    from_=60,
    to=100,
    orient=tk.HORIZONTAL,
    length=300,
    bg="#003DA6",
    fg="white",
    highlightthickness=0,
    troughcolor="#4A90E2",
    command=actualizar_label_calidad
)
slider_calidad.set(85)
slider_calidad.pack(side=tk.LEFT, padx=(0, 10))

label_calidad_valor = tk.Label(
    frame_calidad,
    text="85%",
    font=("Segoe UI", 11, "bold"),
    fg="#F5B83A",
    bg="#003DA6",
    width=5
)
label_calidad_valor.pack(side=tk.LEFT)

tk.Label(
    ventana, 
    text="🛈 Calidad recomendada: 80-90% (balance entre peso y calidad visual)",
    font=("Segoe UI", 8), 
    fg="white", 
    bg="#003DA6"
).pack(pady=(5, 10))

# ==== Botón convertir ====
btn_convertir = tk.Button(
    ventana, 
    text="🔄 Convertir Imagen",
    font=fuente_boton, 
    bg="#4A90E2", 
    fg="white",
    activebackground="#3c78c9", 
    relief="flat",
    cursor="hand2", 
    command=iniciar_conversion,
    padx=30,
    pady=10
)
btn_convertir.pack(pady=(10, 10))

# ==== Label de estado ====
label_estado = tk.Label(
    ventana, 
    text="", 
    font=("Segoe UI", 9), 
    fg="white", 
    bg="#003DA6",
    justify=tk.LEFT
)
label_estado.pack(pady=(5, 10))

# ==== Footer ====
footer = tk.Frame(ventana, bg="#003DA6")
footer.pack(fill="x", side=tk.BOTTOM, pady=(10, 5))

tk.Label(
    footer, 
    text="Dev. Miguel Ramos Alarcón - MRStudio",
    font=("Segoe UI", 9), 
    fg="#F5B83A", 
    bg="#003DA6"
).pack(side=tk.LEFT, padx=10)

link = tk.Label(
    footer, 
    text="GitHub", 
    font=("Segoe UI", 9, "underline"),
    fg="white", 
    bg="#003DA6", 
    cursor="hand2"
)
link.pack(side=tk.RIGHT, padx=(0, 10))
link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/miguelramosalarcon"))

ventana.mainloop()