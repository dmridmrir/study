import os
import random
import threading
import time
import platform
import sensor
import sensor_db

IS_DEBUG = True

class Analyzer(threading.Thread):
    analyzer_id = -1
    analyzer_data_types = ["default"]
    analysis_type = None
    is_sensor_active = 0
    analyzer_status = 0
    sensor_db = None
    update_rate = 1         # 1Hz
    analyzer_data = None
    analyzer_data_count = 0
    log_fd = None

    def __init__(self, t_analyzer_id, t_analyzer_data_types, t_sensor_db, t_update_rate=None) -> None:
        super().__init__()

        self.analyzer_id = t_analyzer_id
        self.analyzer_data_types = t_analyzer_data_types
        self.analysis_type = "default"
        self.analyzer_status = 0
        self.sensor_db = t_sensor_db
        if t_update_rate is not None:
            self.update_rate = t_update_rate
        
        if not os.path.exists("./logs"):
            os.makedirs("./logs")

        self.log_fd = open("./logs/analyzer{0:02d}.txt".format(self.analyzer_id), "w")

    
    def get_sensor_id(self):
        return self.analyzer_id


    def get_sensor_status(self):
        return self.analyzer_status
    

    def write_to_log(self, write_string):
        if not self.log_fd.closed:
            self.log_fd.write(write_string)


    def do_analysis(self):
        self.analyzer_status = 1
        self.analyzer_data_count += 1
        
        self.write_to_log("{2} - Analyzer #{0:02d} | {3}: read sensor data #{1} from db.\n".format(self.analyzer_id, self.analyzer_data_count, platform.node(), time.time()))     
        
        [read_data, read_time, wait_time] = self.read_data_from_db(self.sensor_db)
        if self.analysis_type == "default":
            analyzed_data = read_data
            
        self.write_to_log("{3} - Analyzer #{0:02d} | {4}: finished read and analysis. (read time: {1:0.3f} sec / wait time: {2:0.3f} sec)\n".format(self.analyzer_id, read_time, wait_time, platform.node(), time.time()))
        self.analyzer_status = 0

        return analyzed_data, read_time, wait_time
    

    def read_data_from_db(self, t_sensor_db):
        [read_data, read_time, wait_time] = t_sensor_db.process_read_request(self.analyzer_data_types)
        return [read_data, read_time, wait_time]
    

    def run(self):
        self.is_sensor_active = 1
        while self.is_sensor_active == 1:
            t_start_time = time.time()
            self.analyzer_status = 2

            [req_status, read_time, wait_time] = self.do_analysis()

            self.analyzer_status = 0
            
            t_wait_time = 1 - (time.time() - t_start_time)
            if t_wait_time > 0:
                time.sleep(t_wait_time)
        return

    def stop(self):
        print("Terminate analyzer #{0:02d}".format(self.analyzer_id))
        self.is_sensor_active = 0
        pass
