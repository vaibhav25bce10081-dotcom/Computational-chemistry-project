import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import genlaguerre, factorial, sph_harm # Import directly
import scipy.special as special # Also import as special just in case

st.set_page_config(page_title="CHY1005 Quantum Hub", layout="wide")

page = st.sidebar.selectbox("Navigate Unit 2", ["The Schrödinger Equation", "Radial Solutions", "Angular Solutions"])

if page == "The Schrödinger Equation":
    st.header("The Schrödinger Equation")
    st.latex(r"H\psi = E\psi")
    st.info("Solving for the Hydrogen atom leads to the plots in the other sections.")

elif page == "Radial Solutions":
    st.header("Radial Wave Functions ($R_{nl}$)")
    n = st.slider("n", 1, 4, 1)
    l = st.slider("l", 0, n-1, 0)
    
    r = np.linspace(0, n**2 * 10, 500)
    rho = (2 * r) / (n * 1.0)
    norm = np.sqrt((2/n)**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    laguerre = genlaguerre(n-l-1, 2*l+1)
    R_nl = norm * np.exp(-rho/2) * (rho**l) * laguerre(rho)
    
    fig, ax = plt.subplots()
    ax.plot(r, r**2 * R_nl**2)
    st.pyplot(fig)

elif page == "Angular Solutions":
    st.header("Angular Solutions (Orbital Shapes)")
    l_ang = st.slider("l", 0, 3, 1)
    m_ang = st.slider("m", -l_ang, l_ang, 0)
    
    theta = np.linspace(0, np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    # FIXED LINE: Using the direct import name
    Y_lm = sph_harm(m_ang, l_ang, phi, theta)
    
    r_coords = np.abs(Y_lm.real)
    x = r_coords * np.sin(theta) * np.cos(phi)
    y = r_coords * np.sin(theta) * np.sin(phi)
    z = r_coords * np.cos(theta)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='magma')
    st.pyplot(fig)
