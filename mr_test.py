import random
import sympy
import time

contador = 0

def is_prime(n, k=5):
    global contador
    contador += 1

    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Escreve n-1 como 2^r * d, onde d é ímpar
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Executa o teste k vezes
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
    start_time = time.time()

    x = 0
    while pow(g, x, p) != a:
        x += 1
        if time.time() - start_time > timeout:
            raise TimeoutError("Tempo limite excedido.")

    end_time = time.time()
    return x, end_time - start_time

# Exemplo de uso
N = int(input("Digite um número inteiro N: "))
a = int(input("Digite um número inteiro a: "))
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
