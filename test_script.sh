hadoop fs -rm -r /user/shu09bei/wordindex_test

hadoop fs -rm -r /user/shu09bei/concat

hadoop fs -rm -r /user/shu09bei/indexlabel_score

hadoop fs -rm -r /user/shu09bei/results

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D stream.map.output.field.separator='\t' -D mapred.reduce.tasks=1 -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,2  -files /home/shu09bei/assignment_1/mapper2.py,/home/shu09bei/assignment_1/reducer2.py -mapper /home/shu09bei/assignment_1/mapper2.py -reducer /home/shu09bei/assignment_1/reducer2.py -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -jobconf mapred.map.tasks=1 -input /user/shu09bei/test  -output /user/shu09bei/wordindex_test

mkdir -p /home/shu09bei/assignment_1/wordindex_test

hadoop fs -copyToLocal /user/shu09bei/wordindex_test/* /home/shu09bei/assignment_1/wordindex_test/

cat /home/shu09bei/assignment_1/wordindex_test/* >/home/shu09bei/assignment_1/wordindex_test/wordindex_test_m.txt

cat /home/shu09bei/assignment_1/wordindex_test/wordindex_test_m.txt /home/shu09bei/assignment_1/wordcount_train/wordcount_train_m.txt > /home/shu09bei/assignment_1/concat.txt

hadoop fs -mkdir /user/shu09bei/concat

hadoop fs -copyFromLocal /home/shu09bei/assignment_1/concat.txt /user/shu09bei/concat

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D stream.map.output.field.separator='\t' -D mapred.reduce.tasks=1 -D stream.num.map.output.key.fields=1 -D mapred.text.key.partitioner.options=-k1,1  -files /home/shu09bei/assignment_1/mapper3.py,/home/shu09bei/assignment_1/reducer3.py -mapper /home/shu09bei/assignment_1/mapper3.py -reducer /home/shu09bei/assignment_1/reducer3.py -cacheFile /user/shu09bei/wordcount_train/wordcount_train_m.txt#train_dict -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -input /user/shu09bei/concat/concat.txt -output /user/shu09bei/indexlabel_score

mkdir -p /home/shu09bei/assignment_1/indexlabel_score

hadoop fs -copyToLocal /user/shu09bei/indexlabel_score/* /home/shu09bei/assignment_1/indexlabel_score/

cat /home/shu09bei/assignment_1/indexlabel_score/* >/home/shu09bei/assignment_1/indexlabel_score/indexlabel_score_m.txt

hadoop fs -copyFromLocal /home/shu09bei/assignment_1/indexlabel_score/indexlabel_score_m.txt /user/shu09bei/indexlabel_score

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D stream.map.output.field.separator='\t' -D mapred.reduce.tasks=1 -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,2  -files /home/shu09bei/assignment_1/mapper4.py,/home/shu09bei/assignment_1/reducer4.py -mapper /home/shu09bei/assignment_1/mapper4.py -reducer /home/shu09bei/assignment_1/reducer4.py   -cacheFile /user/shu09bei/wordcount_train/wordcount_train_m.txt#train_dict -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner  -input /user/shu09bei/indexlabel_score/indexlabel_score_m.txt -output /user/shu09bei/results

mkdir -p /home/shu09bei/assignment_1/results/

hadoop fs -get /user/shu09bei/results/* /home/shu09bei/assignment_1/results/

cat /home/shu09bei/assignment_1/results/* >/home/shu09bei/assignment_1/results/results_m.txt

sort -n -k 1,1 /home/shu09bei/assignment_1/results/part-00000 > /home/shu09bei/assignment_1/results/results.txt


