.data
    msg1: .asciiz "enter n (n<=10)"
    msg2: .asciiz "enter r (r<=10)"
    msg3: .asciiz "result : "
    N:    .word 0
    R:    .word 0
    NR:   .word 0
    result: .word 0

.text
.globl main

main:
    li $v0, 4
    la $a0, msg1
    syscall

    li $v0, 5
    syscall
    sw $v0, N

    li $v0, 4
    la $a0, msg2
    syscall

    li $v0, 5
    syscall
    sw $v0, R

    # combination ȣ��
    lw $a0, N
    lw $a1, R
    sub $a2,$a0,$a1	#n-r
    jal combination
    sw $v0, result	#����� ���� (combination�� ���ϰ�

    # ��� ���
    li $v0, 4
    la $a0, msg3
    syscall

    li $v0, 1
    lw $a0, result
    syscall

    # ���α׷� ����
    li $v0, 10
    syscall

# combination
.globl combination

combination:
#���÷�������(���� ����)�� 1���� ����Ҳ��� ������ $s0�ϳ��� ����
#4����Ʈ ũ�⸦ ���� ������ ���̽� �ּҿ� ���ؼ� �� 8 ����Ʈ�� ����
#������ �Ʒ��� ���ϱ� ������ ���̳ʽ� �ؾ���
    subu $sp, $sp, 8
    sw $ra, ($sp)
    sw $s0, 4($sp)

    move $s0, $a0  # n�� s0�� ����

    # n�� 0�̸� ����� 1
    beqz $s0, fact_done
    li $v0, 1
    move $t0, $s0  # t0�� n ����

    factorial_loop_n:
    #n factorial ���
    #n���� 1�� ���̸鼭 v0�������Ϳ� ����
        beqz $t0, factorial_loop_r_done
        mul $v0, $v0, $t0
        subi $t0, $t0, 1
        j factorial_loop_n

    factorial_loop_r_done:
    move $s0, $a1  # r�� s0�� ����

    # r�� 0�̸� ����� 1
    beqz $s0, fact_done
    li $v1, 1
    move $t0, $s0  # t0�� r ����

    factorial_loop_r:
    #r���� 1�� ���̸� v1�������Ϳ� ����
        beqz $t0, factorial_loop_nr_done
        mul $v1, $v1, $t0
        subi $t0, $t0, 1
        j factorial_loop_r

    factorial_loop_nr_done:
    move $s0, $a2  # n-r�� s0�� ����

    # (n-r)�� 0�̸� ����� 1
    #v1�������͸� �״�� ���� �����̱� ������ �ʱ�ȭ ����
    beqz $s0, fact_done
    move $t0, $s0  # t0�� (n-r) ����

    factorial_loop_nr:
    #n-r�� 1�� ���̸� v1�� ����
        beq $t0, $zero, fact_done
        mul $v1, $v1, $t0
        subi $t0, $t0, 1
        j factorial_loop_nr

    fact_done:
    #�� ��� 
    # n! / (r! * (n-r)!)
    #���� v0�� ���� -> ������ �Լ� ���ϰ��� v0�������ͷ� �����س��� ���� v0�� �Ҵ��ؾߵ�
    div $v0,$v1
    mflo $v0
    
    #���������͸� �ǵ��� ��
    #�ٽ� �������ͷ� �̵�
    lw $ra, ($sp)
    lw $s0, 4($sp)
    addu $sp, $sp, 8

    jr $ra
