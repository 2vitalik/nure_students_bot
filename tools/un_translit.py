import re
from string import ascii_letters

# Латинські та укр. голосні для евристик
LAT_VOWELS = set("AEIOUYaeiouy")
UKR_VOWELS = set("АЕЄИІЇОУЮЯаеєиіїоуьюя")

# Базові багатолітерні відповідники (без контекстних Ye/ie, Ya/ia...):
# порядок важливий: довші токени спершу
MULTI_MAP = [
    ("shch", "щ"),
    ("zgh",  "зг"),
    ("kh",   "х"),
    ("ts",   "ц"),
    ("ch",   "ч"),
    ("sh",   "ш"),
    ("zh",   "ж"),
    ("yo",   "йо"),  # уживане у власних іменах: Yosyp → Йосип
]

# Однолітерні відповідники (просте, контекст додамо нижче)
SINGLE_MAP = {
    "a":"а","b":"б","v":"в","h":"г","g":"ґ","d":"д","e":"е","z":"з","k":"к","l":"л",
    "m":"м","n":"н","o":"о","p":"п","r":"р","s":"с","t":"т","u":"у","f":"ф",
}

def apply_case(src_token: str, dst: str) -> str:
    """Зберігає стиль регістру: ВЕРХНІЙ, Тайтл, нижній."""
    if src_token.isupper():
        return dst.upper()
    if src_token[0].isupper() and src_token[1:].islower():
        # Тайтл-кейс: перша велика, решта малі
        return dst[0].upper() + dst[1:]
    return dst

def is_word_start(text: str, i: int) -> bool:
    """Початок слова: попередній символ не літера (лат./укр.)."""
    if i == 0:
        return True
    prev = text[i-1]
    return not (prev.isalpha() or prev in "’'")

def lat_to_uk(text: str) -> str:
    i = 0
    out = []
    while i < len(text):
        # 1) Пунктуація/пропуски — як є
        ch = text[i]
        if not ch.isalpha():
            out.append(ch)
            i += 1
            continue

        # 2) Пробуємо довгі послідовності (з урах. регістру)
        matched = False
        for latin, cyr in MULTI_MAP:
            L = len(latin)
            seg = text[i:i+L]
            if seg.lower() == latin:
                out.append(apply_case(seg, cyr))
                i += L
                matched = True
                break
        if matched:
            continue

        # 3) Контекстні пари Ye/ie, Ya/ia, Yu/iu, Yi/i
        #    (офіційна система: Ye/Yu/Ya/— на початку слова або після апострофа)
        #    Ї: Yi на початку; після апострофа теж очікуємо "i" = ї
        #    Також додаємо поширений "ye/ie" для Є, "yo" для Йо (покрито вище)
        #    Обробляємо з погляду довжини 2
        if i+2 <= len(text):
            seg2 = text[i:i+2]
            seg2_low = seg2.lower()
            at_start = is_word_start(text, i)
            prev_char = out[-1] if out else ""
            prev_is_apostrophe = prev_char in ("’", "'")

            if seg2_low in ("ye","ya","yu","yi","ie","ia","iu"):
                # Визначимо цільову букву
                if seg2_low == "ye":
                    cyr = "є" if (at_start or prev_is_apostrophe) else "є"  # у КМУ всередині це зазвичай "ie", але якщо маємо "ye" — лишаємо Є
                elif seg2_low == "ie":
                    cyr = "є"
                elif seg2_low == "ya":
                    cyr = "я" if (at_start or prev_is_apostrophe) else "я"
                elif seg2_low == "ia":
                    cyr = "я"
                elif seg2_low == "yu":
                    cyr = "ю" if (at_start or prev_is_apostrophe) else "ю"
                elif seg2_low == "iu":
                    cyr = "ю"
                elif seg2_low == "yi":
                    # На початку слова — Ї, інакше часто це розділ "…иі…" але в КМУ "Yi" саме на початку
                    cyr = "ї" if at_start else "ий"

                out.append(apply_case(seg2, cyr))
                i += 2
                continue

        # 4) Окреме опрацювання 'y' та 'i' (найскладніші)
        seg1 = text[i]
        low = seg1.lower()

        if low == "y":
            # За КМУ: "y" = и; але на початку слова перед голосною часто відповідає пригол. [й]
            # Евристика: якщо на початку слова або після голосної і далі голосна → «й», інакше → «и».
            next_ch = text[i+1] if i+1 < len(text) else ""
            prev_cyr = out[-1] if out else ""
            prev_is_vowel = prev_cyr in UKR_VOWELS
            next_is_vowel = next_ch in LAT_VOWELS
            if (is_word_start(text, i) or prev_is_vowel) and next_is_vowel:
                cyr = "й"
            else:
                cyr = "и"
            out.append(apply_case(seg1, cyr))
            i += 1
            continue

        if low == "i":
            # Можливі варіанти: і, ї, (рідше — й всередині; у КМУ внутрішній Й → i, що втрачає відновлюваність)
            # Евристики:
            #  - якщо попередній символ — апостроф → ї (об’їзд)
            #  - якщо попередній уже виведений укр. символ — голосний → ї (Київ → Kyiv)
            #  - якщо кінець слова і перед цим також 'i' → «ій» (Oleksii → Олексій)
            prev_cyr = out[-1] if out else ""
            prev_is_apostrophe = prev_cyr in ("’", "'")
            prev_is_vowel = prev_cyr in UKR_VOWELS
            next_ch = text[i+1] if i+1 < len(text) else ""

            # "…ii" наприкінці слова → "ій" (доволі частий закінч.)
            if next_ch.lower() == "i":
                next2 = text[i+2] if i+2 < len(text) else ""
                if not (next2 and next2.isalpha()):  # фактичний кінець слова
                    # Перше i → "і", друге i → "й"
                    out.append(apply_case(seg1, "і"))
                    out.append(apply_case(next_ch, "й"))
                    i += 2
                    continue

            if prev_is_apostrophe or prev_is_vowel:
                cyr = "ї"
            else:
                cyr = "і"
            out.append(apply_case(seg1, cyr))
            i += 1
            continue

        # 5) Прості однолітерні відповідники
        if low in SINGLE_MAP:
            out.append(apply_case(seg1, SINGLE_MAP[low]))
            i += 1
            continue

        # 6) Якщо літера поза системою (q, w, x, c окремо тощо) — лишаємо як є
        out.append(seg1)
        i += 1

    return "".join(out)


# ---- приклади ----
if __name__ == "__main__":
    samples = [
        "Kyiv",          # Київ
        "Kharkiv",       # Харків
        "Halych",        # Галич
        "Zghurivka",     # Згурівка
        "Yevhen",        # Євген
        "Yosyp",         # Йосип
        "Oleksii",       # Олексій
        "Zaporіzhzhia",  # Запоріжжя (часто пишуть Zaporizhzhia; подвійне zh → ж + жд/жж — це вже не КМУ, але приклад)
        "Kremenchuk",    # Кременчук
        "Lviv",          # Львів
        "Ob'yizd",       # Обʼїзд
        "Pshenychnyi",   # Пшеничний
    ]
    for s in samples:
        print(s, "→", lat_to_uk(s))
