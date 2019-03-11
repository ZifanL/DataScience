WEEK_DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
with open('months') as word_file:
    MONTHS = set(word_file.read().split())
with open('countries') as word_file:
    COUNTRIES = set(word_file.read().split())
TITLES = ['Executive', 'Mr', 'Dr', 'Sir', 'Minister', 'Secretary', 'President', 'Ms', 'Mrs', 'Professor']
PRONOUN = ['It','Its','He','His','She','Her','They','Their','We','Our','I','My','You','Your','These','Those','This','That','The']

def is_not_special_word(token):
	words = token.split()
	for word in words:
		#print(word)
		if word in WEEK_DAYS or word in MONTHS or word in COUNTRIES or word in TITLES or word in PRONOUN:
			#print('*****************'+word)
			return 0
	return 1

def is_not_consecutive(token):
	words = token.split()
	for word in words:
		count = 0
		for letter in word:
			if letter.isupper():
				count += 1
		if count > 1:
			return False
	return True

def post_process(df, Y):
	isNotSpecial = df['token'].apply(is_not_special_word).values
	isNotConsecutive = df['token'].apply(is_not_consecutive).values
	Y = Y*isNotSpecial
	Y = Y*isNotConsecutive
	
	return Y