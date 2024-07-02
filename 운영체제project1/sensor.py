import os
import random
import threading
import time
import platform
import sensor_db

IS_DEBUG = True

class Sensor(threading.Thread):
    sensor_id = -1
    sensor_type = "default"
    sensor_status = 0
    is_sensor_active = 0
    update_rate = 1         # 1Hz
    sensor_data_amount = 1
    sensor_data_count = 0
    log_fd = None

    def __init__(self, t_sensor_id, t_sensor_type, t_sensor_db, t_data_amount=None, t_update_rate=None) -> None:
        super().__init__()

        self.sensor_id = t_sensor_id
        self.sensor_type = t_sensor_type
        self.sensor_status = 0
        self.is_sensor_active = 0
        self.sensor_db = t_sensor_db
        if t_data_amount is not None:
            self.sensor_data_amount = t_data_amount
        if t_update_rate is not None:
            self.update_rate = t_update_rate
        
        if not os.path.exists("./logs"):
            os.makedirs("./logs")

        self.log_fd = open("./logs/sensor{0:02d}.txt".format(self.sensor_id), "w")

    
    def get_sensor_id(self):
        return self.sensor_id


    def get_sensor_status(self):
        return self.sensor_status
    

    def write_to_log(self, write_string):
        if not self.log_fd.closed:
            self.log_fd.write(write_string)


    def read_sensor_data(self):
        self.sensor_status = 1
        self.sensor_data_count += 1
        self.write_to_log("{2} - Sensor #{0:02d} | {3}: read sensor data #{1}.\n".format(self.sensor_id, self.sensor_data_count, platform.node(), time.time()))
        t_sensor_data = random.randrange(0,1)
        self.sensor_status = 0
        return t_sensor_data
    

    def update_data_to_db(self, sensor_db):
        [req_status, write_time, wait_time] = sensor_db.process_write_request(self.sensor_type, self.sensor_data_amount, self.read_sensor_data())
        return [req_status, write_time, wait_time]
    

    def run(self):
        self.is_sensor_active = 1
        while self.is_sensor_active == 1:
            t_start_time = time.time()
            self.sensor_status = 2
            
            self.write_to_log("{2} - Sensor #{0:02d} | {3}: write sensor data #{1} to db.\n".format(self.sensor_id, self.sensor_data_count, platform.node(), time.time()))
            [req_status, write_time, wait_time] = self.update_data_to_db(self.sensor_db)
            self.write_to_log("{3} - Sensor #{0:02d} | {4}: finished write. (write time: {1:0.3f} sec / wait time: {2:0.3f} sec)\n".format(self.sensor_id, write_time, wait_time, platform.node(), time.time()))
            self.sensor_status = 0
            
            t_wait_time = 1 - (time.time() - t_start_time)
            if t_wait_time > 0:
                time.sleep(t_wait_time)
                

    def stop(self):
        print("Terminate Sensor #{0:02d}".format(self.sensor_id))
        self.is_sensor_active = 0
        pass

# sensor and sensorDB test code
if __name__ == "__main__":
    run_time = 60

    t_sensor_db = sensor_db.SensorDB()

    num_sensor = 6
    sensor_list = []
    sensor_type_list = ["default", "accelerometer", "gyroscope", "magnetometer"]

    for i in range(0, num_sensor):
        sensor_list.append(Sensor(i, sensor_type_list[i], t_sensor_db, 50, 1))
    
    for i in range(0, num_sensor):
        t_sensor_thread = sensor_list[i]
        print("Sensor #{0:02d} start".format(sensor_list[i].sensor_id))
        t_sensor_thread.start()

    for i in range(0, run_time):
        print("Current time: {0}".format(i))
        time.sleep(1)

    for i in range(0, num_sensor):
        sensor_list[i].stop()
        print("Sensor #{0:02d} stopped".format(sensor_list[i].sensor_id))

    for i in range(0, num_sensor):
        while sensor_list[i].sensor_status != 0:
            time.sleep(0.01)
        sensor_list[i].log_fd.close()
