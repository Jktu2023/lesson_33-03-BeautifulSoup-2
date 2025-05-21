from googletrans import Translator

translator = Translator()
result = translator.translate('hello', dest='ru')
# text = translator.translate('hello', dest='ja')
print(result.text)


