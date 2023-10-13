	.text
	
	.globl main
main:
	#print msg1
	# 4 = code for print string
	# load address of msg1
	li $v0,4
	la $a0,msg1
	syscall
		
	# get N from user and save
	# 5 = code for read integer
	# move address to $t0
	li $v0,5
	syscall
	move $t0,$v0

	#i와 result값 초기화 
	# 1,2 선언 
	lw $t1,i
	lw $t2,result
	lw $t3,compare
	lw $t4,divide

TRUE:	bgt $t1,$t0,exit  #i > N 이라면 exit으로
	add $t2,$t2,$t1
loop:	addi $t1, $t1, 1  #i++
	div $t1,$t4	  # i % 2 몫은 lo, 나머지는 hi에 저장됨
	mfhi $s1	  # 나머지를 가져옴
	beq $s1,$t3,TRUE  #나머지가 1이라면 TRUE로 그렇지 않다면 loop로 이동
	j loop
	
exit:	li $v0, 4		# print_string syscall code = 4
	la $a0, msg2
	syscall
	
	li $v0,1
	move $a0,$t2
	syscall
	
	.data
		msg1: .asciiz "enter integer N  "
		msg2: .asciiz "result : "
		i: .word 0
		result: .word 0
		compare: .word 1
		divide: .word 2
