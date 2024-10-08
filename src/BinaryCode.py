import os
import utils
from read import read_asm_file


def compile(assembly):
    binary_code = []
    data_section = False
    text_section = False
    data_memory = {}
    label_address_mapping = {}
    instruction_address = 0  # Keep track of the instruction addresses

    register_base_address = '00000000000000000000000000000001'  # Binary representation of $1
    
    for line in assembly:
        line = line.strip()

        if line == '.data':
            data_section = True
            text_section = False
        elif line == '.text':
            data_section = False
            text_section = True
        elif data_section:
            handle_data_section(line, data_memory)
        elif text_section:
            # First check for label definitions
            if ':' in line:
                label = line.split(':')[0].strip()
                label_address_mapping[label] = instruction_address  # Record the label's address
                line = line.split(':')[1].strip()  # Remove label from line
            
            instruction = convert(line, data_memory, register_base_address, instruction_address, label_address_mapping)  # Pass additional parameters
            if instruction:
                binary_code.append(instruction)

            # Increment the instruction address (4 bytes per instruction)
            instruction_address += 4  

    return binary_code, data_memory

def handle_data_section(line, data_memory):
    parts = line.split(':')
    if len(parts) == 2 and '.word' in parts[1]:
        var_name = parts[0].strip()
        value = parts[1].split()[1]  # Get the number after .word
        
        # Assume the address for val1 starts from a fixed base
        address = len(data_memory) * 4  # Assuming each word is 4 bytes
        data_memory[var_name] = (format(address, '032b'), value)  # Store address in binary and value




def convert(line, data_memory, register_base_address, instruction_address, label_address_mapping):
    parts = [part.strip(',') for part in line.split()]

    if parts[0] in utils.R_type_funct_codes:
        instruction = parse_R_type(parts)
    elif parts[0] in utils.I_type_op_codes:
        instruction = parse_I_type(parts, data_memory, instruction_address, label_address_mapping)  # Pass additional parameters
    elif parts[0] in utils.J_type_op_codes:
        instruction = parse_J_type(parts)
    else:
        return None  

    return instruction


def parse_R_type(parts):
    op_code = '000000'
    shamt = '00000'
    funct = utils.R_type_funct_codes[parts[0]]

    rd = utils.Register_codes[parts[1]]
    rs = utils.Register_codes[parts[2]]
    rt = utils.Register_codes[parts[3]]

    return op_code + " " + rs + " " + rt + " " + rd + " " + shamt + " " + funct

def parse_I_type(parts, data_memory, register_base_address):
    instruction = parts[0]
    op_code = utils.I_type_op_codes[instruction]

    if instruction == 'lw':
        rt = utils.Register_codes[parts[1]]
        
        # Assume the address of the variable is stored in $1
        base = '$1'
        rs = utils.Register_codes[base]  # Use the register code for $1
        offset = '0000000000000000'  # No offset since we're assuming the address is directly accessible

        return op_code + " " + rs + " " + rt + " " + offset
    elif instruction == 'beq':
        rs = utils.Register_codes[parts[1]]
        rt = utils.Register_codes[parts[2]]
        
        offset = format(int(parts[3]), '016b')

        return op_code + " " + rs + " " + rt + " " + offset
    elif instruction == 'addi':
        rs = utils.Register_codes[parts[2]]
        rt = utils.Register_codes[parts[1]]
        
        immediate = format(int(parts[3]), '016b')

        return op_code + " " + rs + " " + rt + " " + immediate
    else:
        return None 

def parse_I_type(parts, data_memory, register_base_address):
    instruction = parts[0]
    op_code = utils.I_type_op_codes[instruction]

    if instruction == 'lw':
        rt = utils.Register_codes[parts[1]]
        base = '$1'  # Base address register
        rs = utils.Register_codes[base]  # Get the register code for base

        # Find the address of the variable from data_memory
        address = data_memory[parts[2]][0]  # Get binary address of the variable
        return op_code + " " + rs + " " + rt + " " + address

    elif instruction == 'beq':
        rs = utils.Register_codes[parts[1]]
        rt = utils.Register_codes[parts[2]]
        offset = parts[3]  # This should be the label address; you will need to calculate this

        # Calculate the offset in terms of instruction addresses
        return op_code + " " + rs + " " + rt + " " + offset

    elif instruction == 'addi':
        rs = utils.Register_codes[parts[2]]
        rt = utils.Register_codes[parts[1]]
        immediate = format(int(parts[3]), '016b')  # Correctly convert the immediate to binary

        return op_code + " " + rs + " " + rt + " " + immediate

    


def parse_J_type(parts):
    instruction = parts[0]
    op_code = utils.J_type_op_codes[instruction]

    address = format(int(parts[1]), '026b')

    return op_code + " " + address





def print_output(binary_code, data_memory):
    # Ensure the outputs directory exists
    os.makedirs('outputs', exist_ok=True)  # Create the directory if it doesn't exist

    with open('outputs/binary_output_2.txt', 'w') as f:
        f.write("Data Memory:\n")
        for var, (addr, value) in data_memory.items():
            f.write(f"{var}: {addr}\n")  # Use the binary address
        f.write("\nMachine Code:\n")
        for code in binary_code:
            f.write(f"{code}\n")


if __name__ == "__main__":
    assembly_code = read_asm_file('inputs/test_code_2_mips_sim.asm')  
    
    binary_code, data_memory = compile(assembly_code)
    
    
    print_output(binary_code, data_memory)
