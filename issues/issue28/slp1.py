from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


def iast_to_slp1(s):
    return transliterate(s, sanscript.IAST, sanscript.SLP1)


def slp1_to_iast(s):
    return transliterate(s, sanscript.SLP1, sanscript.IAST)
