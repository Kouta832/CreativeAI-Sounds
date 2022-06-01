def play_ber(file_path,tempo,beats,ber,playber,n):
    #file_path = 再生パス,tempo = テンポ,beats = 拍子,ber = スタート,playber = 再生範囲
    from pydub import AudioSegment
    from pydub.playback import play
    import librosa
    import librosa.display
    
    #再生用ファイルに変更
    sound = AudioSegment.from_file(file_path, "wav")
    y, sr = librosa.load(file_path)
    
    #情報取得
    time = sound.duration_seconds # 再生時間(秒)
    rate = sound.frame_rate  # サンプリングレート(Hz)
    channel = sound.channels  # チャンネル数(1:mono, 2:stereo)
    
    
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
    mstart = onset_times[n] * 1000
    beatms = beatsec * 1000
    
    #開始,終了位置指定
    start = mstart + beats * beatms * (ber-1)
    end = start + beats * beatms * playber
    
    fullber = (time-mstart/1000) / (beatsec*beats)
    print('総小節数:', fullber)
    
    # 抽出
    sounds = sound[start:end]
    #再生
    play(sounds*4)
    
def main():
    path = "/Users/kota/Documents/3年次/プロジェクト学習/曲ファイル/"
    file_name = "10℃.wav"
    tempo = 80
    beats = 4#n拍子
    ber = 17 #n小節目スタート
    playber = 16#再生小節数
    n = 1;#開始場所
    play_ber(path+file_name,tempo,beats,ber,playber,n)
    
if __name__ == "__main__":
    main()