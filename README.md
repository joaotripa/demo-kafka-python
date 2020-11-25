# Demo Kafka Python with GUI

This demo uses python clients to publish and consume sample data from kafka through GUIs.

For more information see (https://docs.confluent.io/current/tutorials/examples/clients/docs/python.html#client-examples-python)

## Prerequisites

Docker 

Kafka Cluster running: 
* on a local machine 
* in a cloud environment

A python environment with Confluent Python Client for Apache Kafka.
To create a virtual environment: 
```
virtualenv kafka-python-venv
source ./demo-kafka-python-venv/bin/activate
pip install -r requirements.txt
```

## Setup

Create a local file (if not created) in project directory, named kafka.config, with configuration parameters to connect to your Kafka cluster.

*Template configuration file for Confluent Cloud
```
# Kafka
bootstrap.servers={{ BROKER_ENDPOINT }}
security.protocol=SASL_SSL
sasl.mechanisms=PLAIN
sasl.username={{ CLUSTER_API_KEY }}
sasl.password={{ CLUSTER_API_SECRET }}
```

*Template configuration file for local host
```
# Kafka
bootstrap.servers=localhost:9092
```

This demo uses docker to run our kafka cluster. For the single purpose of this demo, only the zookeper, broker and ksql-server services are available. If you want any other services, open docker-compose file and uncomment other services.

Inilialize Kafka Cluster: 
```
docker-compose up -d
```

Initialize the virtual environment (if not initialized):
```
source ./demo-kafka-python-venv/bin/activate
```

## Running the Producer
```
./producer.py
```

## Running the Consumer
```
./consumer.py
```