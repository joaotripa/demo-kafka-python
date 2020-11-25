#!/usr/bin/env python
# =============================================================================
#
# JSON Sensor Encoder Module
#
# =============================================================================
from json import JSONEncoder

## Serialize a Sensor Class to JSON           
class SensorEncoder(JSONEncoder):
        def default(self, o):
            """
            Returns a dict representation of a Sensor instance for serialization.

            Args:
                Sensor (Sensor): Sensor instance.

            Returns:
                dict: Dict populated with Sensor attributes to be serialized.

            """
            return dict(SensorID=o.SensorID,
                        SensorDescription=o.SensorDescription,
                        SensorValue=o.SensorValue)