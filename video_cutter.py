import os
from moviepy.editor import VideoFileClip
import argparse
from datetime import datetime

def convert_time_to_seconds(time_str):
    """
    將時間字串轉換為秒數
    支援格式: "HH:MM:SS" 或 "MM:SS" 或純秒數
    """
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

def cut_video(input_file, output_file, start_time, end_time, remove_audio=False):
    """
    切分影片
    
    參數:
    - input_file: 輸入影片檔案路徑
    - output_file: 輸出影片檔案路徑
    - start_time: 開始時間（秒）
    - end_time: 結束時間（秒）
    - remove_audio: 是否移除音訊
    """
    try:
        # 載入影片
        print(f"正在載入影片: {input_file}")
        video = VideoFileClip(input_file)
        
        # 檢查時間範圍
        if end_time > video.duration:
            print(f"警告: 結束時間超過影片長度，將使用影片結尾時間")
            end_time = video.duration
        
        # 切分影片
        print(f"正在切分影片: {start_time}秒 到 {end_time}秒")
        cut_video = video.subclip(start_time, end_time)
        
        # 如果需要移除音訊
        if remove_audio:
            print("正在移除音訊...")
            cut_video = cut_video.without_audio()
        
        # 儲存影片
        print(f"正在儲存影片: {output_file}")
        cut_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        
        # 釋放資源
        video.close()
        cut_video.close()
        
        print(f"✅ 影片已成功儲存至: {output_file}")
        
    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='影片切分工具 - 支援.TS檔案')
    parser.add_argument('input', help='輸入影片檔案路徑')
    parser.add_argument('-o', '--output', help='輸出影片檔案路徑（預設: output_[時間戳記].mp4）')
    parser.add_argument('-s', '--start', required=True, help='開始時間（格式: HH:MM:SS 或 MM:SS 或秒數）')
    parser.add_argument('-e', '--end', required=True, help='結束時間（格式: HH:MM:SS 或 MM:SS 或秒數）')
    parser.add_argument('-n', '--no-audio', action='store_true', help='移除音訊')
    
    args = parser.parse_args()
    
    # 檢查輸入檔案是否存在
    if not os.path.exists(args.input):
        print(f"❌ 錯誤: 找不到輸入檔案 '{args.input}'")
        return
    
    # 設定輸出檔案名稱
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_file = f"output_{base_name}_{timestamp}.mp4"
    
    # 轉換時間
    start_seconds = convert_time_to_seconds(args.start)
    end_seconds = convert_time_to_seconds(args.end)
    
    if start_seconds >= end_seconds:
        print("❌ 錯誤: 開始時間必須小於結束時間")
        return
    
    print("\n=== 影片切分設定 ===")
    print(f"輸入檔案: {args.input}")
    print(f"輸出檔案: {output_file}")
    print(f"開始時間: {args.start} ({start_seconds}秒)")
    print(f"結束時間: {args.end} ({end_seconds}秒)")
    print(f"移除音訊: {'是' if args.no_audio else '否'}")
    print("==================\n")
    
    # 執行切分
    cut_video(args.input, output_file, start_seconds, end_seconds, args.no_audio)

if __name__ == "__main__":
    main()