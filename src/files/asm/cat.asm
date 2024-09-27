.data
    port: 0x3ff
.code
    push port
    ld
    loop:
        ld
        test
        push exit
        jz
        push port
        ld
        swap
        pop
        st
        pop
        push loop
        jmp
    exit:
        hlt