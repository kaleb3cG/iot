from rest_framework import serializers
from . models import IoTDevice, DeviceData

class DeviceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceData
        fields = '__all__'

class IoTDeviceSerializer(serializers.ModelSerializer):
    data_logs = DeviceDataSerializer(many=True, read_only=True)
    class Meta:
        model = IoTDevice
       fields = '__all__'