import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk

from algorithms import (
    gray_scale, binary_donusum, adding_noise, aritmetikislemler, goruntuislemecanny, goruntukirpma,
    histogram, kontrastazalt, median, morfolojik, blurlamafiltresi,
    renkuzayidonusumleri, rotate, thresholding, ZoomInOut
)
from yardimci_fonk import yardimcifonk_gorsel_yukle, yardimcifonk_gorsel_boyutlandir, yardimcifonk_gorsel_goster

class GoruntuIsleme:
    def __init__(self, app):
        self.app = app
        
    def gri_cevirme_uygula(self):
        self.app.islem_yap_ve_goster(gray_scale.gri_tonlama_donusumu_ve_goster, self.app.original_image)
        
    def binary_uygula(self):
        threshold = self.app.deger_giris_penceresi(
            "Binary Dönüşüm",
            "Eşik değerini girin (0-255):",
            0, 255, 127,
        )
        if threshold is not None:
            self.app.islem_yap_ve_goster(binary_donusum.process_array, self.app.original_image, int(threshold))
            
    def dondurme_uygula(self):
        angle_degrees = self.app.deger_giris_penceresi(
            "Görüntü Döndürme",
            "Döndürme açısını girin (derece):",
            -360, 360, 0,
        )
        if angle_degrees is not None:
            self.app.islem_yap_ve_goster(rotate.gorsel_dondurme, self.app.original_image, angle_degrees)
            
    def kirpma_uygula(self):
        height, width = self.app.original_image.shape[:2]
        
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Kırpma Penceresi")
        dialog.geometry("400x400")
        
        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text=f"Görüntü boyutu: {width}x{height}").pack(pady=5)
        
  
        ttk.Label(frame, text="X Başlangıç:").pack(pady=2)
        x_start_var = tk.IntVar(value=0)
        x_scale = ttk.Scale(frame, from_=0, to=width-1, variable=x_start_var, orient="horizontal")
        x_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=x_start_var).pack(pady=2)
        
   
        ttk.Label(frame, text="Y Başlangıç:").pack(pady=2)
        y_start_var = tk.IntVar(value=0)
        y_scale = ttk.Scale(frame, from_=0, to=height-1, variable=y_start_var, orient="horizontal")
        y_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=y_start_var).pack(pady=2)
        
   
        ttk.Label(frame, text="Genişlik:").pack(pady=2)
        width_var = tk.IntVar(value=width//2)
        w_scale = ttk.Scale(frame, from_=1, to=width, variable=width_var, orient="horizontal")
        w_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=width_var).pack(pady=2)
        
       
        ttk.Label(frame, text="Yükseklik:").pack(pady=2)
        height_var = tk.IntVar(value=height//2)
        h_scale = ttk.Scale(frame, from_=1, to=height, variable=height_var, orient="horizontal")
        h_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=height_var).pack(pady=2)
        
     
        
        def apply():
            x_start = x_start_var.get()
            y_start = y_start_var.get()
            crop_width = width_var.get()
            crop_height = height_var.get()
            
            self.app.islem_yap_ve_goster(goruntukirpma.crop_image, 
                self.app.original_image, x_start, y_start, crop_width, crop_height)
            dialog.destroy()
            
        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)
            
    def zoom_uygula(self):
        # Create zoom window directly
        zoom_window = tk.Toplevel(self.app.root)
        zoom_window.title("Yakınlaştırma / Uzaklaştırma")
        zoom_window.geometry("800x600")
        
        # Main container
        main_frame = ttk.Frame(zoom_window,  style="Uygula.TButton")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for zoom controls
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Zoom level label
        ttk.Label(controls_frame, text="Zoom seviyesi girin:").pack(anchor=tk.CENTER, pady=5)
        
        # Zoom range label
        zoom_range_label = ttk.Label(controls_frame, 
                                   text="-5 (10× uzaklaştırma)    0 (%100)    +5 (10× yakınlaştırma)")
        zoom_range_label.pack(anchor=tk.CENTER)
        
        # Zoom slider frame
        slider_frame = tk.Frame(main_frame)
        slider_frame.pack(fill=tk.X, pady=5)
        
        # Zoom factor variable and slider
        zoom_factor = tk.DoubleVar(value=0.0)
        zoom_scale = ttk.Scale(slider_frame, from_=-5.0, to=5.0, variable=zoom_factor, 
                             orient="horizontal", length=600)
        zoom_scale.pack(fill=tk.X, padx=20)
        
        # Zoom value display
        zoom_value_var = tk.StringVar(value="0.0")
        zoom_value_entry = ttk.Entry(main_frame, textvariable=zoom_value_var, width=15, justify=tk.CENTER)
        zoom_value_entry.pack(pady=5)
        
        # Interpolation method frame
        interp_frame = tk.Frame(main_frame)
        interp_frame.pack(pady=10)
        
        # Interpolation method label
        ttk.Label(interp_frame, text="İnterpolasyon Yöntemi:").pack(anchor=tk.CENTER, pady=5)
        
        # Interpolation method selection
        method = tk.StringVar(value="nearest")
        ttk.Radiobutton(interp_frame, text="En Yakın Komşu", variable=method, value="nearest").pack(anchor=tk.W)
        ttk.Radiobutton(interp_frame, text="Bilineer", variable=method, value="bilinear").pack(anchor=tk.W)
        
        # Images frame
        images_frame = tk.Frame(main_frame)
        images_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original image frame
        original_frame = tk.LabelFrame(images_frame, text="Orijinal")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Zoomed image frame
        zoomed_frame = tk.LabelFrame(images_frame, text="Zoom'lu")
        zoomed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Create scrollable canvases for both images
        original_canvas = tk.Canvas(original_frame, bg="white")
        original_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        zoomed_canvas = tk.Canvas(zoomed_frame, bg="white")
        zoomed_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbars to canvases
        original_scrollbar_y = ttk.Scrollbar(original_frame, orient="vertical", command=original_canvas.yview)
        original_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        original_scrollbar_x = ttk.Scrollbar(original_frame, orient="horizontal", command=original_canvas.xview)
        original_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        zoomed_scrollbar_y = ttk.Scrollbar(zoomed_frame, orient="vertical", command=zoomed_canvas.yview)
        zoomed_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        zoomed_scrollbar_x = ttk.Scrollbar(zoomed_frame, orient="horizontal", command=zoomed_canvas.xview)
        zoomed_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure canvases to use scrollbars
        original_canvas.configure(yscrollcommand=original_scrollbar_y.set, xscrollcommand=original_scrollbar_x.set)
        zoomed_canvas.configure(yscrollcommand=zoomed_scrollbar_y.set, xscrollcommand=zoomed_scrollbar_x.set)
        
        # Create frames inside canvases to hold images
        original_inner_frame = tk.Frame(original_canvas)
        original_canvas_window = original_canvas.create_window(0, 0, window=original_inner_frame, anchor=tk.NW)
        
        zoomed_inner_frame = tk.Frame(zoomed_canvas)
        zoomed_canvas_window = zoomed_canvas.create_window(0, 0, window=zoomed_inner_frame, anchor=tk.NW)
        
        # Create image labels inside the frames
        original_label = tk.Label(original_inner_frame)
        original_label.pack()
        
        zoomed_label = tk.Label(zoomed_inner_frame)
        zoomed_label.pack()
        
        # Function to convert zoom slider value to actual scale factor
        def get_scale_factor(zoom_value):
            if zoom_value >= 0:
                # Positive zoom: 1.0 to 10.0 (zoom in)
                return 1.0 + (zoom_value * 1.8)  # 0 -> 1.0, 5 -> 10.0
            else:
                # Negative zoom: 1.0 to 0.1 (zoom out)
                return 1.0 / (1.0 + (abs(zoom_value) * 0.18))  # -5 -> 0.1, 0 -> 1.0
        
        # Function to synchronize scrolling between the two canvases
        def sync_scrolls(*args):
            # Get the current view of the original canvas
            original_view = (original_canvas.xview(), original_canvas.yview())
            
            # Apply the same view to the zoomed canvas
            zoomed_canvas.xview_moveto(original_view[0][0])
            zoomed_canvas.yview_moveto(original_view[1][0])
        
        # Function to update images based on zoom level
        def update_zoom(*args):
            # Get zoom value and update entry
            zoom_value = zoom_factor.get()
            zoom_value_var.set(f"{zoom_value:.1f}")
            
            # Calculate actual scale factor
            scale_factor = get_scale_factor(zoom_value)
            
            # Display original image (not zoomed)
            display_original = self.app.original_image.copy()
            pil_original = Image.fromarray(display_original[..., ::-1])
            photo_original = ImageTk.PhotoImage(pil_original)
            original_label.configure(image=photo_original)
            original_label.image = photo_original
            
            # Create zoomed image
            zoomed_image = ZoomInOut.process_array(self.app.original_image, scale_factor, method.get())
            pil_zoomed = Image.fromarray(zoomed_image[..., ::-1])
            photo_zoomed = ImageTk.PhotoImage(pil_zoomed)
            zoomed_label.configure(image=photo_zoomed)
            zoomed_label.image = photo_zoomed
            
            # Update canvas scroll regions
            original_canvas.configure(scrollregion=original_canvas.bbox("all"))
            zoomed_canvas.configure(scrollregion=zoomed_canvas.bbox("all"))
            
            # Reset view to center
            original_canvas.xview_moveto(0.5)
            original_canvas.yview_moveto(0.5)
            zoomed_canvas.xview_moveto(0.5)
            zoomed_canvas.yview_moveto(0.5)
        
        # Function to handle manual entry of zoom value
        def on_entry_change(*args):
            try:
                value = float(zoom_value_var.get())
                if -5.0 <= value <= 5.0:
                    zoom_factor.set(value)
                    update_zoom()
            except ValueError:
                pass  # Ignore invalid input
        
        # Bind events
        zoom_scale.configure(command=update_zoom)
        zoom_value_var.trace_add("write", on_entry_change)
        method.trace_add("write", update_zoom)
        
        # Bind scroll events to synchronize both canvases
        original_canvas.bind("<Configure>", lambda e: original_canvas.configure(scrollregion=original_canvas.bbox("all")))
        zoomed_canvas.bind("<Configure>", lambda e: zoomed_canvas.configure(scrollregion=zoomed_canvas.bbox("all")))
        
        original_scrollbar_y.bind("<B1-Motion>", sync_scrolls)
        original_scrollbar_x.bind("<B1-Motion>", sync_scrolls)
        
        # Apply button
        def apply_zoom():
            scale_factor = get_scale_factor(zoom_factor.get())
            zoomed_image = ZoomInOut.process_array(self.app.original_image, scale_factor, method.get())
            self.app.processed_image = zoomed_image
            self.app.gorsel_goster(zoomed_image, self.app.processed_label)
            zoom_window.destroy()
        
        ttk.Button(main_frame, text="Uygula ve Kapat", style="Uygula.TButton", 
                  command=apply_zoom).pack(pady=10)
        
        # Initialize the display
        update_zoom()
            
    def hsv_uygula(self):
        self.app.islem_yap_ve_goster(renkuzayidonusumleri.rgbden_hsvye_cevir, self.app.original_image)
        
    def rgb_uygula(self):
        self.app.islem_yap_ve_goster(renkuzayidonusumleri.hsvde_rgbye_cevir, self.app.original_image)
        
    def histogram_goster_uygula(self):
        if self.app.original_image is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return
            
        if self.app.processed_image is None:
            messagebox.showerror("Hata", "Önce görüntü üzerinde bir işlem uygulamalısınız!")
            return
        
   
        hist_window = tk.Toplevel(self.app.root)
        hist_window.title("Histogram İşlemleri")
        hist_window.geometry("800x600")
        
  
        fig = histogram.grafik_histogram(self.app.original_image, self.app.processed_image)
        
     
        canvas = FigureCanvasTkAgg(fig, master=hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
  
        toolbar = NavigationToolbar2Tk(canvas, hist_window)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def histogram_genisletme_uygula(self):
        if self.app.original_image is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return
            
        if len(self.app.original_image.shape) == 2:  # Gri görüntü
            self.app.islem_yap_ve_goster(histogram.histogram_genisletme_gray, self.app.original_image)
        elif len(self.app.original_image.shape) == 3:  # Renkli görüntü
            self.app.islem_yap_ve_goster(histogram.histogram_genisletme_color, self.app.original_image)
        else:
            messagebox.showerror("Hata", "Görüntü formatı tanınamadı!")

    def histogram_germe_uygula(self):
        if self.app.original_image is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return
            
        if len(self.app.original_image.shape) == 2:  # Gri görüntü
            self.app.islem_yap_ve_goster(histogram.histogram_germe_gray, self.app.original_image)
        elif len(self.app.original_image.shape) == 3:  # Renkli görüntü
            self.app.islem_yap_ve_goster(histogram.histogram_germe_color, self.app.original_image)
        else:
            messagebox.showerror("Hata", "Görüntü formatı tanınamadı!")
        
    def aritmetik_islemler_uygula(self):
        if self.app.original_image is None:
            messagebox.showwarning("Uyarı", "Lütfen ilk görüntüyü yükleyin!")
            return
            
        file_path = filedialog.askopenfilename(
            title="İkinci görüntüyü seçin",
            filetypes=[("Görüntü dosyaları", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            second_image = yardimcifonk_gorsel_yukle(file_path)
           
            if second_image.shape != self.app.original_image.shape:
                second_image = aritmetikislemler.resize_manual(
                    second_image, self.app.original_image.shape[:2]
                )
                
            dialog = tk.Toplevel(self.app.root)
            dialog.title("Aritmetik İşlemler")
            dialog.geometry("300x200")
            dialog.configure(bg="#F7D1D1")
            
            operation = tk.StringVar(value="add")
            
            ttk.Radiobutton(dialog, text="Görüntüleri Çıkar", variable=operation, 
                          value="subtract").pack(pady=5)
            ttk.Radiobutton(dialog, text="Görüntüleri Çarp", variable=operation, 
                          value="multiply").pack(pady=5)
        
            
            def apply():
                if operation.get() == "subtract":
                    self.app.islem_yap_ve_goster(aritmetikislemler.cıkarma_manual, 
                        self.app.original_image, second_image)
                elif operation.get() == "multiply":
                    self.app.islem_yap_ve_goster(aritmetikislemler.carpma_manual, 
                        self.app.original_image, second_image)
                dialog.destroy()
                
            ttk.Button(dialog, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)
                
    def konstrat_azaltma_uygula(self):
        factor = self.app.deger_giris_penceresi(
            "Kontrast Azaltma",
            "Kontrast faktörünü girin (0-1):",
            0, 1, 0.5,
        )
        if factor is not None:
            self.app.islem_yap_ve_goster(kontrastazalt.process_array, self.app.original_image, factor)
            
    def konvulasyon_median_uygula(self):
        kernel_size = self.app.deger_giris_penceresi_ozel(
            "Medyan Filtresi",
            "Çekirdek boyutunu girin (tek sayı):",
            3, 29, 3,
        )
        if kernel_size is not None and int(kernel_size) % 2 == 1:
            self.app.islem_yap_ve_goster(median.median_filter_pipeline, self.app.original_image, int(kernel_size))
            
    def blurlama_uygula(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Hareket Bulanıklığı")
        dialog.geometry("300x250")
        dialog.configure(bg="#F7D1D1")
        
        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    
        ttk.Label(frame, text="Çekirdek Boyutu:").pack(pady=2)
        kernel_size = tk.IntVar(value=9)
        ttk.Entry(frame, textvariable=kernel_size).pack(pady=2)
        
     
        ttk.Label(frame, text="Bulanıklık Açısı (derece):").pack(pady=2)
        angle = tk.DoubleVar(value=0)
        a_scale = ttk.Scale(frame, from_=0, to=360, variable=angle, orient="horizontal")
        a_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=angle).pack(pady=2)
        
        
        def apply():
            self.app.islem_yap_ve_goster(blurlamafiltresi.blurlastirma, 
                self.app.original_image, kernel_size.get(), angle.get())
            dialog.destroy()
            
        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)

    def cift_esikleme_uygula(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Çift Eşikleme")
        dialog.geometry("300x250")
        dialog.configure(bg="#F7D1D1")
    
        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    
        ttk.Label(frame, text="Alt Eşik:").pack(pady=2)
        low = tk.IntVar(value=50)
        l_scale = ttk.Scale(frame, from_=0, to=255, variable=low, orient="horizontal")
        l_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=low).pack(pady=2)
    
    
        ttk.Label(frame, text="Üst Eşik:").pack(pady=2)
        high = tk.IntVar(value=150)
        h_scale = ttk.Scale(frame, from_=0, to=255, variable=high, orient="horizontal")
        h_scale.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=high).pack(pady=2)

    
        def apply():
            if low.get() >= high.get():
                messagebox.showerror("Hata", "Üst eşik alt eşikten büyük olmalıdır!")
                return
            self.app.islem_yap_ve_goster(thresholding.cift_esikleme, 
                self.app.original_image, low.get(), high.get())
            dialog.destroy()
        
        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)
            
    def canny_kenar_bulma_uygula(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Canny Kenar Algılama")
        dialog.geometry("300x200")
        dialog.configure(bg="#F7D1D1")

        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

 
        ttk.Label(frame, text="Alt Eşik (Low Threshold):").pack(pady=2)
        low_thresh = tk.IntVar(value=50)
        l_entry = ttk.Entry(frame, textvariable=low_thresh)
        l_entry.pack(pady=2)

    
        ttk.Label(frame, text="Üst Eşik (High Threshold):").pack(pady=2)
        high_thresh = tk.IntVar(value=100)
        h_entry = ttk.Entry(frame, textvariable=high_thresh)
        h_entry.pack(pady=2)


        def apply():
            self.app.islem_yap_ve_goster(goruntuislemecanny.canny_edge_detector,
                self.app.original_image, low_thresh.get(), high_thresh.get())
            dialog.destroy()

        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)
        
    def gurultu_ekleme_uygula(self):
        prob = self.app.deger_giris_penceresi(
            "Tuz & Biber Gürültüsü",
            "Gürültü olasılığını girin (0-1):",
            0, 1, 0.05,
        )
        if prob is not None:
            self.app.islem_yap_ve_goster(adding_noise.add_salt_and_pepper_noise, self.app.original_image, prob)
            
    def gurultu_temizleme_uygula(self):
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Gürültü Temizleme")
        dialog.geometry("300x250")
        dialog.configure(bg="#F7D1D1")
        
        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        filter_type = tk.StringVar(value="median")
        
        ttk.Radiobutton(frame, text="Medyan Filtresi", variable=filter_type, 
                      value="median").pack(pady=5)
        ttk.Radiobutton(frame, text="Ortalama Filtresi", variable=filter_type, 
                      value="mean").pack(pady=5)
        
        ttk.Label(frame, text="Çekirdek Boyutu:(Tek Sayı)").pack(pady=2)
        kernel_size = tk.IntVar(value=3)
        ttk.Entry(frame, textvariable=kernel_size).pack(pady=2)
        
        
        def apply():
            if kernel_size.get() % 2 == 1:
                if filter_type.get() == "median":
                    self.app.islem_yap_ve_goster(adding_noise.median_filter, 
                        self.app.original_image, kernel_size.get())
                else:  # mean
                    self.app.islem_yap_ve_goster(adding_noise.mean_filter, 
                        self.app.original_image, kernel_size.get())
                dialog.destroy()
            else:
                messagebox.showerror("Hata", "Çekirdek boyutu tek sayı olmalıdır!")
                
        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)
                
    def morfolojik_islemler_uygula(self):
        if self.app.original_image is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return
        
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Morfolojik İşlemler")
        dialog.geometry("300x350")
        dialog.configure(bg="#F7D1D1")

        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        operation = tk.StringVar(value="dilate")
    
        ttk.Radiobutton(frame, text="Genişletme", variable=operation, 
                      value="dilate").pack(pady=5)
        ttk.Radiobutton(frame, text="Aşındırma", variable=operation, 
                      value="erozyon").pack(pady=5)
        ttk.Radiobutton(frame, text="Açma", variable=operation, 
                      value="acma").pack(pady=5)
        ttk.Radiobutton(frame, text="Kapama", variable=operation, 
                      value="kapama").pack(pady=5)
    
        ttk.Label(frame, text="Çekirdek Boyutu:").pack(pady=2)
        kernel_size = tk.IntVar(value=3)
        ttk.Entry(frame, textvariable=kernel_size).pack(pady=2)
    
        ttk.Label(frame, text="İterasyon Sayısı:").pack(pady=2)
        iteration_count = tk.IntVar(value=1)
        scale_iter = ttk.Scale(frame, from_=1, to=5, variable=iteration_count, orient="horizontal")
        scale_iter.pack(fill=tk.X, pady=2)
        ttk.Entry(frame, textvariable=iteration_count).pack(pady=2)
    
    
        def apply():
            if kernel_size.get() % 2 == 1:
                try:
                   
                    op_type = operation.get()
                    k_size = kernel_size.get()
                    iters = iteration_count.get()
                
                   
                    if op_type == "dilate":
                        if iters == 1:
                            self.app.islem_yap_ve_goster(morfolojik.dilate, self.app.original_image, k_size)
                        else:
                            self.app.islem_yap_ve_goster(
                                lambda img, k_size, iters: morfolojik.iterasyon_sayisi(img, morfolojik.dilate, k_size, iters),
                                self.app.original_image, k_size, iters
                            )
                    elif op_type == "erozyon":
                        if iters == 1:
                            self.app.islem_yap_ve_goster(morfolojik.erozyon, self.app.original_image, k_size)
                        else:
                            self.app.islem_yap_ve_goster(
                                lambda img, k_size, iters: morfolojik.iterasyon_sayisi(img, morfolojik.erozyon, k_size, iters),
                                self.app.original_image, k_size, iters
                            )
                    elif op_type == "acma":
                        if iters == 1:
                            self.app.islem_yap_ve_goster(morfolojik.acma, self.app.original_image, k_size)
                        else:
                            self.app.islem_yap_ve_goster(
                                lambda img, k_size, iters: morfolojik.iterasyon_sayisi(img, morfolojik.acma, k_size, iters),
                                self.app.original_image, k_size, iters
                            )
                    elif op_type == "kapama":
                        if iters == 1:
                            self.app.islem_yap_ve_goster(morfolojik.kapama, self.app.original_image, k_size)
                        else:
                            self.app.islem_yap_ve_goster(
                                lambda img, k_size, iters: morfolojik.iterasyon_sayisi(img, morfolojik.kapama, k_size, iters),
                                self.app.original_image, k_size, iters
                            )
                    
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Hata", f"İşlem sırasında hata oluştu: {str(e)}")
            else:
                messagebox.showerror("Hata", "Çekirdek boyutu tek sayı olmalıdır!")
            
        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=apply).pack(pady=10)