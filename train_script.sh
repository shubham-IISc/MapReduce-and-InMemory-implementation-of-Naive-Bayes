hadoop fs -rm -r /user/shu09bei/wordcount_train

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D stream.map.output.field.separator='\t' -D mapred.reduce.tasks=1  -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,2  -files /home/shu09bei/assignment_1/mapper1.py,/home/shu09bei/assignment_1/reducer1.py -mapper /home/shu09bei/assignment_1/mapper1.py -reducer /home/shu09bei/assignment_1/reducer1.py -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -input /user/shu09bei/train  -output /user/shu09bei/wordcount_train

mkdir -p /home/shu09bei/assignment_1/wordcount_train

hadoop fs -copyToLocal /user/shu09bei/wordcount_train/* /home/shu09bei/assignment_1/wordcount_train/

cat /home/shu09bei/assignment_1/wordcount_train/* >/home/shu09bei/assignment_1/wordcount_train/wordcount_train_m.txt

hadoop fs -copyFromLocal /home/shu09bei/assignment_1/wordcount_train/wordcount_train_m.txt   /user/shu09bei/wordcount_train

