from googletrans import Translator


def translation(word):
    translator = Translator()
    result = translator.translate(word, dest='ru')
    trans_list = {}
    for key, value in result.extra_data.items():
        trans_list[key] = value

    all_trans = trans_list['all-translations']

    if all_trans:
        possible_translations = all_trans[0][1]
        return possible_translations
    else:
        possible_translations = []
        possible_translations.append(trans_list['translation'][0][0])
        return possible_translations
