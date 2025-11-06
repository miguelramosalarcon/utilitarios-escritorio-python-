import os
import re
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import quote, quote_plus

# ==========================
# Utilidades estilo 
# ==========================

def ruta_recurso(relative_path: str) -> str:
    """Obtiene la ruta correcta para recursos, compatible con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def configurar_icono(ventana: tk.Tk, nombre_icono: str = "logo_miguel.ico") -> bool:
    """Configura el ícono de la ventana de manera segura (Windows)."""
    try:
        ruta_icono = ruta_recurso(nombre_icono)
        if os.path.exists(ruta_icono):
            ventana.iconbitmap(ruta_icono)
            return True
        return False
    except tk.TclError:
        return False

def centrar_ventana(ventana: tk.Tk, ancho: int, alto: int):
    """Centra la ventana en la pantalla."""
    ventana.update_idletasks()
    sw = ventana.winfo_screenwidth()
    sh = ventana.winfo_screenheight()
    x = int((sw - ancho) / 2)
    y = int((sh - alto) / 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ==========================
# Lógica de construcción
# ==========================

PRIMARIO_BG = "#003DA6"      # Fondo principal 
PRIMARIO_ACCION = "#4A90E2"  # Botón principal
ACENTO = "#F5B83A"           # Texto estado / firma
FUENTE = ("Segoe UI", 11)
FUENTE_BTN = ("Segoe UI", 10, "bold")
FUENTE_SMALL = ("Segoe UI", 9)

def normalizar_y_validar_numero(num_raw: str) -> str:
    """
    - Acepta dígitos y '+'.
    - Limpia espacios, guiones y paréntesis.
    - Para la URL de wa.me se usa SOLO dígitos (sin '+').
    """
    limpio = re.sub(r"[ \-\(\)]", "", num_raw.strip())
    if not re.fullmatch(r"\+?\d+", limpio):
        raise ValueError("El número debe contener solo dígitos y opcional '+' al inicio.")
    numero_url = limpio.lstrip("+")
    if not numero_url:
        raise ValueError("Número vacío después de limpiar. Verifica el campo.")
    return numero_url

def construir_link(
    numero: str,
    texto: str,
    utm_source: str,
    utm_medium: str,
    utm_campaign: str,
    utm_content: str,
    utm_term: str
) -> str:
    """
    Construye el enlace final manteniendo el orden:
    text -> utm_source -> utm_medium -> utm_campaign -> utm_content -> utm_term
    Hace URL-encode en todos los valores.
    Devuelve la URL.
    """
    num_final = normalizar_y_validar_numero(numero)

    # 'text' siempre va primero
    text_encoded = quote(texto or "", safe="")
    partes_query = [f"text={text_encoded}"]

    # UTM principales y opcionales (solo si tienen valor)
    if utm_source.strip():
        partes_query.append(f"utm_source={quote_plus(utm_source.strip())}")
    if utm_medium.strip():
        partes_query.append(f"utm_medium={quote_plus(utm_medium.strip())}")
    if utm_campaign.strip():
        partes_query.append(f"utm_campaign={quote_plus(utm_campaign.strip())}")
    if utm_content.strip():
        partes_query.append(f"utm_content={quote_plus(utm_content.strip())}")
    if utm_term.strip():
        partes_query.append(f"utm_term={quote_plus(utm_term.strip())}")

    query_str = "&".join(partes_query) if partes_query else ""
    url = f"https://wa.me/{num_final}?{query_str}"
    return url

# ==========================
# App Tkinter
# ==========================

class WALinkBuilderApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("WA Link Builder - Miguel Ramos A.")
        self.root.configure(bg=PRIMARIO_BG)
        configurar_icono(self.root)
        centrar_ventana(self.root, 1000, 560)  # más compacto (sin extras)
        self.root.resizable(False, False)

        # ---- Cabecera
        tk.Label(
            self.root,
            text="🔗 Generador de enlaces WhatsApp (wa.me)",
            font=("Segoe UI", 14, "bold"),
            bg=PRIMARIO_BG,
            fg="white"
        ).pack(pady=(16, 4))

        tk.Label(
            self.root,
            text="Ingrese número (con código de país), mensaje y parámetros UTM/extra.",
            font=FUENTE_SMALL,
            bg=PRIMARIO_BG,
            fg="white"
        ).pack(pady=(0, 10))

        # ---- Contenedor principal
        cont = tk.Frame(self.root, bg=PRIMARIO_BG)
        cont.pack(fill="both", expand=True, padx=18)

        # ====== Fila: Número ======
        fila_num = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_num.pack(fill="x", pady=(2, 4))
        tk.Label(fila_num, text="📱 Número (con código de país):", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(anchor="w")
        fila_num_inputs = tk.Frame(fila_num, bg=PRIMARIO_BG)
        fila_num_inputs.pack(fill="x")
        self.entry_numero = tk.Entry(fila_num_inputs, width=40, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_numero.pack(side="left", padx=(0, 8))
        tk.Label(
            fila_num_inputs,
            text="Ej.: 51977876360  (Se permite '+', espacios, guiones y paréntesis; se limpiarán)",
            font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white"
        ).pack(side="left")

        # ====== Fila: Mensaje ======
        fila_msg = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_msg.pack(fill="x", pady=(2, 4))
        tk.Label(fila_msg, text="💬 Texto del mensaje:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(anchor="w")
        self.txt_mensaje = tk.Text(fila_msg, height=3, width=90, font=FUENTE, bd=2, relief="solid", fg="#000", wrap="word")
        self.txt_mensaje.pack(fill="x")
        tk.Label(
            fila_msg,
            text="Ej.: Hola, necesito diagnóstico o instalación para un conchador refinador.",
            font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white"
        ).pack(anchor="w", pady=(2, 0))

        # ====== Fila UTM 1: source + medium ======
        fila_utm1 = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_utm1.pack(fill="x", pady=(6, 2))

        tk.Label(fila_utm1, text="🔧 utm_source:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(side="left")
        self.entry_utm_source = tk.Entry(fila_utm1, width=28, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_utm_source.pack(side="left", padx=(8, 30))

        tk.Label(fila_utm1, text="utm_medium:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(side="left")
        self.entry_utm_medium = tk.Entry(fila_utm1, width=28, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_utm_medium.pack(side="left", padx=(8, 0))

        fila_utm1_help = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_utm1_help.pack(fill="x", pady=(2, 0))
        tk.Label(fila_utm1_help, text="Ej.: landing-linea-frio", font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white").pack(side="left", padx=(98, 30))
        tk.Label(fila_utm1_help, text="Ej.: boton", font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white").pack(side="left", padx=(160, 0))

        # ====== Fila UTM 2: campaign + content + term ======
        fila_utm2 = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_utm2.pack(fill="x", pady=(6, 2))

        tk.Label(fila_utm2, text="utm_campaign:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(side="left")
        self.entry_utm_campaign = tk.Entry(fila_utm2, width=40, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_utm_campaign.pack(side="left", padx=(8, 20))

        tk.Label(fila_utm2, text="utm_content:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(side="left")
        self.entry_utm_content = tk.Entry(fila_utm2, width=18, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_utm_content.pack(side="left", padx=(8, 20))

        tk.Label(fila_utm2, text="utm_term:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(side="left")
        self.entry_utm_term = tk.Entry(fila_utm2, width=18, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_utm_term.pack(side="left", padx=(8, 0))

        fila_utm2_help = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_utm2_help.pack(fill="x", pady=(2, 0))
        tk.Label(fila_utm2_help, text="Ej.: servicio-tecnico", font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white").pack(side="left", padx=(108, 20))
        tk.Label(fila_utm2_help, text="Ej.: hero-principal", font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white").pack(side="left", padx=(140, 20))
        tk.Label(fila_utm2_help, text="Ej.: maquinas-de-hielo", font=FUENTE_SMALL, bg=PRIMARIO_BG, fg="white").pack(side="left", padx=(86, 0))

        # ====== Botones ======
        fila_btns = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_btns.pack(fill="x", pady=(12, 6))

        self.btn_construir = tk.Button(
            fila_btns, text="🛠 Construir enlace", font=FUENTE_BTN,
            bg=PRIMARIO_ACCION, fg="white", activebackground="#3c78c9",
            relief="flat", cursor="hand2", command=self.accion_construir
        )
        self.btn_construir.pack(side="left", padx=(0, 8))

        self.btn_copiar = tk.Button(
            fila_btns, text="📋 Copiar enlace", font=FUENTE_BTN,
            bg="white", fg=PRIMARIO_BG, activebackground="#d9d9d9",
            relief="ridge", cursor="hand2", command=self.accion_copiar
        )
        self.btn_copiar.pack(side="left", padx=(0, 8))

        self.btn_copiar_html = tk.Button(
            fila_btns, text="📄 Copiar como HTML", font=FUENTE_BTN,
            bg="white", fg=PRIMARIO_BG, activebackground="#d9d9d9",
            relief="ridge", cursor="hand2", command=self.accion_copiar_html
        )
        self.btn_copiar_html.pack(side="left", padx=(0, 8))

        self.btn_abrir = tk.Button(
            fila_btns, text="🌐 Abrir en navegador", font=FUENTE_BTN,
            bg="white", fg=PRIMARIO_BG, activebackground="#d9d9d9",
            relief="ridge", cursor="hand2", command=self.accion_abrir
        )
        self.btn_abrir.pack(side="left", padx=(0, 8))

        self.btn_limpiar = tk.Button(
            fila_btns, text="🧹 Limpiar", font=FUENTE_BTN,
            bg="white", fg=PRIMARIO_BG, activebackground="#d9d9d9",
            relief="ridge", cursor="hand2", command=self.accion_limpiar
        )
        self.btn_limpiar.pack(side="left", padx=(0, 8))

        self.btn_ejemplo = tk.Button(
            fila_btns, text="⚡ Cargar ejemplo", font=FUENTE_BTN,
            bg="white", fg=PRIMARIO_BG, activebackground="#d9d9d9",
            relief="ridge", cursor="hand2", command=self.cargar_ejemplo
        )
        self.btn_ejemplo.pack(side="left", padx=(0, 0))

        # ====== Resultado ======
        fila_res = tk.Frame(cont, bg=PRIMARIO_BG)
        fila_res.pack(fill="x", pady=(10, 4))
        tk.Label(fila_res, text="🔎 Enlace resultante:", font=FUENTE, bg=PRIMARIO_BG, fg="white").pack(anchor="w")
        self.var_resultado = tk.StringVar(value="")
        self.entry_resultado = tk.Entry(fila_res, textvariable=self.var_resultado, font=FUENTE, bd=2, relief="solid", fg="#000")
        self.entry_resultado.configure(state="readonly")
        self.entry_resultado.pack(fill="x")

        # Estado/advertencias
        self.label_estado = tk.Label(self.root, text="", font=("Segoe UI", 10, "bold"), fg=ACENTO, bg=PRIMARIO_BG, justify="left")
        self.label_estado.pack(pady=(4, 0))

        # ---- Footer
        footer = tk.Frame(self.root, bg=PRIMARIO_BG)
        footer.pack(fill="x", side=tk.BOTTOM, pady=(14, 8))

        tk.Label(
            footer, text="Dev. Miguel Ramos Alarcón",
            font=FUENTE_SMALL, fg=ACENTO, bg=PRIMARIO_BG
        ).pack(side="left", padx=10)

        links = tk.Frame(footer, bg=PRIMARIO_BG)
        links.pack(side="right")
        lbl_git = tk.Label(links, text="GitHub", font=("Segoe UI", 9, "underline"), fg="white", bg=PRIMARIO_BG, cursor="hand2")
        lbl_git.pack(side="left", padx=(0, 10))
        lbl_git.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/miguelramosalarcon"))
        lbl_in = tk.Label(links, text="LinkedIn", font=("Segoe UI", 9, "underline"), fg="white", bg=PRIMARIO_BG, cursor="hand2")
        lbl_in.pack(side="left")
        lbl_in.bind("<Button-1>", lambda e: webbrowser.open_new("https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon"))

        # Enter construye
        self.root.bind("<Return>", lambda e: self.accion_construir())

    # ===== Acciones =====

    def accion_construir(self):
        numero = self.entry_numero.get().strip()
        mensaje = self.txt_mensaje.get("1.0", "end").strip()
        utm_source = self.entry_utm_source.get().strip()
        utm_medium = self.entry_utm_medium.get().strip()
        utm_campaign = self.entry_utm_campaign.get().strip()
        utm_content = self.entry_utm_content.get().strip()
        utm_term = self.entry_utm_term.get().strip()

        try:
            url = construir_link(
                numero, mensaje,
                utm_source, utm_medium, utm_campaign,
                utm_content, utm_term
            )
            # Mostrar resultado
            self.entry_resultado.configure(state="normal")
            self.entry_resultado.delete(0, "end")
            self.entry_resultado.insert(0, url)
            self.entry_resultado.configure(state="readonly")
            self.label_estado.configure(text="✅ Enlace generado correctamente.")
        except ValueError as ve:
            messagebox.showerror("Validación", str(ve))
            self.label_estado.configure(text="")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al construir el enlace:\n{e}")
            self.label_estado.configure(text="")

    def accion_copiar(self):
        url = self.var_resultado.get()
        if not url:
            messagebox.showwarning("Atención", "Primero genera el enlace.")
            return
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            self.root.update()
            self.label_estado.configure(text="📋 Enlace copiado al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar al portapapeles:\n{e}")

    def accion_copiar_html(self):
        url = self.var_resultado.get()
        if not url:
            messagebox.showwarning("Atención", "Primero genera el enlace.")
            return
        html = f'<a href="{url}" target="_blank" rel="noopener">Contactar por WhatsApp</a>'
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(html)
            self.root.update()
            self.label_estado.configure(text="📄 HTML copiado al portapapeles.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar el HTML:\n{e}")

    def accion_abrir(self):
        url = self.var_resultado.get()
        if not url:
            messagebox.showwarning("Atención", "Primero genera el enlace.")
            return
        try:
            webbrowser.open_new(url)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el navegador:\n{e}")

    def accion_limpiar(self):
        self.entry_numero.delete(0, "end")
        self.txt_mensaje.delete("1.0", "end")
        self.entry_utm_source.delete(0, "end")
        self.entry_utm_medium.delete(0, "end")
        self.entry_utm_campaign.delete(0, "end")
        self.entry_utm_content.delete(0, "end")
        self.entry_utm_term.delete(0, "end")
        self.entry_resultado.configure(state="normal")
        self.entry_resultado.delete(0, "end")
        self.entry_resultado.configure(state="readonly")
        self.label_estado.configure(text="")

    def cargar_ejemplo(self):
        self.entry_numero.delete(0, "end")
        self.entry_numero.insert(0, "+51 986 397 210")

        self.txt_mensaje.delete("1.0", "end")
        self.txt_mensaje.insert("1.0", "Hola, necesito diagnóstico o instalación para un conchador refinador.")

        self.entry_utm_source.delete(0, "end")
        self.entry_utm_source.insert(0, "landing-linea-frio")

        self.entry_utm_medium.delete(0, "end")
        self.entry_utm_medium.insert(0, "boton")

        self.entry_utm_campaign.delete(0, "end")
        self.entry_utm_campaign.insert(0, "servicio-tecnico")

        self.entry_utm_content.delete(0, "end")
        self.entry_utm_content.insert(0, "hero-principal")

        self.entry_utm_term.delete(0, "end")
        self.entry_utm_term.insert(0, "maquinas-de-hielo")

        self.label_estado.configure(text="📌 Ejemplo cargado. Ahora haz clic en “Construir enlace”.")

# ==========================
# Main
# ==========================

if __name__ == "__main__":
    root = tk.Tk()
    app = WALinkBuilderApp(root)
    root.mainloop()

