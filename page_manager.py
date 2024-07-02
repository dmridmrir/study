class PageManager(object):

    ref_counter = 0
    page_frame = None
    page_frame_info = None
    page_replacement_algorithm = "FIFO"
    # FIFO, LRU, SC(Second Chance)

    def __init__(self, _page_frame_size, _page_replacement_algorithm="FIFO"):
        self.ref_counter = 0
        self.page_frame = [-1] * _page_frame_size
        self.page_frame_info = [0] * _page_frame_size
        self.page_replacement_algorithm = _page_replacement_algorithm

    def get_curr_page_frame(self):
        return self.page_frame

    def get_curr_page_frame_info(self):
        return self.page_frame_info

    def reference_page(self, _given_page_num):
        is_page_fault = True
        is_page_frame_available = False
        referenced_frame_number = -1

        # 1. check page exists
        for i in range(0, len(self.page_frame)):
            if self.page_frame[i] == _given_page_num:
                referenced_frame_number = i
                
                # i) update frame reference information
                if self.page_replacement_algorithm == "LRU":
                    self.page_frame_info[referenced_frame_number] = self.ref_counter
                elif self.page_replacement_algorithm == "SC":
                    self.page_frame_info[referenced_frame_number] = 1

                is_page_fault = False
                break

        # 2. if page fault occurs, insert or replace page
        if referenced_frame_number == -1:

            # i) check available page exists in the page frame
            for i in range(0, len(self.page_frame_info)):
                if self.page_frame_info[i] == -1:
                    is_page_frame_available = True
                    self.page_frame_info[i] = _given_page_num
                    
                    break
            # ii) if page frame is not available, replace page
            if not is_page_frame_available:
                referenced_frame_number = self.replace_page(_given_page_num)

        # 3. update timestamp (=ref_counter)
        self.ref_counter += 1

        return [is_page_fault, referenced_frame_number]


    def replace_page(self, _given_page_num):
        replaced_frame_number = -1

        if self.page_replacement_algorithm == "FIFO":
            replaced_frame_number = self.replace_page_with_FIFO(_given_page_num)
        elif self.page_replacement_algorithm == "LRU":
            replaced_frame_number = self.replace_page_with_LRU(_given_page_num)
        elif self.page_replacement_algorithm == "SC":
            replaced_frame_number = self.replace_page_with_second_chance(_given_page_num)
        
        return replaced_frame_number


    def replace_page_with_FIFO(self, _given_page_num):
        replaced_frame_number = -1

        # Implement page replacement algorithm with FIFO
        # page frame info에서 가장 작은 값 찾아와서 바꾸기
        min_page_time = min(self.page_frame_info)
        replaced_frame_number = self.page_frame_info.index(min_page_time)

        self.page_frame[replaced_frame_number] = _given_page_num
        self.page_frame_info[replaced_frame_number] = self.ref_counter


        return replaced_frame_number


    def replace_page_with_LRU(self, _given_page_num):
        replaced_frame_number = -1

        # Implement page replacement algorithm with LRU
        # 이것도 page frame info에서 가장 작은 값 찾아와서 바꾸기?
        min_page_time = min(self.page_frame_info)
        replaced_frame_number = self.page_frame_info.index(min_page_time)

        self.page_frame[replaced_frame_number] = _given_page_num
        self.page_frame_info[replaced_frame_number] = self.ref_counter

        return replaced_frame_number


    def replace_page_with_second_chance(self, _given_page_num):
        replaced_frame_number = -1

        # Implement page replacement algorithm with second chance
        # 초기값은 1로 세팅되어있고 순회하면서 0을 찾으면 됨
        # 1을 찾으면 0으로 바꾸면서 순회
        i=0

        while True:
            if self.page_frame_info[i] == 0:
                self.page_frame[i] = _given_page_num
                self.page_frame_info[i] = self.ref_counter
                break
            else:
                self.page_frame_info[i] = 0

            i = (i+1) % len(self.page_frame)    

        return replaced_frame_number