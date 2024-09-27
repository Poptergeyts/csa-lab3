.data
    limit: 0x3e7
    2: 0x2
    3: 0x3
    5: 0x5
    15: 0xf
    io: 0x3ff
.code
    push limit
    ld
    push 5
    ld
    swap
    pop
    swap
    div
    inc
    swap
    ld
    push 5
    ld
    swap
    pop
    swap
    div
    swap
    pop
    mul
    push 2
    ld
    swap
    pop
    swap
    div
    push 5
    ld
    swap
    pop
    mul
    push limit
    ld
    push 3
    ld
    swap
    pop
    swap
    div
    inc
    swap
    ld
    push 3
    ld
    swap
    pop
    swap
    div
    swap
    pop
    mul
    push 2
    ld
    swap
    pop
    swap
    div
    push 3
    ld
    swap
    pop
    mul
    add
    push limit
    ld
    push 15
    ld
    swap
    pop
    swap
    div
    inc
    swap
    ld
    push 15
    ld
    swap
    pop
    swap
    div
    swap
    pop
    mul
    push 2
    ld
    swap
    pop
    swap
    div
    push 15
    ld
    swap
    pop
    mul
    swap
    sub
    push io
    ld
    swap
    pop
    st
    pop
    hlt