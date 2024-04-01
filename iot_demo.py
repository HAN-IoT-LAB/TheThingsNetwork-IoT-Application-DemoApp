from BigBangProcessor import SensorDataProcessor
import os

processor = SensorDataProcessor(os.environ["DEVICE_APP"], os.environ["API_KEY"] )
data_list = processor.get_ttn_devices(limit=10) # Only show the last 10 payload samples.

processor.plot_data(data_list)