	.data
		msg1: .asciiz "enter n (n<=10)"
		msg2: .asciiz "enter r (r<=10)"
		msg3: .asciiz "result : "
	.text
	.globl main
main:
	#msg 1,2를 출력하고 N과 R값을 입력받음
	#함수에 arument를 넘겨줄 때에는 a0,1,2 레지스터를 사용해야 함
	li $v0,4
	la $a0,msg1
	syscall
	
	li $v0,5
	syscall
	move $a1,$v0 # n

	li $v0,4
	la $a0,msg2
	syscall
	
	li $v0,5
	syscall
	move $a2,$v0 # r
	
	sub $a0,$a1,$a2 # n-r
	
	#combination 함수 호출
	jal combination
	
	#결과 출력 단계
	
	li $v0,4
	la $a0,msg3
	syscall
	
	li $v0,1
	addi $a0,$v1,0
	syscall
	
	li $v0,10
	syscall
	

combination:
	li $t0,1	#factorial n의 counter
	li $t1,1	#factorial r의 counter
	li $t2,1	#factorial n-r의 counter
	li $t3,1	#factorial n의 결과 임시저장
	li $t4,1	#factorial r의 결과 임시저장
	li $t5,1	#factorial n-r의 결과 임시저장
	
fact_n:
	# n! 값 구하여 t3레지스터에 저장
	# counter > n 이라면 r! 구하는 과정으로 넘어감
	bgt $t0,$a1,fact_r
	mul $t3,$t3,$t0
	addi $t0,$t0,1
	j fact_n
fact_r:
	# r! 값 구하여 t4레지스터에 저장
	# counter > r 이라면 (n-r)! 구하는 과정으로 넘어감
	bgt $t1,$a2,fact_nr
	mul $t4,$t4,$t1
	addi $t1,$t1,1
	j fact_r
fact_nr:
	# (n-r)! 값 구하여 t5레지스터에 저장
	# counter > n-r 이라면 combination 마무리 단계로 이동
	bgt $t2,$a0,end
	mul $t5,$t5,$t2
	addi $t2,$t2,1
	j fact_nr
end:
	#함수 리턴값을 넘길 떄에는 v레지스터를 사용해야 함
	#나누기의 몫은 lo,레지스터에 저장되어 있음
	#jr $ra 명령어로 ㅎ함수를 종료하고 리턴값 반환
	mul $t6,$t4,$t5
	div $t3,$t6
	mflo $v1
	jr $ra
