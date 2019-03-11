from preprocess import load_file
from feature import feat
import random
from sklearn.ensemble import RandomForestClassifier

def sample_balance(df_in, factor):
	df_true = df_in[df_in['isname'] == True]
	pos_count = df_true.count()[0]
	df_false = df_in[df_in['isname'] == False]
	neg_count = df_false.count()[0]
	if pos_count*factor < neg_count:
		df_false = df_false.sample(n=int(pos_count*factor), random_state=1)
	df_true = df_true.append(df_false)
	df_true = df_true.sample(n=df_true.count()[0], random_state=1)
	return df_true

def precision_recall(df_in, res):
	df_name = df_in[df_in['isname'] == True]
	name_position = set(df_name['namepos'].tolist())
	df_predict = df_in[res == 1]
	df_wrong = df_predict[df_predict['namepos'] == -1]
	df_correct = df_predict[df_predict['namepos'] != -1]
	predict_name_position = set(df_correct['namepos'].tolist())
	not_found = name_position.difference(predict_name_position)
	index_not_found = df_in['namepos'].apply(lambda a: a in not_found)
	df_not_found = df_in[index_not_found]

	count_wrong = df_wrong.count()[0]
	count_predict_correct = len(predict_name_position)
	count_all_correct = len(name_position)

	precision = float(count_predict_correct)/(count_predict_correct+count_wrong)
	recall = float(count_predict_correct)/count_all_correct
	return precision, recall, df_wrong, df_not_found

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

debug = False
train_df_all, train_list = load_file('I')
random.seed(100)
random.shuffle(train_list)

for length in [500]:
	for factor in [4]:
		precision_mean = 0
		recall_mean = 0

		CV_list = [train_list[:40],train_list[40:80],train_list[80:120],train_list[120:160],train_list[160:200]]
		for i in range(5):
			train_index = train_df_all['file'].apply(lambda a: a not in CV_list[i])
			train_df = train_df_all[train_index]
			dev_index = train_df_all['file'].apply(lambda a: a in CV_list[i])
			dev_df = train_df_all[dev_index]
		
			train_df = sample_balance(train_df, factor)
			X_train, Y_train, bag = feat(train_df, None, length)
		
			clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
			clf.fit(X_train, Y_train)

			#dev
			X_dev, Y_dev, bag = feat(dev_df, bag, length)
			
			Y_predict = clf.predict(X_dev)
			
			precision, recall, falsePositive, falseNegative = precision_recall(dev_df, Y_predict)
			if debug:
				falsePositive.to_csv('falsePositive'+str(i)+'.csv')
				falseNegative.to_csv('falseNegative'+str(i)+'.csv')
			
			precision_mean += precision
			recall_mean += recall
		print('LENGTH: '+str(length))
		print('FACTOR: '+str(factor))
		print('PRECISION: '+str(precision_mean/5))
		print('RECALL: '+str(recall_mean/5)) 



