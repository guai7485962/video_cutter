# 影片切分工具

這個工具可以幫助您切分影片檔案（特別是.TS檔案），並可選擇是否移除音訊。

## 安裝需求

首先安裝必要的Python套件：

```bash
pip install moviepy
```

## 使用方法

### 命令列版本 (video_cutter.py)

基本用法：
```bash
python video_cutter.py input.ts -s 00:01:30 -e 00:05:00
```

完整參數：
- `input`: 輸入影片檔案路徑（必填）
- `-s, --start`: 開始時間（必填，格式: HH:MM:SS 或 MM:SS 或秒數）
- `-e, --end`: 結束時間（必填，格式: HH:MM:SS 或 MM:SS 或秒數）
- `-o, --output`: 輸出檔案名稱（選填，預設: output_[時間戳記].mp4）
- `-n, --no-audio`: 移除音訊（選填）

範例：
```bash
# 切分影片從1分30秒到5分鐘
python video_cutter.py video.ts -s 00:01:30 -e 00:05:00

# 切分影片並移除音訊
python video_cutter.py video.ts -s 30 -e 300 -n

# 指定輸出檔案名稱
python video_cutter.py video.ts -s 00:00:30 -e 00:02:00 -o my_clip.mp4
```

### GUI版本 (video_cutter_gui.py)

直接執行即可開啟圖形介面：
```bash
python video_cutter_gui.py
```

1. 點擊「瀏覽」選擇輸入的.TS檔案
2. 設定輸出檔案名稱（會自動填入建議名稱）
3. 輸入開始時間和結束時間
4. 如需移除音訊，勾選「移除音訊」
5. 點擊「開始切分」

## 注意事項

1. 支援的影片格式：.ts, .mp4, .avi, .mov, .mkv 等
2. 輸出格式預設為 MP4 (H.264編碼)
3. 如果結束時間超過影片長度，會自動調整為影片結尾
4. 處理大檔案可能需要較長時間，請耐心等待

## 常見問題

**Q: 為什麼處理.TS檔案特別慢？**
A: .TS檔案通常較大且需要重新編碼，建議使用較短的片段進行測試。

**Q: 可以批次處理多個檔案嗎？**
A: 目前版本不支援批次處理，但您可以編寫簡單的腳本來循環呼叫命令列版本。

**Q: 輸出影片品質如何調整？**
A: 可以修改程式碼中的 `write_videofile` 參數來調整品質設定。