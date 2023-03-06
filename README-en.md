# SoftVC VITS Singing Voice audio to audio

This project is based on so-vits-svc 32kHz verison, with only a partial addition of model inference.

Replace the song vocals to get the target audio. No audio editing software is required.

## Attention

Only inference.

## Pre-preparation

- soft vc hubert：[hubert-soft-0d54a1f4.pt](https://github.com/bshall/hubert/releases/download/v0.1/hubert-soft-0d54a1f4.pt)
  - Place under `hubert`.
- ffmpeg
- pretrained_models for spleeter：[2stems.tar.gz](https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz)
  - Place and extract under `pretrained_models`.

## Inferencing

- Edit `model_path` to your newest checkpoint.

- Place the input audio under the `audio` folder.

- Change `clean_names` to the output file name.

- Use `trans` to edit the pitch shifting amount (semitones).

- Change `spk_list` to the speaker name.
