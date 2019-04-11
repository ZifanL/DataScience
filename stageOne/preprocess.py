import os
import pandas as pd
import re


def load_file(inputdir):
	df = pd.DataFrame(columns=['file','token','num','prefix','suffix','isname','namepos'])
	for file_name in os.listdir(inputdir):
		if file_name.endswith('.txt'):
			print(file_name)
			fp = open(os.path.join(inputdir,file_name),'r')
			text = fp.read()
			words = re.split('[\s,.?:"\';!()]',text)
			words = list(filter(None,words))
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
			files1 = [file_name]*len(words)
			files2 = [file_name]*(len(words)-1)
			files3 = [file_name]*(len(words)-2)

			for i in range(len(words)):
				if words[i].startswith('<person>'):
					t = i
					while not words[t].endswith('</>'):
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
			##print(isname1)
			##print(isname2)
			##print(isname3)
			#print(name_pos1)
			#print(name_pos2)
			#print(name_pos3)

			##print(len(words))

			for i in range(len(words)):
				words[i] = words[i].replace('<person>','').replace('</>','')
			#print(words)
			tokens1 = words.copy()
			##print(len(tokens1))
			tokens2 = words.copy()
			for i in range(len(tokens2)-1):
				tokens2[i] = tokens2[i]+' '+tokens2[i+1]
			del tokens2[-1]
			##print(len(tokens2))
			tokens3 = words.copy()
			for i in range(len(tokens3)-2):
				tokens3[i] = tokens3[i]+' '+tokens3[i+1]+' '+tokens3[i+2]
			del tokens3[-1]
			del tokens3[-1]
			prefix1 = ['null']+words.copy()
			del prefix1[-1]
			prefix2 = ['null']+words.copy()
			del prefix2[-1]
			del prefix2[-1]
			prefix3 = ['null']+words.copy()
			del prefix3[-1]
			del prefix3[-1]
			del prefix3[-1]

			suffix1 = words.copy()+['null']
			del suffix1[0]
			suffix2 = words.copy()+['null']
			del suffix2[0]
			del suffix2[0]
			suffix3 = words.copy()+['null']
			del suffix3[0]
			del suffix3[0]
			del suffix3[0]

			#print(len(files1+files2+files3))
			#print(len(tokens1+tokens2+tokens3))
			#print(len(num1+num2+num3))
			#print(len(prefix1+prefix2+prefix3))
			#print(len(suffix1+suffix2+suffix3))
			#print(len(isname1+isname2+isname3))
			#print(len(name_pos1+name_pos2+name_pos3))

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



	return df



			




