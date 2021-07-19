
CRED = '\033[91m'
CGREEN = '\033[32m'
CEND = '\033[0m'
allowed_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'


def compiler(self):
    # setup variables and the raw code
    errors = "```diff\n"
    labels = set()
    macros = set()
    instructions = []
    lib_code = 'JMP .endFile\n'
    self = remove_comments(self)  # removes comments inline or multi line
    self = self.replace(',', '')  # removes commas from the program
    lines = self.split('\n')
    line = 0
    header_bits = header_minreg = header_minheap = header_run = header_minstack = header_import = False
    for a in lines:
        a = a.split(' ', 1)  # separate operands from opcode
        try:
            if a[1] == 'smt':  # it doesnt matter, we just wanna check if that value exists
                print(CRED + "Syntax Error: Unexpected operand used at line " + str(line) + CEND)
                errors += f"-Syntax Error: Unexpected operand used at line {str(line)}\n"
        except IndexError:
            pass

        if a[0].startswith('.'):  # check duplicated labels and paste them
            i = 1
            while i < len(a[0]):
                if a[0][i] not in allowed_chars:
                    print(CRED + "Illegal Char Error: '" + a[0][i] + "' used at line " + str(line) + CEND)
                    errors += f"-Illegal Char Error: '{a[0][i]}' used at line {str(line)}\n"
                i += 1
            if a[0] in labels:
                print(CRED + "Syntax Error: Duplicate label used at line " + str(line) + CEND)
                errors += f"-Syntax Error: Duplicate label used at line {str(line)}\n"
            else:
                labels.add(a[0])
                instructions.append(a[0])

        else:  # work on the instructions
            opcode = a[0]
            op_num = opcodes(opcode)  # returns the n of operands the instruction needs, or YEET if error
            '''if '[' in a[1]:  # there is some multiword action going on
                i = 0
                operand = []
                while i < len(a[1]):
                    if a[1][i] == '[':  # group operands based on the brackets
                        op = ''
                        while a[1][i] != ']':
                            op += a[1][i]
                            if i < len(a[1]):
                                i += 1
                            else:
                                break
                        operand.append(op + ']')
                    i += 1
            else:'''  # regular operands get separated here
            operand = a[1].split(' ')
            i = 0
            op = []
            for b in operand:  # checking what operand type it is and converting some of them ex: imm to decimal
                op_type = operand_type(b)
                if op_type == 'YEET':  # yeet means error
                    if b == 'SP':  # deal with sp plz
                        pass
                    else:
                        print(CRED + "Syntax Error: Unknown operand type at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Unknown operand type at line {str(line)}\n"
                elif op_type == 'imm':
                    b = str(int(b))
                op.append(b)
            operand = op

            if opcode == 'DW':
                if op_num == 1:
                    if operand[0].isnumeric():
                        instructions.append(opcode + ' ' + operand[0])
                    else:
                        print(CRED + "Syntax Error: Unknown operand at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Unknown operand at line {str(line)}\n"
                else:
                    print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                    errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"
            elif op_num == 'YEET':  # if the previous function returns YEET then its not an opcode
                if opcode == 'BITS':  # deals with minstack header
                    if header_bits:
                        print(CRED + "Syntax Error: More than 1 'BITS' header at line " + str(line) + CEND)
                        errors += f"-Syntax Error: More than 1 'BITS' header at line {str(line)}\n"
                    if len(operand) != 2:
                        print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"
                    else:
                        if operand[0] not in ('==', '>=', '<=', '>', '<'):
                            print(CRED + "Syntax Error: Invalid operand at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Invalid operand at line {str(line)}\n"
                        elif operand[1].isnumeric():
                            instructions.append(opcode + ' ' + (' '.join(operand)))
                            header_bits = True
                        else:
                            print(CRED + "Syntax Error: Unknown operand at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Unknown operand at line {str(line)}\n"

                elif opcode == 'MINREG':  # deals with minreg header
                    if header_minreg:
                        print(CRED + "Syntax Error: More than 1 'MINREG' header at line " + str(line) + CEND)
                        errors += f"-Syntax Error: More than 1 'MINREG' header at line {str(line)}\n"
                    if len(operand) != 1:
                        print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"
                    else:
                        if operand[0].isnumeric():
                            instructions.append(opcode + ' ' + (' '.join(operand)))
                            header_minreg = True
                        else:
                            print(CRED + "Syntax Error: Unknown operand at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Unknown operand at line {str(line)}\n"

                elif opcode == 'MINHEAP':  # deals with minheap header
                    if header_minheap:
                        print(CRED + "Syntax Error: More than 1 'MINHEAP' header at line " + str(line) + CEND)
                        errors += f"-Syntax Error: More than 1 'MINHEAP' header at line {str(line)}\n"
                    if len(operand) != 1:
                        print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"
                    else:
                        if operand[0].isnumeric():
                            instructions.append(opcode + ' ' + (' '.join(operand)))
                            header_minheap = True
                        else:
                            print(CRED + "Syntax Error: Unknown operand at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Unknown operand at line {str(line)}\n"

                elif opcode == 'RUN':  # deals with run ram/rom header
                    if header_run:
                        print(CRED + "Syntax Error: More than 1 'RUN' header at line " + str(line) + CEND)
                        errors += f"-Syntax Error: More than 1 'RUN' header at line {str(line)}\n"
                    if len(operand) != 1:
                        print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"
                    else:
                        if operand[0] == 'RAM' or operand == 'ROM':
                            instructions.append(opcode + ' ' + (' '.join(operand)))
                            header_run = True
                        else:
                            print(CRED + "Syntax Error: Unknown operand at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Unknown operand at line {str(line)}\n"

                elif opcode == 'MINSTACK':  # deals with minstack header
                    if header_minstack:
                        print(CRED + "Syntax Error: More than 1 'MINSTACK' header at line " + str(line) + CEND)
                        errors += f"-Syntax Error: More than 1 'MINSTACK' header at line {str(line)}\n"
                    if len(operand) != 1:
                        print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                        errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"
                    else:
                        if operand[0] == 'RAM' or operand == 'ROM':
                            instructions.append(opcode + ' ' + (' '.join(operand)))
                            header_minstack = True
                        else:
                            print(CRED + "Syntax Error: Unknown operand at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Unknown operand at line {str(line)}\n"

                elif opcode == 'IMPORT':  # deals with IMPORT header
                    header_import = True
                    for b in operand:
                        if b == 'advmath':  # expand for more libraries when the time comes
                            from libraries import advmath

                        elif b == 'float':
                            from libraries import float

                        elif b == 'array':
                            from libraries import array

                        elif b == 'string':
                            from libraries import string

                        else:
                            print(CRED + "Syntax Error: Unknown Library at line " + str(line) + CEND)
                            errors += f"-Syntax Error: Unknown Library at line {str(line)}\n"

                else:  # unknown instruction error
                    print(CRED + "Syntax Error: Unknown instruction at line " + str(line) + CEND)
                    errors += f"-Syntax Error: Unknown instruction at line {str(line)}\n"

            else:
                if op_num == len(operand):  # regular instruction, just add it
                    instructions.append(opcode + ' ' + (' '.join(operand)))

                elif op_num == (len(operand) + 1):  # enable smart typing to copy 1st operand to 2nd op
                    instructions.append(opcode + ' ' + str(operand[0]) + ' ' + (' '.join(operand)))

                else:
                    print(CRED + "Syntax Error: Wrong number of operands at line " + str(line) + CEND)
                    errors += f"-Syntax Error: Wrong number of operands at line {str(line)}\n"

        line += 1
    code = ''
    for a in instructions:
        code += a + '\n'

    if header_import:
        lib_code += '.endFile'
        for a in lib_code:
            code += a + '\n'

    if errors == "```diff\n":
        output = '```' + code[:-1] + '```'
    else:
        if code == '':
            output = errors[:-1] + '```'
        else:
            output = f"{errors[:-1]}``````{code[:-1]}```"

    return output


# helper functions below
def remove_comments(self):  # removes all inline comments and multiline comments from the program
    i = 0
    output = ''
    commented = False
    while i < len(self):
        if commented:
            try:
                if self[i] == '*' and self[i + 1] == '/':
                    i += 2
                    commented = False
            except IndexError:
                pass
        else:
            try:
                if self[i] == '/' and self[i + 1] == '*':
                    i += 2
                    commented = True
                else:
                    if self[i] == '/' and self[i + 1] == '/':
                        i += 2
                        while self[i] != '\n':
                            i += 1
            except IndexError:
                pass
            output += self[i]

        i += 1
    return output


def opcodes(self):  # checks if the opcode is correct and returns the number of operands expected
    operands = {
        # CORE
        'ADD': 3,
        'RSH': 2,
        'LOD': 2,
        'STR': 2,
        'BGE': 3,
        'NOR': 3,
        'IMM': 2,
        # I/O
        'IN': 2,
        'OUT': 2,
        # BASIC
        'SUB': 3,
        'JMP': 1,
        'MOV': 2,
        'NOP': 0,
        'LSH': 2,
        'INC': 2,
        'DEC': 2,
        'NEG': 2,
        'AND': 3,
        'OR': 3,
        'NOT': 2,
        'XOR': 3,
        'XNOR': 3,
        'NAND': 3,
        'BRE': 3,
        'BNE': 3,
        'BRL': 3,
        'BRG': 3,
        'BLE': 3,
        'BZR': 2,
        'BNZ': 2,
        'BRN': 2,
        'BRP': 2,
        'BEV': 2,
        'BOD': 2,
        'PSH': 2,
        'POP': 2,
        'CAL': 2,
        'RET': 0,
        'HLT': 0,
        'CPY': 2,
        'BRC': 3,
        'BNC': 3,
        # COMPLEX
        'MLT': 3,
        'DIV': 3,
        'MOD': 3,
        'BSR': 3,
        'BSL': 3,
        'SRS': 2,
        'BSS': 3,
        'SETE': 3,
        'SETNE': 3,
        'SETL': 3,
        'SETG': 3,
        'SETLE': 3,
        'SETGE': 3,
        'SETC': 3,
        'SETNC': 3,
        'LLOD': 3,
        'LSTR': 3,
        # urcl++ exclusive below
        'LIB': 2,
    }
    try:
        output = operands[self]
    except KeyError:
        output = 'YEET'
    return output


def operand_type(self):
    op_type = {
        'R': 'reg',
        '$': 'reg',
        '#': 'mem',
        'M': 'mem',
        '&': 'pattern',
        '%': 'port',
        "'": 'char',
        '"': 'char',  # we can evolve so '' means char and "" means string later urclpp exclusive feature tho
        '.': 'label',
        '[': 'address',
        '+': 'relative',  # i want to remove these two relatives
        '-': 'relative',
        '@': 'macros'
    }
    try:
        output = op_type[self]
    except KeyError:
        if self.isnumeric():
            output = 'imm'
        else:
            output = 'YEET'
    return output


print(compiler('''.label
ADD R1 R2
.label
DEC R2'''))


'''def libraries(self):
    try:
        func = getattr(string, self)
        func('a', 'b', 'c')
    except AttributeError:
        print(CRED + "Syntax Error: Unknown Library function at line " + str(line) + CEND)
        errors += f"-Syntax Error: Unknown Library function at line {str(line)}\n"
    return'''

