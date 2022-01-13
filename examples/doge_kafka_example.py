import json

from doge import Subject, Transition, KafkaSinkFactory
from examples.doge_example_common import create_example_data_online_generator


def key_function(subject: Subject, transition: Transition) -> str:
    return str(subject.user_id)


def value_function(timestamp: int, subject: Subject, transition: Transition) -> str:
    value = {
        'timestamp': timestamp,
        'user': {
            'user_id': subject.user_id,
            'balance': subject.balance,
            'loan_balance': subject.loan_balance
        },
        'event': transition.trigger
    }
    return json.dumps(value)


if __name__ == '__main__':
    factory = KafkaSinkFactory(['localhost:9092'], 'doge-kafka-example')
    sink = factory.create('test_topic', key_function, value_function)

    datagen = create_example_data_online_generator(sink)

    datagen.start()
