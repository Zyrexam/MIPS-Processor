.data
    num1: .word 15
    num2: .word 25

.text
    lw $t0, num1
    lw $t1, num2
    add $t2, $t0, $t1
    sub $t3, $t1, $t0
    and $t4, $t0, $t1
    or  $t5, $t0, $t1
    slt $t6, $t0, $t1
    j end_label

end_label:
    add $t7, $t2, $t3