from preprocess import load_file
from feature import feat
from postprocess import post_process
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

factor = 4.0
length = 500
debug = False

train_df, train_list = load_file('I')
test_df, test_list = load_file('J')

train_df = sample_balance(train_df, factor)
X_train, Y_train, bag = feat(train_df, None, length)

#train
clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)
clf.fit(X_train, Y_train)

#test
X_test, Y_test, bag = feat(test_df, bag, length)
Y_predict = clf.predict(X_test)
Y_predict = post_process(test_df, Y_predict)
			
precision, recall, falsePositive, falseNegative = precision_recall(test_df, Y_predict)
if debug:
	falsePositive.to_csv('falsePositive.csv')
	falseNegative.to_csv('falseNegative.csv')
print('Precision:')
print(precision)

print('Recall:')
print(recall)
			
		



