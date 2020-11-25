#!/usr/bin/env python
# =============================================================================
#
# Produce messages to Kafka
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================

from producer_lib import ProducerEntity as Producer
from sensor import Sensor
from uuid import uuid4
from sensorencoder import SensorEncoder

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
        self.master.title("Demo Kafka Python Publisher")

        """Defining Data Variables"""
        self.SensorA = []
        self.SensorB = []
        self.SensorC = []
        self.SensorAData = StringVar()
        self.SensorBData = StringVar()
        self.SensorCData = StringVar()
        self.randomize("SensorA")
        self.randomize("SensorB")
        self.randomize("SensorC")
        
        """Display the main window"""
        self.titleLabel = Label(self.master, text="Publisher GUI", pady=15)
        self.titleLabel.pack()
        self.CreateWidgets()
        
    def CreateWidgets(self):
        """Create all the widgets that we need"""
                
        self.dataFrame = Frame(self.master) 
        self.dataFrame.pack()

        #Creating a frame for each sensor
        self.SensorAFrame = Frame(self.dataFrame)
        self.SensorAFrame.pack(side = LEFT, padx = 10)

        self.SensorBFrame = Frame(self.dataFrame)
        self.SensorBFrame.pack(side = LEFT, padx = 10)

        self.SensorCFrame = Frame(self.dataFrame)
        self.SensorCFrame.pack(side = LEFT, padx = 10)

        # Creating labels to display each sensor data
        self.SensorATitleLabel = Label(self.SensorAFrame,text="Sensor A Data", pady=10)
        self.SensorATitleLabel.pack()

        self.SensorBTitleLabel = Label(self.SensorBFrame,text="Sensor B Data",pady=10)
        self.SensorBTitleLabel.pack()

        self.SensorCTitleLabel = Label(self.SensorCFrame,text="Sensor C Data",pady=10)
        self.SensorCTitleLabel.pack()

        # Creating labels to display each sensor data
        self.SensorALabel = Label(self.SensorAFrame,textvariable=self.SensorAData, pady=5)
        self.SensorALabel.pack()

        self.SensorBLabel = Label(self.SensorBFrame,textvariable=self.SensorBData, pady=5)
        self.SensorBLabel.pack()

        self.SensorCLabel = Label(self.SensorCFrame,textvariable=self.SensorCData, pady=5)
        self.SensorCLabel.pack()

        # Creating randomize buttons to randomize data to publish
        self.RandomizeAButton = Button(self.SensorAFrame,text="Randomize", command=lambda: self.randomize('SensorA'))
        self.RandomizeAButton.pack()

        self.RandomizeBButton = Button(self.SensorBFrame,text="Randomize", command=lambda: self.randomize('SensorB'))
        self.RandomizeBButton.pack()

        self.RandomizeCButton = Button(self.SensorCFrame,text="Randomize", command=lambda: self.randomize('SensorC'))
        self.RandomizeCButton.pack()

        #Creating publish buttons for each sensor
        self.PublishAButton = Button(self.SensorAFrame,text="Publish", command=lambda: self.button_click('SensorA', self.SensorA))
        self.PublishAButton.pack()

        self.PublishBButton = Button(self.SensorBFrame,text="Publish", command=lambda: self.button_click('SensorB', self.SensorB))
        self.PublishBButton.pack()

        self.PublishCButton = Button(self.SensorCFrame,text="Publish", command=lambda: self.button_click('SensorC', self.SensorC))
        self.PublishCButton.pack()
        
    def randomize(self, sensor):
        if (sensor == "SensorA"):
            sensorAID = "sensor_"+str(uuid4())
            sensorADesc = "Sensor Type A"
            sensorAValue = str(random.randint(0,100)) + "ºC"
            self.SensorAData.set("ID: " + sensorAID + "\nDescription: " + sensorADesc 
                + "\nValue: " + sensorAValue)
            self.SensorA = Sensor(sensorID=sensorAID,sensorDesc=sensorADesc,sensorValue=sensorAValue)
        if (sensor == "SensorB"):
            sensorBID = "sensor_"+str(uuid4())
            sensorBDesc = "Sensor Type B"
            sensorBValue = str(random.randint(0,100)) + "ºC"
            self.SensorBData.set("ID: " + sensorBID + "\nDescription: " + sensorBDesc 
                + "\nValue: " + sensorBValue)
            self.SensorB = Sensor(sensorID=sensorBID,sensorDesc=sensorBDesc,sensorValue=sensorBValue)
        if (sensor == "SensorC"):
            sensorCID = "sensor_"+str(uuid4())
            sensorCDesc = "Sensor Type C"
            sensorCValue = str(random.randint(0,100)) + "ºC"
            self.SensorCData.set("ID: " + sensorCID + "\nDescription: " + sensorCDesc 
                + "\nValue: " + sensorCValue)
            self.SensorC = Sensor(sensorID=sensorCID,sensorDesc=sensorCDesc,sensorValue=sensorCValue)

    def button_click(self, sensor, data):
            self.butActLabel = Label(self.master, text="Successfully published data from " + sensor)
            self.butActLabel.after(2000, self.butActLabel.destroy)
            self.butActLabel.pack()

            #Publish
            publish(sensor,str(uuid4()),data, SensorEncoder)


#Producing Sample Messages
def publish(topic, key, sensor, encoder):
    producer.produce(topic, str(uuid4()), sensor, encoder)
    producer.flush()


def getTopics(conf):
    topics = ["SensorA","SensorB","SensorC"]
    # Create topic if needed
    for topic in topics:
        kafka_lib.create_topic(conf, topic)
    return topics


if __name__ == "__main__":
    conf = kafka_lib.read_config('kafka.config')
    # Create Producer instance
    producer = Producer(conf)

    getTopics(conf)

    guiFrame = GUIFramework()
    guiFrame.mainloop()
   
