import numpy as np
import matplotlib.pyplot as plt
import math
import scienceplots

plt.style.use('science')

filename = 'qrng_bits.txt'
with open(filename, "r") as f:
    bits = f.read().strip()

bits = [int(b) for b in bits if b in '01']

n_bits = len(bits)
size = math.ceil(math.sqrt(n_bits))
padded_bits = bits + [0]*(size**2 - n_bits)
bit_array = np.array(padded_bits).reshape((size, size))

plt.figure(figsize=(6,6))
plt.imshow(bit_array, cmap='gray_r')  # 0 = white, 1 = black
plt.axis('off')
plt.title('IBM-Quantum Bits (1 million)')
plt.savefig('ibm_quantum_bits.png')
plt.show()