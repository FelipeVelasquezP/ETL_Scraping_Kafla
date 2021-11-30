from kafka import KafkaConsumer

consumer = KafkaConsumer('quickstart-events', bootstrap_servers=['localhost:909>

for message in consumer:
        print(message.value.decode("utf-8"))

