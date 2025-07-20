# 🎬 Compresor de Videos MP4 - Aplicación de Escritorio en Python

Una herramienta de escritorio moderna, intuitiva y ligera para **comprimir archivos de video `.mp4`** con distintos niveles de calidad visual, desarrollada en Python usando Tkinter, FFmpeg y PyInstaller.

> ✅ Creado por: [**Miguel Ramos Alarcón**](https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon)  
> 💼 Especialista en TI & Automatización - Desarrollo de herramientas para el usuario final.

---

## 🚀 Características

- 🖥 **Interfaz gráfica elegante** (Tkinter, estilo corporativo)
- 🔄 **Compresión con un clic**, usando FFmpeg embebido
- 📉 **Tres niveles de calidad**: Alta, media, baja
- 📁 **Apertura automática de la carpeta de destino**
- ⚡ **Compresión sin consola** (modo silencioso con PyInstaller)
- 🧪 Compatible con cualquier Windows (sin necesidad de instalación)
- 🎨 Branding personalizado, íconos y diseño UX/UX profesional

---

## 🖼️ Capturas de pantalla

| Interfaz principal                             | Modal de compresión en progreso                |
|-----------------------------------------------|-----------------------------------------------|
| ![UI principal](./screenshots/ui_main.png)    | ![Modal](./screenshots/ui_modal.png)          |

---

## 🔧 Requisitos técnicos

- Este `.exe` es **portable**: no requiere instalación
- Compatible con **Windows 7 / 10 / 11**
- Ya incluye **FFmpeg integrado**
- No necesitas tener Python instalado

---

## 📦 Estructura de carpetas
compresor-videos-mp4/
│
├── Compresor_MP4.exe # Ejecutable final
├── compresor_mp4.py # Código fuente (GUI + lógica)
├── ffmpeg.exe # Motor de compresión
├── logo_miguel.ico # Ícono personalizado
├── README.md # Este archivo
└── screenshots/ # Capturas para mostrar uso


---

## ✨ Fragmentos destacados del código

### 💡 Interfaz centrada y responsiva

```python
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
subprocess.run(
    ["ffmpeg", "-i", archivo, "-vcodec", "libx264", "-crf", crf, "-preset", "medium", "-y", archivo_salida],
    check=True,
    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
)

Descargar ejecutable
👉 Puedes descargar el .exe ya listo desde la sección Releases del repositorio o directamente desde esta carpeta.

📬 Contáctame
Desarrollado con 💙 por Miguel Ramos Alarcón
📌 LinkedIn
📁 GitHub

🧪 Licencia
Este proyecto está licenciado bajo la MIT License. Eres libre de usar, modificar y compartir, siempre reconociendo la autoría.


---
