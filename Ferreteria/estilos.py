# estilos.py - Configuración de estilos modernos para la interfaz gráfica

# ============================================
# VARIABLES DE COMPATIBILIDAD (para main.py)
# ============================================
COLOR_PRIMARIO = "#1E3A8A"  # Azul profundo moderno
COLOR_SECUNDARIO = "#3B82F6"  # Azul brillante
COLOR_FONDO = "#F8FAFC"  # Fondo principal (gris muy claro)
COLOR_EXITO = "#10B981"  # Verde esmeralda
COLOR_PELIGRO = "#EF4444"  # Rojo coral
COLOR_ADVERTENCIA = "#F59E0B"  # Ámbar cálido
COLOR_TEXTO = "#1E293B"  # Azul muy oscuro
COLOR_TEXTO_CLARO = "#FFFFFF"  # Blanco

# ============================================
# NUEVOS COLORES MODERNOS
# ============================================
COLOR_TERCIARIO = "#10B981"  # Verde esmeralda
COLOR_CUATERNARIO = "#8B5CF6"  # Púrpura vibrante
COLOR_INFO = "#3B82F6"  # Azul informativo

# Colores de fondo adicionales
COLOR_FONDO_PRINCIPAL = COLOR_FONDO  # Alias
COLOR_FONDO_SECUNDARIO = "#FFFFFF"  # Blanco puro
COLOR_FONDO_TERCIARIO = "#F1F5F9"  # Gris suave

# Colores de texto adicionales
COLOR_TEXTO_OSCURO = COLOR_TEXTO  # Alias
COLOR_TEXTO_MEDIO = "#475569"  # Gris azulado
COLOR_TEXTO_DESTACADO = "#1E3A8A"  # Azul destacado

# Gradientes para botones
GRADIENTE_PRIMARIO = ["#2563EB", "#1D4ED8"]  # Azul gradiente
GRADIENTE_EXITO = ["#10B981", "#059669"]  # Verde gradiente
GRADIENTE_PELIGRO = ["#EF4444", "#DC2626"]  # Rojo gradiente
GRADIENTE_SECUNDARIO = ["#8B5CF6", "#7C3AED"]  # Púrpura gradiente

# Fuentes modernas
FUENTE_TITULO = ("Segoe UI", 22, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 16, "bold")
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 10, "bold")
FUENTE_PEQUEÑA = ("Segoe UI", 9)
FUENTE_MONEDA = ("Segoe UI", 12, "bold")

# Configuraciones de botones con efecto hover moderno
ESTILO_BOTON_PRINCIPAL = {
    "font": FUENTE_BOTON,
    "bg": COLOR_PRIMARIO,
    "fg": COLOR_TEXTO_CLARO,
    "activebackground": "#1D4ED8",
    "activeforeground": COLOR_TEXTO_CLARO,
    "relief": "flat",
    "cursor": "hand2",
    "padx": 24,
    "pady": 12,
    "border": 0,
    "highlightthickness": 0,
    "bd": 0
}

ESTILO_BOTON_EXITO = {
    "font": FUENTE_BOTON,
    "bg": COLOR_EXITO,
    "fg": COLOR_TEXTO_CLARO,
    "activebackground": "#059669",
    "activeforeground": COLOR_TEXTO_CLARO,
    "relief": "flat",
    "cursor": "hand2",
    "padx": 24,
    "pady": 12,
    "border": 0,
    "highlightthickness": 0,
    "bd": 0
}

ESTILO_BOTON_PELIGRO = {
    "font": FUENTE_BOTON,
    "bg": COLOR_PELIGRO,
    "fg": COLOR_TEXTO_CLARO,
    "activebackground": "#DC2626",
    "activeforeground": COLOR_TEXTO_CLARO,
    "relief": "flat",
    "cursor": "hand2",
    "padx": 24,
    "pady": 12,
    "border": 0,
    "highlightthickness": 0,
    "bd": 0
}

ESTILO_BOTON_SECUNDARIO = {
    "font": FUENTE_BOTON,
    "bg": "#95A5A6",  # Manteniendo el original para compatibilidad
    "fg": COLOR_TEXTO_CLARO,
    "activebackground": "#7F8C8D",
    "activeforeground": COLOR_TEXTO_CLARO,
    "relief": "flat",
    "cursor": "hand2",
    "padx": 20,  # Manteniendo original
    "pady": 10   # Manteniendo original
}

ESTILO_BOTON_TERCIARIO = {
    "font": FUENTE_BOTON,
    "bg": COLOR_SECUNDARIO,  # Usando COLOR_SECUNDARIO
    "fg": COLOR_TEXTO_CLARO,
    "activebackground": "#2563EB",
    "activeforeground": COLOR_TEXTO_CLARO,
    "relief": "flat",
    "cursor": "hand2",
    "padx": 24,
    "pady": 12,
    "border": 0,
    "highlightthickness": 0,
    "bd": 0
}

