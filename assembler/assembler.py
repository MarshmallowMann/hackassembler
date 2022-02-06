import sys

symbolTable = {
    'R0': '0',
    'R1': '1',
    'R2': '2',
    'R3': '3',
    'R4': '4',
    'R5': '5',
    'R6': '6',
    'R7': '7',
    'R8': '8',
    'R9': '9',
    'R10': '10',
    'R11': '11',
    'R12': '12',
    'R13': '13',
    'R14': '14',
    'R15': '15',
    'SCREEN': '16384',
    'KBD': '24576',
    'SP': '0',
    'LCC': '1',
    'ARG': '2',
    'THIS': '3',
    'THAT': '4'
}


def parse(line):
    # Removes comments and whitespace
    line = line.replace(' ', '')
    line = line.split('//', 1)[0]
    line = line.split('\n', 1)[0]

    return line


def buildSymbol(lines):
    # builds the symbol table
    currentLine = 0
    # First pass ( Bind values to symbolic names)
    for line in lines:
        isAddress = line.startswith('@')
        if "=" in line or ";" in line:
            isInstruction = True
        else:
            isInstruction = False
        if isAddress or isInstruction:
            currentLine += 1
        elif line.startswith("(") and line.endswith(")"):
            symbolName = line.replace("(", "").replace(")", "")
            symbolTable[symbolName] = currentLine

    # Second Pass ( Bind variables to memory addresses)
    minAddress = 16
    for line in lines:
        isAddress = line.startswith('@')
        if isAddress:
            value = line[1:]
            if value not in symbolTable and not value.isnumeric():
                symbolTable[value] = minAddress
                minAddress += 1
    return

def instructionConverter(line):
    # Converts C instructions to binary
    COMPUTATIONS = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }
    DESTINATIONS = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    JUMPS = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    if line.startswith("(") and line.endswith(")") or line.startswith("@") :
        return
    dest, jump = "", ""
    comp = line.split("=").pop().split(";")[0]
    if "=" in line:
        dest = line.split("=")[0]
    if ";" in line:
        jump = line.split(";").pop()
    return f"111{COMPUTATIONS[comp]}{DESTINATIONS[dest]}{JUMPS[jump]}"


def addressConverter(line):
    # Converts A instructions to binary
    if line.startswith("@"):
        value = line[1:]
        if value in symbolTable:
            return f"{int(symbolTable[value]):0>16b}"
        return f"{int(value):0>16b}"
    else:
        return




def main():
    # Check Usage
    if (len(sys.argv)) != 2:
        print("Usage: assembler.py <file.asm>")
        exit(1)
    # Get file name and extension
    fileIn = sys.argv[1]
    fileName = fileIn.split('.')[0]
    fileExtension = fileIn.split('.')[1]

    # Check ASM extension
    if fileExtension != "asm":
        print("Usage: assembler.py <file.asm>")
        exit(2)

    # Open out file
    fileOut = fileName + ".hack"

    with open(fileOut, 'w', encoding='utf-8') as fOut:
        with open(fileIn, 'r', encoding='utf-8') as fIn:

            parsedFile = []
            # Reads the lines from the in file
            lines = fIn.readlines()

            # Parse file
            for line in lines:
                line = parse(line)
                if line != '':
                    parsedFile.append(line)

            # Build Symbol Table
            buildSymbol(parsedFile)

            binaryList = []
            # Converts lines from parsedFile to binary
            for line in parsedFile:
                if addressConverter(line) is not None:
                    binaryList.append(addressConverter(line))
                elif instructionConverter(line) is not None:
                    binaryList.append(instructionConverter(line))
            # Joins the list with a new line
            output = "\n".join(binaryList)
            # Writes to file
            fOut.write(output)

if __name__ == '__main__':
    main()
