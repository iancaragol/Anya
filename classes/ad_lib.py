import googletrans
import difflib
from googletrans import Translator

class AdLibber:
    def __init__(self, verbose):
        self.translator = Translator()
        self.verbose = verbose

    def translate_and_format(self, messages, languages):
        languages_arr = languages.lower().split('>')

        for l in languages_arr:
            if self.verbose:
                print("Translating to: " + l)
            trans_msg = self.translate_all(messages, l)

        return self.format(trans_msg, languages)

    def translate_all(self, messages, dest_language):
        text_only = [m[1] for m in messages]
        translated_text = self.translator.translate(text_only, dest=dest_language)

        for i in range(len(messages)):
            if self.verbose:
                print(messages[i])

            messages[i] = (messages[i][0], translated_text[i].text)

        return messages

    def format(self, messages, languages):
        f_string = """```md
Languages: [{}]\n\n""".format(languages.lower())

        for m in messages:
            if len(messages) > 1:
                add_string = "[{}]: {}\n".format(m[0], m[1])
                f_string += add_string
            else:
                add_string = "{}\n".format(m[1])
                f_string += add_string

        f_string.strip()
        f_string += "```"

        return f_string

    def check_languages(self, languages):
        languages_arr = languages.lower().split('>')

        for l in languages_arr:
            if l not in googletrans.LANGUAGES.keys():
                closest_strs = difflib.get_close_matches(l, googletrans.LANGUAGES.keys(), cutoff=0.4)
                return False, "`I did not recognize the language code {}. Use !languages to see all available language codes.`"
        return True, ""

    def get_language_codes(self):
        return "```" + str(googletrans.LANGUAGES).replace(',', '\n')[1:-1] + "```"