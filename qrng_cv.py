'''
Qiskit-based CV-like QRNG => qiskit’s standard qiskit library is qubit-based, not continuous-variable (CV)

building a discrete qubit system with n_qubits, where the amplitudes are taken from a discretized Gaussian (from gaussian_amplitudes

=> not true cv qrng 
'''

import hashlib
from typing import List, Tuple

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def gaussian_amplitudes(n_qubits: int, sigma: float = 0.25, span_sigmas: float = 5.0) -> Tuple[np.ndarray, np.ndarray]:
    '''
    Build a discretized zero-mean Gaussian over 2^n bins.
    Returns (amplitudes, x_grid), where amplitudes are sqrt(probabilities).
    '''
    dim = 2 ** n_qubits
    L = span_sigmas * sigma
    x = np.linspace(-L, L, dim, endpoint=False) + (2 * L) / (2 * dim)  # bin midpoints
    pdf = np.exp(-(x ** 2) / (2 * sigma ** 2))
    pdf /= pdf.sum()  # normalize
    amps = np.sqrt(pdf)
    amps /= np.linalg.norm(amps)  # numerical safety
    return amps.astype(np.complex128), x


def build_cv_qrng_circuit(amps: np.ndarray) -> QuantumCircuit:
    n_qubits = int(np.log2(len(amps)))
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.initialize(amps, range(n_qubits))  # Use initialize instead of StatePreparation
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def sample_gaussian_indices(n_qubits: int = 8, shots: int = 50_000,
                            sigma: float = 0.25, span_sigmas: float = 5.0) -> List[int]:
    '''
    Return a list of measured bin indices distributed ~Gaussian.
    '''
    amps, _ = gaussian_amplitudes(n_qubits, sigma, span_sigmas)
    qc = build_cv_qrng_circuit(amps)

    backend = AerSimulator()
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    idxs = []
    for bitstr, c in counts.items():
        index = int(bitstr[::-1], 2)
        idxs.extend([index] * c)
    return idxs


def extract_uniform_bytes_from_indices(indices: List[int], bytes_needed: int = 1024, chunk: int = 1024) -> bytes:
    '''
    Simple extractor: hash blocks of indices with SHA-256.
    '''
    out = bytearray()
    i = 0
    while len(out) < bytes_needed and i < len(indices):
        block = indices[i:i + chunk]
        b = ','.join(map(str, block)).encode('utf-8')
        digest = hashlib.sha256(b).digest()
        out.extend(digest)
        i += chunk
    return bytes(out[:bytes_needed])


def indices_to_quadrature_samples(indices: List[int], x_grid: np.ndarray) -> np.ndarray:
    '''
    Convert measured bin indices into representative quadrature samples (bin midpoints).
    '''
    indices = np.asarray(indices)
    return x_grid[indices]


def main():
    n_qubits = 8
    shots = 50_000
    sigma = 0.25
    span_sigmas = 5.0
    bytes_out = 1024
    save_file = 'qrng_bytes.bin'

    amps, x_grid = gaussian_amplitudes(n_qubits, sigma, span_sigmas)

    print(f'Preparing CV-like Gaussian with {2 ** n_qubits} bins, sigma={sigma}, span=±{span_sigmas}σ')

    indices = sample_gaussian_indices(n_qubits, shots, sigma, span_sigmas)
    x_samples = indices_to_quadrature_samples(indices, x_grid)
    print(f'Collected {len(x_samples)} CV-like samples.')

    rng_bytes = extract_uniform_bytes_from_indices(indices, bytes_needed=bytes_out)
    with open(save_file, 'wb') as f:
        f.write(rng_bytes)
    print(f'Wrote {len(rng_bytes)} bytes of randomness to: {save_file}')

    mean = float(np.mean(x_samples))
    std = float(np.std(x_samples, ddof=1))
    print(f'Quadrature sample mean ≈ {mean:.4f}, std ≈ {std:.4f} (target σ={sigma})')

    bits_to_check = 100_000
    bitstring = ''.join(f'{b:08b}' for b in rng_bytes)[:bits_to_check]
    ones = bitstring.count('1')
    zeros = len(bitstring) - ones
    print(f'Post-extraction bit balance over {bits_to_check} bits: ones={ones}, zeros={zeros}')


if __name__ == '__main__':
    main()
