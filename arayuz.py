import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import time

from goruntu_isleme import GoruntuIsleme
from yardimci_fonk import yardimcifonk_gorsel_yukle, yardimcifonk_gorsel_kaydet, yardimcifonk_gorsel_goster, yardimcifonk_gorsel_boyutlandir

class GoruntuIslemeArayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Görüntü İşleme Teknikleri")
        self.root.geometry("1200x800")

        self.root.configure(bg="white")
        self.original_image = None
        self.processed_image = None
        self.processing = False
        self.loading_frames = []
        self.current_frame = 0
        

        self.processor = GoruntuIsleme(self)
        
        self.arayuz_olustur()
        
    def arayuz_olustur(self):

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Uygula.TButton",
                        background="#F7D1D1",
                        foreground="black",
                        font=("Segoe UI", 10),
                        borderwidth=1)
        style.map("Uygula.TButton",
                  background=[("active", "#EF9E9E")])
        
        style.configure("Blue.TButton",
                        background="#B0E2FF",
                        foreground="black",
                        font=("Segoe UI", 10),
                        borderwidth=1)
        style.map("Blue.TButton",
                  background=[("active", "#87ceff")])
        
        style.configure("temelislemler.TButton",
                        background="#EADAED",
                        foreground="black",
                        font=("Segoe UI", 10),
                        borderwidth=1)
        style.map("temelislemler.TButton",
                  background=[("active", "#B497BD")])
        
        style.configure("histogram.TButton",
                        background="#FBF3A7",
                        foreground="black",
                        font=("Segoe UI", 10),
                        borderwidth=1)
        style.map("histogram.TButton",
                  background=[("active", "#FFE135")])
        
        style.configure("iyilestirme.TButton",
                        background="#96EAA2",
                        foreground="black",
                        font=("Segoe UI", 10),
                        borderwidth=1)
        style.map("iyilestirme.TButton",
                  background=[("active", "#69DD79")])
        
        style.configure("temizle.TButton",
                        background="#FFCA9A",
                        foreground="black",
                        font=("Segoe UI", 10),
                        borderwidth=1)
        style.map("temizle.TButton",
                  background=[("active", "#FFA04B")])

        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        
        image_frame = tk.Frame(main_frame, bg="white")
        image_frame.pack(fill=tk.BOTH, expand=True)

       
        original_frame = tk.LabelFrame(image_frame, text="Orijinal Görüntü", bg="white")
        original_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=5)
        
      
        self.original_canvas = tk.Canvas(original_frame, width=350, height=350, bg="white", highlightthickness=0)
        self.original_canvas.pack(expand=True, padx=10, pady=10)
        self.original_label = tk.Label(self.original_canvas, bg="white")
        self.original_canvas.create_window(175, 175, window=self.original_label, anchor=tk.CENTER)


        self.loading_frame = tk.Frame(image_frame, bg="white", width=100, height=350)
        self.loading_frame.pack(side=tk.LEFT, padx=5)
        self.loading_frame.pack_propagate(False)  
        

        self.loading_label = tk.Label(self.loading_frame, bg="white")
        self.loading_label.pack(expand=True)

       
        processed_frame = tk.LabelFrame(image_frame, text="İşlenmiş Görüntü", bg="white")
        processed_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=5)
        
       
        self.processed_canvas = tk.Canvas(processed_frame, width=350, height=350, bg="white", highlightthickness=0)
        self.processed_canvas.pack(expand=True, padx=10, pady=10)
        self.processed_label = tk.Label(self.processed_canvas, bg="white")
        self.processed_canvas.create_window(175, 175, window=self.processed_label, anchor=tk.CENTER)

      
        file_ops_frame = tk.Frame(main_frame, bg="white")
        file_ops_frame.pack(pady=10)

        load_btn = ttk.Button(file_ops_frame, text="Görüntüyü Yükle", command=self.gorsel_yukle, style="Blue.TButton")
        load_btn.pack(side=tk.LEFT, padx=20)

        save_btn = ttk.Button(file_ops_frame, text="İşlenen Görüntüyü Kaydet", command=self.gorsel_kaydet, style="Blue.TButton")
        save_btn.pack(side=tk.LEFT, padx=20)

        clear_btn = ttk.Button(file_ops_frame, text="Temizle", command=self.gorsel_temizle, style="temizle.TButton")
        clear_btn.pack(side=tk.LEFT, padx=20)

        
        operation_frame = tk.Frame(main_frame, bg="white")
        operation_frame.pack(fill=tk.BOTH, expand=True, pady=10)

       
        basic_ops = tk.LabelFrame(operation_frame, text="Temel Görüntü Dönüşümleri", bg="white")
        basic_ops.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        ttk.Button(basic_ops, text="Gri Tonlama", style="temelislemler.TButton", 
                   command=self.processor.gri_cevirme_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(basic_ops, text="Binary Dönüşümü (Siyah-Beyaz)", style="temelislemler.TButton", 
                   command=self.processor.binary_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(basic_ops, text="Görüntü Döndürme", style="temelislemler.TButton", 
                   command=self.processor.dondurme_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(basic_ops, text="Görüntü Kırpma", style="temelislemler.TButton", 
                   command=self.processor.kirpma_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(basic_ops, text="Zoom IN/OUT", style="temelislemler.TButton", 
                   command=self.processor.zoom_uygula).pack(fill=tk.X, padx=5, pady=2)

       
        color_ops = tk.LabelFrame(operation_frame, text="Renk ve Histogram İşlemleri", bg="white")
        color_ops.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        ttk.Button(color_ops, text="RGB'den HSV'ye", style="histogram.TButton", 
                   command=self.processor.hsv_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(color_ops, text="HSV'den RGB'ye", style="histogram.TButton", 
                   command=self.processor.rgb_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(color_ops, text="Histogram Genişletme", style="histogram.TButton", 
                   command=self.processor.histogram_genisletme_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(color_ops, text="Histogram Germe", style="histogram.TButton", 
                   command=self.processor.histogram_germe_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(color_ops, text="Histogram Gösterme", style="histogram.TButton", 
                   command=self.processor.histogram_goster_uygula).pack(fill=tk.X, padx=5, pady=2)


        
        advanced_ops = tk.LabelFrame(operation_frame, text="Görüntü İyileştirme ve Analiz İşlemleri", bg="white")
        advanced_ops.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        left_column = tk.Frame(advanced_ops, bg="white")
        right_column = tk.Frame(advanced_ops, bg="white")
        left_column.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        right_column.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        ttk.Button(left_column, text="Aritmetik İşlemler", style="iyilestirme.TButton", 
                   command=self.processor.aritmetik_islemler_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(left_column, text="Kontrast Azaltma", style="iyilestirme.TButton", 
                   command=self.processor.konstrat_azaltma_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(left_column, text="Medyan Filtreleme", style="iyilestirme.TButton", 
                   command=self.processor.konvulasyon_median_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(left_column, text="Hareket Bulanıklığı (Motion)", style="iyilestirme.TButton", 
                   command=self.processor.blurlama_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(left_column, text="Çift Eşikleme", style="iyilestirme.TButton", 
                   command=self.processor.cift_esikleme_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(right_column, text="Canny Kenar Tespiti", style="iyilestirme.TButton", 
                   command=self.processor.canny_kenar_bulma_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(right_column, text="Tuz & Biber Gürültüsü Ekleme", style="iyilestirme.TButton", 
                   command=self.processor.gurultu_ekleme_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(right_column, text="Gürültü Temizleme", style="iyilestirme.TButton", 
                   command=self.processor.gurultu_temizleme_uygula).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(right_column, text="Morfolojik İşlemler", style="iyilestirme.TButton", 
                   command=self.processor.morfolojik_islemler_uygula).pack(fill=tk.X, padx=5, pady=2)

    def gorsel_temizle(self):
       
        self.original_label.config(image="", text="")

        
        if hasattr(self, 'processed_label'):
            self.processed_label.config(image="", text="")

      
        self.original_image = None
        self.processed_image = None

    def deger_giris_penceresi(self, title, prompt, min_val, max_val, default=None, examples=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        
        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text=prompt).pack(pady=5)
        
        if examples:
            ttk.Label(frame, text=f"Örnekler: {examples}", font=("Arial", 9, "italic")).pack(pady=2)
        
        value = tk.DoubleVar(value=default if default is not None else min_val)
        
        scale = ttk.Scale(frame, from_=min_val, to=max_val, variable=value, orient="horizontal")
        scale.pack(fill=tk.X, pady=5)
        
        entry = ttk.Entry(frame, textvariable=value)
        entry.pack(pady=5)
        
        result = {"value": None}
        
        def on_ok():
            try:
                val = float(value.get())
                if min_val <= val <= max_val:
                    result["value"] = val
                    dialog.destroy()
                else:
                    messagebox.showerror("Hata", f"Değer {min_val} ile {max_val} arasında olmalıdır!")
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir sayı giriniz!")
        
        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=on_ok).pack(pady=10)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return result["value"]
    
    def deger_giris_penceresi_ozel(self, title, prompt, min_val, max_val, default=None, examples=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x220")

        frame = ttk.Frame(dialog, style="Uygula.TButton")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text=prompt).pack(pady=5)

        if examples:
            ttk.Label(frame, text=f"Örnekler: {examples}", font=("Arial", 9, "italic")).pack(pady=2)

     
        value = tk.IntVar(value=default if default is not None else min_val)

        scale = tk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            orient="horizontal",
            variable=value,
            resolution=2,  
            tickinterval=2
        )
        scale.pack(fill=tk.X, pady=5)

        result = {"value": None}

        def on_ok():
            val = value.get()

            if val % 2 == 1 and min_val <= val <= max_val:
                result["value"] = val
                dialog.destroy()
            else:
                messagebox.showerror("Hata", "Lütfen tek sayı seçiniz!")

        ttk.Button(frame, text="Uygula", style="Uygula.TButton", command=on_ok).pack(pady=10)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

        return result["value"]
        
    def gorsel_yukle(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Görüntü dosyaları", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
        )
        if file_path:
            try:
                self.original_image = yardimcifonk_gorsel_yukle(file_path)
                self.gorsel_goster(self.original_image, self.original_label)
                self.processed_image = None
                self.processed_label.configure(image='')
            except Exception as e:
                messagebox.showerror("Hata", str(e))
                
    def gorsel_kaydet(self):
        if self.processed_image is None:
            messagebox.showwarning("Uyarı", "Kaydedilecek işlenmiş görüntü yok!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG dosyaları", "*.png"), ("JPEG dosyaları", "*.jpg"), ("Tüm dosyalar", "*.*")]
        )
        if file_path:
            try:
                yardimcifonk_gorsel_kaydet(self.processed_image, file_path)
                messagebox.showinfo("Başarılı", "Görüntü başarıyla kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Görüntü kaydedilemedi: {str(e)}")
                
    def gorsel_goster(self, image, label):
        if image is None:
            return
        
       
        display_image = yardimcifonk_gorsel_boyutlandir(image)
    
     
        photo = yardimcifonk_gorsel_goster(display_image)
        label.configure(image=photo)
        label.image = photo
        
    def yukleniyor_ikonu(self):
       
        self.loading_frames = []
        for i in range(8):  
           
            img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
          
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            
            
            center = (32, 32)
            radius = 20
            
       
            start_angle = i * 45
            end_angle = start_angle + 270
            

            draw.arc([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], 
                     start_angle, end_angle, fill=(0, 120, 215), width=5)
            
           
            photo = ImageTk.PhotoImage(img)
            self.loading_frames.append(photo)
    
    def yukleniyor_ikonu_baslat(self):
        
        self.loading_label.config(image=self.loading_frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.loading_frames)
        self.animation_id = self.root.after(100, self.yukleniyor_ikonu_baslat)
    
    def yukleniyor_ikonu_durdur(self):
    
        if hasattr(self, 'animation_id'):
            self.root.after_cancel(self.animation_id)
        self.loading_label.config(image='')
        
    def islem_yap_ve_goster(self, func, *args, **kwargs):
        if self.processing:
            return
            
        if self.original_image is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return
            
        self.processing = True
       
        self.yukleniyor_ikonu()
        
        self.yukleniyor_ikonu_baslat()          
        
        def process():
            try:
                result = func(*args, **kwargs)
                self.processed_image = result
                self.root.after(0, lambda: self.gorsel_goster(result, self.processed_label))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
            finally:
               
                self.root.after(0, self.yukleniyor_ikonu_durdur)
                self.processing = False

        threading.Thread(target=process).start()
