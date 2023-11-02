.data
	arrA:   .word 1,1,1,1,1,2,2,2,2,2,3,3,3,3,3
	arrx:   .word 1,2,3,4,5
	result: .space 12   # 3 워드 크기의 공간 할당
	line :  .asciiz "\n"
.text

.globl main
main:
    la $s0, arrA
    la $s1, arrx
    la $s2, result    

    li $t0, 3    # A 행렬의 행
    li $t1, 5    # x 행렬의 행
    li $t2, 0    # counter i

outer_loop:
    bge $t2, $t0, print_result	# i >= A 행렬의 행 -> 결과 출력

    li $t3, 0	# j 초기화
    li $t4, 0	# 내적 임시 저장 초기화

inner_loop:
    bge $t3, $t1, inner_done  # j >= x 행렬의 행 -> 내적 끝

    # 주소 계산
    mul $t5, $t2, $t1	# A 행렬의 주소 계산
    add $t5, $t5, $t3	#base address + (row index * col zise + col index) * data size	
    sll $t5, $t5, 2

    mul $t6, $t3, 1	# x 행렬의 주소 계산
    sll $t6, $t6, 2	# col index는 항상 0이라서 생량   

    lw $t7, arrA($t5)	# A 행렬의 값 로드
    lw $t8, arrx($t6)	# x 행렬의 값 로드

    mul $t9, $t7, $t8	# 값 곱셈
    add $t4, $t4, $t9	# 임시 저장 값에 덧셈

    addi $t3, $t3, 1	# j 증가
    j inner_loop

inner_done:
    sw $t4, ($s2)	# 결과 행렬에 저장
    addi $s2, $s2, 4	# 결과 행렬의 다음 주소로 이동
    addi $t2, $t2, 1	# i 증가
    j outer_loop

print_result:
    la $s2, result  # 결과 행렬의 주소를 $s2에 설정
    li $t0, 0  # 반복자 초기화

print_loop:
    beq $t0, 3, exit  # 반복자가 3이면 종료

    li $v0, 1
    lw $a0, ($s2)  # 결과 행렬의 원소 로드
    syscall

    li $v0, 4
    la $a0, line  # 줄바꿈 문자열 출력
    syscall

    addi $s2, $s2, 4  # 결과 행렬의 다음 원소로 이동
    addi $t0, $t0, 1  # 반복자 증가
    j print_loop

exit:
    li $v0, 10
    syscall
