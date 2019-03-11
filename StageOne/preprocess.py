import os
import pandas as pd
import re

def is_all_capital(token):
	words = token.split()
	for word in words:
		#print(word)
		if not word[0].isupper():
			return False
	return True

def remove_punct(token):
	token = token.replace('.', '')
	token = token.replace('?', '')
	token = token.replace('!', '')
	token = token.replace(':', '')
	if len(token) == 0:
		token = '~null'
	return token

def no_stop_in_middle(token):
	words = token.strip()
	for word in words:
		if word == '.':
			return False
	token_concat = ''.join(words)
	if '.' in token_concat and not token_concat.endswith('.'):
		return False
	if ':' in token_concat and not token_concat.endswith(':'):
		return False
	if '?' in token_concat and not token_concat.endswith('?'):
		return False
	if '!' in token_concat and not token_concat.endswith('!'):
		return False
	return True

def load_file(inputdir):
	file_count = 0
	name_count = 0
	file_list = []
	print('Start loading files...')
	df = pd.DataFrame(columns=['file','token','num','prefix','suffix','isname','namepos'])
	for root, dirs, files in os.walk(inputdir, topdown=False):
		for file_name in files:
			if file_name.endswith('.txt'):
				file_count += 1
				print(os.path.join(root,file_name))
				file_list.append(os.path.join(root,file_name))
				fp = open(os.path.join(root,file_name),'r')
				text = fp.read()
				#words = re.split('[\s,.?:"\';!()]',text)
				words = re.split('[\s,"\';()]',text)
				words = list(filter(None,words))
				#print(words)

				for i in range(len(words)):
					if words[i] == '<person>':
						words[i+1] = words[i]+words[i+1]
						words[i] = ''
					if words[i] == '</>':
						words[i-1] = words[i-1]+words[i]
						words[i] = ''
				words = list(filter(None,words))
				#print(words)

				isname1 = [False]*len(words)
				isname2 = [False]*(len(words)-1)
				isname3 = [False]*(len(words)-2)
				name_pos1 = [-1]*len(words)
				name_pos2 = [-1]*(len(words)-1)
				name_pos3 = [-1]*(len(words)-2)
				num1 = [1]*len(words)
				num2 = [2]*(len(words)-1)
				num3 = [3]*(len(words)-2)
				files1 = [os.path.join(root,file_name)]*len(words)
				files2 = [os.path.join(root,file_name)]*(len(words)-1)
				files3 = [os.path.join(root,file_name)]*(len(words)-2)

				for i in range(len(words)):
					if words[i].startswith('<person>'):
						name_count += 1
						t = i
						while not words[t].strip('.').strip('?').strip('!').strip(':').endswith('</>'):
							t += 1
						for j in range(i,t+1):
							isname1[j] = True
							name_pos1[j] = i
						for j in range(i,t):
							isname2[j] = True
							name_pos2[j] = i
						for j in range(i,t-1):
							isname3[j] = True
							name_pos3[j] = i

				for i in range(len(words)):
					words[i] = words[i].replace('<person>','').replace('</>','')

				tokens1 = words.copy()
				tokens2 = words.copy()
				for i in range(len(tokens2)-1):
					tokens2[i] = tokens2[i]+' '+tokens2[i+1]
				del tokens2[-1]

				tokens3 = words.copy()
				for i in range(len(tokens3)-2):
					tokens3[i] = tokens3[i]+' '+tokens3[i+1]+' '+tokens3[i+2]
				del tokens3[-1]
				del tokens3[-1]
				prefix1 = ['~null']+words.copy()
				del prefix1[-1]
				prefix2 = ['~null']+words.copy()
				del prefix2[-1]
				del prefix2[-1]
				prefix3 = ['~null']+words.copy()
				del prefix3[-1]
				del prefix3[-1]
				del prefix3[-1]

				suffix1 = words.copy()+['~null']
				del suffix1[0]
				suffix2 = words.copy()+['~null']
				del suffix2[0]
				del suffix2[0]
				suffix3 = words.copy()+['~null']
				del suffix3[0]
				del suffix3[0]
				del suffix3[0]

				df_tmp = pd.DataFrame({
					'file': files1+files2+files3,
					'token': tokens1+tokens2+tokens3,
					'num': num1+num2+num3,
					'prefix': prefix1+prefix2+prefix3,
					'suffix': suffix1+suffix2+suffix3,
					'isname': isname1+isname2+isname3,
					'namepos': name_pos1+name_pos2+name_pos3
								   })
				df = df.append(df_tmp)

	isCapital = df['token'].apply(is_all_capital)
	df = df[isCapital]
	noStopInMiddle = df['token'].apply(no_stop_in_middle)
	df = df[noStopInMiddle]
	df['token'] = df['token'].apply(remove_punct)
	df['suffix'] = df['suffix'].apply(remove_punct)
	
	print('------------- Data has been loaded -------------')
	print('Total number of files: '+str(file_count))
	print('Total number of names: '+str(name_count))	

	return df, file_list