import analyzer
import time
import sensor
import sensor_db
import random


# test code
if __name__ == "__main__":
    run_time = 60
    
    sensor_list = []
    sensor_type_list = [
        "default",
        "accelerometer",
        "gyroscope",
        "magnetometer",
        "barometer"
    ]

    analyzer_list = []
    analyzer_data_type_list = [
        "default",
        "accelerometer",
        "gyroscope",
        "magnetometer",
        "barometer",
        ["accelerometer", "gyroscope", "magnetometer"]
    ]

    t_sensor_db = sensor_db.SensorDB()

    for i in range(0, len(sensor_type_list)):
        sensor_list.append(sensor.Sensor(i, sensor_type_list[i], t_sensor_db, 50, 1))
    
    for i in range(0, len(sensor_type_list)):
        t_sensor_thread = sensor_list[i]
        print("Sensor #{0:02d} start".format(sensor_list[i].sensor_id))
        t_sensor_thread.start()
    
    time.sleep(1)

    for j in range(0, len(analyzer_data_type_list)):
        analyzer_list.append(analyzer.Analyzer(j, analyzer_data_type_list[j], t_sensor_db, 1))
    
    for j in range(0, len(analyzer_data_type_list)):
        t_analyzer_thread = analyzer_list[j]
        print("Analyzer #{0:02d} start".format(analyzer_list[j].analyzer_id))
        t_analyzer_thread.start()

    for k in range(0, run_time):
        print("Current time: {0}".format(k))
        time.sleep(1)

    for i in range(0, len(sensor_type_list)):
        sensor_list[i].stop()
        print("Sensor #{0:02d} stopped".format(sensor_list[i].sensor_id))
        
    for j in range(0, len(analyzer_data_type_list)):
        analyzer_list[j].stop()
        print("Analyzer #{0:02d} stopped".format(analyzer_list[j].analyzer_id))

    for i in range(0, len(sensor_type_list)):
        while sensor_list[i].sensor_status != 0:
            time.sleep(0.01)
        sensor_list[i].log_fd.close()

    for j in range(0, len(analyzer_data_type_list)):
        while analyzer_list[j].analyzer_status != 0:
            time.sleep(0.01)
        analyzer_list[j].log_fd.close()
