#!/usr/bin/env python
# =============================================================================
#
# Consume messages from Kafka
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================

from confluent_kafka import Consumer
from uuid import uuid4
import json
import kafka_lib

class ConsumerEntity(object):
    """ 
    Create Consumer instance
    'auto.offset.reset=earliest' to start reading from the beginning of the
    topic if no committed offsets exist

    Args: 
        conf (dict): Consumer configurations

    Returns:
           
    """
    def __init__(self, conf):
        consumer_group = "consumer_group_" + str(uuid4())
        self.consumer = Consumer({
            'bootstrap.servers': conf['bootstrap.servers'],
            #'sasl.mechanisms': conf['sasl.mechanisms'],
            #'security.protocol': conf['security.protocol'],
            #'sasl.username': conf['sasl.username'],
            #'sasl.password': conf['sasl.password'],
            'group.id': consumer_group,
            'auto.offset.reset': 'earliest',
        })

    def subscribe(self, topics):
        """ 
        Subscribe to topic
        
        Args:
            topics (array str): topics name/id

        Returns:

        """
        self.consumer.subscribe(topics)
    
    def unsubscribe(self):
        """ 
        Unsubscribe to topic
        
        Args:
            topics (array str): topics name/id

        Returns:

        """
        self.consumer.unsubscribe()

    def consume(self):
        """ 
        Consume records
        
        Args:

        Returns: records
            
        """
        return self.consumer.poll(1.0)

    def close(self):
        self.consumer.close()            
