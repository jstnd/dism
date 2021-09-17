# DISM

DISM (Diminished Instruction Set Machine) is a virtual machine with a simple, RISC-like instruction set. It contains 8 general-purpose registers and a block of data memory from address `0` to address `65535`, implemented using integer arrays (initialized to `0`) denoted as `R` and `M` respectively, as well as a program counter `PC` to store the address of the next instruction to execute.

## Instructions

Below, `n` denotes a natural number, while `i` denotes an integer.

| Instruction | Meaning |
| ----------- | ------- |
| `add d s1 s2` | `R[d] <- R[s1] + R[s2]` |
| `sub d s1 s2` | `R[d] <- R[s1] - R[s2] (R[d] <- 0 when R[s2] > R[s1])` |
| `mul d s1 s2` | `R[d] <- R[s1] * R[s2]` |
| `mov d n` | `R[d] <- n` |
| `lod d s i` | `R[d] <- M[R[s] + i` |
| `str d i s` | `M[R[d] + i] <- R[s]` |
| `jmp s i` | `PC <- R[s] + i` |
| `beq s1 s2 n` | `If R[s1] = R[s2] then PC <- n` |
| `bgt s1 s2 n` | `If R[s1] > R[s2] then PC <- n` |
| `rdn n` | `Read natural number from screen into R[d]` |
| `ptn s` | `Print natural number R[s] to screen` |
| `hlt s` | `Halt the DISM with code R[s]` |

Instructions may optionally be preceded by a 'label' followed by a colon. A label is represented as a `#` followed by a string of alphanumeric characters. When a label is used in front of instruction, other instructions may reference that labeled instruction's location in memory using the label itself.

## Examples

The below program and other examples can be found in the `examples` directory.

```
; reads n and m and then prints n m times
	rdn 1         ;read n into register 1
        rdn 2         ;read m into register 2
        mov 3 1       ;move value 1 into register 3
#LOOP:  beq 2 0 #END  ;if m==0 then goto end
        ptn 1         ;print n
        sub 2 2 3     ;m--
        jmp 0 #LOOP   ;goto loop beginning
#END:   hlt 0         ;halt with code 0
```