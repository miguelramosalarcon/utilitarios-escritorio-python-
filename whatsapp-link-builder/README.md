# 💬 WA Link Builder - Generador de enlaces WhatsApp con parámetros UTM

Una herramienta de escritorio moderna y profesional para **crear enlaces personalizados de WhatsApp (`wa.me`)** con texto automático y parámetros de seguimiento **UTM**, ideal para campañas digitales, formularios de contacto, catálogos o páginas web.

> ✅ Creado por: [**Miguel Ramos Alarcón**](https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon)  
> 🧑‍💼 **Programador Web | Especialista SEO | Soporte TI**

---

## 🚀 Características principales

- 🧮 Genera enlaces listos para WhatsApp con texto precargado  
- 🔗 Permite añadir parámetros **UTM** para seguimiento en Google Analytics  
- 🧠 Valida automáticamente el número de teléfono (formato +51 / 51999999999)  
- 📋 Copia el enlace o su versión HTML con un solo clic  
- 🌐 Abre el enlace directamente en el navegador  
- ⚡ Incluye ejemplo precargado y opción para limpiar campos  
- 🎨 Diseño profesional con branding MRStudio  
- 🪶 Desarrollado con Python + Tkinter + PyInstaller  

---

## 🖼 Vista general de la interfaz

| Interfaz principal |  |
|--------------------|--|
| ![WA Link Builder](./screenshot/wa-link-builder-ui.jpg) | |

---

## 🧭 Descripción de cada sección

### 🧩 1. Cabecera
**Título:**  
> “Generador de enlaces WhatsApp (wa.me)”  
Explica la función principal de la app.  
Bajo el título se muestra una breve instrucción:  
> “Ingrese número (con código de país), mensaje y parámetros UTM/extra.”

---

### 📱 2. Campo de número
**Etiqueta:** “Número (con código de país)”  
- Permite ingresar el número al cual se enviará el mensaje.  
- Se aceptan formatos como:  
+51977876360
51 977 876 360
(51) 977-876-360

- El sistema limpiará automáticamente espacios, paréntesis y guiones.  
- El número se valida antes de generar el enlace.

---

### 💬 3. Texto del mensaje
Caja de texto donde puedes escribir el mensaje que aparecerá precargado en WhatsApp.  
Ejemplo:  
> “Hola, necesito diagnóstico o instalación para un conchador refinador.”

---

### 🧭 4. Parámetros UTM

Los **UTM** (Urchin Tracking Module) son etiquetas que se añaden a las URLs para **medir el origen y rendimiento de campañas digitales** en herramientas como **Google Analytics**.  
Permiten saber **desde dónde** llega un clic (botón, landing, anuncio, etc.).

| Parámetro | Descripción | Ejemplo |
|------------|--------------|----------|
| `utm_source` | Fuente o plataforma que origina el clic | `landing-linea-frio`, `instagram`, `facebook` |
| `utm_medium` | Medio o tipo de canal | `boton`, `banner`, `email` |
| `utm_campaign` | Nombre de la campaña o promoción | `servicio-tecnico`, `promo-navidad` |
| `utm_content` | Diferenciador del contenido | `hero-principal`, `sidebar` |
| `utm_term` | Palabra clave o producto | `maquinas-de-hielo`, `hornos-industriales` |

Cada parámetro es opcional, pero al completarlos correctamente podrás analizar en Analytics desde qué sección o medio provienen tus contactos por WhatsApp.

---

### 🧰 5. Botones principales

| Botón | Función |
|--------|---------|
| **🛠 Construir enlace** | Genera el enlace `wa.me` con el número, mensaje y parámetros UTM. |
| **📋 Copiar enlace** | Copia el enlace completo al portapapeles. |
| **📄 Copiar como HTML** | Copia una versión HTML lista para insertar en una web:<br>`<a href="...">Contactar por WhatsApp</a>` |
| **🌐 Abrir en navegador** | Abre el enlace generado directamente en tu navegador predeterminado. |
| **🧹 Limpiar** | Borra todos los campos del formulario. |
| **⚡ Cargar ejemplo** | Completa los campos automáticamente con un ejemplo práctico para probar. |

---

### 🔎 6. Resultado
Campo de solo lectura donde aparece el enlace final generado.  
Ejemplo:
https://wa.me/51977876360?text=Hola%2C%20necesito%20diagn%C3%B3stico%20o%20instalaci%C3%B3n&utm_source=landing-linea-frio&utm_medium=boton&utm_campaign=servicio-tecnico&utm_content=hero-principal&utm_term=maquinas-de-hielo


Puedes copiarlo o abrirlo directamente.

---

### 🧑‍💻 7. Pie de página
Muestra tu firma profesional:  
> “Dev. Miguel Ramos Alarcón”  
con enlaces directos a tu **GitHub** y **LinkedIn**.  

---

## 📦 Estructura de carpeta
wa-link-builder/
│
├── WA_Link_Builder.exe # Ejecutable final portable
├── wa_link_builder.py # Código fuente (GUI + lógica)
├── wa_link_builder.spec # Configuración de compilación PyInstaller
├── logo_miguel.ico # Ícono personalizado MRStudio
├── screenshots/ # Capturas de interfaz
└── README.md # Este archivo


---

## ✨ Ejemplo de uso rápido

1️⃣ Ingresa el número: `+51977876360`  
2️⃣ Escribe el mensaje: `Hola, necesito una cotización.`  
3️⃣ Completa UTMs:  
utm_source = landing-principal
utm_medium = boton
utm_campaign = promo-lanzamiento

4️⃣ Haz clic en **Construir enlace**  
5️⃣ Copia o abre el enlace en el navegador 🚀

---

## 📬 Contacto

Desarrollado con 💙 por **Miguel Ramos Alarcón**  
📌 [LinkedIn](https://pe.linkedin.com/in/miguel-alonso-ramos-alarcon)  
📁 [GitHub](https://github.com/miguelramosalarcon)

> [!IMPORTANT]
> _"En medio de la adversidad, reside la oportunidad." — Albert Einstein_

---

## 🧪 Licencia

Este proyecto está licenciado bajo la **MIT License**.  
Eres libre de usarlo, modificarlo y compartirlo, siempre reconociendo la autoría.

---