# Configuraciones de entradas de texto modernas
ESTILO_ENTRY = {
    "font": FUENTE_NORMAL,
    "relief": "solid",  # Manteniendo original para compatibilidad
    "borderwidth": 1
}

# Configuraciones de etiquetas modernas
ESTILO_LABEL_TITULO = {
    "font": FUENTE_TITULO,
    "bg": COLOR_FONDO,
    "fg": COLOR_PRIMARIO
}

ESTILO_LABEL_SUBTITULO = {
    "font": FUENTE_SUBTITULO,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO_MEDIO
}

ESTILO_LABEL_NORMAL = {
    "font": FUENTE_NORMAL,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO
}

ESTILO_LABEL_SECUNDARIO = {
    "font": FUENTE_NORMAL,
    "bg": COLOR_FONDO,
    "fg": COLOR_TEXTO_MEDIO
}

ESTILO_LABEL_DESTACADO = {
    "font": FUENTE_MONEDA,
    "bg": COLOR_FONDO,
    "fg": COLOR_EXITO
}

# Configuraciones de frames con sombras sutiles
ESTILO_FRAME_PRINCIPAL = {
    "bg": COLOR_FONDO,
    "relief": "flat"
}

ESTILO_FRAME_SECUNDARIO = {
    "bg": COLOR_FONDO_SECUNDARIO,  # Blanco para contraste
    "relief": "solid",
    "borderwidth": 1
}

ESTILO_FRAME_TARJETA = {
    "bg": COLOR_FONDO_SECUNDARIO,
    "relief": "flat",
    "highlightthickness": 0,
    "bd": 0
}

ESTILO_FRAME_ACENTUADO = {
    "bg": COLOR_FONDO_TERCIARIO,
    "relief": "flat",
    "highlightthickness": 0,
    "bd": 0
}

# Configuraciones de Treeview (tablas) modernas
ESTILO_TREEVIEW = {
    "background": COLOR_FONDO_SECUNDARIO,
    "foreground": COLOR_TEXTO_OSCURO,
    "fieldbackground": COLOR_FONDO_SECUNDARIO,
    "font": FUENTE_NORMAL,
    "rowheight": 30
}

# Estilos para encabezados de tabla
ESTILO_TREEVIEW_HEADING = {
    "background": COLOR_FONDO_TERCIARIO,
    "foreground": COLOR_TEXTO_OSCURO,
    "relief": "flat",
    "borderwidth": 0,
    "font": ("Segoe UI", 10, "bold")
}

# Configuraciones de Combobox modernas
ESTILO_COMBOBOX = {
    "font": FUENTE_NORMAL,
    "state": "readonly"
}

# Configuraciones de separadores
ESTILO_SEPARADOR = {
    "bg": "#E2E8F0",
    "height": 1,
    "relief": "flat"
}

# Configuraciones de notificaciones/alerts
ESTILO_ALERTA_EXITO = {
    "bg": "#D1FAE5",
    "fg": "#065F46",
    "font": FUENTE_NORMAL,
    "relief": "flat",
    "bd": 1,
    "highlightbackground": "#A7F3D0"
}

ESTILO_ALERTA_ERROR = {
    "bg": "#FEE2E2",
    "fg": "#991B1B",
    "font": FUENTE_NORMAL,
    "relief": "flat",
    "bd": 1,
    "highlightbackground": "#FECACA"
}

ESTILO_ALERTA_ADVERTENCIA = {
    "bg": "#FEF3C7",
    "fg": "#92400E",
    "font": FUENTE_NORMAL,
    "relief": "flat",
    "bd": 1,
    "highlightbackground": "#FDE68A"
}

# Dimensiones de ventana
ANCHO_VENTANA = 1300
ALTO_VENTANA = 750
PADDING_GENERAL = 12
PADDING_PEQUEÑO = 6
PADDING_GRANDE = 20

# Configuraciones de scrollbar modernas
ESTILO_SCROLLBAR = {
    "troughcolor": COLOR_FONDO_TERCIARIO,
    "background": COLOR_SECUNDARIO,
    "borderwidth": 0,
    "relief": "flat",
    "width": 12
}

# Estilos para badges/etiquetas
ESTILO_BADGE_EXITO = {
    "bg": "#D1FAE5",
    "fg": "#065F46",
    "font": ("Segoe UI", 9, "bold"),
    "relief": "flat",
    "padx": 8,
    "pady": 4,
    "bd": 0
}

