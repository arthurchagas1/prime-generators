import random
import sympy
import time

# Inicializa o contador global
contador = 0

# Lista de números primos pequenos para otimização
PRIMOS_PEQUENOS = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
    307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397,
    401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599,
    601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
    701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
    809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887,
    907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
]

def is_prime(n, k=5):
    global contador
    contador += 1  # Incrementa o contador a cada execução

    # Verificações rápidas para números pequenos e casos triviais
    if n in PRIMOS_PEQUENOS:
        return True
    if n <= 1:
        return False
    if n % 2 == 0:
        return False

    # Testa a divisibilidade por primos pequenos
    for prime in PRIMOS_PEQUENOS:
        if prime * prime > n:
            break
        if n % prime == 0:
            return False

    # Escreve n-1 como 2^r * d, onde d é ímpar
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Executa o teste de Miller-Rabin k vezes
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def next_prime(N):
    p = N + 1
    while True:
        if is_prime(p):
            return p
        p += 1

def find_generator(p):
    if p == 2:
        return 1, 1

    # Verifica se p é um número primo
    if not sympy.isprime(p):
        raise ValueError("O número p precisa ser primo para encontrar um gerador.")

    # Calcula φ(p) = p - 1
    phi_p = p - 1

    # Encontra os fatores primos de φ(p)
    factors = sympy.factorint(phi_p)

    # Percorre os possíveis valores de g
    for g in range(2, p):
        is_generator = True

        # Verifica se g é relativamente primo a p
        if sympy.gcd(g, p) != 1:
            continue

        # Verifica se g^((p-1)/pi) mod p != 1 para todos os fatores primos de φ(p)
        for factor, _ in factors.items():
            if pow(g, phi_p // factor, p) == 1:
                is_generator = False
                break

        if is_generator:
            return g, phi_p  # g é um gerador e a ordem de Zp* é phi_p

    # Se não encontrarmos um gerador, retornamos um elemento com ordem alta
    g = random.randint(2, p - 1)
    order = 2  # A menor ordem possível
    while pow(g, order, p) != 1:
        order *= 2  # Duplica a ordem
    return g, order

def discrete_logarithm(a, g, p, timeout=60):
    start_time = time.time()  # Marca o início do cálculo

    x = 0
    while pow(g, x, p) != a:
        x += 1
        if time.time() - start_time > timeout:
            raise TimeoutError("Tempo limite excedido.")  # Lança exceção se o tempo limite for excedido

    end_time = time.time()  # Marca o final do cálculo
    return x, end_time - start_time

# Exemplo de uso
def main():
    N = int(input("Digite um número inteiro N (N > 0): "))
    a = int(input("Digite um número inteiro a (a > 0): "))

    if N <= 0 or a <= 0:
        print("Ambos os números devem ser maiores que 0.")
        return

    p = next_prime(N)
    print(f"O menor primo p > {N} é {p}. O teste de Miller-Rabin foi executado {contador} vezes.")

    g, order = find_generator(p)
    if order == p - 1:
        print(f"Um gerador de Z{p}*: {g}, com ordem mínima estimada: {order}")
    else:
        print(f"Um elemento com ordem alta em Z{p}*: {g}, com ordem mínima estimada: {order}")

    try:
        result, time_taken = discrete_logarithm(a, g, p)
        print(f"O logaritmo discreto de {a} módulo {p} na base {g} é {result}. Tempo de cálculo: {time_taken:.6f} segundos.")
    except TimeoutError as e:
        print(e)

if __name__ == "__main__":
    main()
