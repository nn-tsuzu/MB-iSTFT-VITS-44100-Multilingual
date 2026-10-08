# from typing import Optional
import pyopenjtalk# , re
from .tools import multi_replace
# from ..symbols import _punctuation

JTALK_TO_IPA = {
    # 母音
    "u":"ɯ",
    # 子音
    "y":"j",
    "j":"d͡ʑ",
    "f":"ɸ",
    "r":"ɾ",
    "ry":"ɾʲ",
    "ky":"kʲ",
    "gy":"gʲ",
    "ny":"ɲ",
    "sh":"ɕ",
    "ch":"t͡ɕ",
    "ts":"t͡s",
    "my":"mʲ",
    # ん
    "nk":"ŋk",
    "ng":"ŋg",
    "np":"mp",
    "nb":"mb",
    "nm":"mm",
}


class G2P_Japanese_to_Phoneme:
    def phonemize(text: str):
        # strに変換・細かく音素変換
        base = text
        text = pyopenjtalk.g2p(text).lower().replace(" ", "")

        if text == "":
            raise KeyError(f"{base} is a not Japanese!!")
        text = multi_replace(text, JTALK_TO_IPA)

        # 促音記号（cl）の直後の文字を取得して重ね、促音を表現 「あっつい」->「attui」
        match = text.find("cl")
        if match != -1:
            cl_char = text[match + len("cl") : match + len("cl") + 1]
            return text.replace("cl" + cl_char,  cl_char * 2)
        return text