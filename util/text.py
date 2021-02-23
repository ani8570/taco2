from jamo import hangul_to_jamo
from jamo.jamo import JAMO_LEADS_MODERN, JAMO_TAILS_MODERN, JAMO_VOWELS_MODERN

PAD = '_'
EOS = '~'
SPACE = ' '
JLM = "".join(JAMO_LEADS_MODERN) # 초성
JVM = "".join(JAMO_VOWELS_MODERN) # 중성
JTM = "".join(JAMO_TAILS_MODERN) # 종성
VALID_CHARS = JLM + JVM + JTM + SPACE
symbols = PAD + EOS + VALID_CHARS

_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

def text_to_sequence(text) :
    sequence = []
    if not ord(JAMO_LEADS_MODERN[0]) <= ord(text[0]) <= ord(JAMO_LEADS_MODERN[-1]) : #ord 문자 -> 정수 , chr 정수 -> 문자
        text = ''.join(list(hangul_to_jamo(text)))
    for s in text:
        sequence.append(_symbol_to_id[s])
    sequence.append(_symbol_to_id['~'])
    return sequence

def sequence_to_text(sequence):
    result = ''
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            result += s
    return result.replace('}{',' ')