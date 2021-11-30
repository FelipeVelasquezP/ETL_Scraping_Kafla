from kafka import KafkaProducer
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql import functions as f
import time

spark = SparkSession.builder.master("local[*]").getOrCreate()
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

sc=spark.sparkContext
sqlContext = SQLContext(sc)
df= sqlContext.read.csv("ETL_Scraping_Kafla/Punto\ 2/SPY_TICK_TRADE.csv", heade>

sample2 = df.rdd.map(lambda x: (x.PRICE))

for row in sample2.collect():
    time.sleep(2)
    st=str(row).encode()
    producer.send('quickstart-events',st)

producer.flush()
