import pymysql
import random
from datetime import datetime, timedelta

# 生成数据
data = []
start_date = datetime(2024, 4, 3)
end_date = datetime(2024, 4, 13)

# 设定每天生成的数据的时间间隔
time_interval = timedelta(minutes=144)  # 每2.4小时（144分钟）生成一条数据

# 10个传感器
for i in range(1, 11):
    date = start_date
    while date <= end_date:
        time = date
        while time < date + timedelta(days=1):
            temperature = round(random.uniform(0, 27), 2)  # 温度在27°以内
            humidity = round(random.uniform(0, 80), 2)  # 湿度在80%以内
            data.append((i, temperature, humidity, time))
            time += time_interval
        date += timedelta(days=1)

random.shuffle(data)  # 生成的数据混洗，更接近现实场景

# 连接到数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123mysql',
    db='python_wendu',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # 创建sensor_wendu数据表
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS sensor_wendu (id INT, "
            "wendu FLOAT, "
            "shidu FLOAT, "
            "time DATETIME, "
            "INDEX(id))"
        )

        # 将数据写入sensor_wendu数据表
        for row in data:
            cursor.execute(
                "INSERT INTO sensor_wendu (id, wendu, shidu, time) VALUES (%s, %s, %s, %s)",
                row
            )

    # 提交事务
    connection.commit()
finally:
    connection.close()
#之前写的部分，能间隔xxx秒产生数据
#import pymysql
# import random
# from datetime import datetime, timedelta
#
# # 生成数据
# data = []
# start_time = datetime.now()
#
# # 10个传感器
# for i in range(1, 11):
#     time = start_time
#     # 每个传感器生成100条数据
#     for _ in range(100):
#         temperature = round(random.uniform(0, 27), 2)  # 温度在27°以内
#         humidity = round(random.uniform(0, 80), 2)  # 湿度在80%以内
#         data.append((i, temperature, humidity, time))
#         time += timedelta(seconds=40)  # 时间每20秒递增  每个月每天随机采集
#
# # 连接到数据库
# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='123mysql',
#     db='python_wendu',
#     cursorclass=pymysql.cursors.DictCursor
# )
#
# try:
#     with connection.cursor() as cursor:
#         # 创建sensor_wendu数据表
#         cursor.execute("CREATE TABLE IF NOT EXISTS sensor_wendu (id INT, wendu FLOAT, shidu FLOAT, time DATETIME, \
#             INDEX(id))")
#
#         # 将数据写入sensor_wendu数据表
#         for row in data:
#             cursor.execute("INSERT INTO sensor_wendu (id, wendu, shidu, time) VALUES (%s, %s, %s, %s)", row)
#
#     # 提交事务
#     connection.commit()
# finally:
#     connection.close()