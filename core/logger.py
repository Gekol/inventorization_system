import json
from datetime import datetime

import pika


def get_callback(folder_path):
    def callback(ch, method, properties, body):
        logs = json.loads(open(f"{folder_path}/{method.routing_key}.json", "r").read())
        current_moment = datetime.now()
        data = {
            "datetime": f"{current_moment.year}/"
                        f"{('0' if current_moment.month < 10 else '') + str(current_moment.month)}/"
                        f"{('0' if current_moment.day < 10 else '') + str(current_moment.day)} "
                        f"{('0' if current_moment.hour < 10 else '') + str(current_moment.hour)}:"
                        f"{('0' if current_moment.minute < 10 else '') + str(current_moment.minute)}:"
                        f"{('0' if current_moment.second < 10 else '') + str(current_moment.second)}",
            "data": json.loads(body)
        }
        if len(logs) > 0:
            last_log_time = datetime.strptime(logs[len(logs) - 1]["datetime"], "%Y/%m/%d %H:%M:%S")
            logs = [data] + logs if current_moment.date() == last_log_time.date() else [data]
        else:
            logs = [data]
        log_file = open(f"{folder_path}/{method.routing_key}.json", "w")
        json.dump(logs, log_file)

    return callback


class Logger:
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    def run_server(self, folder_path):
        result = self.channel.queue_declare(queue='', exclusive=True, durable=True)
        queue_name = result.method.queue

        severities = ["error", "warning", "info"]

        for severity in severities:
            self.channel.queue_bind(
                exchange='direct_logs', queue=queue_name, routing_key=severity)
        print(' [*] Waiting for logs. To exit press CTRL+C')
        self.channel.basic_consume(queue=queue_name, on_message_callback=get_callback(folder_path), auto_ack=True)

        self.channel.start_consuming()

    def emit_log(self, severity, message):
        self.channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)


if __name__ == '__main__':
    logger = Logger()
    logger.run_server("../logs")
