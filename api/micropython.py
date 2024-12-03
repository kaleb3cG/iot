import machine
import urequests
import ujson
import utime

class ESP32IoTClient:
    def _init_(self, base_url, device_token):
        self.base_url = base_url
        self.device_token = device_token
        self.headers = {
            'Content-Type':'application/json',
            'Authorization':f'Token {self.device_token}'
        }

    def send_sensor_data(self, sensor_data):
        try:
            # Implement exponential backoff for retries
            max_retries = 3
            for attempt in range(max_retries)
            try:
                response = urequests.post(
                    f"{self.base_url}/api/devices/log_data/",
                    headers=self.headers,
                    json=sensor_data
                )

                if response.status_code == 200:
                    return True
                # Exponential backoff
                utime.sleep(2** attempt)

                


