import itertools
from gruut import sentences


class G2P_US_English_to_Phoneme:
    def phonemize(text):
        i = []

        for sent in sentences(text, lang="en-us", espeak=True):
            for word in sent:
                if word.phonemes:
                    i.append(word.phonemes)
                    # i.append([" "])

        text = "".join(list(itertools.chain.from_iterable(i)))
        return text
    

class G2P_multilang_to_Phoneme:
    "also supported British english"
    def phonemize(text, lang):
        i = []

        for sent in sentences(text, lang=lang):
            for word in sent:
                if word.phonemes:
                    i.append(word.phonemes) 
                    # i.append([" "])

        text = "".join(list(itertools.chain.from_iterable(i)))
        return text


if __name__ == "__main__":
    text = "A bottle of water. This is a test, test!!"

    print("us: ", G2P_US_English_to_Phoneme.phonemize(text))
    print("gb: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="en"))

    """print("Arabic: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="ar"))
    print("Czech: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="cs"))
    print("German: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="de"))
    print("Spanish: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="es"))
    print("Farsi: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="fa"))
    print("French: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="fr"))
    print("Italian: ", G2P_multilang_to_Phoneme.phonemize(text="text", lang="it"))
    print("Luxembourgish: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="lb"))
    print("Dutch: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="nl"))
    print("Russian: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="ru"))
    print("Swedish: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="sv"))
    print("Swahili: ", G2P_multilang_to_Phoneme.phonemize(text=text, lang="sw"))"""