.data
	arrA:   .word 1,1,1,1,1,2,2,2,2,2,3,3,3,3,3
	arrx:   .word 1,2,3,4,5
	result: .space 12   # 3 ���� ũ���� ���� �Ҵ�
	line :  .asciiz "\n"
.text

.globl main
main:
    la $s0, arrA
    la $s1, arrx
    la $s2, result    

    li $t0, 3    # A ����� ��
    li $t1, 5    # x ����� ��
    li $t2, 0    # counter i

outer_loop:
    bge $t2, $t0, print_result	# i >= A ����� �� -> ��� ���

    li $t3, 0	# j �ʱ�ȭ
    li $t4, 0	# ���� �ӽ� ���� �ʱ�ȭ

inner_loop:
    bge $t3, $t1, inner_done  # j >= x ����� �� -> ���� ��

    # �ּ� ���
    mul $t5, $t2, $t1	# A ����� �ּ� ���
    add $t5, $t5, $t3	#base address + (row index * col zise + col index) * data size	
    sll $t5, $t5, 2

    mul $t6, $t3, 1	# x ����� �ּ� ���
    sll $t6, $t6, 2	# col index�� �׻� 0�̶� ����   

    lw $t7, arrA($t5)	# A ����� �� �ε�
    lw $t8, arrx($t6)	# x ����� �� �ε�

    mul $t9, $t7, $t8	# �� ����
    add $t4, $t4, $t9	# �ӽ� ���� ���� ����

    addi $t3, $t3, 1	# j ����
    j inner_loop

inner_done:
    sw $t4, ($s2)	# ��� ��Ŀ� ����
    addi $s2, $s2, 4	# ��� ����� ���� �ּҷ� �̵�
    addi $t2, $t2, 1	# i ����
    j outer_loop

print_result:
    la $s2, result  # ��� ����� �ּҸ� $s2�� ����
    li $t0, 0  # �ݺ��� �ʱ�ȭ

print_loop:
    beq $t0, 3, exit  # �ݺ��ڰ� 3�̸� ����

    li $v0, 1
    lw $a0, ($s2)  # ��� ����� ���� �ε�
    syscall

    li $v0, 4
    la $a0, line  # �ٹٲ� ���ڿ� ���
    syscall

    addi $s2, $s2, 4  # ��� ����� ���� ���ҷ� �̵�
    addi $t0, $t0, 1  # �ݺ��� ����
    j print_loop

exit:
    li $v0, 10
    syscall
