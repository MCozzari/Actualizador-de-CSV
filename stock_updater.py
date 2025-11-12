import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from pathlib import Path
import threading
import sys
import traceback
import csv

class StockUpdaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Actualizador de Stock y Precios v1.0")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Configurar icono si existe
        try:
            # El icono se puede agregar después
            pass
        except:
            pass
        
        # Variables para almacenar rutas de archivos
        self.excel_path = tk.StringVar()
        self.csv_path = tk.StringVar()
        
        self.setup_ui()
        
        # Centrar ventana
        self.center_window()
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Header con título y descripción
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 30))
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="🏪 Actualizador de Stock y Precios", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        desc_label = ttk.Label(header_frame, text="Actualiza automáticamente el stock y precios de tu tienda online", 
                              font=("Arial", 10), foreground="gray")
        desc_label.grid(row=1, column=0)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Instrucciones
        instructions_frame = ttk.LabelFrame(main_frame, text="📋 Instrucciones", padding="15")
        instructions_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        instructions = [
            "1️⃣ Selecciona el archivo Excel con tu base de datos de productos",
            "2️⃣ Selecciona el archivo CSV de tu tienda online", 
            "3️⃣ Haz clic en 'Actualizar Stock y Precios' y espera el resultado"
        ]
        
        for i, instruction in enumerate(instructions):
            ttk.Label(instructions_frame, text=instruction, font=("Arial", 9)).grid(
                row=i, column=0, sticky=tk.W, pady=2)
        
        # Sección archivo Excel
        excel_frame = ttk.LabelFrame(main_frame, text="📊 Archivo Excel (Base de datos)", padding="15")
        excel_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        excel_frame.columnconfigure(1, weight=1)
        
        ttk.Label(excel_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.excel_entry = ttk.Entry(excel_frame, textvariable=self.excel_path, 
                                    state="readonly", font=("Arial", 9))
        self.excel_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.excel_button = ttk.Button(excel_frame, text="📁 Seleccionar", 
                                      command=self.select_excel_file)
        self.excel_button.grid(row=0, column=2)
        
        # Status Excel
        self.excel_status = ttk.Label(excel_frame, text="", foreground="orange")
        self.excel_status.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Sección archivo CSV  
        csv_frame = ttk.LabelFrame(main_frame, text="🛒 Archivo CSV (Tienda online)", padding="15")
        csv_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        csv_frame.columnconfigure(1, weight=1)
        
        ttk.Label(csv_frame, text="Archivo:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.csv_entry = ttk.Entry(csv_frame, textvariable=self.csv_path, 
                                  state="readonly", font=("Arial", 9))
        self.csv_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.csv_button = ttk.Button(csv_frame, text="📁 Seleccionar", 
                                    command=self.select_csv_file)
        self.csv_button.grid(row=0, column=2)
        
        # Status CSV
        self.csv_status = ttk.Label(csv_frame, text="", foreground="orange")
        self.csv_status.grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Botón procesar
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.process_button = ttk.Button(button_frame, text="🚀 Actualizar Stock y Precios", 
                                        command=self.process_files, state="disabled",
                                        style="Accent.TButton")
        self.process_button.pack(pady=10)
        
        # Configurar estilo del botón principal
        style.configure("Accent.TButton", font=("Arial", 11, "bold"))
        
        # Barra de progreso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.progress_label = ttk.Label(progress_frame, text="", font=("Arial", 8))
        self.progress_label.grid(row=1, column=0, pady=(5, 0))
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="📋 Información del proceso", padding="10")
        results_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Frame para el texto y scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.log_text = tk.Text(text_frame, height=12, wrap=tk.WORD, font=("Consolas", 9),
                               bg="#f8f9fa", relief="flat", borderwidth=1)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 2))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar peso de las filas
        main_frame.rowconfigure(7, weight=1)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=8, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(footer_frame, text="💡 Tip: Los archivos con stock y precios actualizados se guardan automáticamente", 
                 font=("Arial", 8), foreground="gray").pack()
        
        # Mensaje inicial
        self.log("🎉 ¡Bienvenido al Actualizador de Stock y Precios!")
        self.log("👆 Selecciona tus archivos arriba y haz clic en 'Actualizar Stock y Precios'")
        self.log("")
        
    def log(self, message, color="black"):
        """Añadir mensaje al área de log con colores"""
        self.log_text.insert(tk.END, f"{message}\n")
        
        # Configurar colores para diferentes tipos de mensajes
        if "✅" in message or "éxito" in message.lower():
            color = "#28a745"
        elif "❌" in message or "error" in message.lower():
            color = "#dc3545"
        elif "⚠️" in message or "advertencia" in message.lower():
            color = "#ffc107"
        elif "🔄" in message or "procesando" in message.lower():
            color = "#007bff"
            
        # Aplicar color a la última línea
        last_line_start = self.log_text.index("end-2l linestart")
        last_line_end = self.log_text.index("end-2l lineend")
        self.log_text.tag_add("colored", last_line_start, last_line_end)
        self.log_text.tag_config("colored", foreground=color)
        
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def select_excel_file(self):
        """Seleccionar archivo Excel"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel - Base de datos",
            filetypes=[
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=os.getcwd()
        )
        if file_path:
            self.excel_path.set(file_path)
            filename = os.path.basename(file_path)
            self.excel_status.config(text=f"✅ {filename}", foreground="green")
            self.log(f"📊 Excel seleccionado: {filename}")
            self.check_ready_to_process()
            
    def select_csv_file(self):
        """Seleccionar archivo CSV"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV - Tienda online",
            filetypes=[
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=os.getcwd()
        )
        if file_path:
            self.csv_path.set(file_path)
            filename = os.path.basename(file_path)
            self.csv_status.config(text=f"✅ {filename}", foreground="green")
            self.log(f"🛒 CSV seleccionado: {filename}")
            self.check_ready_to_process()
            
    def check_ready_to_process(self):
        """Verificar si ambos archivos están seleccionados"""
        if self.excel_path.get() and self.csv_path.get():
            self.process_button.config(state="normal")
            self.log("🎯 ¡Listo para procesar! Haz clic en 'Actualizar Stock y Precios'")
        else:
            self.process_button.config(state="disabled")
            
    def update_progress(self, text):
        """Actualizar texto de progreso"""
        self.progress_label.config(text=text)
        self.root.update_idletasks()
            
    def process_files(self):
        """Procesar archivos en un hilo separado"""
        self.process_button.config(state="disabled")
        self.excel_button.config(state="disabled")
        self.csv_button.config(state="disabled")
        self.progress.start()
        self.update_progress("Iniciando procesamiento...")
        
        # Limpiar log anterior
        self.log_text.delete("1.0", tk.END)
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._process_files_thread, daemon=True)
        thread.start()
        
    def _process_files_thread(self):
        """Hilo para procesar archivos"""
        try:
            self.log("🚀 INICIANDO ACTUALIZACIÓN DE STOCK Y PRECIOS")
            self.log("=" * 50)
            
            # Leer archivo Excel
            self.update_progress("Leyendo archivo Excel...")
            self.log("🔄 Leyendo archivo Excel...")
            
            almacen = pd.read_excel(
                self.excel_path.get(), 
                sheet_name='productos_db', 
                header=2,
                dtype=str  # TODO como string
            )
            self.log(f"✅ Excel procesado: {len(almacen):,} productos encontrados")


            self.update_progress("Leyendo archivo CSV...")
            self.log("🔄 Leyendo archivo CSV...")

            # Leer archivo CSV manteniendo tipos originales
            tienda = pd.read_csv(
                self.csv_path.get(), 
                encoding='cp1252', 
                sep=';',
                dtype=str,  # TODO como string
                keep_default_na=False,  # No convertir a NaN
                quotechar='"',
                doublequote=True,
                engine='python'
            )

            self.log(f"✅ CSV procesado: {len(tienda):,} productos encontrados")
            # Limpiar y convertir columnas numéricas (formato USA)
            self.log("🔧 Limpiando formato de números (comas de miles, punto decimal)...")

            # Limpiar Stock - formato USA: 1,234.56
            if 'Stock' in tienda.columns:
                tienda['Stock'] = tienda['Stock'].astype(str).str.replace(',', '', regex=False)  # Quitar comas de miles
                tienda['Stock'] = pd.to_numeric(tienda['Stock'], errors='coerce')

            # Limpiar Precio - formato USA
            if 'Precio' in tienda.columns:
                tienda['Precio'] = tienda['Precio'].astype(str).str.replace('$', '', regex=False)  # Quitar símbolo $
                tienda['Precio'] = tienda['Precio'].str.replace(',', '', regex=False)  # Quitar comas de miles
                tienda['Precio'] = pd.to_numeric(tienda['Precio'], errors='coerce')

            self.log("✅ Formato de números corregido")
            
            # Guardar orden original de columnas
            orden_columnas_original = tienda.columns.tolist()
            self.log(f"📋 Orden de columnas guardado: {len(orden_columnas_original)} columnas")
            
            # Procesar datos
            self.update_progress("Procesando y validando datos...")
            self.log("🔄 Configurando índices y validando datos...")
            
            # Verificar columnas requeridas
            if 'COD. BARRA' not in almacen.columns:
                raise ValueError("El Excel no tiene la columna 'COD. BARRA'")
            if 'STOCK' not in almacen.columns:
                raise ValueError("El Excel no tiene la columna 'STOCK'")
            if 'PRECIO VENTA' not in almacen.columns:
                raise ValueError("El Excel no tiene la columna 'PRECIO VENTA'")
            if 'Código de barras' not in tienda.columns:
                raise ValueError("El CSV no tiene la columna 'Código de barras'")
                
            # Normalizar SKU/COD. BARRA a mayúsculas para matching
            self.log("🔧 Normalizando códigos SKU (ignorando mayúsculas)...")
            almacen['COD. BARRA'] = almacen['COD. BARRA'].astype(str).str.upper().str.strip()
            tienda['Código de barras'] = tienda['Código de barras'].astype(str).str.upper().str.strip()

            # Configurar índices
            almacen = almacen.set_index('COD. BARRA')
            
            # Verificar y remover duplicados
            duplicados = almacen.index[almacen.index.duplicated()]
            if len(duplicados) > 0:
                self.log(f"⚠️ Encontrados {len(duplicados)} códigos duplicados en Excel")
                self.log("🔧 Removiendo duplicados (manteniendo el último)...")
                almacen = almacen[~almacen.index.duplicated(keep='last')]
            
            # Actualizar stock y precios
            self.update_progress("Actualizando stock y precios...")
            self.log("🔄 Actualizando valores de stock y precios...")

            # Crear mapeos desde el almacén
            almacen_stock_map = almacen['STOCK'].to_dict()
            almacen_precio_map = almacen['PRECIO VENTA'].to_dict()

            # Crear diccionarios con códigos normalizados (mayúsculas)
            almacen_stock_upper = {str(k).upper().strip(): v for k, v in almacen_stock_map.items()}
            almacen_precio_upper = {str(k).upper().strip(): v for k, v in almacen_precio_map.items()}

            # Crear columna temporal normalizada para matching
            tienda['_codigo_temp'] = tienda['Código de barras'].str.upper().str.strip()

            # Mapear nuevos valores
            stock_nuevo = tienda['_codigo_temp'].map(almacen_stock_upper)
            precio_nuevo = tienda['_codigo_temp'].map(almacen_precio_upper)

            # Actualizar SOLO donde hay coincidencia (preservando tipo string)
            mask_stock = stock_nuevo.notna()
            mask_precio = precio_nuevo.notna()

            if mask_stock.any():
                tienda.loc[mask_stock, 'Stock'] = stock_nuevo[mask_stock].apply(
                    lambda x: str(x) if pd.notna(x) else ''
                )

            if mask_precio.any():
                tienda.loc[mask_precio, 'Precio'] = precio_nuevo[mask_precio].apply(
                    lambda x: str(x) if pd.notna(x) else ''
                )
                
            # Eliminar columna temporal
            tienda.drop('_codigo_temp', axis=1, inplace=True)

            # Contar actualizaciones
            actualizados_stock = mask_stock.sum()
            actualizados_precio = mask_precio.sum()
            self.log(f"✅ Productos con nuevo stock: {actualizados_stock}")
            self.log(f"✅ Productos con nuevo precio: {actualizados_precio}")

            # Contar cuántos se actualizaron realmente
            actualizados_stock = stock_nuevo.notna().sum()
            actualizados_precio = precio_nuevo.notna().sum()
            self.log(f"✅ Productos con nuevo stock: {actualizados_stock}")
            self.log(f"✅ Productos con nuevo precio: {actualizados_precio}")
            
            # Verificar que se actualizaron los datos
            stock_actualizados = tienda['Stock'].notna().sum()
            precio_actualizados = tienda['Precio'].notna().sum()
            self.log(f"✅ Stock actualizados: {stock_actualizados}")
            self.log(f"✅ Precios actualizados: {precio_actualizados}")
            
            # Mantener orden original de columnas
            self.log("🔧 Restaurando orden original de columnas...")
            tienda = tienda[orden_columnas_original]
            
            # Limpiar espacios en columnas de texto (excepto SKU que ya está limpio)
            self.log("🧹 Limpiando espacios en columnas de texto...")
            for col in tienda.columns:
                if tienda[col].dtype == 'object' and col != 'Código de barras':
                    tienda[col] = tienda[col].astype(str).str.strip()
            
            # Generar archivo de salida
            self.update_progress("Guardando archivo actualizado...")
            output_path = self.get_output_path()
            self.log(f"💾 Guardando archivo: {os.path.basename(output_path)}")
            
            # Convertir números de vuelta a formato USA antes de guardar
            self.log("🔧 Convirtiendo a formato con comas de miles...")


            # Reemplazar todos los NaN por string vacío antes de guardar
            self.log("🔧 Limpiando valores NaN...")
            tienda = tienda.fillna('')

            # Limpiar NaN, "NaN", "nan" y configurar valores por defecto
            self.log("🔧 Limpiando valores NaN y configurando valores por defecto...")

            # Reemplazar strings "nan", "NaN", "None" por NaN real
            tienda = tienda.replace(['nan', 'NaN', 'NAN', 'None', 'none'], pd.NA)

            # Configurar valores por defecto según columna
            valores_defecto = {
                'Nombre de propiedad 1': 'Modelo único',
                'Valor de propiedad 1': 'único',                    
            }

            # Aplicar valores por defecto
            for columna, valor_defecto in valores_defecto.items():
                if columna in tienda.columns:
                    tienda[columna] = tienda[columna].fillna(valor_defecto)

            # Cualquier otro NaN restante lo dejamos vacío
            tienda = tienda.fillna('')

            self.log("✅ Valores NaN limpiados y configurados")

            # Guardar directamente sin conversiones
            tienda.to_csv(
                output_path,
                index=False,
                sep=';',
                encoding='cp1252',
                quoting=csv.QUOTE_MINIMAL
            )
            
            # Calcular estadísticas
            total_productos = len(tienda)
            productos_con_stock = tienda['Stock'].notna().sum()
            productos_sin_stock = tienda['Stock'].isna().sum()
            productos_con_precio = tienda['Precio'].notna().sum()
            productos_sin_precio = tienda['Precio'].isna().sum()

            # Convertir temporalmente a numérico SOLO para estadísticas
            stock_numerico = pd.to_numeric(tienda['Stock'], errors='coerce')
            precio_numerico = pd.to_numeric(tienda['Precio'], errors='coerce')

            productos_stock_cero = (stock_numerico == 0).sum()
            productos_stock_positivo = (stock_numerico > 0).sum()
            productos_stock_negativo = (stock_numerico < 0).sum()

            # Calcular precios promedio
            precio_promedio = precio_numerico.mean()
            precio_minimo = precio_numerico.min()
            precio_maximo = precio_numerico.max()
            
            # Mostrar resultados
            self.log("")
            self.log("🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
            self.log("=" * 50)
            self.log("📊 ESTADÍSTICAS FINALES:")
            self.log(f"   📦 Total de productos: {total_productos:,}")
            self.log("")
            self.log("   📊 STOCK:")
            self.log(f"     ✅ Con stock actualizado: {productos_con_stock:,}")
            self.log(f"     ❌ Sin información de stock: {productos_sin_stock:,}")
            self.log(f"     🟢 Con stock positivo: {productos_stock_positivo:,}")
            self.log(f"     🔴 Con stock en cero: {productos_stock_cero:,}")
            self.log(f"     🟠 Con stock negativo: {productos_stock_negativo:,}")
            self.log("")
            self.log("   💰 PRECIOS:")
            self.log(f"     ✅ Con precio actualizado: {productos_con_precio:,}")
            self.log(f"     ❌ Sin información de precio: {productos_sin_precio:,}")
            if not pd.isna(precio_promedio):
                self.log(f"     📊 Precio promedio: ${precio_promedio:,.2f}")
                self.log(f"     📈 Precio máximo: ${precio_maximo:,.2f}")
                self.log(f"     📉 Precio mínimo: ${precio_minimo:,.2f}")
            self.log("")
            self.log(f"   📈 Porcentaje stock actualizado: {(productos_con_stock/total_productos)*100:.1f}%")
            self.log(f"   💲 Porcentaje precios actualizados: {(productos_con_precio/total_productos)*100:.1f}%")
            self.log("")
            self.log(f"📁 Archivo guardado en:")
            self.log(f"   {output_path}")
            
            # Mostrar diálogo de éxito
            self.root.after(0, lambda: self.show_success_dialog(
                productos_con_stock, productos_con_precio, total_productos, output_path
            ))
            
        except FileNotFoundError as e:
            error_msg = f"No se pudo encontrar el archivo: {str(e)}"
            self.log(f"❌ ERROR: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Error de archivo", error_msg))
            
        except ValueError as e:
            error_msg = str(e)
            self.log(f"❌ ERROR: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Error de formato", error_msg))
            
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            self.log(f"❌ ERROR: {error_msg}")
            self.log("🔍 Detalles técnicos:")
            self.log(traceback.format_exc())
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        finally:
            # Restaurar interfaz
            self.root.after(0, self.restore_interface)
            
    def restore_interface(self):
        """Restaurar interfaz después del procesamiento"""
        self.progress.stop()
        self.update_progress("")
        self.process_button.config(state="normal")
        self.excel_button.config(state="normal")
        self.csv_button.config(state="normal")
        
    def show_success_dialog(self, productos_stock, productos_precio, total_productos, output_path):
        """Mostrar diálogo de éxito"""
        porcentaje_stock = (productos_stock/total_productos)*100
        porcentaje_precio = (productos_precio/total_productos)*100
        
        message = (
            f"🎉 ¡Stock y precios actualizados exitosamente!\n\n"
            f"📊 Resultados:\n"
            f"   📦 Stock: {productos_stock:,} de {total_productos:,} productos ({porcentaje_stock:.1f}%)\n"
            f"   💰 Precios: {productos_precio:,} de {total_productos:,} productos ({porcentaje_precio:.1f}%)\n\n"
            f"📁 Archivo guardado:\n{os.path.basename(output_path)}\n\n"
            f"📂 ¿Deseas abrir la carpeta donde se guardó?"
        )
        
        result = messagebox.askyesno("¡Éxito!", message)
        if result:
            self.open_file_location(output_path)
    
    def open_file_location(self, file_path):
        """Abrir la ubicación del archivo"""
        try:
            if sys.platform.startswith('win'):
                os.startfile(os.path.dirname(file_path))
            elif sys.platform.startswith('darwin'):
                os.system(f'open "{os.path.dirname(file_path)}"')
            else:
                os.system(f'xdg-open "{os.path.dirname(file_path)}"')
        except Exception as e:
            self.log(f"⚠️ No se pudo abrir la carpeta: {e}")
            
    def get_output_path(self):
        """Generar ruta de archivo de salida"""
        csv_path = Path(self.csv_path.get())
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"{csv_path.stem}_stock_precios_actualizado_{timestamp}.csv"
        return csv_path.parent / output_name

def main():
    try:
        root = tk.Tk()
        app = StockUpdaterApp(root)
        
        # Manejar cierre de ventana
        def on_closing():
            root.quit()
            root.destroy()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        # Si hay error al iniciar, mostrar mensaje básico
        import tkinter.messagebox as mb
        mb.showerror("Error", f"Error al iniciar la aplicación:\n{str(e)}")

if __name__ == "__main__":
    main()