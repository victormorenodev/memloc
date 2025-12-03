"""
    Memory precisa ser um vetor
    Memory, uma vez inicializada, deve ter métodos acessíveis para manipular seus espaços
    alloc só pode ser chamado se Memory for inicializada
"""

MAX_SIZE = 64
block_counter = 1

class Memory:
    def __init__(self, size):
        self.size = size
        self.space = size

class MemBlock:
    def __init__(self, id, size):
        self.id = id
        self.size = size

def alloc(size):
    global block_counter
    block = MemBlock(block_counter, size)
    block_counter += 1
    return block

def init(size):
    return Memory(size)

def check_input(input):
    parts = input.strip().split()

    # init Memory
    if len(parts) == 2 and parts[0] == 'init' and parts[1].isdigit():
        size = int(parts[1])
        if (size <= MAX_SIZE):
            memory = init(size)
            print('Memória de tamanho ' + str(memory.size) + ' bytes inicializada')
        else:
            print('Tamanho de memória acima do limite!')

    # alloc MemBlock
    if len(parts) == 2 and parts[0] == 'alloc' and parts[1].isdigit():
        size = int(parts[1])
        if (size <= MAX_SIZE):
            block = alloc(size)
            print('Bloco de ID ' + str(block.id) + ' e tamanho ' + str(size) + ' alocado')
        else:
            print('Tamanho de bloco acima do limite!')

# Main loop
while True:
    try:
        cmd = check_input(input('> '))
    except KeyboardInterrupt:
        break
