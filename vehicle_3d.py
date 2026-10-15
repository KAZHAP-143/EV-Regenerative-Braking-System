
import plotly.graph_objects as go


def create_vehicle_3d(position=0):
    fig = go.Figure()

    # Vehicle body
    fig.add_trace(go.Mesh3d(
        x=[position, position+4, position+4, position,
           position, position+4, position+4, position],
        y=[-1, -1, 1, 1, -1, -1, 1, 1],
        z=[0.5, 0.5, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5],
        i=[0, 0, 0, 1, 1, 2, 3, 4, 4, 5, 6, 6],
        j=[1, 2, 4, 2, 5, 3, 7, 5, 6, 6, 7, 4],
        k=[2, 4, 5, 5, 6, 7, 4, 6, 7, 7, 4, 7],
        color="royalblue",
        opacity=1,
        name="EV Body"
    ))

    # Road surface
    fig.add_trace(go.Surface(
        x=[[-20, 100], [-20, 100]],
        y=[[-5, -5], [5, 5]],
        z=[[0, 0], [0, 0]],
        colorscale=[[0, "gray"], [1, "gray"]],
        showscale=False,
        name="Road"
    ))

    fig.update_layout(
        title="3D Electric Vehicle Simulation",
        scene=dict(
            xaxis=dict(
    title="Distance (m)",
    range=[position - 10, position + 15]
),
yaxis=dict(
    title="Road Width (m)",
    range=[-6, 6]
),
zaxis=dict(
    title="Height (m)",
    range=[0, 6]
),
camera=dict(
    eye=dict(x=1.8, y=-2.2, z=1.2)
),
            xaxis_title="Distance (m)",
            yaxis_title="Road Width (m)",
            zaxis_title="Height (m)",
            aspectmode="data"
        ),
        height=550,
        showlegend=False
    )

    return fig
