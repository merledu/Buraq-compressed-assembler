# Buraq-compressed-assembler
This is the compressed assembler for RISC-V. It comperss 32 bit assembly into 16 bit.

## How to run compressed assembler?
First install `Python 3.7+` to run this  `compressed assembler`.
After installing `Python` install `bitstring` library of python by running
`pip install bitstring` or `pip3 install bitstring`

Clone the repository by running
`$ git clone https://github.com/Talha-Ahmed-1/Buraq-compressed-assembler.git`

After cloning change the directory by running
`$ cd Buraq-compressed-assembler`

In this directory two files are present `assembly.txt` and `machine.txt`.
In `assembly.txt` write machine code line by line and give line space after machine codes then, write assembly line by line (only use ABI names of register and dont forget to use commas as separator for register, label, immediate etc) and leave a blank line space
Example format of assembly.txt given below.
`02242783
00448493

lw a5,34(s0)
addi s1,s1,4
`
Change the file name of `assembly.txt` to `newFormatMachineCode.txt` and `machine.txt` to `Machine_Code.txt`

Run the assembler by running
`$ python assembler.py` or `$ python3 assembler.py`

After running compressor will write compressable compressed machine code to the `Machine_Code.txt` file.
