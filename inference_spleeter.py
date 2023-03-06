import os
import io
import logging
from pathlib import Path


import librosa
import numpy as np
import soundfile
from pydub import AudioSegment

from inference import infer_tool
from inference import slicer
from inference.infer_tool import Svc

logging.getLogger('numba').setLevel(logging.WARNING)
chunks_dict = infer_tool.read_temp("inference/chunks_temp.json")

origin = ["audio/XXX.mp3"]
length_of_audio = len(origin[0]) - 10
trans = [0]
spk_list = ['someone'] # 目前只支持单人  
slice_db = -40  # 默认-40，嘈杂的音频可以-30，干声保留呼吸可以-50
wav_format = 'wav'  # 音频输出格式，最好是wav

path = os.getcwd()
audio_path = path + '/' + origin[0]
os.system("spleeter separate " + audio_path + " -o " + path + "/audio/audio_output" + " -p spleeter:2stems")

clean_names = ["vocals"]

model_path = "32k/G_144000.pth"
config_path = "32k/config.json"
svc_model = Svc(model_path, config_path)

infer_tool.fill_a_to_b(trans, clean_names)
for clean_name, tran in zip(clean_names, trans):
    raw_audio_path = f"audio/audio_output/{origin[0][6:6+length_of_audio]}/{clean_name}"
    if "." not in raw_audio_path:
        raw_audio_path += ".wav"
    infer_tool.format_wav(raw_audio_path)
    wav_path = Path(raw_audio_path).with_suffix('.wav')
    chunks = slicer.cut(wav_path, db_thresh=slice_db)
    audio_data, audio_sr = slicer.chunks2audio(wav_path, chunks)

    for spk in spk_list:
        audio = []
        for (slice_tag, data) in audio_data:
            print(f'#=====segment start, {round(len(data) / audio_sr, 3)}s======')
            length = int(np.ceil(len(data) / audio_sr * svc_model.target_sample))
            raw_path = io.BytesIO()
            soundfile.write(raw_path, data, audio_sr, format="wav")
            raw_path.seek(0)
            if slice_tag:
                print('jump empty segment')
                _audio = np.zeros(length)
            else:
                out_audio, out_sr = svc_model.infer(spk, tran, raw_path)
                _audio = out_audio.cpu().numpy()
            audio.extend(list(_audio))

        res_path = f'./audio/inference_output/{origin[0][6:6+length_of_audio]}_{tran}key_{spk}.{wav_format}'
        soundfile.write(res_path, audio, svc_model.target_sample, format=wav_format)

print("Inference finish")
print("Beginning synthesis...")

# 转换为单声道
# os.system("ffmpeg -y -i " + path + f'/raw/audio_output/{origin[0][6:6+length_of_audio]}/accompaniment.wav ' + "-ac 1 " + path + f'/raw/audio_output/{origin[0][6:6+length_of_audio]}/accompaniment_1.wav ')

sound_origin = AudioSegment.from_wav(path + f'/audio/audio_output/{origin[0][6:6+length_of_audio]}/accompaniment.wav')
sound_vocals = AudioSegment.from_wav(path + f'/audio/inference_output/{origin[0][6:6+length_of_audio]}_{tran}key_{spk}.{wav_format}')

# 左右声道可用
# output = AudioSegment.from_mono_audiosegments(sound_origin, sound_vocals)
output = sound_origin.overlay(sound_vocals)
output.export(path+ f'/audio_results/{origin[0][6:6+length_of_audio]}_{tran}key_{spk}.{wav_format}')



