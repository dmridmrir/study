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

    # combination 호출
    lw $a0, N
    lw $a1, R
    sub $a2,$a0,$a1	#n-r
    jal combination
    sw $v0, result	#결과값 저장 (combination의 리턴값

    # 결과 출력
    li $v0, 4
    la $a0, msg3
    syscall

    li $v0, 1
    lw $a0, result
    syscall

    # 프로그램 종료
    li $v0, 10
    syscall

# combination
.globl combination

combination:
#스택레시즈터(로컬 변수)는 1개만 사용할꺼기 때문에 $s0하나만 선언
#4바이트 크기를 갖기 떄문에 베이스 주소와 더해서 총 8 바이트를 뺴줌
#스택은 아래로 향하기 때문에 마이너스 해야함
    subu $sp, $sp, 8
    sw $ra, ($sp)
    sw $s0, 4($sp)

    move $s0, $a0  # n을 s0에 복사

    # n이 0이면 결과는 1
    beqz $s0, fact_done
    li $v0, 1
    move $t0, $s0  # t0에 n 복사

    factorial_loop_n:
    #n factorial 계산
    #n값을 1씩 줄이면서 v0레지스터에 곱함
        beqz $t0, factorial_loop_r_done
        mul $v0, $v0, $t0
        subi $t0, $t0, 1
        j factorial_loop_n

    factorial_loop_r_done:
    move $s0, $a1  # r을 s0에 복사

    # r이 0이면 결과는 1
    beqz $s0, fact_done
    li $v1, 1
    move $t0, $s0  # t0에 r 복사

    factorial_loop_r:
    #r값을 1씩 줄이며 v1레지스터에 곱함
        beqz $t0, factorial_loop_nr_done
        mul $v1, $v1, $t0
        subi $t0, $t0, 1
        j factorial_loop_r

    factorial_loop_nr_done:
    move $s0, $a2  # n-r을 s0에 복사

    # (n-r)이 0이면 결과는 1
    #v1레지스터를 그대로 갖다 쓸것이기 떄문에 초기화 안함
    beqz $s0, fact_done
    move $t0, $s0  # t0에 (n-r) 복사

    factorial_loop_nr:
    #n-r을 1씩 줄이며 v1에 곱함
        beq $t0, $zero, fact_done
        mul $v1, $v1, $t0
        subi $t0, $t0, 1
        j factorial_loop_nr

    fact_done:
    #답 계산 
    # n! / (r! * (n-r)!)
    #몫을 v0에 저장 -> 위에서 함수 리턴값을 v0레지스터로 지정해놔서 답을 v0에 할당해야됨
    div $v0,$v1
    mflo $v0
    
    #스택포인터를 되돌려 줌
    #다시 레지스터로 이동
    lw $ra, ($sp)
    lw $s0, 4($sp)
    addu $sp, $sp, 8

    jr $ra
