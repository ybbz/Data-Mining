# encoding=utf-8

"""
connect mysql, query teble and get data, cut the queried data with jieba, statistic and save data
"""

import jieba
import mysql.connector
import datetime

# connect mysql
conn = mysql.connector.connect(host="localhost", user="name", passwd="password", db="database")
cursor = conn.cursor()

# query teble
cursor.execute('select name from case')
values = cursor.fetchall()
print("queried" + str(len(values)))

word_list = [] 
word_dict = {} 
word_frequency = []

file_origin = '/Users/ybbz/Desktop/case.txt'
file_count = '/Users/ybbz/Desktop/casecount.txt'


# get format time
def getTime():
    now = datetime.datetime.now() 
    format_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return format_time


# process and save data
with open(file_origin, 'w') as f1:
    pass
with open(file_origin, 'a') as f1, open(file_count, 'w') as f2:
    count = 0
    for value in values:
        f1.write(value[0] + "\n")
        value_cut = jieba.cut_for_search(value[0])
        for cut in value_cut:
            word_list.append(cut)
        count += 1
    print("processed" + str(count))

    # statistic
    for word in word_list:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1

    time = getTime()

    # save data
    for key in word_dict:
        f2.write(key + ' ' + str(word_dict[key]) + "\n")
        item = (key, word_dict[key], time)
        word_frequency.append(item)
    print("processed" + str(count))

    # save the result to database
    sql = "insert into corpus(name,frequency,create_time) values(%s, %s, %s)"
    cursor.executemany(sql, word_frequency)
    conn.commit()
    print("done !")
