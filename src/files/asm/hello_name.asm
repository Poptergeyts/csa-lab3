.data
    question: 'What is your name? '
	greeting: 'Hello, '
	sign: '!'
	name: ' ' 32
	io: 0x3ff
.code
    push question
    print_question_loop:
        ld
        test
        push print_question_exit
        jz
        push io
        ld
        swap
        pop
        st
        pop
        inc
        push print_question_loop
        jmp
    print_question_exit:
        pop
        pop
        push name
        push io
        ld
    get_name_loop:
        ld
        test
        push get_name_exit
        jz
        swap
        pop
        swap
        pop
        swap
        st
        inc
        push io
        ld
        push get_name_loop
        jmp
    get_name_exit:
        swap
        pop
        swap
        pop
        swap
        st
        pop
        push greeting
    print_greeting_loop:
        ld
        test
        push print_greeting_exit
        jz
        push io
        ld
        swap
        pop
        st
        pop
        inc
        push print_greeting_loop
        jmp
    print_greeting_exit:
        pop
        pop
        push name
    print_name_loop:
        ld
        test
        push print_name_exit
        jz
        push io
        ld
        swap
        pop
        st
        pop
        inc
        push print_name_loop
        jmp
    print_name_exit:
        pop
        pop
        push sign
        ld
        push io
        ld
        swap
        pop
        st
        pop
        pop
        hlt
