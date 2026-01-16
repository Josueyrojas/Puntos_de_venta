# main.py - Clase principal del punto de venta

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from metodos import (
    Gestor_Inventario, GestorVentas, GestorProveedores, GestorClientes,
    ProductoVenta, GeneradorReportes, GeneradorTicket, validar_numero, 
    formatear_moneda, obtener_regimenes_fiscales, obtener_usos_cfdi
)
from estilos import *


class PuntoVenta:
    """Clase principal del punto de venta"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Punto de Venta")
        self.root.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.root.configure(bg=COLOR_FONDO)
        
        # Inicializar gestores
        self.gestor_inventario = Gestor_Inventario()
        self.gestor_ventas = GestorVentas(self.gestor_inventario)  # Ahora recibe gestor_inventario
        self.gestor_proveedores = GestorProveedores()
        self.gestor_clientes = GestorClientes()
        self.generador_reportes = GeneradorReportes(self.gestor_ventas)
        
        # Variables
        self.var_descripcion = tk.StringVar()  # Cambiado de var_codigo a var_descripcion
        self.var_cantidad = tk.StringVar(value="1")
        self.var_pago = tk.StringVar()
        
        # Crear interfaz con pestañas
        self.crear_interfaz()
        self.actualizar_totales()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica completa con pestañas"""
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        
        # Pestaña Punto de Venta
        frame_venta = tk.Frame(self.notebook, **ESTILO_FRAME_PRINCIPAL)
        self.notebook.add(frame_venta, text="Punto de Venta")
        self.crear_pestana_venta(frame_venta)
        
        # Pestaña Inventario
        frame_inventario = tk.Frame(self.notebook, **ESTILO_FRAME_PRINCIPAL)
        self.notebook.add(frame_inventario, text="Inventario")
        self.crear_pestana_inventario(frame_inventario)
        
        # Pestaña Clientes
        frame_clientes = tk.Frame(self.notebook, **ESTILO_FRAME_PRINCIPAL)
        self.notebook.add(frame_clientes, text="Clientes")
        self.crear_pestana_clientes(frame_clientes)
        
        # Pestaña Proveedores
        frame_proveedores = tk.Frame(self.notebook, **ESTILO_FRAME_PRINCIPAL)
        self.notebook.add(frame_proveedores, text="Proveedores")
        self.crear_pestana_proveedores(frame_proveedores)
    
    def crear_pestana_venta(self, parent):
        """Crea la pestaña de punto de venta"""
        # Título
        label_titulo = tk.Label(parent, text="PUNTO DE VENTA", **ESTILO_LABEL_TITULO)
        label_titulo.pack(pady=(0, 20))
        
        # Frame superior (entrada de productos)
        self.crear_frame_entrada(parent)
        
        # Frame central (tabla de productos)
        self.crear_frame_tabla(parent)
        
        # Frame inferior (totales y pago)
        self.crear_frame_totales(parent)
        
        # Frame de botones de acción
        self.crear_frame_acciones(parent)
    
    def crear_frame_entrada(self, parent):
        """Crea el frame de entrada de productos con autocompletado"""
        frame_entrada = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_entrada.pack(fill=tk.BOTH, expand=False, pady=(0, 10), padx=PADDING_GENERAL)
        
        # Frame superior con entrada y cantidad
        frame_superior = tk.Frame(frame_entrada, bg=COLOR_FONDO)
        frame_superior.pack(fill=tk.X, pady=(0, 5))
        
        # DESCRIPCIÓN del producto
        tk.Label(frame_superior, text="Descripción:", **ESTILO_LABEL_NORMAL).grid(
            row=0, column=0, padx=PADDING_GENERAL, pady=PADDING_GENERAL, sticky="w"
        )
        self.entry_descripcion = tk.Entry(frame_superior, textvariable=self.var_descripcion, **ESTILO_ENTRY, width=25)
        self.entry_descripcion.grid(row=0, column=1, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        self.entry_descripcion.bind('<Return>', lambda e: self.agregar_producto())
        self.entry_descripcion.bind('<KeyRelease>', lambda e: self.actualizar_sugerencias())
        self.entry_descripcion.focus()
        
        # Cantidad
        tk.Label(frame_superior, text="Cantidad:", **ESTILO_LABEL_NORMAL).grid(
            row=0, column=2, padx=PADDING_GENERAL, pady=PADDING_GENERAL, sticky="w"
        )
        entry_cantidad = tk.Entry(frame_superior, textvariable=self.var_cantidad, **ESTILO_ENTRY, width=10)
        entry_cantidad.grid(row=0, column=3, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        entry_cantidad.bind('<Return>', lambda e: self.agregar_producto())
        
        # Botón agregar
        btn_agregar = tk.Button(
            frame_superior, 
            text="AGREGAR (F3)", 
            command=self.agregar_producto,
            **ESTILO_BOTON_PRINCIPAL
        )
        btn_agregar.grid(row=0, column=4, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        
        # Frame inferior con lista de sugerencias
        frame_sugerencias = tk.Frame(frame_entrada, bg=COLOR_FONDO)
        frame_sugerencias.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame_sugerencias, text="Productos encontrados (Doble clic para agregar):", 
                **ESTILO_LABEL_SECUNDARIO).pack(anchor="w", padx=5, pady=(5, 2))
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(frame_sugerencias)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox de sugerencias
        self.lista_sugerencias = tk.Listbox(
            frame_sugerencias, 
            height=6, 
            font=FUENTE_NORMAL,
            yscrollcommand=scrollbar.set
        )
        self.lista_sugerencias.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.lista_sugerencias.bind('<Double-Button-1>', self.seleccionar_producto_sugerido)
        scrollbar.config(command=self.lista_sugerencias.yview)
    
    def actualizar_sugerencias(self):
        """Actualiza la lista de sugerencias mientras el usuario escribe"""
        descripcion = self.var_descripcion.get().strip()
        self.lista_sugerencias.delete(0, tk.END)
        
        if not descripcion:
            return
        
        # Buscar productos que coincidan
        resultados = self.gestor_inventario.buscar_producto_por_descripcion(descripcion)
        
        # Mostrar hasta 10 resultados
        for codigo_barras, producto in resultados[:10]:
            nombre = producto.get('nombre', '')
            precio = producto.get('precio_minorista', 0)
            stock = producto.get('stock', 0)
            
            # Mostrar nombre, precio y stock
            texto = f"{nombre} - ${precio:.2f} (Stock: {stock})"
            self.lista_sugerencias.insert(tk.END, texto)
    
    def seleccionar_producto_sugerido(self, event=None):
        """Selecciona un producto de la lista de sugerencias"""
        seleccion = self.lista_sugerencias.curselection()
        if not seleccion:
            return
        
        indice = seleccion[0]
        descripcion = self.var_descripcion.get().strip()
        
        if not descripcion:
            return
        
        # Buscar el producto nuevamente para obtener datos completos
        resultados = self.gestor_inventario.buscar_producto_por_descripcion(descripcion)
        
        if indice < len(resultados):
            # Establecer cantidad en 1 por defecto
            self.var_cantidad.set("1")
            
            # Agregar el producto
            self.agregar_producto()

    
    def crear_pestana_inventario(self, parent):
        """Crea la pestaña de gestión de inventario"""
        # Título
        label_titulo = tk.Label(parent, text="GESTIÓN DE INVENTARIO", **ESTILO_LABEL_TITULO)
        label_titulo.pack(pady=(0, 20))
        
        # Frame de formulario
        frame_form = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_form.pack(fill=tk.X, pady=(0, 10))
        
        # Variables para el formulario
        self.var_inv_codigo_barras = tk.StringVar()
        self.var_inv_codigo = tk.StringVar()
        self.var_inv_numero_producto = tk.StringVar()
        self.var_inv_nombre = tk.StringVar()
        self.var_inv_descripcion = tk.StringVar()
        self.var_inv_clasificacion = tk.StringVar()
        self.var_inv_precio_minorista = tk.StringVar()
        self.var_inv_precio_mayoreo = tk.StringVar()
        self.var_inv_costo = tk.StringVar()
        self.var_inv_proveedor = tk.StringVar()
        self.var_inv_unidad = tk.StringVar(value="pz")
        self.var_inv_fabricante = tk.StringVar()
        self.var_inv_tipo = tk.StringVar()
        self.var_inv_codigoA = tk.StringVar()
        self.var_inv_codigoB = tk.StringVar()
        self.var_inv_codigoC = tk.StringVar()
        self.var_inv_stock = tk.StringVar()
        
        # Primera fila
        tk.Label(frame_form, text="Cód. Barras:", **ESTILO_LABEL_NORMAL).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_codigo_barras, **ESTILO_ENTRY, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Código:", **ESTILO_LABEL_NORMAL).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_codigo, **ESTILO_ENTRY, width=15).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="No. Producto:", **ESTILO_LABEL_NORMAL).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_numero_producto, **ESTILO_ENTRY, width=10).grid(row=0, column=5, padx=5, pady=5)
        
        # Segunda fila
        tk.Label(frame_form, text="Nombre:", **ESTILO_LABEL_NORMAL).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_nombre, **ESTILO_ENTRY, width=30).grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        tk.Label(frame_form, text="Proveedor:", **ESTILO_LABEL_NORMAL).grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.combo_proveedores = ttk.Combobox(frame_form, textvariable=self.var_inv_proveedor, **ESTILO_COMBOBOX, width=20)
        self.combo_proveedores.grid(row=1, column=4, columnspan=2, padx=5, pady=5)
        self.actualizar_combo_proveedores()
        
        # Tercera fila
        tk.Label(frame_form, text="Precio Minorista:", **ESTILO_LABEL_NORMAL).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_precio_minorista, **ESTILO_ENTRY, width=12).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Precio Mayoreo:", **ESTILO_LABEL_NORMAL).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_precio_mayoreo, **ESTILO_ENTRY, width=12).grid(row=2, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Costo:", **ESTILO_LABEL_NORMAL).grid(row=2, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_costo, **ESTILO_ENTRY, width=12).grid(row=2, column=5, padx=5, pady=5)
        
        # Cuarta fila
        tk.Label(frame_form, text="Clasificación:", **ESTILO_LABEL_NORMAL).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_clasificacion, **ESTILO_ENTRY, width=15).grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Fabricante:", **ESTILO_LABEL_NORMAL).grid(row=3, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_fabricante, **ESTILO_ENTRY, width=15).grid(row=3, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Tipo:", **ESTILO_LABEL_NORMAL).grid(row=3, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_tipo, **ESTILO_ENTRY, width=15).grid(row=3, column=5, padx=5, pady=5)
        
        # Quinta fila
        tk.Label(frame_form, text="Descripción:", **ESTILO_LABEL_NORMAL).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_descripcion, **ESTILO_ENTRY, width=50).grid(row=4, column=1, columnspan=4, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_form, text="Unidad:", **ESTILO_LABEL_NORMAL).grid(row=4, column=5, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_unidad, **ESTILO_ENTRY, width=5).grid(row=4, column=6, padx=5, pady=5)
        
        # Sexta fila
        tk.Label(frame_form, text="Código A:", **ESTILO_LABEL_NORMAL).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_codigoA, **ESTILO_ENTRY, width=15).grid(row=5, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Código B:", **ESTILO_LABEL_NORMAL).grid(row=5, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_codigoB, **ESTILO_ENTRY, width=15).grid(row=5, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Código C:", **ESTILO_LABEL_NORMAL).grid(row=5, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_codigoC, **ESTILO_ENTRY, width=15).grid(row=5, column=5, padx=5, pady=5)
        
        tk.Label(frame_form, text="Stock:", **ESTILO_LABEL_NORMAL).grid(row=5, column=6, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_inv_stock, **ESTILO_ENTRY, width=10).grid(row=5, column=7, padx=5, pady=5)
        
        # Botones
        frame_botones = tk.Frame(frame_form, bg=COLOR_FONDO)
        frame_botones.grid(row=6, column=0, columnspan=8, pady=10)
        
        tk.Button(frame_botones, text="AGREGAR", command=self.agregar_producto_inventario, **ESTILO_BOTON_EXITO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="EDITAR", command=self.editar_producto_inventario, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="ELIMINAR", command=self.eliminar_producto_inventario, **ESTILO_BOTON_PELIGRO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="LIMPIAR", command=self.limpiar_formulario_inventario, **ESTILO_BOTON_SECUNDARIO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="IMPORTAR", command=self.importar_inventario, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="EXPORTAR", command=self.exportar_inventario, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="GENERAR PLANTILLA", command=self.generar_plantilla_inventario, **ESTILO_BOTON_SECUNDARIO).pack(side=tk.LEFT, padx=5)
        
        # Tabla de productos
        self.crear_tabla_inventario(parent)
    
    def crear_pestana_clientes(self, parent):
        """Crea la pestaña de gestión de clientes"""
        # Título
        label_titulo = tk.Label(parent, text="GESTIÓN DE CLIENTES", **ESTILO_LABEL_TITULO)
        label_titulo.pack(pady=(0, 20))
        
        # Frame de formulario
        frame_form = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_form.pack(fill=tk.X, pady=(0, 10))
        
        # Variables para el formulario
        self.var_cli_rfc = tk.StringVar()
        self.var_cli_razon_social = tk.StringVar()
        self.var_cli_regimen_fiscal = tk.StringVar()
        self.var_cli_uso_cfdi = tk.StringVar()
        self.var_cli_codigo_postal = tk.StringVar()
        self.var_cli_direccion_fiscal = tk.StringVar()
        self.var_cli_estado = tk.StringVar()
        self.var_cli_ciudad = tk.StringVar()
        self.var_cli_municipio = tk.StringVar()
        self.var_cli_colonia = tk.StringVar()
        self.var_cli_telefono = tk.StringVar()
        self.var_cli_correo = tk.StringVar()
        
        # Primera fila
        tk.Label(frame_form, text="RFC:", **ESTILO_LABEL_NORMAL).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_rfc, **ESTILO_ENTRY, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Razón Social:", **ESTILO_LABEL_NORMAL).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_razon_social, **ESTILO_ENTRY, width=40).grid(row=0, column=3, columnspan=3, padx=5, pady=5)
        
        # Segunda fila
        tk.Label(frame_form, text="Régimen Fiscal:", **ESTILO_LABEL_NORMAL).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.combo_regimen_fiscal = ttk.Combobox(frame_form, textvariable=self.var_cli_regimen_fiscal, **ESTILO_COMBOBOX, width=40)
        self.combo_regimen_fiscal.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        self.cargar_regimenes_fiscales()
        
        tk.Label(frame_form, text="Uso CFDI:", **ESTILO_LABEL_NORMAL).grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.combo_uso_cfdi = ttk.Combobox(frame_form, textvariable=self.var_cli_uso_cfdi, **ESTILO_COMBOBOX, width=30)
        self.combo_uso_cfdi.grid(row=1, column=5, columnspan=2, padx=5, pady=5)
        self.cargar_usos_cfdi()
        
        # Tercera fila
        tk.Label(frame_form, text="Código Postal:", **ESTILO_LABEL_NORMAL).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_codigo_postal, **ESTILO_ENTRY, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Estado:", **ESTILO_LABEL_NORMAL).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_estado, **ESTILO_ENTRY, width=20).grid(row=2, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Ciudad:", **ESTILO_LABEL_NORMAL).grid(row=2, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_ciudad, **ESTILO_ENTRY, width=20).grid(row=2, column=5, padx=5, pady=5)
        
        # Cuarta fila
        tk.Label(frame_form, text="Municipio:", **ESTILO_LABEL_NORMAL).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_municipio, **ESTILO_ENTRY, width=20).grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Colonia:", **ESTILO_LABEL_NORMAL).grid(row=3, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_colonia, **ESTILO_ENTRY, width=20).grid(row=3, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Teléfono:", **ESTILO_LABEL_NORMAL).grid(row=3, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_telefono, **ESTILO_ENTRY, width=20).grid(row=3, column=5, padx=5, pady=5)
        
        # Quinta fila
        tk.Label(frame_form, text="Dirección Fiscal:", **ESTILO_LABEL_NORMAL).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_direccion_fiscal, **ESTILO_ENTRY, width=50).grid(row=4, column=1, columnspan=4, padx=5, pady=5)
        
        tk.Label(frame_form, text="Correo:", **ESTILO_LABEL_NORMAL).grid(row=4, column=5, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cli_correo, **ESTILO_ENTRY, width=25).grid(row=4, column=6, padx=5, pady=5)
        
        # Botones
        frame_botones = tk.Frame(frame_form, bg=COLOR_FONDO)
        frame_botones.grid(row=5, column=0, columnspan=7, pady=10)
        
        tk.Button(frame_botones, text="AGREGAR", command=self.agregar_cliente, **ESTILO_BOTON_EXITO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="EDITAR", command=self.editar_cliente, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="ELIMINAR", command=self.eliminar_cliente, **ESTILO_BOTON_PELIGRO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="LIMPIAR", command=self.limpiar_formulario_clientes, **ESTILO_BOTON_SECUNDARIO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="IMPORTAR CSV", command=self.importar_clientes_csv, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="EXPORTAR CSV", command=self.exportar_clientes_csv, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="GENERAR PLANTILLA", command=self.generar_plantilla_clientes, **ESTILO_BOTON_SECUNDARIO).pack(side=tk.LEFT, padx=5)
        
        # Tabla de clientes
        self.crear_tabla_clientes(parent)
    
    def crear_pestana_proveedores(self, parent):
        """Crea la pestaña de gestión de proveedores"""
        # Título
        label_titulo = tk.Label(parent, text="GESTIÓN DE PROVEEDORES", **ESTILO_LABEL_TITULO)
        label_titulo.pack(pady=(0, 20))
        
        # Frame de formulario
        frame_form = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_form.pack(fill=tk.X, pady=(0, 10))
        
        # Variables para el formulario
        self.var_prov_id = tk.StringVar()
        self.var_prov_alias = tk.StringVar()
        self.var_prov_rfc = tk.StringVar()
        self.var_prov_razon_social = tk.StringVar()
        self.var_prov_personal = tk.StringVar()
        self.var_prov_telefono = tk.StringVar()
        self.var_prov_codigo_postal = tk.StringVar()
        self.var_prov_estado = tk.StringVar()
        self.var_prov_ciudad = tk.StringVar()
        self.var_prov_municipio = tk.StringVar()
        self.var_prov_colonia = tk.StringVar()
        self.var_prov_direccion = tk.StringVar()
        self.var_prov_fax = tk.StringVar()
        self.var_prov_correo = tk.StringVar()
        self.var_prov_pagina_web = tk.StringVar()
        self.var_prov_tipo_pago = tk.StringVar(value="mensual")
        self.var_prov_condiciones = tk.StringVar()
        
        # Primera fila
        tk.Label(frame_form, text="ID Proveedor:", **ESTILO_LABEL_NORMAL).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_id, **ESTILO_ENTRY, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Alias:", **ESTILO_LABEL_NORMAL).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_alias, **ESTILO_ENTRY, width=20).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="RFC:", **ESTILO_LABEL_NORMAL).grid(row=0, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_rfc, **ESTILO_ENTRY, width=15).grid(row=0, column=5, padx=5, pady=5)
        
        # Segunda fila
        tk.Label(frame_form, text="Razón Social:", **ESTILO_LABEL_NORMAL).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_razon_social, **ESTILO_ENTRY, width=40).grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Personal:", **ESTILO_LABEL_NORMAL).grid(row=1, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_personal, **ESTILO_ENTRY, width=20).grid(row=1, column=5, padx=5, pady=5)
        
        # Tercera fila
        tk.Label(frame_form, text="Teléfono:", **ESTILO_LABEL_NORMAL).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_telefono, **ESTILO_ENTRY, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Código Postal:", **ESTILO_LABEL_NORMAL).grid(row=2, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_codigo_postal, **ESTILO_ENTRY, width=10).grid(row=2, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Estado:", **ESTILO_LABEL_NORMAL).grid(row=2, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_estado, **ESTILO_ENTRY, width=15).grid(row=2, column=5, padx=5, pady=5)
        
        # Cuarta fila
        tk.Label(frame_form, text="Ciudad:", **ESTILO_LABEL_NORMAL).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_ciudad, **ESTILO_ENTRY, width=15).grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(frame_form, text="Municipio:", **ESTILO_LABEL_NORMAL).grid(row=3, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_municipio, **ESTILO_ENTRY, width=15).grid(row=3, column=3, padx=5, pady=5)
        
        tk.Label(frame_form, text="Colonia:", **ESTILO_LABEL_NORMAL).grid(row=3, column=4, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_colonia, **ESTILO_ENTRY, width=15).grid(row=3, column=5, padx=5, pady=5)
        
        # Quinta fila
        tk.Label(frame_form, text="Dirección:", **ESTILO_LABEL_NORMAL).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_direccion, **ESTILO_ENTRY, width=50).grid(row=4, column=1, columnspan=4, padx=5, pady=5)
        
        tk.Label(frame_form, text="Fax:", **ESTILO_LABEL_NORMAL).grid(row=4, column=5, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_fax, **ESTILO_ENTRY, width=15).grid(row=4, column=6, padx=5, pady=5)
        
        # Sexta fila
        tk.Label(frame_form, text="Correo:", **ESTILO_LABEL_NORMAL).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_correo, **ESTILO_ENTRY, width=25).grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        
        tk.Label(frame_form, text="Página Web:", **ESTILO_LABEL_NORMAL).grid(row=5, column=3, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_pagina_web, **ESTILO_ENTRY, width=25).grid(row=5, column=4, columnspan=2, padx=5, pady=5)
        
        # Séptima fila
        tk.Label(frame_form, text="Tipo Pago:", **ESTILO_LABEL_NORMAL).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.combo_tipo_pago = ttk.Combobox(frame_form, textvariable=self.var_prov_tipo_pago, **ESTILO_COMBOBOX, width=15)
        self.combo_tipo_pago.grid(row=6, column=1, padx=5, pady=5)
        self.combo_tipo_pago['values'] = ['semanal', 'quincenal', 'mensual']
        
        tk.Label(frame_form, text="Condiciones:", **ESTILO_LABEL_NORMAL).grid(row=6, column=2, padx=5, pady=5, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_prov_condiciones, **ESTILO_ENTRY, width=40).grid(row=6, column=3, columnspan=3, padx=5, pady=5)
        
        # Botones
        frame_botones = tk.Frame(frame_form, bg=COLOR_FONDO)
        frame_botones.grid(row=7, column=0, columnspan=7, pady=10)
        
        tk.Button(frame_botones, text="AGREGAR", command=self.agregar_proveedor, **ESTILO_BOTON_EXITO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="EDITAR", command=self.editar_proveedor, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="ELIMINAR", command=self.eliminar_proveedor, **ESTILO_BOTON_PELIGRO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="LIMPIAR", command=self.limpiar_formulario_proveedores, **ESTILO_BOTON_SECUNDARIO).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="IMPORTAR CSV", command=self.importar_proveedores_csv, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="EXPORTAR CSV", command=self.exportar_proveedores_csv, **ESTILO_BOTON_PRINCIPAL).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="GENERAR PLANTILLA", command=self.generar_plantilla_proveedores, **ESTILO_BOTON_SECUNDARIO).pack(side=tk.LEFT, padx=5)
        
        # Tabla de proveedores
        self.crear_tabla_proveedores(parent)
    
    def cargar_regimenes_fiscales(self):
        """Carga los regímenes fiscales en el combobox"""
        if hasattr(self, 'combo_regimen_fiscal'):
            reg_fiscales = obtener_regimenes_fiscales()
            valores = [f"{r['clave']} - {r['descripcion']}" for r in reg_fiscales]
            self.combo_regimen_fiscal['values'] = valores
    
    def cargar_usos_cfdi(self):
        """Carga los usos de CFDI en el combobox"""
        if hasattr(self, 'combo_uso_cfdi'):
            usos = obtener_usos_cfdi()
            valores = [f"{u['clave']} - {u['descripcion']}" for u in usos]
            self.combo_uso_cfdi['values'] = valores
    
    def crear_tabla_inventario(self, parent):
        """Crea la tabla de inventario"""
        frame_tabla = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ("Cód. Barras", "Código", "No. Prod", "Nombre", "Descripción", "Clasificación", 
                   "P. Minorista", "P. Mayoreo", "Costo", "Proveedor", "Unidad", "Fabricante", 
                   "Tipo", "Stock")
        self.tabla_inventario = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set, height=15
        )
        
        anchos = {
            "Cód. Barras": 100, "Código": 80, "No. Prod": 70, "Nombre": 150, 
            "Descripción": 150, "Clasificación": 100, "P. Minorista": 90, 
            "P. Mayoreo": 90, "Costo": 80, "Proveedor": 100, "Unidad": 60,
            "Fabricante": 100, "Tipo": 80, "Stock": 60
        }
        for col in columnas:
            self.tabla_inventario.heading(col, text=col)
            self.tabla_inventario.column(col, width=anchos.get(col, 100), anchor="center")
        
        self.tabla_inventario.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        scrollbar.config(command=self.tabla_inventario.yview)
        
        self.tabla_inventario.bind('<Double-Button-1>', lambda e: self.cargar_producto_seleccionado())
        self.actualizar_tabla_inventario()
    
    def crear_tabla_clientes(self, parent):
        """Crea la tabla de clientes"""
        frame_tabla = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ("RFC", "Razón Social", "Régimen Fiscal", "Uso CFDI", "Código Postal", 
                   "Dirección Fiscal", "Estado", "Ciudad", "Municipio", "Colonia", 
                   "Teléfono", "Correo")
        self.tabla_clientes = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set, height=15
        )
        
        anchos = {
            "RFC": 120, "Razón Social": 200, "Régimen Fiscal": 150, "Uso CFDI": 100,
            "Código Postal": 90, "Dirección Fiscal": 200, "Estado": 100, "Ciudad": 100,
            "Municipio": 100, "Colonia": 120, "Teléfono": 100, "Correo": 150
        }
        for col in columnas:
            self.tabla_clientes.heading(col, text=col)
            self.tabla_clientes.column(col, width=anchos.get(col, 100), anchor="center")
        
        self.tabla_clientes.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        scrollbar.config(command=self.tabla_clientes.yview)
        
        self.tabla_clientes.bind('<Double-Button-1>', lambda e: self.cargar_cliente_seleccionado())
        self.actualizar_tabla_clientes()
    
    def crear_tabla_proveedores(self, parent):
        """Crea la tabla de proveedores"""
        frame_tabla = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ("ID", "Alias", "RFC", "Razón Social", "Personal", "Teléfono", 
                   "Código Postal", "Estado", "Ciudad", "Municipio", "Colonia", 
                   "Dirección", "Fax", "Correo", "Página Web", "Tipo Pago", "Condiciones")
        self.tabla_proveedores = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings", yscrollcommand=scrollbar.set, height=15
        )
        
        anchos = {
            "ID": 80, "Alias": 100, "RFC": 120, "Razón Social": 180, "Personal": 120,
            "Teléfono": 100, "Código Postal": 90, "Estado": 100, "Ciudad": 100,
            "Municipio": 100, "Colonia": 120, "Dirección": 180, "Fax": 100,
            "Correo": 150, "Página Web": 150, "Tipo Pago": 80, "Condiciones": 150
        }
        for col in columnas:
            self.tabla_proveedores.heading(col, text=col)
            self.tabla_proveedores.column(col, width=anchos.get(col, 100), anchor="center")
        
        self.tabla_proveedores.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        scrollbar.config(command=self.tabla_proveedores.yview)
        
        self.tabla_proveedores.bind('<Double-Button-1>', lambda e: self.cargar_proveedor_seleccionado())
        self.actualizar_tabla_proveedores()
    
    def actualizar_combo_proveedores(self):
        """Actualiza el combobox de proveedores"""
        if hasattr(self, 'combo_proveedores'):
            proveedores_lista = self.gestor_proveedores.obtener_lista_simplificada()
            valores = [f"{p['id_proveedor']} - {p['alias']}" for p in proveedores_lista]
            self.combo_proveedores['values'] = valores
    
    def actualizar_tabla_inventario(self):
        """Actualiza la tabla de inventario"""
        if hasattr(self, 'tabla_inventario'):
            for item in self.tabla_inventario.get_children():
                self.tabla_inventario.delete(item)
            
            for codigo_barras, producto in self.gestor_inventario.obtener_todos().items():
                # Formatear precios
                precio_minorista = formatear_moneda(producto.get('precio_minorista', 0))
                precio_mayoreo = formatear_moneda(producto.get('precio_mayoreo', 0))
                costo = formatear_moneda(producto.get('costo', 0))
                
                self.tabla_inventario.insert("", tk.END, values=(
                    codigo_barras,
                    producto.get('codigo', ''),
                    producto.get('numero_producto', ''),
                    producto.get('nombre', ''),
                    producto.get('descripcion', ''),
                    producto.get('clasificacion', ''),
                    precio_minorista,
                    precio_mayoreo,
                    costo,
                    producto.get('proveedor', ''),
                    producto.get('unidad', 'pz'),
                    producto.get('fabricante', ''),
                    producto.get('tipo', ''),
                    producto.get('stock', 0)
                ))
    
    def actualizar_tabla_clientes(self):
        """Actualiza la tabla de clientes"""
        if hasattr(self, 'tabla_clientes'):
            for item in self.tabla_clientes.get_children():
                self.tabla_clientes.delete(item)
            
            for rfc, cliente in self.gestor_clientes.obtener_todos().items():
                self.tabla_clientes.insert("", tk.END, values=(
                    rfc,
                    cliente.get('razon_social', ''),
                    cliente.get('regimen_fiscal', ''),
                    cliente.get('uso_cfdi', ''),
                    cliente.get('codigo_postal', ''),
                    cliente.get('direccion_fiscal', ''),
                    cliente.get('estado', ''),
                    cliente.get('ciudad', ''),
                    cliente.get('municipio', ''),
                    cliente.get('colonia', ''),
                    cliente.get('telefono', ''),
                    cliente.get('correo', '')
                ))
    
    def actualizar_tabla_proveedores(self):
        """Actualiza la tabla de proveedores"""
        if hasattr(self, 'tabla_proveedores'):
            for item in self.tabla_proveedores.get_children():
                self.tabla_proveedores.delete(item)
            
            for id_prov, proveedor in self.gestor_proveedores.obtener_todos().items():
                self.tabla_proveedores.insert("", tk.END, values=(
                    id_prov,
                    proveedor.get('alias', ''),
                    proveedor.get('rfc', ''),
                    proveedor.get('razon_social', ''),
                    proveedor.get('personal', ''),
                    proveedor.get('telefono', ''),
                    proveedor.get('codigo_postal', ''),
                    proveedor.get('estado', ''),
                    proveedor.get('ciudad', ''),
                    proveedor.get('municipio', ''),
                    proveedor.get('colonia', ''),
                    proveedor.get('direccion', ''),
                    proveedor.get('fax', ''),
                    proveedor.get('correo', ''),
                    proveedor.get('pagina_web', ''),
                    proveedor.get('tipo_pago', ''),
                    proveedor.get('condiciones', '')
                ))
    
    def cargar_producto_seleccionado(self):
        """Carga el producto seleccionado en el formulario"""
        seleccion = self.tabla_inventario.selection()
        if seleccion:
            item = self.tabla_inventario.item(seleccion[0])
            valores = item['values']
            
            self.var_inv_codigo_barras.set(valores[0])
            self.var_inv_codigo.set(valores[1])
            self.var_inv_numero_producto.set(valores[2])
            self.var_inv_nombre.set(valores[3])
            self.var_inv_descripcion.set(valores[4])
            self.var_inv_clasificacion.set(valores[5])
            self.var_inv_precio_minorista.set(valores[6].replace('$', '').replace(',', ''))
            self.var_inv_precio_mayoreo.set(valores[7].replace('$', '').replace(',', ''))
            self.var_inv_costo.set(valores[8].replace('$', '').replace(',', ''))
            self.var_inv_proveedor.set(valores[9])
            self.var_inv_unidad.set(valores[10])
            self.var_inv_fabricante.set(valores[11])
            self.var_inv_tipo.set(valores[12])
            self.var_inv_stock.set(valores[13])
    
    def cargar_cliente_seleccionado(self):
        """Carga el cliente seleccionado en el formulario"""
        seleccion = self.tabla_clientes.selection()
        if seleccion:
            item = self.tabla_clientes.item(seleccion[0])
            valores = item['values']
            
            self.var_cli_rfc.set(valores[0])
            self.var_cli_razon_social.set(valores[1])
            self.var_cli_regimen_fiscal.set(valores[2])
            self.var_cli_uso_cfdi.set(valores[3])
            self.var_cli_codigo_postal.set(valores[4])
            self.var_cli_direccion_fiscal.set(valores[5])
            self.var_cli_estado.set(valores[6])
            self.var_cli_ciudad.set(valores[7])
            self.var_cli_municipio.set(valores[8])
            self.var_cli_colonia.set(valores[9])
            self.var_cli_telefono.set(valores[10])
            self.var_cli_correo.set(valores[11])
    
    def cargar_proveedor_seleccionado(self):
        """Carga el proveedor seleccionado en el formulario"""
        seleccion = self.tabla_proveedores.selection()
        if seleccion:
            item = self.tabla_proveedores.item(seleccion[0])
            valores = item['values']
            
            self.var_prov_id.set(valores[0])
            self.var_prov_alias.set(valores[1])
            self.var_prov_rfc.set(valores[2])
            self.var_prov_razon_social.set(valores[3])
            self.var_prov_personal.set(valores[4])
            self.var_prov_telefono.set(valores[5])
            self.var_prov_codigo_postal.set(valores[6])
            self.var_prov_estado.set(valores[7])
            self.var_prov_ciudad.set(valores[8])
            self.var_prov_municipio.set(valores[9])
            self.var_prov_colonia.set(valores[10])
            self.var_prov_direccion.set(valores[11])
            self.var_prov_fax.set(valores[12])
            self.var_prov_correo.set(valores[13])
            self.var_prov_pagina_web.set(valores[14])
            self.var_prov_tipo_pago.set(valores[15])
            self.var_prov_condiciones.set(valores[16])
    
    def agregar_producto_inventario(self):
        """Agrega un producto al inventario"""
        # Validaciones básicas
        campos_obligatorios = [
            self.var_inv_codigo_barras.get(),
            self.var_inv_codigo.get(),
            self.var_inv_nombre.get(),
            self.var_inv_precio_minorista.get(),
            self.var_inv_stock.get()
        ]
        
        if not all(campos_obligatorios):
            messagebox.showerror("Error", "Complete todos los campos obligatorios (*)")
            return
        
        # Validar números
        numeros = [
            ('Precio Minorista', self.var_inv_precio_minorista.get(), "float"),
            ('Precio Mayoreo', self.var_inv_precio_mayoreo.get() or "0", "float"),
            ('Costo', self.var_inv_costo.get() or "0", "float"),
            ('Stock', self.var_inv_stock.get(), "int")
        ]
        
        for nombre, valor, tipo in numeros:
            if valor and not validar_numero(valor):
                messagebox.showerror("Error", f"El campo {nombre} debe ser un número válido")
                return
        
        # Obtener ID de proveedor del combobox
        proveedor_seleccionado = self.var_inv_proveedor.get()
        id_proveedor = proveedor_seleccionado.split(' - ')[0] if proveedor_seleccionado else ""
        
        try:
            self.gestor_inventario.agregar_producto(
                codigo_barras=self.var_inv_codigo_barras.get(),
                codigo=self.var_inv_codigo.get(),
                numero_producto=self.var_inv_numero_producto.get(),
                nombre=self.var_inv_nombre.get(),
                descripcion=self.var_inv_descripcion.get(),
                clasificacion=self.var_inv_clasificacion.get(),
                precio_minorista=float(self.var_inv_precio_minorista.get()),
                precio_mayoreo=float(self.var_inv_precio_mayoreo.get() or 0),
                costo=float(self.var_inv_costo.get() or 0),
                proveedor=id_proveedor,
                unidad=self.var_inv_unidad.get(),
                fabricante=self.var_inv_fabricante.get(),
                tipo=self.var_inv_tipo.get(),
                codigoA=self.var_inv_codigoA.get(),
                codigoB=self.var_inv_codigoB.get(),
                codigoC=self.var_inv_codigoC.get(),
                stock=int(self.var_inv_stock.get())
            )
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_formulario_inventario()
            self.actualizar_tabla_inventario()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def editar_producto_inventario(self):
        """Edita un producto del inventario"""
        if not self.var_inv_codigo_barras.get():
            messagebox.showerror("Error", "Seleccione un producto para editar")
            return
        
        # Validaciones básicas
        campos_obligatorios = [
            self.var_inv_codigo.get(),
            self.var_inv_nombre.get(),
            self.var_inv_precio_minorista.get(),
            self.var_inv_stock.get()
        ]
        
        if not all(campos_obligatorios):
            messagebox.showerror("Error", "Complete todos los campos obligatorios (*)")
            return
        
        # Validar números
        numeros = [
            ('Precio Minorista', self.var_inv_precio_minorista.get(), "float"),
            ('Precio Mayoreo', self.var_inv_precio_mayoreo.get() or "0", "float"),
            ('Costo', self.var_inv_costo.get() or "0", "float"),
            ('Stock', self.var_inv_stock.get(), "int")
        ]
        
        for nombre, valor, tipo in numeros:
            if valor and not validar_numero(valor):
                messagebox.showerror("Error", f"El campo {nombre} debe ser un número válido")
                return
        
        # Obtener ID de proveedor del combobox
        proveedor_seleccionado = self.var_inv_proveedor.get()
        id_proveedor = proveedor_seleccionado.split(' - ')[0] if proveedor_seleccionado else ""
        
        try:
            self.gestor_inventario.editar_producto(
                codigo_barras=self.var_inv_codigo_barras.get(),
                codigo=self.var_inv_codigo.get(),
                numero_producto=self.var_inv_numero_producto.get(),
                nombre=self.var_inv_nombre.get(),
                descripcion=self.var_inv_descripcion.get(),
                clasificacion=self.var_inv_clasificacion.get(),
                precio_minorista=float(self.var_inv_precio_minorista.get()),
                precio_mayoreo=float(self.var_inv_precio_mayoreo.get() or 0),
                costo=float(self.var_inv_costo.get() or 0),
                proveedor=id_proveedor,
                unidad=self.var_inv_unidad.get(),
                fabricante=self.var_inv_fabricante.get(),
                tipo=self.var_inv_tipo.get(),
                codigoA=self.var_inv_codigoA.get(),
                codigoB=self.var_inv_codigoB.get(),
                codigoC=self.var_inv_codigoC.get(),
                stock=int(self.var_inv_stock.get())
            )
            messagebox.showinfo("Éxito", "Producto editado correctamente")
            self.limpiar_formulario_inventario()
            self.actualizar_tabla_inventario()
        except Exception as e:
            messagebox.showerror("Error", f"Error al editar producto: {str(e)}")
    
    def eliminar_producto_inventario(self):
        """Elimina un producto del inventario"""
        if not self.var_inv_codigo_barras.get():
            messagebox.showerror("Error", "Seleccione un producto para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                if self.gestor_inventario.eliminar_producto(self.var_inv_codigo_barras.get()):
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                    self.limpiar_formulario_inventario()
                    self.actualizar_tabla_inventario()
                else:
                    messagebox.showerror("Error", "Producto no encontrado")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
    
    def limpiar_formulario_inventario(self):
        """Limpia el formulario de inventario"""
        self.var_inv_codigo_barras.set("")
        self.var_inv_codigo.set("")
        self.var_inv_numero_producto.set("")
        self.var_inv_nombre.set("")
        self.var_inv_descripcion.set("")
        self.var_inv_clasificacion.set("")
        self.var_inv_precio_minorista.set("")
        self.var_inv_precio_mayoreo.set("")
        self.var_inv_costo.set("")
        self.var_inv_proveedor.set("")
        self.var_inv_unidad.set("pz")
        self.var_inv_fabricante.set("")
        self.var_inv_tipo.set("")
        self.var_inv_codigoA.set("")
        self.var_inv_codigoB.set("")
        self.var_inv_codigoC.set("")
        self.var_inv_stock.set("")
    
    def agregar_cliente(self):
        """Agrega un cliente"""
        # Obtener clave de régimen fiscal y uso CFDI
        regimen_seleccionado = self.var_cli_regimen_fiscal.get()
        uso_cfdi_seleccionado = self.var_cli_uso_cfdi.get()
        
        regimen_clave = regimen_seleccionado.split(' - ')[0] if ' - ' in regimen_seleccionado else regimen_seleccionado
        uso_cfdi_clave = uso_cfdi_seleccionado.split(' - ')[0] if ' - ' in uso_cfdi_seleccionado else uso_cfdi_seleccionado
        
        exito, mensaje = self.gestor_clientes.agregar_cliente(
            rfc=self.var_cli_rfc.get(),
            razon_social=self.var_cli_razon_social.get(),
            regimen_fiscal=regimen_clave,
            uso_cfdi=uso_cfdi_clave,
            codigo_postal=self.var_cli_codigo_postal.get(),
            direccion_fiscal=self.var_cli_direccion_fiscal.get(),
            estado=self.var_cli_estado.get(),
            ciudad=self.var_cli_ciudad.get(),
            municipio=self.var_cli_municipio.get(),
            colonia=self.var_cli_colonia.get(),
            telefono=self.var_cli_telefono.get(),
            correo=self.var_cli_correo.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_clientes()
            self.actualizar_tabla_clientes()
        else:
            messagebox.showerror("Error", mensaje)
    
    def editar_cliente(self):
        """Edita un cliente existente"""
        if not self.var_cli_rfc.get():
            messagebox.showerror("Error", "Seleccione un cliente para editar")
            return
        
        # Obtener clave de régimen fiscal y uso CFDI
        regimen_seleccionado = self.var_cli_regimen_fiscal.get()
        uso_cfdi_seleccionado = self.var_cli_uso_cfdi.get()
        
        regimen_clave = regimen_seleccionado.split(' - ')[0] if ' - ' in regimen_seleccionado else regimen_seleccionado
        uso_cfdi_clave = uso_cfdi_seleccionado.split(' - ')[0] if ' - ' in uso_cfdi_seleccionado else uso_cfdi_seleccionado
        
        exito, mensaje = self.gestor_clientes.editar_cliente(
            rfc=self.var_cli_rfc.get(),
            razon_social=self.var_cli_razon_social.get(),
            regimen_fiscal=regimen_clave,
            uso_cfdi=uso_cfdi_clave,
            codigo_postal=self.var_cli_codigo_postal.get(),
            direccion_fiscal=self.var_cli_direccion_fiscal.get(),
            estado=self.var_cli_estado.get(),
            ciudad=self.var_cli_ciudad.get(),
            municipio=self.var_cli_municipio.get(),
            colonia=self.var_cli_colonia.get(),
            telefono=self.var_cli_telefono.get(),
            correo=self.var_cli_correo.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_clientes()
            self.actualizar_tabla_clientes()
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_cliente(self):
        """Elimina un cliente"""
        if not self.var_cli_rfc.get():
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            exito, mensaje = self.gestor_clientes.eliminar_cliente(self.var_cli_rfc.get())
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario_clientes()
                self.actualizar_tabla_clientes()
            else:
                messagebox.showerror("Error", mensaje)
    
    def limpiar_formulario_clientes(self):
        """Limpia el formulario de clientes"""
        self.var_cli_rfc.set("")
        self.var_cli_razon_social.set("")
        self.var_cli_regimen_fiscal.set("")
        self.var_cli_uso_cfdi.set("")
        self.var_cli_codigo_postal.set("")
        self.var_cli_direccion_fiscal.set("")
        self.var_cli_estado.set("")
        self.var_cli_ciudad.set("")
        self.var_cli_municipio.set("")
        self.var_cli_colonia.set("")
        self.var_cli_telefono.set("")
        self.var_cli_correo.set("")
    
    def agregar_proveedor(self):
        """Agrega un proveedor"""
        exito, mensaje = self.gestor_proveedores.agregar_proveedor(
            id_proveedor=self.var_prov_id.get(),
            alias=self.var_prov_alias.get(),
            rfc=self.var_prov_rfc.get(),
            razon_social=self.var_prov_razon_social.get(),
            personal=self.var_prov_personal.get(),
            telefono=self.var_prov_telefono.get(),
            codigo_postal=self.var_prov_codigo_postal.get(),
            estado=self.var_prov_estado.get(),
            ciudad=self.var_prov_ciudad.get(),
            municipio=self.var_prov_municipio.get(),
            colonia=self.var_prov_colonia.get(),
            direccion=self.var_prov_direccion.get(),
            fax=self.var_prov_fax.get(),
            correo=self.var_prov_correo.get(),
            pagina_web=self.var_prov_pagina_web.get(),
            tipo_pago=self.var_prov_tipo_pago.get(),
            condiciones=self.var_prov_condiciones.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_proveedores()
            self.actualizar_tabla_proveedores()
            self.actualizar_combo_proveedores()
        else:
            messagebox.showerror("Error", mensaje)
    
    def editar_proveedor(self):
        """Edita un proveedor existente"""
        if not self.var_prov_id.get():
            messagebox.showerror("Error", "Seleccione un proveedor para editar")
            return
        
        exito, mensaje = self.gestor_proveedores.editar_proveedor(
            id_proveedor=self.var_prov_id.get(),
            alias=self.var_prov_alias.get(),
            rfc=self.var_prov_rfc.get(),
            razon_social=self.var_prov_razon_social.get(),
            personal=self.var_prov_personal.get(),
            telefono=self.var_prov_telefono.get(),
            codigo_postal=self.var_prov_codigo_postal.get(),
            estado=self.var_prov_estado.get(),
            ciudad=self.var_prov_ciudad.get(),
            municipio=self.var_prov_municipio.get(),
            colonia=self.var_prov_colonia.get(),
            direccion=self.var_prov_direccion.get(),
            fax=self.var_prov_fax.get(),
            correo=self.var_prov_correo.get(),
            pagina_web=self.var_prov_pagina_web.get(),
            tipo_pago=self.var_prov_tipo_pago.get(),
            condiciones=self.var_prov_condiciones.get()
        )
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.limpiar_formulario_proveedores()
            self.actualizar_tabla_proveedores()
            self.actualizar_combo_proveedores()
        else:
            messagebox.showerror("Error", mensaje)
    
    def eliminar_proveedor(self):
        """Elimina un proveedor"""
        if not self.var_prov_id.get():
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este proveedor?"):
            exito, mensaje = self.gestor_proveedores.eliminar_proveedor(self.var_prov_id.get())
            
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario_proveedores()
                self.actualizar_tabla_proveedores()
                self.actualizar_combo_proveedores()
            else:
                messagebox.showerror("Error", mensaje)
    
    def limpiar_formulario_proveedores(self):
        """Limpia el formulario de proveedores"""
        self.var_prov_id.set("")
        self.var_prov_alias.set("")
        self.var_prov_rfc.set("")
        self.var_prov_razon_social.set("")
        self.var_prov_personal.set("")
        self.var_prov_telefono.set("")
        self.var_prov_codigo_postal.set("")
        self.var_prov_estado.set("")
        self.var_prov_ciudad.set("")
        self.var_prov_municipio.set("")
        self.var_prov_colonia.set("")
        self.var_prov_direccion.set("")
        self.var_prov_fax.set("")
        self.var_prov_correo.set("")
        self.var_prov_pagina_web.set("")
        self.var_prov_tipo_pago.set("mensual")
        self.var_prov_condiciones.set("")
    
    def importar_inventario(self):
        """Importa inventario desde archivo"""
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            respuesta = messagebox.askyesno("Importar", "¿Desea sobrescribir el inventario existente?")
            exito, mensaje = self.gestor_inventario.importar_inventario(ruta, respuesta)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_tabla_inventario()
            else:
                messagebox.showerror("Error", mensaje)
    
    def exportar_inventario(self):
        """Exporta inventario a archivo"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            if self.gestor_inventario.exportar_inventario(ruta):
                messagebox.showinfo("Éxito", "Inventario exportado correctamente")
            else:
                messagebox.showerror("Error", "Error al exportar inventario")
    
    def generar_plantilla_inventario(self):
        """Genera plantilla CSV para inventario"""
        exito, mensaje = self.gestor_inventario.generar_plantilla_csv() if hasattr(self.gestor_inventario, 'generar_plantilla_csv') else (False, "Función no disponible")
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
    
    def importar_clientes_csv(self):
        """Importa clientes desde CSV"""
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            respuesta = messagebox.askyesno("Importar", "¿Desea sobrescribir los clientes existentes?")
            exito, mensaje = self.gestor_clientes.importar_clientes_csv(ruta, respuesta)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_tabla_clientes()
            else:
                messagebox.showerror("Error", mensaje)
    
    def exportar_clientes_csv(self):
        """Exporta clientes a CSV"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            exito, mensaje = self.gestor_clientes.exportar_clientes_csv(ruta)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)
    
    def generar_plantilla_clientes(self):
        """Genera plantilla CSV para clientes"""
        exito, mensaje = self.gestor_clientes.generar_plantilla_csv()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
    
    def importar_proveedores_csv(self):
        """Importa proveedores desde CSV"""
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            respuesta = messagebox.askyesno("Importar", "¿Desea sobrescribir los proveedores existentes?")
            exito, mensaje = self.gestor_proveedores.importar_proveedores_csv(ruta, respuesta)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.actualizar_tabla_proveedores()
                self.actualizar_combo_proveedores()
            else:
                messagebox.showerror("Error", mensaje)
    
    def exportar_proveedores_csv(self):
        """Exporta proveedores a CSV"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            exito, mensaje = self.gestor_proveedores.exportar_proveedores_csv(ruta)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showerror("Error", mensaje)
    
    def generar_plantilla_proveedores(self):
        """Genera plantilla CSV para proveedores"""
        exito, mensaje = self.gestor_proveedores.generar_plantilla_csv()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
    
    def crear_frame_tabla(self, parent):
        """Crea el frame con la tabla de productos"""
        frame_tabla = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview (tabla)
        columnas = ("Cód. Barras", "Nombre", "Descripción", "Precio Unit.", "Cantidad", "Subtotal", "Es Mayoreo")
        self.tabla_productos = ttk.Treeview(
            frame_tabla, 
            columns=columnas, 
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        
        # Configurar columnas
        anchos = {
            "Cód. Barras": 100, 
            "Nombre": 200,
            "Descripción": 150,
            "Precio Unit.": 100, 
            "Cantidad": 80, 
            "Subtotal": 100,
            "Es Mayoreo": 80
        }
        for col in columnas:
            self.tabla_productos.heading(col, text=col)
            self.tabla_productos.column(col, width=anchos.get(col, 100), anchor="center")
        
        self.tabla_productos.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        scrollbar.config(command=self.tabla_productos.yview)
        
        # Doble clic para eliminar
        self.tabla_productos.bind('<Double-Button-1>', lambda e: self.eliminar_producto_seleccionado())
    
    def crear_frame_totales(self, parent):
        """Crea el frame de totales"""
        frame_totales = tk.Frame(parent, **ESTILO_FRAME_SECUNDARIO)
        frame_totales.pack(fill=tk.X, pady=(0, 10))
        
        # Labels de totales
        frame_left = tk.Frame(frame_totales, bg=COLOR_FONDO)
        frame_left.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(frame_left, text="SUBTOTAL:", **ESTILO_LABEL_NORMAL).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(frame_left, text="IVA (16%):", **ESTILO_LABEL_NORMAL).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(frame_left, text="TOTAL:", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_PRIMARIO).grid(
            row=2, column=0, sticky="w", pady=5
        )
        
        self.label_subtotal = tk.Label(frame_left, text="$0.00", **ESTILO_LABEL_NORMAL)
        self.label_subtotal.grid(row=0, column=1, sticky="e", padx=20, pady=5)
        
        self.label_iva = tk.Label(frame_left, text="$0.00", **ESTILO_LABEL_NORMAL)
        self.label_iva.grid(row=1, column=1, sticky="e", padx=20, pady=5)
        
        self.label_total = tk.Label(frame_left, text="$0.00", font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_EXITO)
        self.label_total.grid(row=2, column=1, sticky="e", padx=20, pady=5)
        
        # Frame de pago
        frame_right = tk.Frame(frame_totales, bg=COLOR_FONDO)
        frame_right.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Label(frame_right, text="Pago con:", **ESTILO_LABEL_NORMAL).grid(row=0, column=0, sticky="w", pady=5)
        entry_pago = tk.Entry(frame_right, textvariable=self.var_pago, **ESTILO_ENTRY, width=15)
        entry_pago.grid(row=0, column=1, padx=10, pady=5)
        entry_pago.bind('<Return>', lambda e: self.finalizar_venta())
        
        self.label_cambio = tk.Label(frame_right, text="Cambio: $0.00", **ESTILO_LABEL_NORMAL)
        self.label_cambio.grid(row=1, column=0, columnspan=2, pady=5)
    
    def crear_frame_acciones(self, parent):
        """Crea el frame de botones de acción"""
        frame_acciones = tk.Frame(parent, **ESTILO_FRAME_PRINCIPAL)
        frame_acciones.pack(fill=tk.X)
        
        # Primera fila de botones
        frame_fila1 = tk.Frame(frame_acciones, bg=COLOR_FONDO)
        frame_fila1.pack(fill=tk.X, pady=(0, 5))
        
        btn_finalizar = tk.Button(
            frame_fila1, 
            text="FINALIZAR VENTA (F1)", 
            command=self.finalizar_venta,
            **ESTILO_BOTON_EXITO,
            width=20
        )
        btn_finalizar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = tk.Button(
            frame_fila1, 
            text="CANCELAR VENTA (F2)", 
            command=self.cancelar_venta,
            **ESTILO_BOTON_PELIGRO,
            width=20
        )
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
        btn_inventario = tk.Button(
            frame_fila1, 
            text="INVENTARIO (F4)", 
            command=self.abrir_inventario,
            **ESTILO_BOTON_PRINCIPAL,
            width=20
        )
        btn_inventario.pack(side=tk.LEFT, padx=5)
        
        # Segunda fila de botones
        frame_fila2 = tk.Frame(frame_acciones, bg=COLOR_FONDO)
        frame_fila2.pack(fill=tk.X)
        
        btn_historial = tk.Button(
            frame_fila2, 
            text="HISTORIAL VENTAS (F5)", 
            command=self.abrir_historial,
            **ESTILO_BOTON_PRINCIPAL,
            width=20
        )
        btn_historial.pack(side=tk.LEFT, padx=5)
        
        btn_reportes = tk.Button(
            frame_fila2, 
            text="REPORTES (F6)", 
            command=self.abrir_reportes,
            **ESTILO_BOTON_PRINCIPAL,
            width=20
        )
        btn_reportes.pack(side=tk.LEFT, padx=5)
        
        # Atajos de teclado
        self.root.bind('<F1>', lambda e: self.finalizar_venta())
        self.root.bind('<F2>', lambda e: self.cancelar_venta())
        self.root.bind('<F3>', lambda e: self.agregar_producto())
        self.root.bind('<F4>', lambda e: self.abrir_inventario())
        self.root.bind('<F5>', lambda e: self.abrir_historial())
        self.root.bind('<F6>', lambda e: self.abrir_reportes())
    
    def agregar_producto(self):
        """Agrega un producto a la venta por descripción"""
        descripcion = self.var_descripcion.get().strip()
        cantidad_str = self.var_cantidad.get().strip()
        
        if not descripcion:
            messagebox.showwarning("Advertencia", "Ingrese una descripción del producto")
            return
        
        if not validar_numero(cantidad_str, "int"):
            messagebox.showerror("Error", "La cantidad debe ser un número entero")
            return
        
        cantidad = int(cantidad_str)
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return
        
        # Buscar producto por descripción
        resultado = self.gestor_ventas.agregar_producto_por_descripcion(descripcion, cantidad)
        
        if not resultado[0]:
            messagebox.showerror("Error", resultado[1])
            return
        
        messagebox.showinfo("Éxito", resultado[1])
        
        self.actualizar_tabla()
        self.actualizar_totales()
        
        # Limpiar campos
        self.var_descripcion.set("")
        self.var_cantidad.set("1")
        self.lista_sugerencias.delete(0, tk.END)
        self.entry_descripcion.focus()
        self.var_cantidad.set("1")
        self.var_descripcion.focus()
    
    def eliminar_producto_seleccionado(self):
        """Elimina el producto seleccionado de la tabla"""
        seleccion = self.tabla_productos.selection()
        if not seleccion:
            return
        
        item = self.tabla_productos.item(seleccion[0])
        codigo_barras = item['values'][0]
        
        respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar producto {codigo_barras}?")
        if respuesta:
            self.gestor_ventas.eliminar_producto(codigo_barras)
            self.actualizar_tabla()
            self.actualizar_totales()
    
    def actualizar_tabla(self):
        """Actualiza la tabla de productos"""
        # Limpiar tabla
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        
        # Agregar productos
        for producto in self.gestor_ventas.obtener_productos_venta():
            self.tabla_productos.insert("", tk.END, values=(
                producto.codigo_barras,
                producto.nombre,
                producto.descripcion[:30] + "..." if len(producto.descripcion) > 30 else producto.descripcion,
                formatear_moneda(producto.obtener_precio_unitario()),
                producto.cantidad,
                formatear_moneda(producto.subtotal()),
                "Sí" if producto.cantidad >= 6 else "No"
            ))
    
    def actualizar_totales(self):
        """Actualiza los totales de la venta"""
        subtotal = self.gestor_ventas.calcular_subtotal()
        iva = self.gestor_ventas.calcular_iva(subtotal)
        total = subtotal + iva
        
        self.label_subtotal.config(text=formatear_moneda(subtotal))
        self.label_iva.config(text=formatear_moneda(iva))
        self.label_total.config(text=formatear_moneda(total))
        
        # Calcular cambio si hay pago
        if self.var_pago.get() and validar_numero(self.var_pago.get()):
            pago = float(self.var_pago.get())
            cambio = self.gestor_ventas.calcular_cambio(pago, total)
            self.label_cambio.config(text=f"Cambio: {formatear_moneda(cambio)}")
        else:
            self.label_cambio.config(text="Cambio: $0.00")
    
    def finalizar_venta(self):
        """Finaliza la venta actual"""
        if not self.gestor_ventas.obtener_productos_venta():
            messagebox.showwarning("Advertencia", "No hay productos en la venta")
            return
        
        pago_str = self.var_pago.get().strip()
        if not pago_str or not validar_numero(pago_str):
            messagebox.showerror("Error", "Ingrese un monto de pago válido")
            return
        
        pago = float(pago_str)
        
        # Procesar venta
        exito, mensaje, venta = self.gestor_ventas.procesar_venta(pago)
        
        if not exito:
            messagebox.showerror("Error", mensaje)
            return
        
        # Generar y guardar ticket
        ruta_ticket = GeneradorTicket.guardar_ticket(venta)
        
        # Mostrar resumen
        mensaje_resumen = f"VENTA FINALIZADA\n\n"
        mensaje_resumen += f"Folio: {venta['folio']}\n"
        mensaje_resumen += f"Subtotal: {formatear_moneda(venta['subtotal'])}\n"
        mensaje_resumen += f"IVA: {formatear_moneda(venta['iva'])}\n"
        mensaje_resumen += f"Total: {formatear_moneda(venta['total'])}\n"
        mensaje_resumen += f"Pago: {formatear_moneda(venta['pago'])}\n"
        mensaje_resumen += f"Cambio: {formatear_moneda(venta['cambio'])}\n\n"
        mensaje_resumen += f"Ticket guardado en:\n{ruta_ticket}"
        
        messagebox.showinfo("Venta Finalizada", mensaje_resumen)
        
        # Limpiar venta
        self.gestor_ventas.limpiar_venta()
        self.actualizar_tabla()
        self.actualizar_totales()
        self.var_pago.set("")
        self.var_descripcion.focus()
    
    def cancelar_venta(self):
        """Cancela la venta actual"""
        if not self.gestor_ventas.obtener_productos_venta():
            messagebox.showinfo("Información", "No hay productos para cancelar")
            return
        
        respuesta = messagebox.askyesno("Confirmar", "¿Cancelar la venta actual?")
        if respuesta:
            self.gestor_ventas.limpiar_venta()
            self.actualizar_tabla()
            self.actualizar_totales()
            self.var_pago.set("")
            self.var_descripcion.focus()
            messagebox.showinfo("Cancelado", "Venta cancelada")
    
    def abrir_inventario(self):
        """Cambia a la pestaña de inventario"""
        self.notebook.select(1)  # Índice 1 es la pestaña de Inventario
        self.actualizar_combo_proveedores()
    
    def abrir_historial(self):
        """Abre la ventana de historial de ventas"""
        VentanaHistorialVentas(self.root, self.gestor_ventas)
    
    def abrir_reportes(self):
        """Abre la ventana de reportes"""
        VentanaReportes(self.root, self.generador_reportes)


class VentanaHistorialVentas:
    """Ventana para ver el historial de ventas"""
    
    def __init__(self, parent, gestor_ventas):
        self.gestor_ventas = gestor_ventas
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Historial de Ventas")
        self.ventana.geometry("1000x600")
        self.ventana.configure(bg=COLOR_FONDO)
        
        # Variables
        self.var_folio = tk.StringVar()
        self.var_descripcion = tk.StringVar()
        
        self.crear_interfaz()
        self.cargar_ventas()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana"""
        frame_principal = tk.Frame(self.ventana, **ESTILO_FRAME_PRINCIPAL)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        
        # Título
        tk.Label(frame_principal, text="HISTORIAL DE VENTAS", **ESTILO_LABEL_TITULO).pack(pady=(0, 20))
        
        # Frame de búsqueda
        frame_busqueda = tk.Frame(frame_principal, **ESTILO_FRAME_SECUNDARIO)
        frame_busqueda.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(frame_busqueda, text="Buscar por Folio:", **ESTILO_LABEL_NORMAL).pack(side=tk.LEFT, padx=10)
        tk.Entry(frame_busqueda, textvariable=self.var_folio, **ESTILO_ENTRY, width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_busqueda, 
            text="BUSCAR FOLIO", 
            command=self.buscar_venta_por_folio,
            **ESTILO_BOTON_PRINCIPAL
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_busqueda, text="Buscar por Descripción:", **ESTILO_LABEL_NORMAL).pack(side=tk.LEFT, padx=10)
        tk.Entry(frame_busqueda, textvariable=self.var_descripcion, **ESTILO_ENTRY, width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_busqueda, 
            text="BUSCAR DESCRIPCIÓN", 
            command=self.buscar_venta_por_descripcion,
            **ESTILO_BOTON_PRINCIPAL
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_busqueda, 
            text="MOSTRAR TODAS", 
            command=self.cargar_ventas,
            **ESTILO_BOTON_PRINCIPAL
        ).pack(side=tk.LEFT, padx=5)
        
        # Tabla
        frame_tabla = tk.Frame(frame_principal, **ESTILO_FRAME_SECUNDARIO)
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ("Folio", "Fecha", "Total", "IVA", "Subtotal", "Productos", "Descuento")
        self.tabla = ttk.Treeview(
            frame_tabla, 
            columns=columnas, 
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        anchos = {"Folio": 80, "Fecha": 150, "Total": 100, "IVA": 100, "Subtotal": 100, 
                 "Productos": 100, "Descuento": 100}
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos.get(col, 100), anchor="center")
        
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        scrollbar.config(command=self.tabla.yview)
        
        # Doble click para ver detalles
        self.tabla.bind('<Double-Button-1>', lambda e: self.ver_detalle_venta())
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_botones.pack(fill=tk.X)
        
        tk.Button(
            frame_botones, 
            text="VER DETALLE", 
            command=self.ver_detalle_venta,
            **ESTILO_BOTON_PRINCIPAL,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones, 
            text="REIMPRIMIR TICKET", 
            command=self.reimprimir_ticket,
            **ESTILO_BOTON_PRINCIPAL,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones, 
            text="EXPORTAR CSV", 
            command=self.exportar_historial,
            **ESTILO_BOTON_EXITO,
            width=20
        ).pack(side=tk.LEFT, padx=5)
    
    def cargar_ventas(self):
        """Carga todas las ventas en la tabla"""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        ventas = self.gestor_ventas.obtener_historial()
        ventas.reverse()  # Más recientes primero
        
        for venta in ventas:
            self.tabla.insert("", tk.END, values=(
                venta.get('folio', 'N/A'),
                venta['fecha'],
                formatear_moneda(venta['total']),
                formatear_moneda(venta['iva']),
                formatear_moneda(venta['subtotal']),
                len(venta['productos']),
                formatear_moneda(venta.get('descuento_total', 0))
            ))
    
    def buscar_venta_por_folio(self):
        """Busca una venta por folio"""
        folio = self.var_folio.get().strip()
        if not folio:
            messagebox.showwarning("Advertencia", "Ingrese un folio")
            return
        
        if not folio.isdigit():
            messagebox.showwarning("Advertencia", "El folio debe ser un número")
            return
        
        venta = self.gestor_ventas.buscar_venta_por_folio(int(folio))
        
        if not venta:
            messagebox.showerror("Error", f"No se encontró venta con folio: {folio}")
            return
        
        # Limpiar tabla y mostrar solo esta venta
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        self.tabla.insert("", tk.END, values=(
            venta.get('folio', 'N/A'),
            venta['fecha'],
            formatear_moneda(venta['total']),
            formatear_moneda(venta['iva']),
            formatear_moneda(venta['subtotal']),
            len(venta['productos']),
            formatear_moneda(venta.get('descuento_total', 0))
        ))
    
    def buscar_venta_por_descripcion(self):
        """Busca ventas por descripción"""
        descripcion = self.var_descripcion.get().strip()
        if not descripcion:
            messagebox.showwarning("Advertencia", "Ingrese una descripción")
            return
        
        ventas = self.gestor_ventas.buscar_ventas_por_descripcion(descripcion)
        
        if not ventas:
            messagebox.showerror("Error", f"No se encontraron ventas con: '{descripcion}'")
            return
        
        # Limpiar tabla y mostrar resultados
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        for venta in ventas:
            self.tabla.insert("", tk.END, values=(
                venta.get('folio', 'N/A'),
                venta['fecha'],
                formatear_moneda(venta['total']),
                formatear_moneda(venta['iva']),
                formatear_moneda(venta['subtotal']),
                len(venta['productos']),
                formatear_moneda(venta.get('descuento_total', 0))
            ))
    
    def ver_detalle_venta(self):
        """Muestra el detalle de la venta seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una venta")
            return
        
        item = self.tabla.item(seleccion[0])
        folio = item['values'][0]
        
        venta = self.gestor_ventas.buscar_venta_por_folio(int(folio))
        if not venta:
            messagebox.showerror("Error", "No se pudo cargar el detalle de la venta")
            return
        
        # Crear ventana de detalle
        ventana_detalle = tk.Toplevel(self.ventana)
        ventana_detalle.title(f"Detalle de Venta - Folio: {folio}")
        ventana_detalle.geometry("800x500")
        ventana_detalle.configure(bg=COLOR_FONDO)
        
        frame = tk.Frame(ventana_detalle, **ESTILO_FRAME_PRINCIPAL)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Información general
        tk.Label(frame, text=f"VENTA - Folio: {folio}", **ESTILO_LABEL_TITULO).pack(pady=(0, 10))
        tk.Label(frame, text=f"Fecha: {venta['fecha']}", **ESTILO_LABEL_NORMAL).pack()
        
        # Tabla de productos
        frame_productos = tk.Frame(frame, **ESTILO_FRAME_SECUNDARIO)
        frame_productos.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_productos)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columnas = ("Producto", "Descripción", "Cantidad", "Precio Unit.", "Subtotal", "Mayoreo")
        tabla = ttk.Treeview(frame_productos, columns=columnas, show="headings", 
                           yscrollcommand=scrollbar.set, height=10)
        
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=100, anchor="center")
        
        tabla.column("Producto", width=150)
        tabla.column("Descripción", width=200)
        
        for prod in venta['productos']:
            tabla.insert("", tk.END, values=(
                prod['nombre'],
                prod.get('descripcion', '')[:30] + "..." if len(prod.get('descripcion', '')) > 30 else prod.get('descripcion', ''),
                prod['cantidad'],
                formatear_moneda(prod.get('precio_aplicado', prod.get('precio', 0))),
                formatear_moneda(prod['subtotal']),
                "Sí" if prod.get('es_mayoreo', False) else "No"
            ))
        
        tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=tabla.yview)
        
        # Totales
        frame_totales = tk.Frame(frame, bg=COLOR_FONDO)
        frame_totales.pack(fill=tk.X, pady=10)
        
        if venta.get('descuento_total', 0) > 0:
            tk.Label(frame_totales, text=f"Descuento por mayoreo: {formatear_moneda(venta['descuento_total'])}", 
                    **ESTILO_LABEL_NORMAL).pack()
        
        tk.Label(frame_totales, text=f"Subtotal: {formatear_moneda(venta['subtotal'])}", 
                **ESTILO_LABEL_NORMAL).pack()
        tk.Label(frame_totales, text=f"IVA: {formatear_moneda(venta['iva'])}", 
                **ESTILO_LABEL_NORMAL).pack()
        tk.Label(frame_totales, text=f"TOTAL: {formatear_moneda(venta['total'])}", 
                font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_EXITO).pack()
    
    def reimprimir_ticket(self):
        """Reimprime el ticket de la venta seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una venta")
            return
        
        item = self.tabla.item(seleccion[0])
        folio = item['values'][0]
        
        venta = self.gestor_ventas.buscar_venta_por_folio(int(folio))
        if not venta:
            messagebox.showerror("Error", "No se pudo cargar la venta")
            return
        
        ruta_ticket = GeneradorTicket.guardar_ticket(venta, f"ticket_reimpreso_{folio}.txt")
        messagebox.showinfo("Éxito", f"Ticket guardado en:\n{ruta_ticket}")
    
    def exportar_historial(self):
        """Exporta el historial de ventas a CSV"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            ventas = self.gestor_ventas.obtener_historial()
            
            if not ventas:
                messagebox.showerror("Error", "No hay ventas para exportar")
                return
            
            import csv
            with open(ruta, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Folio', 'Fecha', 'Subtotal', 'IVA', 'Total', 'Pago', 'Cambio', 'Productos', 'Descuento'])
                
                for venta in ventas:
                    writer.writerow([
                        venta.get('folio', ''),
                        venta.get('fecha', ''),
                        venta.get('subtotal', 0),
                        venta.get('iva', 0),
                        venta.get('total', 0),
                        venta.get('pago', 0),
                        venta.get('cambio', 0),
                        len(venta.get('productos', [])),
                        venta.get('descuento_total', 0)
                    ])
            
            messagebox.showinfo("Éxito", f"Historial exportado a:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")


class VentanaReportes:
    """Ventana para ver reportes de ventas"""
    
    def __init__(self, parent, generador_reportes):
        self.generador_reportes = generador_reportes
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Reportes de Ventas")
        self.ventana.geometry("900x600")
        self.ventana.configure(bg=COLOR_FONDO)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de la ventana"""
        frame_principal = tk.Frame(self.ventana, **ESTILO_FRAME_PRINCIPAL)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=PADDING_GENERAL, pady=PADDING_GENERAL)
        
        # Título
        tk.Label(frame_principal, text="REPORTES", **ESTILO_LABEL_TITULO).pack(pady=(0, 20))
        
        # Frame de botones
        frame_botones = tk.Frame(frame_principal, **ESTILO_FRAME_SECUNDARIO)
        frame_botones.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(
            frame_botones, 
            text="VENTAS DE HOY", 
            command=self.reporte_dia_actual,
            **ESTILO_BOTON_EXITO,
            width=20
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(
            frame_botones, 
            text="GENERAR REPORTE CSV", 
            command=self.generar_reporte_csv,
            **ESTILO_BOTON_PRINCIPAL,
            width=25
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(
            frame_botones, 
            text="EXPORTAR DATOS COMPLETOS", 
            command=self.exportar_datos_completos,
            **ESTILO_BOTON_PRINCIPAL,
            width=25
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Text widget para mostrar reportes
        frame_texto = tk.Frame(frame_principal, **ESTILO_FRAME_SECUNDARIO)
        frame_texto.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.texto_reporte = tk.Text(
            frame_texto, 
            font=FUENTE_NORMAL,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.texto_reporte.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.texto_reporte.yview)
    
    def reporte_dia_actual(self):
        """Genera reporte de ventas del día actual"""
        reporte = self.generador_reportes.generar_reporte_diario()
        
        texto = "=" * 50 + "\n"
        texto += f"REPORTE DE VENTAS DEL DÍA\n"
        texto += f"Fecha: {reporte['fecha']}\n"
        texto += "=" * 50 + "\n\n"
        texto += f"Cantidad de ventas: {reporte['cantidad_ventas']}\n"
        texto += f"Total vendido: {formatear_moneda(reporte['total'])}\n"
        texto += "\n" + "=" * 50 + "\n\n"
        
        self.mostrar_reporte(texto)
    
    def generar_reporte_csv(self):
        """Genera reporte en formato CSV"""
        try:
            self.generador_reportes.generar_reporte_csv()
            messagebox.showinfo("Éxito", "Reporte CSV generado exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte CSV: {str(e)}")
    
    def exportar_datos_completos(self):
        """Exporta datos completos de ventas"""
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        if not ruta:
            return
        
        try:
            import csv
            from metodos import GestorVentas
            
            # Obtener todas las ventas
            ventas = self.generador_reportes.gestor_ventas.obtener_historial()
            
            if not ventas:
                messagebox.showerror("Error", "No hay datos para exportar")
                return
            
            # Crear archivo CSV
            with open(ruta, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Folio', 'Fecha', 'Producto', 'Descripción', 'Cantidad', 
                               'Precio Unitario', 'Subtotal', 'IVA', 'Total', 'Pago', 'Cambio'])
                
                for venta in ventas:
                    for producto in venta.get('productos', []):
                        writer.writerow([
                            venta.get('folio', ''),
                            venta.get('fecha', ''),
                            producto.get('nombre', ''),
                            producto.get('descripcion', ''),
                            producto.get('cantidad', 0),
                            producto.get('precio_aplicado', producto.get('precio', 0)),
                            producto.get('subtotal', 0),
                            venta.get('iva', 0),
                            venta.get('total', 0),
                            venta.get('pago', 0),
                            venta.get('cambio', 0)
                        ])
            
            messagebox.showinfo("Éxito", f"Datos exportados a:\n{ruta}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar datos: {str(e)}")
    
    def mostrar_reporte(self, texto):
        """Muestra el reporte en el text widget"""
        self.texto_reporte.delete(1.0, tk.END)
        self.texto_reporte.insert(1.0, texto)


def main():
    """Función principal"""
    root = tk.Tk()
    app = PuntoVenta(root)
    root.mainloop()


if __name__ == "__main__":
    main()