import glob
import os
import subprocess

# カレントディレクトリのパスを取得
current_directory = os.getcwd()

# すべての下位（それ以下も含む）フォルダにあるビデオを検索する。
videos = glob.glob('./**/*.mp4', recursive=True)

count = 0
# ビデオの容量が100MB以上か判定し、大きければ圧縮
for video in videos:
    # 圧縮済のビデオ名を生成
    compressed_video = video[:-4] + '_圧縮済.mp4'
    # ファイル名が "_圧縮済.mp4" で終わる動画または、すでに圧縮済のビデオが存在する場合はスキップ
    if video.endswith("_圧縮済.mp4") or os.path.exists(compressed_video):
        print(f"{video} は既に圧縮済みまたは圧縮済みのファイルが存在します。スキップします。")
        continue
    size = os.path.getsize(video)
    if size > 100000000:
        # 圧縮
        subprocess.call(['ffmpeg', '-i', video, '-crf', '40', compressed_video])
