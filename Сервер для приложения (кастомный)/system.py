
import random

def urlCheck(text):
	text = text.lower()
	if "http" in text or "https" in text:
		for i in range(len(text.split(" "))):
			if "http" in text.split(" ")[i] or "https" in text.split(" ")[i]:
				return "url"
			else:return 'noUrl'
	else:return 'noUrl'


def generateId(amount: int):
	code = ""
	for x in range(amount):
		code = code + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
	return code


