from googletrans import Translator

class AdLibber:
    def __init__(self):
        self.translator = Translator()

    def translate_and_format(self, messages, languages):
        languages_arr = langauges.split('>').lower()

        for l in languages_arr:
            print("Translating to: " + l)
            trans_msg = self.translate_all(messages, l)

        return self.format(trans_msg, langauges)

    def translate_all(self, messages, dest_language):
        text_only = [m[1] for m in messages]
        translated_text = self.translator.translate(text_only, dest=dest_language)

        for i in range(len(messages)):
            messages[i] = (messages[i][0], translated_text[i][1])

        return messages

    def format(self, messages, languages):
        f_string = "```asciidoc\n" + "Languages: [{}]\n".format(languages.lower())

        for m in messages:
            add_string = "[{}]: {}\n".format(m[0], m[1])
            f_string += add_string

        f_string.strip()
        f_string += "```"

        return f_string