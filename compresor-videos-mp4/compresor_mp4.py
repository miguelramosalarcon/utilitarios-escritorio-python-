# ================================================================
# 🎬 COMPRESOR DE VIDEOS MP4 - APLICACIÓN DE ESCRITORIO
# ------------------------------------------------
# Desarrollado por: Miguel Ramos Alarcón
# 📧 Email: mramos20681@gmail.com
# 🌐 LinkedIn: https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon
# 💻 GitHub: https://github.com/miguelramosalarcon
# 🏷 Marca personal: MRStudio (https://mrstudio.dev)
#
# Descripción:
# Aplicación de escritorio en Python para comprimir archivos de video .MP4
# usando FFmpeg y Tkinter. Incluye interfaz moderna, opciones de calidad,
# ejecución silenciosa y compatibilidad con PyInstaller.
#
# Versión: 1.0.0
# Fecha: Noviembre 2025
# Licencia: MIT License
# ------------------------------------------------
# “En medio de la adversidad, reside la oportunidad.” — Albert Einstein
# ================================================================

import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import platform
import threading
import sys

# ==== Ruta segura para PyInstaller ====
def ruta_recurso(relative_path):
    """Obtiene la ruta correcta para recursos, compatible con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # Cuando se ejecuta desde PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Cuando se ejecuta desde el script original
        return os.path.join(os.path.abspath("."), relative_path)

# ==== Función para obtener la ruta de ffmpeg ====
def obtener_ffmpeg_path():
    """Obtiene la ruta correcta de ffmpeg para la aplicación portable"""
    if hasattr(sys, '_MEIPASS'):
        # Cuando está ejecutándose como exe empaquetado
        ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path
    else:
        # Cuando está ejecutándose como script Python
        # Buscar ffmpeg en el mismo directorio del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_path = os.path.join(script_dir, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path
    
    # Fallback: intentar usar ffmpeg del sistema
    return 'ffmpeg'

# ==== Función para verificar ffmpeg ====
def verificar_ffmpeg():
    """Verifica si ffmpeg está disponible"""
    ffmpeg_path = obtener_ffmpeg_path()
    try:
        result = subprocess.run([ffmpeg_path, '-version'], 
                              capture_output=True, 
                              text=True,
                              creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
        return result.returncode == 0
    except FileNotFoundError:
        return False
    except Exception:
        return False

# ==== Función para configurar ícono de manera segura ====
def configurar_icono(ventana, nombre_icono="logo_miguel.ico"):
    """Configura el ícono de la ventana de manera segura"""
    try:
        ruta_icono = ruta_recurso(nombre_icono)
        if os.path.exists(ruta_icono):
            ventana.iconbitmap(ruta_icono)
            return True
        else:
            print(f"Advertencia: No se encontró el ícono en {ruta_icono}")
            return False
    except tk.TclError as e:
        print(f"Error al cargar el ícono: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al cargar el ícono: {e}")
        return False

# ==== Carpeta de salida ====
OUTPUT_DIR = "videos-comprimidos"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==== Centrar ventana ====
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ==== Abrir carpeta de salida ====
def abrir_carpeta():
    ruta_abs = os.path.abspath(OUTPUT_DIR)
    if platform.system() == "Windows":
        os.startfile(ruta_abs)
    elif platform.system() == "Darwin":
        subprocess.run(["open", ruta_abs])
    else:
        subprocess.run(["xdg-open", ruta_abs])

# ==== Selección de archivo ====
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos MP4", "*.mp4")])
    if archivo:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, archivo)

# ==== Hilo de compresión ====
def hilo_comprimir_video(archivo, crf, calidad, ventana_modal):
    try:
        size_original = os.path.getsize(archivo) / (1024 * 1024)

        archivo_salida = os.path.join(
            OUTPUT_DIR,
            os.path.basename(archivo).replace(".mp4", f"_comprimido_{calidad.lower().split()[0]}.mp4")
        )

        # Usar la función para obtener la ruta correcta de ffmpeg
        ffmpeg_path = obtener_ffmpeg_path()
        
        comando = [
            ffmpeg_path, "-i", archivo,
            "-vcodec", "libx264",
            "-crf", crf,
            "-preset", "medium",
            "-y", archivo_salida
        ]
        
        resultado = subprocess.run(
            comando,
            check=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        )

        size_final = os.path.getsize(archivo_salida) / (1024 * 1024)

        ventana_modal.destroy()
        label_estado.config(
            text=f"✅ Video comprimido correctamente.\n🗂 Tamaño: {size_original:.1f} MB → {size_final:.1f} MB",
            font=("Segoe UI", 10, "bold"), fg="#F5B83A"
        )
        abrir_carpeta()

    except subprocess.CalledProcessError as e:
        ventana_modal.destroy()
        messagebox.showerror("Error de FFmpeg", f"Error al comprimir el video:\n{e.stderr if e.stderr else str(e)}")
    except FileNotFoundError:
        ventana_modal.destroy()
        messagebox.showerror("Error", "No se encontró FFmpeg. Asegúrate de que esté incluido en la aplicación.")
    except Exception as e:
        ventana_modal.destroy()
        messagebox.showerror("Error", f"Ocurrió un problema:\n{e}")
    finally:
        btn_comprimir.config(state=tk.NORMAL)

# ==== Inicia compresión ====
def comprimir_video():
    archivo = entry_archivo.get()
    if not archivo or not os.path.exists(archivo):
        messagebox.showerror("Error", "Seleccione un archivo MP4 válido.")
        return

    # Verificar que ffmpeg esté disponible antes de comprimir
    if not verificar_ffmpeg():
        messagebox.showerror("Error", "FFmpeg no está disponible. La aplicación no puede comprimir videos sin FFmpeg.")
        return

    calidad = combo_calidad.get()
    crf = {
        "Alta calidad (mayor peso)": "20",
        "Media calidad": "28",
        "Alta compresión (menor peso)": "35"
    }.get(calidad, "28")

    modal = tk.Toplevel(ventana)
    modal.title("Comprimiendo...")
    
    # Configurar ícono para la ventana modal
    configurar_icono(modal)
    
    modal.geometry("360x100")
    modal.configure(bg="#003DA6")
    modal.resizable(False, False)
    modal.grab_set()
    modal.transient(ventana)
    centrar_ventana(modal, 360, 100)

    tk.Label(modal, text="🔄 Comprimiendo video, por favor espere...",
             font=("Segoe UI", 10), fg="white", bg="#003DA6").pack(pady=10)

    barra = ttk.Progressbar(modal, mode="indeterminate", length=300)
    barra.pack(pady=5)
    barra.start(10)

    btn_comprimir.config(state=tk.DISABLED)
    label_estado.config(text="")

    hilo = threading.Thread(
        target=hilo_comprimir_video,
        args=(archivo, crf, calidad, modal),
        daemon=True
    )
    hilo.start()

# ==== Ventana principal ====
ventana = tk.Tk()
ventana.title("Compresor de Videos MP4 - Miguel Ramos A.")

# Configurar ícono de manera segura
configurar_icono(ventana)

ventana.configure(bg="#003DA6")
centrar_ventana(ventana, 650, 400)
ventana.resizable(False, False)

fuente = ("Segoe UI", 11)
fuente_boton = ("Segoe UI", 10, "bold")

tk.Label(ventana, text="📁 Seleccione un archivo MP4 para comprimir:",
         font=fuente, bg="#003DA6", fg="white").pack(pady=(20, 5))

frame_input = tk.Frame(ventana, bg="#003DA6")
frame_input.pack()

entry_archivo = tk.Entry(frame_input, width=50, font=fuente, bd=2, relief="solid", fg="#000")
entry_archivo.pack(side=tk.LEFT, padx=(0, 5))

btn_explorar = tk.Button(frame_input, text="Buscar", font=("Segoe UI", 10),
                         command=seleccionar_archivo, cursor="hand2", bg="white")
btn_explorar.pack(side=tk.LEFT)

tk.Label(ventana, text="📉 Seleccione el nivel de calidad:",
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

tk.Label(
    ventana,
    text="🛈 A mayor calidad, mayor tamaño del archivo. A mayor compresión, menor calidad visual.",
    font=("Segoe UI", 9),
    fg="white",
    bg="#003DA6"
).pack(pady=(5, 10))

btn_comprimir = tk.Button(ventana, text="🔽 Comprimir Video", font=fuente_boton,
                          bg="#4A90E2", fg="white", activebackground="#3c78c9",
                          relief="flat", cursor="hand2", command=comprimir_video)
btn_comprimir.pack(pady=(0, 10))

btn_abrir_carpeta = tk.Button(
    ventana,
    text="📂 Abrir carpeta de videos comprimidos",
    font=("Segoe UI", 10),
    bg="white",
    fg="#003DA6",
    activebackground="#d9d9d9",
    relief="ridge",
    cursor="hand2",
    command=abrir_carpeta
)
btn_abrir_carpeta.pack(pady=(0, 10))

label_estado = tk.Label(ventana, text="", font=("Segoe UI", 10), fg="white", bg="#003DA6")
label_estado.pack()

# ==== Footer ====
footer_frame = tk.Frame(ventana, bg="#003DA6")
footer_frame.pack(fill="x", side=tk.BOTTOM, pady=(15, 5))

label_autor = tk.Label(footer_frame, text="Dev. Miguel Ramos Alarcon",
                       font=("Segoe UI", 9), fg="#F5B83A", bg="#003DA6")
label_autor.pack(side=tk.LEFT, padx=10)

frame_links = tk.Frame(footer_frame, bg="#003DA6")
frame_links.pack(side=tk.RIGHT)

label_github = tk.Label(frame_links, text="GitHub",
                        font=("Segoe UI", 9, "underline"), fg="white",
                        bg="#003DA6", cursor="hand2")
label_github.pack(side=tk.LEFT, padx=(0, 10))
label_github.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/miguelramosalarcon"))

label_linkedin = tk.Label(frame_links, text="LinkedIn",
                          font=("Segoe UI", 9, "underline"), fg="white",
                          bg="#003DA6", cursor="hand2")
label_linkedin.pack(side=tk.LEFT)
label_linkedin.bind("<Button-1>", lambda e: webbrowser.open_new("https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon"))

# ==== Verificación inicial de ffmpeg ====
if __name__ == "__main__":
    # Verificar ffmpeg al inicio
    if not verificar_ffmpeg():
        print("Advertencia: FFmpeg no detectado. Asegúrate de incluirlo en el build.")
    
    ventana.mainloop()