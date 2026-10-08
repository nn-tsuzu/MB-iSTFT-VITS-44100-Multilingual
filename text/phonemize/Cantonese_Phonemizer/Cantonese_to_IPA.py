import pycantonese
from chinese_converter import to_traditional
import itertools

TONE = (
    {
        "1":"˥",
        "2":"˧˥",
        "3":"˧",
        "4":"˨˩",
        "5":"˩˧",
        "6":"˨"
    }
)

class G2P_Cantonese_to_Phoneme:
    def phonemize(text: str):
        text = to_traditional(text)
        # print(text)

        # chinese character to jyutping
        pairs = pycantonese.characters_to_jyutping(text)
        result = []
        # print(pairs)

        for char, jyut in pairs:
            if jyut == None:
                result.append(char)
                continue
            ipa = pycantonese.jyutping_to_ipa(jyut, tones=TONE)
            result.append(ipa)
        return "".join(list(itertools.chain.from_iterable(result))).replace(" ", "")
    

if __name__ == "__main__": 
    text = "香港人講廣東話、中國人講中文。"
    print("Cantonese: ", G2P_Cantonese_to_Phoneme.phonemize(text=text))

    text = "香港人講廣東話, 中國人講中文."
    print("Cantonese: ", G2P_Cantonese_to_Phoneme.phonemize(text=text))