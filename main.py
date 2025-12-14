"""
    Memory precisa ser um vetor
    Memory, uma vez inicializada, deve ter métodos acessíveis para manipular seus espaços
    alloc só pode ser chamado se Memory for inicializada
"""

from __future__ import annotations

MAX_SIZE = 64

class FitAlg:
    """
        rule = "worst": escolhe o maior bloco livre
        rule = "first": escolhe o primeiro bloco livre
        rule = "best": escolhe o menor bloco maior ou igual ao tamanho solicitado
    """
    def choose_block(memory: Memory, size: int, rule: str) -> [int, int]: 
        mem = memory.get_mem()
        block_counter = memory.get_block_counter();
        begin = -1
        block_candidate = [-1, -1]
        for index, value in enumerate(mem):
            if (value == 0):
                if (begin == -1):
                    begin = index
            if (value == 1 or index == len(mem)-1):
                if (begin != -1 and (index - begin + 1) >= size):
                    if (rule == "first"):
                        return [begin, begin + size - 1]
                    if (rule == "worst"):
                        if (block_candidate[0] == -1 or block_candidate[1] - block_candidate[0] < index - begin):
                            block_candidate = [begin, index]
                    else:
                        if (block_candidate[0] == -1 or block_candidate[1] - block_candidate[0] > index - begin):
                            block_candidate = [begin, index]
                begin = -1
        if (block_candidate[0] != -1):
            return [block_candidate[0], block_candidate[0] + size - 1]
        else:
            return [-1, -1]

    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = choose_block(memory, size, "")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

class Memory:
    def __init__(self, size: int):
        self.mem = [0] * size
        self.mem_blocks = []
        self.size = size
        self.space = size
        self.block_counter = 1

    def get_mem(self) -> list:
        return self.mem

    def get_block_counter(self) -> int:
        return self.block_counter

    def choose_block(self, size: int, alg: str):
        begin, end = FitAlg.choose_block(self, size, alg)
        if (begin == -1):
            print("Não há espaço suficiente para alocar o bloco de memória solicitado! Libere mais memória ou aloque uma quantidade menor.")
        else:
            print(f"O bloco escolhido para o algoritmo solicitado é ({begin}, {end})")
        return

    def alloc(self, size: int, alg: FitAlg) -> MemBlock:
        global block_counter
        block = alg.fit(self, size)
        if (block == None):
            print("Não há espaço suficiente para alocar o bloco de memória solicitado! Libere mais memória ou aloque uma quantidade menor.")
            return
        for i in range(block.begin, block.end+1):
            self.mem[i] = 1
        self.mem_blocks.append(block)
        self.block_counter += 1
        print(f"Bloco de ID {block.id} e tamanho {size} alocado!")
        return block;

    def free_id(self, id: int):
        for block in self.mem_blocks:
            if (block.id == id):
                for i in range(block.begin, block.end+1):
                    self.mem[i] = 0;
                self.mem_blocks.remove(block)
                print(f"Bloco de ID {block.id} liberado!")
                del block
                return
        print(f"Não foi encontrado um bloco de memória com o id {id}")

    def show(self):
        print(f"Mapa de Memória ({self.size} bytes)")

        print("-" + "-"*self.size + "-")

        print('[' + ''.join('.' if v == 0 else '#' for v in self.mem) + ']')

        ids_list = ['.']*self.size 

        for block in self.mem_blocks:
            for index,_ in enumerate(ids_list):
                if (index >= block.begin and index <= block.end):
                    ids_list[index] = str(block.id)

        print('[' + ''.join(ids_list) + ']')

        print("-" + "-"*self.size + "-")

class MemBlock:
    def __init__(self, id: int, size: int, begin: int, end: int):
        self.id = id
        self.size = size
        self.begin = begin
        self.end = end

class FirstFit(FitAlg):
    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = FitAlg.choose_block(memory, size, "first")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

class BestFit(FitAlg):
    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = FitAlg.choose_block(memory, size, "best")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

class WorstFit(FitAlg):
    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = FitAlg.choose_block(memory, size, "worst")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

def init(size: int):
    if (size > MAX_SIZE):
        raise OverflowError("Tamanho de memória acima do suportado!")
    print(f"Memória de {size} bytes inicializada!")
    return Memory(size)

# Main loop
memory = None
while True:
    try:
        cmd = input('> ')
        parts = cmd.strip().split()

        if len(parts) <= 0:
            continue

        # init Memory
        if parts[0] == 'init':
            if len(parts) != 2:
                print("Estrutura de init inválida! Use init <tamanho>")
                continue
            if (not parts[1].isdigit()):
                print("Tamanho de bloco inválido!")
                continue
            size = int(parts[1])
            memory = init(size)

        # alloc/chooseblock MemBlock 
        if (parts[0] == "alloc" or parts[0] == "chooseblock"):
            if len(parts) != 3:
                print("Estrutura de comando inválida! Use <alloc/chooseblock> <tamanho> <algoritmo>")
                continue
            if (not parts[1].isdigit()):
                print("Tamanho de bloco inválido!")
                continue;
            if (memory == None):
                print("Memória não inicializada! Antes de alocar algum bloco, inicialize a memória com 'init <tamanho>'!")
                continue
            command = parts[0]
            size = int(parts[1])
            alg = parts[2]
            if (alg == "first"):
                if (command == "alloc"):
                    memory.alloc(size, FirstFit)
                else:
                    memory.choose_block(size, alg)
            elif (alg == "best"):
                if (command == "alloc"):
                    memory.alloc(size, BestFit)
                else:
                    memory.choose_block(size, alg)
            elif (alg == "worst"):
                if (command == "alloc"):
                    memory.alloc(size, WorstFit)
                else:
                    memory.choose_block(size, alg)
            else:
                print("Algoritmo de alocação inválido!")
                continue

        # freeid
        if parts[0] == 'freeid' and parts[1].isdigit():
            if len(parts) != 2:
                print("Estrutura de freeid inválida! Use freeid <id>") 
                continue
            if (memory == None):
                print("Memória não inicializada! Antes de liberar algum bloco, inicialize a memória com 'init <tamanho>'!")
                continue
            id = int(parts[1])
            memory.free_id(id)

        # show
        if len(parts) == 1 and parts[0] == 'show':
            if (memory == None):
                print("Memória não inicializada! Antes de usar o show, inicialize a memória com 'init <tamanho>'!")
                continue
            memory.show()
        
    except KeyboardInterrupt:
        break