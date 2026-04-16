import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, factorial, sph_harm
from mpl_toolkits.mplot3d import Axes3D

# Page Configuration
st.set_page_config(page_title="CHY1005: Quantum Chemistry Hub", layout="wide")

# Sidebar for Course Navigation
st.sidebar.title("Syllabus: Unit 2")
page = st.sidebar.radio("Select Topic", ["Schrödinger Equation", "Radial Solutions", "Angular Solutions"])

# --- Topic 1: The Schrödinger Equation ---
if page == "Schrödinger Equation":
    st.header("The Schrödinger Equation & Wave Functions")
    st.write("""
    Unit 2 of the syllabus introduces the foundation of quantum mechanics. 
    The Schrödinger equation allows us to find the allowed energy levels of quantum systems.
    """)
    
    st.subheader("The General Form")
    st.latex(r"\hat{H}\psi = E\psi")
    
    st.write("For a Hydrogen atom, the wave function $\psi$ is separated into radial and angular parts:")
    st.latex(r"\psi_{n,l,m}(r, \theta, \phi) = R_{n,l}(r) Y_{l,m}(\theta, \phi)")
    
    st.info("Navigate to the other sections to visualize these specific solutions.")

# --- Topic 2: Radial Solutions ---
elif page == "Radial Solutions":
    st.header("Radial Probability Density $P(r)$")
    st.write("Visualization of the probability of finding an electron at distance $r$ from the nucleus.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        n = st.slider("Principal Quantum Number (n)", 1, 4, 1)
        l = st.slider("Azimuthal Quantum Number (l)", 0, n-1, 0)
        st.write(f"Currently plotting: **{n}{'s' if l==0 else 'p' if l==1 else 'd' if l==2 else 'f'} orbital**")

    # Physical Logic
    a0 = 1.0 # Bohr radius units
    r = np.linspace(0, n**2 * 10, 500)
    rho = (2 * r) / (n * a0)
    
    # Normalization and Laguerre Calculation
    norm = np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    poly = genlaguerre(n-l-1, 2*l+1)
    R_nl = norm * np.exp(-rho/2) * (rho**l) * poly(rho)
    prob_density = r**2 * R_nl**2

    with col2:
        fig, ax = plt.subplots()
        ax.plot(r, prob_density, color='#e74c3c', lw=2)
        ax.fill_between(r, prob_density, alpha=0.2, color='#e74c3c')
        ax.set_xlabel("Radius r (Bohr units)")
        ax.set_ylabel("Probability Density $P(r)$")
        ax.set_title(f"Radial Distribution for n={n}, l={l}")
        st.pyplot(fig)

# --- Topic 3: Angular Solutions ---
elif page == "Angular Solutions":
    st.header("Angular Solutions (Orbital Shapes)")
    st.write("These spherical harmonics define the geometric shape and orientation of the orbital.")

    l_val = st.slider("Orbital Shape (l)", 0, 3, 1)
    m_val = st.slider("Orientation (m)", -l_val, l_val, 0)

    # Grid for Spherical Harmonics
    theta = np.linspace(0, np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)

    # Calculating Spherical Harmonics
    # Signature: sph_harm(m, n, phi, theta) -> SciPy uses n for l
    Y_lm = sph_harm(m_val, l_val, phi, theta)
    
    # We plot the absolute square for probability shape
    r_mag = np.abs(Y_lm)**2

    # Conversion to Cartesian
    x = r_mag * np.sin(theta) * np.cos(phi)
    y = r_mag * np.sin(theta) * np.sin(phi)
    z = r_mag * np.cos(theta)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none', alpha=0.9)
    
    ax.set_title(f"3D Orbital Shape (l={l_val}, m={m_val})")
    ax.axis('off') # Hide axes for a cleaner look
    st.pyplot(fig)
