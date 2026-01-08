import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Calculus Gradient Visualizer", layout="wide")

st.title("MAT201: Gradient & Steepest Ascent Visualizer")
st.markdown("""
This interactive tool demonstrates the geometric meaning of the **Gradient**.
The gradient vector $\\nabla f$ always points in the direction of the greatest rate of increase (steepest ascent).
""")

# --- Sidebar: Controls ---
st.sidebar.header("1. Select Function & Parameters")

# Define function options
function_option = st.sidebar.selectbox(
    "Choose a surface f(x, y):",
    ("Paraboloid (Simple): x^2 + y^2", 
     "Saddle Surface (Medium): x^2 - y^2", 
     "Wave Surface (Complex): sin(x) * cos(y)")
)

st.sidebar.subheader("2. Move Point P(x, y)")
x_val = st.sidebar.slider("X Coordinate", -2.0, 2.0, 1.0, 0.1)
y_val = st.sidebar.slider("Y Coordinate", -2.0, 2.0, 1.0, 0.1)

# --- Math Logic ---
x = np.linspace(-2.5, 2.5, 50)
y = np.linspace(-2.5, 2.5, 50)
X, Y = np.meshgrid(x, y)

if "Paraboloid" in function_option:
    Z = X**2 + Y**2
    # Calculate Z for the point
    z_point = x_val**2 + y_val**2
    # Calculate Partial Derivatives (Gradient)
    dz_dx = 2 * x_val
    dz_dy = 2 * y_val
    func_str = "f(x,y) = x^2 + y^2"
    
elif "Saddle" in function_option:
    Z = X**2 - Y**2
    z_point = x_val**2 - y_val**2
    dz_dx = 2 * x_val
    dz_dy = -2 * y_val
    func_str = "f(x,y) = x^2 - y^2"

else: # Wave
    Z = np.sin(X) * np.cos(Y)
    z_point = np.sin(x_val) * np.cos(y_val)
    dz_dx = np.cos(x_val) * np.cos(y_val)
    dz_dy = -np.sin(x_val) * np.sin(y_val)
    func_str = "f(x,y) = sin(x)cos(y)"

# --- Main Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Calculations")
    st.info(f"**Current Point:** P({x_val}, {y_val})")
    st.markdown("The Gradient Vector formula:")
    st.latex(r"\nabla f = \left[ \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right]")
    
    st.write("Calculated Gradient Vector at P:")
    st.latex(f"\\vec{{v}} = [{dz_dx:.2f}, {dz_dy:.2f}]")
    
    st.success("""
    **Observation:**
    The RED arrow represents the gradient vector.
    Notice how it always points 'uphill' in the steepest direction from the red dot.
    """)

# --- 3D Visualization ---
with col2:
    fig = go.Figure()

    # 1. Plot the Surface
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8, name='Surface'))

    # 2. Plot the Point
    fig.add_trace(go.Scatter3d(
        x=[x_val], y=[y_val], z=[z_point],
        mode='markers', marker=dict(size=8, color='red'),
        name='Point P'
    ))

    # 3. Plot the Gradient Arrow
    # Scale arrow to make it visible but not overwhelming
    scale = 0.5 
    fig.add_trace(go.Cone(
        x=[x_val], y=[y_val], z=[z_point],
        u=[dz_dx], v=[dz_dy], w=[abs(dz_dx)+abs(dz_dy)], # Pointing slightly up for visibility
        sizemode="absolute", sizeref=scale, anchor="tail",
        colorscale=[[0, 'red'], [1, 'red']], showscale=False,
        name='Gradient Direction'
    ))

    fig.update_layout(
        title=f"3D View: {func_str}",
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Real World Application Section ---
st.divider()
st.subheader("Real World Application: Gradient Descent in AI")
st.markdown("""
The concept of the **Gradient** is not just theoretical calculus; it is the engine behind modern **Artificial Intelligence**.

1.  **Machine Learning Training:** When training a neural network (like ChatGPT or Gemini), we define a "Loss Function" which represents the error of the model. This looks like a multi-dimensional valley.
2.  **Optimization:** To minimize error, algorithms calculate the gradient to find the direction of steepest ascent.
3.  **Gradient Descent:** The model then moves in the **opposite direction** (steepest descent) to reach the bottom of the valley (minimum error).

*This application visualizes how calculating partial derivatives helps us find direction in complex multi-dimensional spaces.*
""")
