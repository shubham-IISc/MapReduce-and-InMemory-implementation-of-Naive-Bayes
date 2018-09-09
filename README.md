# MapReduce and InMemory implementation of naive bayes

## InMemory implementation
Requirements-pandas,numpy
Kindly change the dataset paths accordingly in naivebayes_InMemory.py file.


## MapReduce implementation
Here,train.sh assumes the datasets to be present in HDFS(already uploaded on turing cluster). Script involves task performed with single reducer. Increase mapred.reduce.tasks in script file as per required. Also, in case of multiple reducers use reducer4_parallel instead of reducer4 in test.sh.
Final predictions will be saved in results folder. My predictions for the given test set have been uploaded as result_5.txt.
Kindly run train.sh first and then test.sh
