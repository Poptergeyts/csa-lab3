.data
	msg: 'Hello World!'
	io: 0x3ff
.code
    push msg
    loop:
        ld
        test
        push exit
        jz
        push io
        ld
        swap
        pop
        st
        pop
        inc
        push loop
        jmp
    exit:
        hlt