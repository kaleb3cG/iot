from django.urls import path, include
from rest_framework import DefaultRouters
from . views import IoTDeviceViews, IoTDeviceView, DeviceDataListView

router = DefaultRouter()
router.register(r'devices', IoTDeviceViews)

urlpatterns = [
    path('', include(router.urls))
    path('device-list/', IoTDeviceView.as_view(), name='device-list'),
    path('device-data/', DeviceDataListView.as_view(), name='device-data'),
]