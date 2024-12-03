from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . serializers import IoTDeviceSerializer, DeviceDataSerializer
from . models import IoTDevice, DeviceData
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class IoTDeviceViews(viewsets.ModelViewSet):
    queryset = IoTDevice.objects.all()
    serializer_class = IoTDeviceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['POST'])
    def create(self, request):
        # Validate device token
        token = request.data.get('auth_token')
        try:
            device = IoTDevice.objects.get(auth_token=token)
        except IoTDevice.DoesNotExist:
            return Response(
                {"error": "Invalid device authentication"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    def log_data(self, request, pk=None):
        """
        Custom action to log data for a specific device
        """
        device = self.get_object()
        serializer = DeviceDataSerializer(data={    
            'device': device.id,
            **request.data
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'])
    def latest_data(self, request, pk=None):
        """
        Retrieve the latest data for a specific device
        """
        device = self.get_object()
        latest_data = DeviceData.objects.filter(device=device).order_by('-timestamp').first()
        
        if latest_data:
            serializer = DeviceDataSerializer(latest_data)
            return Response(serializer.data)
        return Response({"detail": "No data available"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['GET'])
    def active_devices(self, request):
        """
        List all active devices
        """
        # Assuming 'active' is a field in your IoTDevice model
        active_devices = self.queryset.filter(status='active')
        serializer = self.get_serializer(active_devices, many=True)
        return Response(serializer.data)

class IoTDeviceView(APIView):
    permission_classes = [AllowAny]  # Allow any device to interact
    
    def get(self, request):
        """
        Retrieve all devices with basic information
        """
        devices = IoTDevice.objects.all()
        serializer = IoTDeviceSerializer(devices, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new IoT device
        """
        serializer = IoTDeviceSerializer(data=request.data)
        if serializer.is_valid():
            # Additional validation can be added here
            device = serializer.save()
            return Response({
                'message': 'Device registered successfully',
                'device_id': device.id,
                'details': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        # Provide more detailed error response
        return Response({
            'message': 'Device registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DeviceDataListView(generics.ListCreateAPIView):
    """
    List and create device data logs
    """
    queryset = DeviceData.objects.all()
    serializer_class = DeviceDataSerializer
    
    def get_queryset(self):
        """
        Optionally filter data logs by device
        """
        device_id = self.request.query_params.get('device_id', None)
        if device_id:
            return DeviceData.objects.filter(device_id=device_id)
        return DeviceData.objects.all()
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with additional validation
        """
        try:
            # Ensure the device exists
            device_id = request.data.get('device')
            get_object_or_404(IoTDevice, id=device_id)
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            return Response({
                'message': 'Data logged successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'message': 'Failed to log data',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)