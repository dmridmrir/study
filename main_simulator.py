import random
import page_manager

PAGE_LIST_LENGTH = 100
FRAME_SIZE = 8
PAGE_SIZE = 16

# Generate page schedule
def generate_page_schedule(_length, _page_range=[0, 16]):
    t_page_list = [0] * _length

    for i in range(0, _length):
        t_rand_val = random.randint(_page_range[0], _page_range[1])
        t_page_list[i] = t_rand_val
    
    return t_page_list

if __name__ == "__main__":
    page_list_length = PAGE_LIST_LENGTH
    page_frame_size = FRAME_SIZE
    logical_page_size = PAGE_SIZE

    given_page_reference_list = generate_page_schedule(page_list_length, [0, logical_page_size])

    sim_page_manager = page_manager.PageManager(page_frame_size)

    page_fault_count = 0

    print("==================================================")
    print("Generated page reference list:")
    print("--------------------------------------------------")
    print(given_page_reference_list)

    input()

    print("Ref # | Page # |   PF | Frame # | Page (f->t) | Page Frames")
    print("=========================================================================")

    for i in range(0, page_list_length):
        tmp_page_frame = sim_page_manager.get_curr_page_frame().copy()
        # tmp_page_frame = sim_page_manager.get_curr_page_frame()

        is_page_fault, replaced_frame_num = sim_page_manager.reference_page(given_page_reference_list[i])

        curr_page_frame = sim_page_manager.get_curr_page_frame()
        curr_page_frame_info = sim_page_manager.get_curr_page_frame_info()

        if is_page_fault:
            page_fault_count += 1
            print("{0:5d} | {5:6d} |  YES | {2:7d} |  {3:3d} -> {4:3d} | {6}".format(i, is_page_fault, replaced_frame_num, tmp_page_frame[replaced_frame_num], curr_page_frame[replaced_frame_num], given_page_reference_list[i], curr_page_frame))
        else:
            print("{0:5d} | {4:6d} |   NO | {2} |  {3:3d}        | {5}".format(i, is_page_fault, "       ", tmp_page_frame[replaced_frame_num], given_page_reference_list[i], curr_page_frame))



        # print(is_page_fault, given_page_reference_list[i], replaced_frame_num)
        # print(curr_page_frame)
        # print(curr_page_frame_info)
        
    print("Total page fault count:", page_fault_count)
        
