import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from moviepy.editor import VideoFileClip
import threading

class VideoCutterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("影片切分工具")
        self.root.geometry("600x400")
        
        # 變數
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.start_time = tk.StringVar(value="00:00:00")
        self.end_time = tk.StringVar(value="00:00:10")
        self.remove_audio = tk.BooleanVar(value=False)
        
        self.create_widgets()
        
    def create_widgets(self):
        # 輸入檔案選擇
        tk.Label(self.root, text="輸入影片檔案:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="瀏覽", command=self.browse_input).grid(row=0, column=2, padx=10, pady=10)
        
        # 輸出檔案設定
        tk.Label(self.root, text="輸出影片檔案:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.output_file, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="瀏覽", command=self.browse_output).grid(row=1, column=2, padx=10, pady=10)
        
        # 時間設定
        tk.Label(self.root, text="開始時間 (HH:MM:SS):").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.start_time, width=20).grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        tk.Label(self.root, text="結束時間 (HH:MM:SS):").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.end_time, width=20).grid(row=3, column=1, sticky="w", padx=10, pady=10)
        
        # 音訊選項
        tk.Checkbutton(self.root, text="移除音訊", variable=self.remove_audio).grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        # 進度條
        self.progress = ttk.Progressbar(self.root, length=400, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, padx=10, pady=20)
        
        # 狀態標籤
        self.status_label = tk.Label(self.root, text="準備就緒", fg="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10)
        
        # 開始按鈕
        tk.Button(self.root, text="開始切分", command=self.start_cutting, bg="green", fg="white", width=20, height=2).grid(row=7, column=0, columnspan=3, pady=20)
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="選擇影片檔案",
            filetypes=[("影片檔案", "*.ts *.mp4 *.avi *.mov *.mkv"), ("所有檔案", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # 自動設定輸出檔案名稱
            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_name = f"output_{base_name}.mp4"
            self.output_file.set(output_name)
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="儲存影片檔案",
            defaultextension=".mp4",
            filetypes=[("MP4檔案", "*.mp4"), ("所有檔案", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
    
    def convert_time_to_seconds(self, time_str):
        """將時間字串轉換為秒數"""
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(float, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:
                minutes, seconds = map(float, parts)
                return minutes * 60 + seconds
        else:
            return float(time_str)
    
    def start_cutting(self):
        # 檢查輸入
        if not self.input_file.get():
            messagebox.showerror("錯誤", "請選擇輸入影片檔案")
            return
        
        if not self.output_file.get():
            messagebox.showerror("錯誤", "請設定輸出檔案名稱")
            return
        
        # 在新執行緒中執行切分操作
        thread = threading.Thread(target=self.cut_video_thread)
        thread.start()
    
    def cut_video_thread(self):
        try:
            # 開始進度條
            self.progress.start()
            self.status_label.config(text="正在處理中...", fg="orange")
            
            # 轉換時間
            start_seconds = self.convert_time_to_seconds(self.start_time.get())
            end_seconds = self.convert_time_to_seconds(self.end_time.get())
            
            if start_seconds >= end_seconds:
                self.root.after(0, lambda: messagebox.showerror("錯誤", "開始時間必須小於結束時間"))
                return
            
            # 載入影片
            video = VideoFileClip(self.input_file.get())
            
            # 檢查時間範圍
            if end_seconds > video.duration:
                end_seconds = video.duration
            
            # 切分影片
            cut_video = video.subclip(start_seconds, end_seconds)
            
            # 如果需要移除音訊
            if self.remove_audio.get():
                cut_video = cut_video.without_audio()
            
            # 儲存影片
            cut_video.write_videofile(self.output_file.get(), codec='libx264', audio_codec='aac')
            
            # 釋放資源
            video.close()
            cut_video.close()
            
            # 更新狀態
            self.root.after(0, lambda: self.status_label.config(text="✅ 切分完成！", fg="green"))
            self.root.after(0, lambda: messagebox.showinfo("成功", f"影片已儲存至:\n{self.output_file.get()}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"❌ 錯誤: {str(e)}", fg="red"))
            self.root.after(0, lambda: messagebox.showerror("錯誤", f"處理失敗:\n{str(e)}"))
        
        finally:
            # 停止進度條
            self.progress.stop()

def main():
    root = tk.Tk()
    app = VideoCutterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()