ESTILO_BADGE_PELIGRO = {
    "bg": "#FEE2E2",
    "fg": "#991B1B",
    "font": ("Segoe UI", 9, "bold"),
    "relief": "flat",
    "padx": 8,
    "pady": 4,
    "bd": 0
}

ESTILO_BADGE_INFO = {
    "bg": "#DBEAFE",
    "fg": "#1E40AF",
    "font": ("Segoe UI", 9, "bold"),
    "relief": "flat",
    "padx": 8,
    "pady": 4,
    "bd": 0
}

# Estilos para tarjetas de estadísticas
ESTILO_TARJETA_ESTADISTICA = {
    "bg": COLOR_FONDO_SECUNDARIO,
    "relief": "flat",
    "highlightthickness": 1,
    "highlightbackground": "#E2E8F0",
    "bd": 0
}

# Importar tkinter para las funciones de ayuda
import tkinter as tk

# Funciones de ayuda para crear elementos con estilo
def crear_boton_redondeado(parent, texto, comando, estilo=ESTILO_BOTON_PRINCIPAL, radio=8):
    """Crea un botón con bordes redondeados"""
    btn = tk.Button(parent, text=texto, command=comando, **estilo)
    return btn

def crear_frame_con_sombra(parent, estilo=ESTILO_FRAME_TARJETA):
    """Crea un frame con efecto de sombra sutil"""
    frame = tk.Frame(parent, **estilo)
    return frame

def crear_badge(parent, texto, estilo=ESTILO_BADGE_INFO):
    """Crea una etiqueta estilo badge"""
    badge = tk.Label(parent, text=texto, **estilo)
    return badge

def crear_separador_horizontal(parent):
    """Crea un separador horizontal"""
    separator = tk.Frame(parent, **ESTILO_SEPARADOR)
    return separator

# Estilos para diferentes tipos de datos
ESTILO_MONEDA = {
    "font": FUENTE_MONEDA,
    "bg": COLOR_FONDO,
    "fg": COLOR_EXITO
}

ESTILO_MONEDA_NEGATIVA = {
    "font": FUENTE_MONEDA,
    "bg": COLOR_FONDO,
    "fg": COLOR_PELIGRO
}

ESTILO_CANTIDAD = {
    "font": ("Segoe UI", 11, "bold"),
    "bg": COLOR_FONDO,
    "fg": COLOR_PRIMARIO
}

# Clase para botones con hover effects personalizados
class BotonModerno(tk.Button):
    def __init__(self, parent, texto, comando=None, estilo_base=ESTILO_BOTON_PRINCIPAL, color_hover=None, **kwargs):
        # Combinar estilos
        estilo_final = estilo_base.copy()
        estilo_final.update(kwargs)
        
        super().__init__(parent, text=texto, command=comando, **estilo_final)
        
        # Configurar efectos hover
        self.color_normal = estilo_final.get('bg', COLOR_PRIMARIO)
        self.color_hover = color_hover or self._oscurecer_color(self.color_normal, 0.2)
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, e):
        self.configure(bg=self.color_hover)
    
    def _on_leave(self, e):
        self.configure(bg=self.color_normal)
    
    @staticmethod
    def _oscurecer_color(color, factor=0.2):
        """Oscurece un color hexadecimal"""
        if len(color) == 7 and color[0] == '#':
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = int(max(0, r * (1 - factor)))
            g = int(max(0, g * (1 - factor)))
            b = int(max(0, b * (1 - factor)))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color

# Estilos para pestañas (Notebook)
ESTILO_NOTEBOOK = {
    "background": COLOR_FONDO,
    "borderwidth": 0
}

ESTILO_NOTEBOOK_TAB = {
    "background": COLOR_FONDO_TERCIARIO,
    "foreground": COLOR_TEXTO_MEDIO,
    "padding": [12, 6],
    "font": ("Segoe UI", 10, "bold")
}

ESTILO_NOTEBOOK_TAB_SELECCIONADA = {
    "background": COLOR_FONDO_SECUNDARIO,
    "foreground": COLOR_PRIMARIO,
    "padding": [12, 6],
    "font": ("Segoe UI", 10, "bold")
}

# Configuración de tema oscuro (opcional)
COLORES_TEMA_OSCURO = {
    "fondo_principal": "#0F172A",
    "fondo_secundario": "#1E293B",
    "fondo_terciario": "#334155",
    "texto_oscuro": "#F1F5F9",
    "texto_medio": "#CBD5E1",
    "texto_claro": "#FFFFFF",
    "primario": "#3B82F6",
    "secundario": "#8B5CF6"
}

# Nota: Para usar el tema oscuro, se necesitaría una función que cambie dinámicamente los estilos