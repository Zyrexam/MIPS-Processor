R_type_funct_codes = {
    'add': '100000',
    'sub': '100010',
    'and': '100100',
    'or': '100101',
    'slt': '101010'
}

I_type_op_codes = {
    'lw': '100011',
    'beq': '000100',
    'addi': '001000'
}

J_type_op_codes = {
    'j': '000011'
}

Register_codes = {
    '$zero': '00000', 
    '$1': '00001',  
    '$t0': '01000', 
    '$t1': '01001', 
    '$t2': '01010', 
    '$t3': '01011', 
    '$t4': '01100', 
    '$t5': '01101', 
    '$t6': '01110', 
    '$t7': '01111', 
    '$s0': '10000', 
    '$s1': '10001', 
    '$s2': '10010', 
    '$s3': '10011', 
    '$s4': '10100', 
    '$s5': '10101', 
    '$s6': '10110', 
    '$s7': '10111', 
    '$sp': '11101', 
    '$fp': '11110', 
    '$ra': '11111'
}

binary_to_register = {v: k for k, v in Register_codes.items()}