import re

def multi_replace(string, mapping):
    """
    文字列中の複数の文字列やパターンを同時に置換します。
    .replace を連ねる場合と違い、ある置換結果がさらに別の置換を受けてしまうことはありません。
    よって二つのワードを相互に入れ替えることもできます。

    mapping: 検索対象をキー、その置換文字列を値とする辞書。
        キーとしてstrまたはreパターンオブジェクトを指定できる。
        キーがreパターンオブジェクトの場合は、置換文字列中でグループ参照 '\\1', '\\2',... が有効。
    """
    catch_all_pattern = '|'.join(map(to_pattern, mapping))
    replacer = make_replacer(mapping)

    return re.subn(catch_all_pattern, replacer, string)[0]


_PatternType = type(re.compile(''))  # workaround for Python which does't have typing module

def to_pattern(key):
    if isinstance(key, str):
        return '(' + re.escape(key) + ')'
    elif isinstance(key, _PatternType):
        return '(' + key.pattern + ')'
    else:
        raise ValueError(key + " is not a str, neither re.compile.")


def make_replacer(mapping):

    def _replacer(match):
        src = match.group(0)
        for key, val in mapping.items():
            if src == key:
                return val
            elif isinstance(key, _PatternType) and re.match("(?:" + key.pattern + r")\Z", src):  # workaround for Python which doesn't have re.fullmatch
                return key.sub(val, src)

    return _replacer
