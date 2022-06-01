#ライブラリ読み込み
from pydub import AudioSegment
from pydub.playback import play
import matplotlib.pyplot as plt
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

#再生パス指定
path = "/Users/kota/Documents/3年次/プロジェクト学習/曲ファイル/"
file_name = "Fine.wav"
file_path = path + file_name

#再生用ファイルに変更
sound = AudioSegment.from_file(file_path, "wav")
y, sr = librosa.load(file_path)

#情報取得
time = sound.duration_seconds # 再生時間(秒)
rate = sound.frame_rate  # サンプリングレート(Hz)
channel = sound.channels  # チャンネル数(1:mono, 2:stereo)

#曲情報
tempo = 130
beats = 4 #n拍子
ber = 1 #n小節目スタート
#再生小節数
playber = 72

#情報出力
print('チャンネル数：', channel)
print('サンプリングレート：', rate)
print(f"テンポ {tempo :.2f} beats per minute")
print('再生時間：', time)
print('拍子：', beats)
print('再生小節： %d ~ %d'%(ber, ber+playber))

#音楽開始位置取得(onset_times[0])
frame_length = 2048
hop_length = frame_length // 4
onset_frames = librosa.onset.onset_detect(y, sr=sr, hop_length=hop_length)
onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)

#１拍秒数
beatsec = 60.0 / tempo

#単位をms変換
mstart = onset_times[0] * 1000
beatms = beatsec * 1000

#開始,終了位置指定
start = mstart + beats * beatms * (ber-1)
end = start + beats * beatms * playber

fullber = (time-mstart/1000) / (beatsec*beats)
print('総小節数:', fullber)

# 音声データをリストで抽出
#list_sound = sound.get_array_of_samples()

# リストをグラフ化
#plt.plot(list_sound)
#plt.grid()

# 抽出(0s~10s)
sound1 = sound[start:end]

# 最後を抽出(10s)
#sound2 = sound[-10000:]

#逆再生
#soundr = sound1.reverse()

#速度2倍
#sounds = soundr.speedup(playback_speed=2, crossfade=0)

# フェードイン（5秒）、フェードアウト（2秒）
#soundf = sounds.fade_in(5000).fade_out(2000)

# 繰り返し（2回再生）
#soundd = sound1 * 2

#結合
#sound3 = soundf + sound1

#音楽再生
play(sound1)

# 指定したフォーマットとビットレートで保存
#sound1.export("outputs.wav", format="wav" ,bitrate="192k")