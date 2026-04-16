import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, factorial
import scipy.special as special

st.set_page_config(page_title="CHY1005 Quantum Hub", layout="wide")

# Sidebar Navigation
page = st.sidebar.selectbox("Navigate Unit 2", ["The Schrödinger Equation", "Radial Solutions", "Angular Solutions"])

# --- SECTION 1: SCHRÖDINGER EQUATION ---
if page == "The Schrödinger Equation":
    st.header("The Schrödinger Equation")
    st.write("Unit 2 focuses on the fundamental equation of Quantum Chemistry.")
    
    st.latex(r"H\psi = E\psi")
    
    st.subheader("Time-Independent Form")
    st.latex(r"-\frac{\hbar^2}{2m} \nabla^2 \psi + V\psi = E\psi")
    
    st.info("In this website, we solve this for the Hydrogen atom to find the Radial and Angular components.")

# --- SECTION 2: RADIAL SOLUTIONS ---
elif page == "Radial Solutions":
    st.header("Radial Wave Functions ($R_{nl}$)")
    st.write("Visualizing the probability of finding an electron at distance $r$.")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        n = st.slider("Principal Quantum Number (n)", 1, 4, 1)
        l = st.slider("Azimuthal Quantum Number (l)", 0, n-1, 0)
    
    # Math Logic
    a0 = 1.0 # Bohr radius units
    r = np.linspace(0, n**2 * 10, 500)
    rho = (2 * r) / (n * a0)
    norm = np.sqrt((2/(n*a0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    laguerre = genlaguerre(n-l-1, 2*l+1)
    R_nl = norm * np.exp(-rho/2) * (rho**l) * laguerre(rho)
    prob_density = r**2 * R_nl**2

    with col2:
        fig, ax = plt.subplots()
        ax.plot(r, prob_density, color='#1f77b4', lw=2)
        ax.fill_between(r, prob_density, alpha=0.2)
        ax.set_xlabel("r (Bohr radius units)")
        ax.set_ylabel("Probability Density $P(r)$")
        st.pyplot(fig)

# --- SECTION 3: ANGULAR SOLUTIONS ---
elif page == "Angular Solutions":
    st.header("Angular Solutions & Spherical Harmonics")
    st.write("These solutions define the shapes of the orbitals (s, p, d, f).")
    
    l_ang = st.slider("l (Orbital Shape)", 0, 3, 1) # 0=s, 1=p, 2=d
    m_ang = st.slider("m (Orientation)", -l_ang, l_ang, 0)
    
    # Create a 3D grid
    theta = np.linspace(0, np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # Calculate Spherical Harmonics
    Y_lm = sph_harm(m_ang, l_ang, phi, theta)
    r_coords = np.abs(Y_lm.real) # Simplified for visualization
    
    # Convert to Cartesian for 3D plotting
    x = r_coords * np.sin(theta) * np.cos(phi)
    y = r_coords * np.sin(theta) * np.sin(phi)
    z = r_coords * np.cos(theta)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='viridis', edgecolors='k', alpha=0.8)
    st.pyplot(fig)
