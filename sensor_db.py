import time
import queue
import threading


class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()


    def acquire_read(self):
        with self.read_lock:
            self.readers+=1
            if(self.readers == 1):
                self.write_lock.acquire()
            
            # TODO: implement read lock acquire with threading.Lock.acquire() write가 안잠겨있으면 열어주기
        

    def release_read(self):
        with self.read_lock:
            self.readers-=1
            if(self.readers == 0):
                self.write_lock.release()
            # TODO: implement read lock release with threading.Lock.release() readlock 해제


    def acquire_write(self):
        self.write_lock.acquire()
        # TODO: implement write lock acquire with threading.Lock.acquire()  read,write 둘다 안잠겨있으면 열어주기
        

    def release_write(self):
        self.write_lock.release()
        # TODO: implement write lock release with threading.Lock.release()  writelock 해제
        


class SensorDB(object):

    sensor_data_db = {}
    global_lock = ReadWriteLock()
    read_write_lock_table = {}
    #센서 유형별로 table에 저장

    def __init__(self) -> None:
        super().__init__()
        self.curr_reader_num = 0
        self.curr_writer_num = 0

    
    def write_data_to_db(self, t_sensor_type, t_sensor_data_amount, t_sensor_value):
        t_update_time = t_sensor_data_amount * 0.01
        self.global_lock.acquire_write()
        self.sensor_data_db[t_sensor_type] = t_sensor_value
        self.global_lock.release_write()
        time.sleep(t_update_time)
        return 1
    
            
    def read_data_from_db(self, t_sensor_types):
        return_dict = {}

        for elem in t_sensor_types:
            return_dict[elem] = self.sensor_data_db[elem]

        return return_dict
    
    
    def process_write_request(self, t_sensor_type, t_sensor_data_amount, t_sensor_value):
        result = []

        #write lock을 얻기위해 대기
        s_waittime = time.time()
        if t_sensor_type not in self.read_write_lock_table:
            self.read_write_lock_table[t_sensor_type] = ReadWriteLock()
        lock = self.read_write_lock_table[t_sensor_type]
        lock.acquire_write()
        e_waittime =  time.time()

        #write
        s_writetime = time.time()
        result.append(self.write_data_to_db(t_sensor_type, t_sensor_data_amount, t_sensor_value))
        e_writetime = time.time()


        #end
        lock.release_write()
        result.append(e_writetime-s_writetime)
        result.append(e_waittime-s_waittime)
        return result
        # TODO: Implement writer lock acquire, release, and timestamps (t_start_wait_time, t_start_write_time, t_end_write_time)
    


    def process_read_request(self, t_sensor_types):
        result = {}

        #read lock을 얻기위해 대기
        s_waittime = time.time()  
        locks = []
        for t_sensor_type in t_sensor_types:
            if t_sensor_type not in self.read_write_lock_table:
                self.read_write_lock_table[t_sensor_type] = ReadWriteLock()  
            lock = self.read_write_lock_table[t_sensor_type]
            locks.append(lock)
            lock.acquire_read()  
        e_waittime = time.time()  

        #read
        s_readtime = time.time()  
        try:
            result.update(self.read_data_from_db(t_sensor_types))  
        except KeyError as e:
            result[str(e)] = None  
        e_readtime = time.time()  

        #end
        for lock in locks:
            lock.release_read()  

        return [result, e_readtime - s_readtime, e_waittime - s_waittime]
    
        # TODO: Implement read lock acquire, release, and timestamps (t_start_wait_time, t_start_write_time, t_end_write_time)
    
    

    def print_db_contents(self):
        print(self.sensor_data_db)
    

    def get_db_contents(self):
        return(self.sensor_data_db)
