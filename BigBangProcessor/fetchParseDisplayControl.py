import requests
import json
import base64
import struct
import matplotlib.pyplot as plt
import pandas as pd

class SensorDataProcessor:
    def __init__(self, application_id, api_key):
        self.application_id = application_id
        self.api_key = api_key
        
        self.SensorTypes = {
            'DIG_IN': {'type': 0, 'precision': 1, 'signed': False, 'bytes': 1},
            'DIG_OUT': {'type': 1, 'precision': 1, 'signed': False, 'bytes': 1},
            'ANL_IN': {'type': 2, 'precision': 100, 'signed': True, 'bytes': 2},
            'ANL_OUT': {'type': 3, 'precision': 100, 'signed': True, 'bytes': 2},
            'ILLUM_SENS': {'type': 101, 'precision': 1, 'signed': False, 'bytes': 2},
            'PRSNC_SENS': {'type': 102, 'precision': 1, 'signed': False, 'bytes': 1},
            'TEMP_SENS': {'type': 103, 'precision': 10, 'signed': True, 'bytes': 2},
            'HUM_SENS': {'type': 104, 'precision': 10, 'signed': False, 'bytes': 2},
            'ACCRM_SENS': {'type': 113, 'precision': 1000, 'signed': True, 'bytes': 6},
            'BARO_SENS': {'type': 115, 'precision': 10, 'signed': False, 'bytes': 2},
            'GYRO_SENS': {'type': 134, 'precision': 100, 'signed': True, 'bytes': 6},
            'GPS_LOC': {'type': 136, 'precision': 10000, 'signed': True, 'bytes': 12},
        }

    def decode_value(self, bytes_payload, index, sensor_type):
        byte_format = "<"  # Use little-endian
        num_bytes = sensor_type['bytes']
        is_signed = sensor_type['signed']
        precision = sensor_type['precision']

        if index + num_bytes > len(bytes_payload):
            print(f"Warning: Insufficient bytes in payload to decode {sensor_type}.")
            return None, index

        if num_bytes == 1:
            byte_format += 'b' if is_signed else 'B'
        elif num_bytes == 2:
            byte_format += 'h' if is_signed else 'H'
        elif num_bytes == 4:
            byte_format += 'i' if is_signed else 'I'
        elif num_bytes == 6:
            x, y, z = struct.unpack_from("<hhh", bytes_payload, index)
            return (x / precision, y / precision, z / precision), index + num_bytes
        else:
            print(f"Unsupported byte size: {num_bytes}")
            return None, index

        value = struct.unpack_from(byte_format, bytes_payload, index)[0]
        scaled_value = value / precision
        return scaled_value, index + num_bytes

    def decode_payload(self, encoded_payload):
        bytes_payload = base64.b64decode(encoded_payload)
        decoded_data = {}
        i = 0
        while i < len(bytes_payload):
            if i + 2 <= len(bytes_payload):
                data_type, channel = bytes_payload[i], bytes_payload[i + 1]
                i += 2
            else:
                print("Warning: Insufficient bytes for DataType and Channel.")
                break

            for sensor_name, sensor_type in self.SensorTypes.items():
                if sensor_type['type'] == data_type:
                    if i < len(bytes_payload):
                        value, new_index = self.decode_value(bytes_payload, i, sensor_type)
                        if value is not None:
                            decoded_data[f"{sensor_name}_CH{channel}"] = value
                            i = new_index
                            break
                    else:
                        print("Warning: Insufficient bytes for data.")
            else:
                print(f"Unknown data type: {data_type} at index {i-2}")
        
        return decoded_data

    def get_ttn_devices(self, limit=50):
        url = f"https://eu1.cloud.thethings.network/api/v3/as/applications/{self.application_id}/packages/storage/uplink_message"
        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
        response_data_list = []

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                raw_data_lines = response.text.splitlines()
                for line in reversed(raw_data_lines):
                    response_data = json.loads(line)
                    if 'frm_payload' in response_data['result']['uplink_message']:
                        encoded_payload = response_data['result']['uplink_message']['frm_payload']
                        decoded_payload_data = self.decode_payload(encoded_payload)
                        response_data_list.append(decoded_payload_data)
                        if len(response_data_list) >= limit:
                            break
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)
        else:
            print(f"Failed to fetch payload. Status code: {response.status_code}")
        
        return response_data_list

    def plot_data(self, data_list):
        df = pd.DataFrame(data_list)
        total_plots = len(df.columns)
        for column in df.columns:
            if isinstance(df[column].iloc[0], tuple):
                total_plots += 2

        plt.figure(figsize=(10, 2 * total_plots))
        current_plot = 1
        for column in df.columns:
            if isinstance(df[column].iloc[0], tuple):
                acc_data = pd.DataFrame(df[column].tolist(), columns=['X', 'Y', 'Z'])
                for axis in ['X', 'Y', 'Z']:
                    plt.subplot(total_plots, 1, current_plot)
                    plt.plot(acc_data[axis], label=f'{column} {axis}-axis')
                    plt.title(f'{column} {axis}-axis')
                    plt.ylabel('Acceleration')
                    plt.legend()
                    current_plot += 1
            else:
                plt.subplot(total_plots, 1, current_plot)
                plt.plot(df[column], label=column)
                plt.title(column)
                plt.legend()
                current_plot += 1

        plt.tight_layout()
        plt.show()