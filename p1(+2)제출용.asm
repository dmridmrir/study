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

	#i=1, result = 0 �� �ʱ�ȭ 
	lw $t1,i
	lw $t2,result

	#loop
	# i > N �̶�� exit��
	#�׷��� �ʴٸ�
	#result += i
	#i += 2 ���� loop�� 

loop:	add $t2,$t2,$t1
	addi $t1,$t1,2
	bgt $t1,$t0,exit 
	j loop
	
	#exit
	#result ���
exit:	li $v0, 4		# print_string syscall code = 4
	la $a0, msg2
	syscall
	
	li $v0,1		#integer ��� �ڵ� 1
	move $a0,$t2		#result ���� $a0�� �̵�
	syscall
	
	.data
		msg1: .asciiz "enter integer N  "
		msg2: .asciiz "result : "
		i: .word 1
		result: .word 0

