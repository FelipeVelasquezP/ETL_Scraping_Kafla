from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split,avg
from pyspark.sql import functions as f
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col, conv, hex

spark = SparkSession \
    .builder \
    .appName("ProgramaSensores") \
    .getOrCreate()

print('FUNCIONO')

lines = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers","localhost:9092") \
    .option("subscribe","quickstart-events") \
    .load()
print('FINALIZO')

df=lines.withColumn("Price", conv(col("value"), 16, 16).cast("bigint"))
df2=df.withColumn("PRICE1",df["PRICE"]).withColumn("PRICE2",df["PRICE"])
query=df2.agg({'PRICE': 'avg','PRICE1': 'max','PRICE2': 'min'})
query=query.withColumnRenamed('min(PRICE2)', 'Valor Minimo')
query=query.withColumnRenamed('max(PRICE1)', 'Valor Maximo')
query=query.withColumnRenamed('avg(PRICE)', 'Promedio')


writer = query \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start().awaitTermination()
