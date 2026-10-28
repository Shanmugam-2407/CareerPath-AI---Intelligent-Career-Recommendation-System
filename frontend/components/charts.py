"""
Plotly Chart components for data visualizations.
"""
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


def render_skill_match_gauge(match_percentage: float):
    """Renders an interactive Plotly gauge chart for skill match percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_percentage,
        number={"suffix": "%", "font": {"size": 42, "color": "#38bdf8"}},
        title={"text": "Target Career Skill Match", "font": {"size": 18, "color": "#f8fafc"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
            "bar": {"color": "#0284c7", "thickness": 0.25},
            "bgcolor": "#0f172a",
            "borderwidth": 2,
            "bordercolor": "#334155",
            "steps": [
                {"range": [0, 40], "color": "rgba(239, 68, 68, 0.2)"},
                {"range": [40, 75], "color": "rgba(245, 158, 11, 0.2)"},
                {"range": [75, 100], "color": "rgba(16, 185, 129, 0.2)"}
            ],
            "threshold": {
                "line": {"color": "#34d399", "width": 4},
                "thickness": 0.75,
                "value": match_percentage
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_domain_prediction_chart(rankings: list):
    """Renders a horizontal bar chart of top ML career domain probabilities."""
    # Take top 6
    top_ranks = rankings[:6]
    domains = [r["domain"] for r in reversed(top_ranks)]
    probs = [r["probability"] * 100 for r in reversed(top_ranks)]

    fig = go.Figure(go.Bar(
        x=probs,
        y=domains,
        orientation='h',
        marker=dict(
            color=probs,
            colorscale="Viridis",
            line=dict(color="#38bdf8", width=1)
        ),
        text=[f"{p:.1f}%" for p in probs],
        textposition="outside"
    ))

    fig.update_layout(
        title="ML Career Domain Probabilities",
        title_font=dict(size=18, color="#f8fafc"),
        xaxis=dict(title="Probability (%)", range=[0, 105], showgrid=True, gridcolor="#1e293b"),
        yaxis=dict(title="Domain", tickfont=dict(size=12, color="#e2e8f0")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_skill_gap_bar(known_count: int, missing_count: int):
    """Renders a stacked/grouped bar chart of Mastered vs Missing skills."""
    fig = go.Figure(data=[
        go.Bar(name="Mastered", x=["Skill Inventory"], y=[known_count], marker_color="#10b981"),
        go.Bar(name="Missing", x=["Skill Inventory"], y=[missing_count], marker_color="#ef4444")
    ])
    fig.update_layout(
        barmode='stack',
        title="Required Skills Composition",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=240,
        margin=dict(l=10, r=10, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_overall_progress_chart(completion_pct: float):
    """Renders a donut chart of overall curriculum progress."""
    remaining = max(100.0 - completion_pct, 0.0)
    labels = ["Completed", "Remaining"]
    values = [completion_pct, remaining]
    colors = ["#38bdf8", "#1e293b"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.7,
        marker=dict(colors=colors, line=dict(color="#0f172a", width=2)),
        textinfo='none'
    )])

    fig.update_layout(
        annotations=[dict(text=f"{completion_pct:.1f}%", x=0.5, y=0.5, font_size=28, font_color="#38bdf8", showarrow=False)],
        showlegend=True,
        legend=dict(font=dict(color="#94a3b8")),
        paper_bgcolor="rgba(0,0,0,0)",
        height=240,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
