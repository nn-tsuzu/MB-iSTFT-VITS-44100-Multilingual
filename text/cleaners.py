import re
import unicodedata

try:
  from .phonemize.text_to_IPA_converter import auto_g2p
except:
  # for test
  from phonemize.text_to_IPA_converter import auto_g2p


# Regular expression matching whitespace:
# _whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
]]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def text_cleaner(text:str):
    """
    全角を半角に変換 + 句読点をカンマ・コンマに変換する
    英語の略語もついでに変換する
    """
    text = expand_abbreviations(text)
    text = unicodedata.normalize('NFKC', text)
    text = text.replace("。", ".").replace("、", ",").replace("…", "...")
    text = text.replace("，", ",")
    return text


converter = auto_g2p()
def all_languages_cleaner(text:str, language=None):
    """text to ipa"""
    text = text_cleaner(text)
    text = converter(text, language)
    return text

# print(all_languages_cleaner("天気が良いから散歩しよう。アンニョンハセヨ。안녕하세요."))