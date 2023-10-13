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

	#i�� result�� �ʱ�ȭ 
	# 1,2 ���� 
	lw $t1,i
	lw $t2,result
	lw $t3,compare
	lw $t4,divide

TRUE:	bgt $t1,$t0,exit  #i > N �̶�� exit����
	add $t2,$t2,$t1
loop:	addi $t1, $t1, 1  #i++
	div $t1,$t4	  # i % 2 ���� lo, �������� hi�� �����
	mfhi $s1	  # �������� ������
	beq $s1,$t3,TRUE  #�������� 1�̶�� TRUE�� �׷��� �ʴٸ� loop�� �̵�
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
