import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, factorial

def hydrogen_orbital_plotter():
    # Constants
    a0 = 0.529  # Bohr radius in Angstroms
    Z = 1       # Atomic number for Hydrogen
    
    # Input Quantum Numbers
    print("--- Hydrogen Radial Probability Plotter ---")
    n = int(input("Enter principal quantum number (n >= 1): "))
    l = int(input(f"Enter azimuthal quantum number (0 <= l < {n}): "))
    
    if l >= n or n < 1 or l < 0:
        print("Invalid quantum numbers. Ensure n >= 1 and 0 <= l < n.")
        return

    # Range of r (distance from nucleus)
    # Higher n orbitals extend further out
    r_max = n**2 * 10 * a0
    r = np.linspace(0, r_max, 1000)
    
    # Normalized coordinate rho
    rho = (2 * Z * r) / (n * a0)
    
    # Normalization Constant for the Radial Wave Function
    norm = np.sqrt((2 * Z / (n * a0))**3 * factorial(n - l - 1) / (2 * n * factorial(n + l)))
    
    # Associated Laguerre Polynomial L_{n-l-1}^{2l+1}(rho)
    laguerre = genlaguerre(n - l - 1, 2 * l + 1)
    
    # Radial Wave Function R_{nl}(r)
    R_nl = norm * np.exp(-rho / 2) * (rho**l) * laguerre(rho)
    
    # Radial Probability Density P(r) = r^2 * |R(r)|^2
    prob_density = (r**2) * (R_nl**2)

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(r, prob_density, label=f'Orbital: n={n}, l={l}', color='#2c3e50', lw=2)
    plt.fill_between(r, prob_density, alpha=0.3, color='#3498db')
    
    plt.title(f'Radial Probability Density for Hydrogen ($n={n}, l={l}$)')
    plt.xlabel('Distance from Nucleus $r$ (Å)')
    plt.ylabel('Probability Density $P(r)$')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    hydrogen_orbital_plotter()
