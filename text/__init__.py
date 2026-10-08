try:
  from . import cleaners
  from .phonemize.symbols import symbols
except:
  # for test
  import cleaners
  from phonemize.symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}


def text_to_sequence(text, cleaner_names, language=None):
  '''
  IPA to strings. example: ni˧˥xɑʊ˨˩˦ -> 1234567
  IPAを数値に変換する。返り値のsequenceをtensor化すればモデルに入力できる。
  
  Args:
    text: string to convert to a sequence
    cleaner_names: names of the cleaner functions to run the text through
  Returns:
    List of integers corresponding to the symbols in the text
  '''
  sequence = []
  clean_text  = _clean_text(text, cleaner_names, language)
  
  if type(clean_text) is list:
    clean_text = "".join(clean_text).replace("  ", " ")

  for symbol in clean_text:
    symbol_id = _symbol_to_id[symbol]
    sequence += [symbol_id]
  return sequence


def cleaned_text_to_sequence(cleaned_text):
  '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
    Args:
      text: string to convert to a sequence
    Returns:
      List of integers corresponding to the symbols in the text
  '''
  sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
  return sequence


def sequence_to_text(sequence):
  '''Converts a sequence of IDs back to a string'''
  result = ''
  for symbol_id in sequence:
    s = _id_to_symbol[symbol_id]
    result += s
  return result


def _clean_text(text, cleaner_names, language=None):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text, language)
  return text 


if __name__ == "__main__":
  t  = text_to_sequence(text="你好，世界！こんにちは。Programing  쪼와요~", cleaner_names=["all_languages_cleaner"])
  print("mix: ", t)

  t  = _clean_text(text="１週間して、そのニュースは本当になった。", language="ja", cleaner_names=["all_languages_cleaner"])
  print("Japanese: ", t)
