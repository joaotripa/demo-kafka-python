#!/usr/bin/env python
# =============================================================================
#
# Sensor Class
#
# =============================================================================

class Sensor(object):

    """
    Sensor record

    Args:
        SensorID (str): Sensor ID

        SensorDescription (str): Sensor description

        SensorValue (str): Sensor value 

    """
    def __init__(self, sensorID,sensorDesc,sensorValue):
        self.SensorID = sensorID
        self.SensorDescription = sensorDesc
        self.SensorValue = sensorValue

    def toDict(self):
        """
        Returns a dict representation of a Sensor instance for serialization.

        Args:
            Sensor (Sensor): Sensor instance.

        Returns:
            dict: Dict populated with Sensor attributes to be serialized.

        """
        return dict(SensorID=self.SensorID,
                    SensorDescription=self.SensorDescription,
                    SensorSpecs=self.SensorValue)



