# Simulador de Alocação de Memória

Este projeto implementa um **simulador de alocação de memória** em Python, inspirado em conceitos de Sistemas Operacionais. Ele permite inicializar uma memória linear e realizar alocações e liberações utilizando diferentes **algoritmos de alocação**.

---

## Funcionalidades

- Inicialização de memória com tamanho definido
- Alocação de blocos de memória
- Liberação de blocos por **ID** ou por **endereço inicial**
- Visualização do mapa de memória
- Estatísticas de uso e fragmentação

---

## Algoritmos de Alocação Suportados

- **First Fit**: aloca no primeiro bloco livre suficiente
- **Best Fit**: aloca no menor bloco livre possível
- **Worst Fit**: aloca no maior bloco livre disponível

---

## Comandos Disponíveis

### Inicializar memória
```bash
init <tamanho>
```
- Tamanho máximo: `128` bytes

---

### Alocar memória
```bash
alloc <tamanho> <algoritmo>
```
Exemplos:
```bash
alloc 16 first
alloc 8 best
alloc 32 worst
```

---

### Escolher bloco (sem alocar)
```bash
chooseblock <tamanho> <algoritmo>
```

---

### Liberar memória
Por ID:
```bash
freeid <id>
```

Por endereço inicial:
```bash
freeaddr <endereço>
```

---

### Visualizar memória
```bash
show
```
- Mostra o mapa binário (`.` livre / `#` ocupado)
- Mostra os IDs dos blocos alocados

---

### Estatísticas
```bash
stats
```
Inclui:
- Espaço total, ocupado e livre
- Fragmentação externa (buracos)
- Fragmentação interna
- Uso efetivo da memória

---

## Estrutura do Código

- `Memory`: gerencia o vetor de memória e os blocos alocados
- `MemBlock`: representa um bloco de memória
- `FitAlg`: superclasse dos algoritmos de alocação
- `FirstFit`, `BestFit`, `WorstFit`: implementações específicas

---

## Execução

```bash
python main.py
```

Use os comandos interativamente no prompt `>`.

---

## Objetivo Acadêmico

Este projeto tem finalidade **educacional**, sendo adequado para estudo de:
- Gerência de memória
- Fragmentação interna e externa
- Estratégias clássicas de alocação

---

## Requisitos

- Python 3.10+

---

## Observações

- O sistema não utiliza memória real; trata-se de uma **simulação lógica**.
- Strings `.` e `#` são usadas apenas para visualização.