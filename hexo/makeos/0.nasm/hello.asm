	global	_start

	section	.text
_start:	mov	rax,	1	;system call for write
	mov	rdi,	1	;file handle 1 is stdout
	mov	rsi,	message	;address of string
	mov	rdx,	13
	syscall
	mov	rax,	60
	xor	rdi,	rdi
	syscall

	section	.data
message: db	"Hello, World!", 10
