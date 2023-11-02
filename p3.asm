	.data
		msg1: .asciiz "enter n (n<=10)"
		msg2: .asciiz "enter r (r<=10)"
		msg3: .asciiz "result : "
	.text
	.globl main
main:
	#msg 1,2�� ����ϰ� N�� R���� �Է¹���
	#�Լ��� arument�� �Ѱ��� ������ a0,1,2 �������͸� ����ؾ� ��
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
	
	#combination �Լ� ȣ��
	jal combination
	
	#��� ��� �ܰ�
	
	li $v0,4
	la $a0,msg3
	syscall
	
	li $v0,1
	addi $a0,$v1,0
	syscall
	
	li $v0,10
	syscall
	

combination:
	li $t0,1	#factorial n�� counter
	li $t1,1	#factorial r�� counter
	li $t2,1	#factorial n-r�� counter
	li $t3,1	#factorial n�� ��� �ӽ�����
	li $t4,1	#factorial r�� ��� �ӽ�����
	li $t5,1	#factorial n-r�� ��� �ӽ�����
	
fact_n:
	# n! �� ���Ͽ� t3�������Ϳ� ����
	# counter > n �̶�� r! ���ϴ� �������� �Ѿ
	bgt $t0,$a1,fact_r
	mul $t3,$t3,$t0
	addi $t0,$t0,1
	j fact_n
fact_r:
	# r! �� ���Ͽ� t4�������Ϳ� ����
	# counter > r �̶�� (n-r)! ���ϴ� �������� �Ѿ
	bgt $t1,$a2,fact_nr
	mul $t4,$t4,$t1
	addi $t1,$t1,1
	j fact_r
fact_nr:
	# (n-r)! �� ���Ͽ� t5�������Ϳ� ����
	# counter > n-r �̶�� combination ������ �ܰ�� �̵�
	bgt $t2,$a0,end
	mul $t5,$t5,$t2
	addi $t2,$t2,1
	j fact_nr
end:
	#�Լ� ���ϰ��� �ѱ� ������ v�������͸� ����ؾ� ��
	#�������� ���� lo,�������Ϳ� ����Ǿ� ����
	#jr $ra ��ɾ�� ���Լ��� �����ϰ� ���ϰ� ��ȯ
	mul $t6,$t4,$t5
	div $t3,$t6
	mflo $v1
	jr $ra
