# SoftVC VITS Singing Voice audio to audio

本项目基于so-vits-svc 32kHz版本，仅增加了部分模型推断功能。

替换歌曲人声以获得目标歌曲音频。不需要任何音频编辑软件。

## 注意

只有推断功能。

## 预准备

- soft vc hubert：[hubert-soft-0d54a1f4.pt](https://github.com/bshall/hubert/releases/download/v0.1/hubert-soft-0d54a1f4.pt)
  - 放在 `hubert`目录下
- ffmpeg
- pretrained_models for spleeter：[2stems.tar.gz](https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz)
  - 解压到 `pretrained_models`目录下

## Inferencing

- 更改`model_path`为你自己训练的最新模型记录点

- 将待转换的音频放在`audio`文件夹下

- `clean_names` 写待转换的音频名称

- `trans` 填写变调半音数量

- `spk_list` 填写合成的说话人名称

  执行
  
  ```
  python inference_spleeter.py
  ```

输出结果为完整歌曲，在audio_results目录下。