import torch
import commons
import utils
import os
import soundcard as sc
import soundfile as sf
from models import SynthesizerTrn
from text.phonemize.symbols import symbols
from text import text_to_sequence, sequence_to_text


class inference():
  def __init__(self, config_path, model_path):
    self.hps = utils.get_hparams_from_file(config_path)

    self.net_g = SynthesizerTrn(
      len(symbols), 
      self.hps.data.filter_length // 2 + 1,
      self.hps.train.segment_size // self.hps.data.hop_length,
      **self.hps.model
    ).eval()
    _ = utils.load_checkpoint(model_path, self.net_g, None)
    #self.net_g.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    # play audio by system default
    self.speaker = sc.get_speaker(sc.default_speaker().name)

  def get_text(self, text, hps):
      text_norm = text_to_sequence(text, cleaner_names=["all_languages_cleaner"])
      if hps.data.add_blank:
          text_norm = commons.intersperse(text_norm, 0)
      text_norm = torch.LongTensor(text_norm)
      return text_norm

  def tts(self, text, save_dir='./audio_output'):
    os.makedirs(save_dir, exist_ok=True)
    text_stn = self.get_text(text, self.hps)

    with torch.no_grad():
      x_tst = text_stn.unsqueeze(0)
      x_tst_lengths = torch.LongTensor([text_stn.size(0)])

      audio = self.net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()

      # play audio
      self.speaker.play(audio, self.hps.data.sampling_rate)
      save_path = os.path.join(save_dir, f"{text}.wav")
      sf.write(file=save_path, data=audio, samplerate=self.hps.data.sampling_rate, format="WAV")


if __name__ == '__main__':
  infer = inference(
    config_path="./finetune_model_dir/JSUT_240k_steps/config.json", 
    model_path="./finetune_model_dir/JSUT_240k_steps-New/G_0.pth"
  )
  infer.tts(text="天気が良いから散歩にいこう。")