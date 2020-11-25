#!/usr/bin/env python
# =============================================================================
#
# Consume messages from Kafka
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================

from consumer_lib import ConsumerEntity as Consumer
from uuid import uuid4
from sensor import Sensor
from tkinter import *

import json
import kafka_lib
import random


class GUIFramework(Frame):
    """This is the GUI"""
    
    def __init__(self,master=None):
        """Initialize yourself"""
        
        """Initialise the base class"""
        Frame.__init__(self,master)
        
        """Set the Window Title"""
        self.master.title("Demo Kafka Python Subscriber")

        """Defining auxiliary variables"""
        self.TopicCheckBoxes = []
        self.checkBoxVar = dict()
        self.checkboxvarA = IntVar()
        self.checkboxvarB = IntVar()
        self.checkboxvarC = IntVar()

        """Display the main window"""
        self.titleLabel = Label(self.master, text="Subscriber GUI", pady=15)
        self.titleLabel.pack()
        self.CreateWidgets()
        
    def CreateWidgets(self):
        """Create all the widgets that we need"""
                
        self.dataFrame = Frame(self.master) 
        self.dataFrame.pack()

        #Creating a frame for records and last message
        self.RecordsFrame = Frame(self.dataFrame)
        self.RecordsFrame.pack(side = LEFT, padx = 10)

        self.LastMsgFrame = Frame(self.dataFrame)
        self.LastMsgFrame.pack(side = LEFT, padx = 10)

        # Creating labels for records and last message
        self.RecordsTitleLabel = Label(self.RecordsFrame,text="Records", pady=10)
        self.RecordsTitleLabel.pack()

        self.LastMsgTitleLabel = Label(self.LastMsgFrame,text="Last Message Receives",pady=10)
        self.LastMsgTitleLabel.pack()

        #Creating text display with scrollbar for incoming record messages and last message
        self.RecordsTextBox = Text(self.RecordsFrame, width=35, height=20)
        self.RecordsScrollBar = Scrollbar(self.RecordsFrame)
        self.RecordsScrollBar.config(command=self.RecordsTextBox.yview)
        self.RecordsScrollBar.pack(side=RIGHT, fill=Y)
        self.RecordsTextBox.config(yscrollcommand=self.RecordsScrollBar.set)
        self.RecordsTextBox.pack()

        self.LastMsgTextBox = Text(self.LastMsgFrame, width=35, height=20)
        self.LastMsgScrollBar = Scrollbar(self.LastMsgFrame)
        self.LastMsgScrollBar.config(command=self.LastMsgTextBox.yview)
        self.LastMsgScrollBar.pack(side=RIGHT, fill=Y)
        self.LastMsgTextBox.config(yscrollcommand=self.LastMsgScrollBar.set)
        self.LastMsgTextBox.pack()

        #Creating topics checkboxes to subscribe and unsubscribe
        self.checkBoxFrame = Frame(self.master) 
        self.checkBoxFrame.pack(pady=15)

        self.addCheckBoxes(getTopics())
        
        #Creating topics subscribe button 
        self.SubscribeButton = Button(self.master,text="Subscribe", command=lambda: self.button_subscribe())
        self.SubscribeButton.pack(pady=5)

        # for i in range(35):
        #     self.updateRecordTextBox()
        #     self.updateLastMsgTextBox()
        
    def button_subscribe(self):
        sub_topics = []
        unsub_topics = []

        for checkbox in self.TopicCheckBoxes:
            topic = checkbox.cget("text")
            checkboxValue= self.checkBoxVar.get(topic).get()
            if (checkboxValue == 1):
                sub_topics.append(topic)
            elif(checkboxValue == 0):
                unsub_topics.append(topic)
 
        self.butActLabel = Label(self.master, text="Subscribing to " + ' and '.join(map(str, sub_topics)))
        self.butActLabel.after(2000, self.butActLabel.destroy)
        self.butActLabel.pack()

        self.butActLabel2 = Label(self.master, text="Unsubscribing to " + ' and '.join(map(str, unsub_topics)))
        self.butActLabel2.after(2000, self.butActLabel2.destroy)
        self.butActLabel2.pack()

        #Subscribe and Unsubscribe
        unsubscribe()
        subscribe(sub_topics)


    def updateTextBoxes(self, text):
        self.updateRecordTextBox(text)
        self.updateLastMsgTextBox(text)
    
    def updateRecordTextBox(self, text):
        self.RecordsTextBox.insert(END, text)
        self.RecordsTextBox.pack()

    def updateLastMsgTextBox(self, text):
        self.LastMsgTextBox.delete("1.0",END)
        self.LastMsgTextBox.insert(END, text)
        self.LastMsgTextBox.pack()

    def addCheckBoxes(self, topics):
        for topic in topics:
            self.checkBoxVar[topic] = IntVar()
            TopicCheckBox = Checkbutton(self.checkBoxFrame, text=topic, variable=self.checkBoxVar[topic])
            TopicCheckBox.pack(side = LEFT, padx=5)
            self.TopicCheckBoxes.append(TopicCheckBox)
        
def subscribe(topics):
    # Subscribe to topic
    consumer.subscribe(topics)

def unsubscribe():
    #Unsubscribe to topics
    consumer.unsubscribe()

def getTopics():
    topics = ["SensorA","SensorB","SensorC"]
    return topics

if __name__ == '__main__':

    # Read configurations and initialize
    conf = kafka_lib.read_config('kafka.config')

    # Create Consumer instance
    consumer = Consumer(conf)

    #Initialize GUI
    guiFrame = GUIFramework()
    

    # Process messages
    try:
        while True:
            #guiFrame.mainloop()
            guiFrame.update()
            msg = consumer.consume()
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = msg.key()
                record_value = msg.value()
                
                key = json.loads(record_key)
                data = json.loads(record_value)
                print("Consumed record with key {} and value {}"
                    .format(key, data))
                strdata = ""
                for subkey in data:
                    value = data.get(subkey)
                    strdata = strdata + "\n" + str(subkey) + ": " + str(value)
                guiFrame.updateTextBoxes(strdata)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()           
