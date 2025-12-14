from __future__ import annotations

MAX_SIZE = 128 # Tamanho máximo alocável pra memória

# Superclasse dos algoritmos de alocação
class FitAlg:
    """
        rule = "worst": escolhe o maior bloco livre
        rule = "first": escolhe o primeiro bloco livre
        rule = "best": escolhe o menor bloco maior ou igual ao tamanho solicitado
    """
    def choose_block(memory: Memory, size: int, rule: str) -> [int, int]:  # retorna o espaço de endereçamento ideal pro algoritmo e tamanho escolhidos
        mem = memory.get_mem()
        block_counter = memory.get_block_counter();
        begin = -1
        block_candidate = [-1, -1] # bloco de memória candidato [início, fim]
        for index, value in enumerate(mem):
            if (value == 0):
                if (begin == -1):
                    begin = index
            if (value == 1 or index == len(mem)-1):
                if (begin != -1 and (index - begin + 1) >= size):
                    if (rule == "first"):
                        return [begin, begin + size - 1] # se é first, apenas retorne o primeiro espaço livre que encontrar
                    if (rule == "worst"):
                        if (block_candidate[0] == -1 or block_candidate[1] - block_candidate[0] < index - begin): # se é worst, fique apenas com o maior
                            block_candidate = [begin, index]
                    else:
                        if (block_candidate[0] == -1 or block_candidate[1] - block_candidate[0] > index - begin): # se é best, fique apenas com o mais compacto
                            block_candidate = [begin, index]
                begin = -1
        if (block_candidate[0] != -1): # se encontrou algum candidato
            return [block_candidate[0], block_candidate[0] + size - 1]
        else: # se não, retorne um inválido
            return [-1, -1]

    def fit(memory: Memory, size: int) -> MemBlock: # o fit basicamente chama o choose_block e retorna o MemBlock com base no bloco escolhido
        begin, end = choose_block(memory, size, "")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

# Classe principal que contém todos os métodos de manipulação de memória
class Memory: 
    def __init__(self, size: int):
        self.mem = [0] * size
        self.mem_blocks = []
        self.size = size
        self.space = size
        self.block_counter = 1

    def get_mem(self) -> list: # retorna o array de memória
        return self.mem

    def get_block_counter(self) -> int: # retorna o contador de blocos atual
        return self.block_counter

    def choose_block(self, size: int, alg: str): # apenas chama o choose_block e retorna
        begin, end = FitAlg.choose_block(self, size, alg)
        if (begin == -1):
            print("Não há espaço suficiente para alocar o bloco de memória solicitado! Libere mais memória ou aloque uma quantidade menor.")
        else:
            print(f"O bloco escolhido para o algoritmo solicitado é ({begin}, {end})")
        return

    def alloc(self, size: int, alg: FitAlg) -> MemBlock: # efetivamente aloca o bloco de memória criado na memória
        global block_counter
        block = alg.fit(self, size)
        if (block == None):
            print("Não há espaço suficiente para alocar o bloco de memória solicitado! Libere mais memória ou aloque uma quantidade menor.")
            return
        for i in range(block.begin, block.end+1):
            self.mem[i] = 1
        self.mem_blocks.append(block)
        self.block_counter += 1
        self.space -= size
        print(f"Bloco de ID {block.id} e tamanho {size} alocado!")
        return block;

    def free_id(self, id: int): # libera um bloco de memória alocado pelo id
        for block in self.mem_blocks:
            if (block.id == id):
                for i in range(block.begin, block.end+1):
                    self.mem[i] = 0;
                self.mem_blocks.remove(block)
                print(f"Bloco de ID {block.id} e endereço @{block.begin} liberado!")
                self.space += block.size
                del block
                return
        print(f"Não foi encontrado um bloco de memória com o id {id}")

    def free_addr(self, addr: int): # libera um bloco de memória alocado pelo endereço (início do bloco)
        id = -1
        for block in self.mem_blocks:
            if (block.begin == addr):
                id = block.id
        if (id == -1):
            print("Não existe um bloco de memória alocado com esse endereço!")
            return
        self.free_id(id)

    def show(self): # mostra o estado da memória atual
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

        print("\n")

        active_blocks = [""] * len(self.mem_blocks)
        for index, b in enumerate(self.mem_blocks):
            active_blocks[index] = f"[id={b.id}] @{b.begin} +{b.size}B"

        print("Blocos ativos: " + " | ".join(active_blocks))

    def stats(self): # mostra estatísticas sobre a memória
        def get_external_frag(): # calcula a fragmentação externa (buracos na memória)
            holes = 0
            in_hole = 0
            for i in self.mem:
                if (i == 0 and in_hole == 0):
                    holes += 1
                    in_hole = 1
                if (i == 1 and in_hole == 1):
                    in_hole = 0
            return holes

        def get_internal_frag(): # calcula a fragmentação interna (buracos dentro dos blocos de memória alocados)
            b = 0
            for block in self.mem_blocks:
                for index, value in enumerate(self.mem):
                    if index >= block.begin and index <= block.end:
                        if value == 0:
                            b += 1
            return b

        external_frag = str(get_external_frag())
        internal_frag = str(get_internal_frag())
        occupied = self.size - self.space
        effective_use = (round((occupied/self.size), 2)) * 100.0

        print("== Estatísticas ==")
        print(f"Tamanho total: {self.size} bytes")
        print(f"Ocupado: {occupied} bytes | Livre: {self.space} bytes")
        print(f"Buracos (fragmentação externa): {external_frag}")
        print(f"Fragmentação interna: {internal_frag} bytes")
        print(f"Uso efetivo: {effective_use}%")

# Classe que representa um bloco de memória alocado
class MemBlock:
    def __init__(self, id: int, size: int, begin: int, end: int):
        self.id = id
        self.size = size
        self.begin = begin
        self.end = end

# Subclasse que chama o FirstFit
class FirstFit(FitAlg):
    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = FitAlg.choose_block(memory, size, "first")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

# Subclasse que chama o BestFit
class BestFit(FitAlg):
    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = FitAlg.choose_block(memory, size, "best")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

# Subclasse que chama o WorstFIt
class WorstFit(FitAlg):
    def fit(memory: Memory, size: int) -> MemBlock:
        begin, end = FitAlg.choose_block(memory, size, "worst")
        if (begin != -1):
            block_counter = memory.get_block_counter()
            return MemBlock(block_counter, size, begin, end)
        return None

def init(size: int): # inicia o bloco de memória
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

        # freeaddr
        if parts[0] == 'freeaddr' and parts[1].isdigit():
            if len(parts) != 2:
                print("Estrutura de freeaddr inválida! Use freeaddr <id>") 
                continue
            if (memory == None):
                print("Memória não inicializada! Antes de liberar algum bloco, inicialize a memória com 'init <tamanho>'!")
                continue
            addr = int(parts[1])
            memory.free_addr(addr)

        # show
        if len(parts) == 1 and parts[0] == 'show':
            if (memory == None):
                print("Memória não inicializada! Antes de usar o show, inicialize a memória com 'init <tamanho>'!")
                continue
            memory.show()

        # stats
        if len(parts) == 1 and parts[0] == 'stats':
            if (memory == None):
                print("Memória não inicializada! Antes de usar o stats, inicialize a memória com 'init <tamanho>'!")
                continue
            memory.stats()
        
    except KeyboardInterrupt: # se o usuaŕio sair (control c)
        break