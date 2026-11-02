"""
Plotly Chart components for data visualizations.
Modern SaaS dark-mode charts with responsive layouts and glowing accents.
"""
import plotly.graph_objects as go
import streamlit as st
from typing import List, Dict, Any


def render_skill_match_gauge(match_percentage: float):
    """Renders an interactive Plotly gauge chart for target domain skill match percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_percentage,
        number={
            "suffix": "%",
            "font": {"size": 44, "color": "#38bdf8", "family": "Plus Jakarta Sans"}
        },
        title={
            "text": "<b>Target Career Readiness</b>",
            "font": {"size": 16, "color": "#f8fafc", "family": "Plus Jakarta Sans"}
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#64748b",
                "tickfont": {"color": "#94a3b8", "size": 10}
            },
            "bar": {"color": "#38bdf8", "thickness": 0.28},
            "bgcolor": "rgba(15, 23, 42, 0.8)",
            "borderwidth": 1,
            "bordercolor": "rgba(255, 255, 255, 0.1)",
            "steps": [
                {"range": [0, 40], "color": "rgba(239, 68, 68, 0.25)"},
                {"range": [40, 75], "color": "rgba(245, 158, 11, 0.25)"},
                {"range": [75, 100], "color": "rgba(16, 185, 129, 0.25)"}
            ],
            "threshold": {
                "line": {"color": "#10b981", "width": 4},
                "thickness": 0.75,
                "value": match_percentage
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=270,
        margin=dict(l=25, r=25, t=50, b=25)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_domain_prediction_chart(rankings: List[Dict[str, Any]]):
    """Renders a sleek horizontal bar chart of top ML career domain probabilities."""
    top_ranks = rankings[:6] if rankings else []
    if not top_ranks:
        st.info("No probability distributions available.")
        return

    domains = [r["domain"] for r in reversed(top_ranks)]
    probs = [r["probability"] * 100 for r in reversed(top_ranks)]

    # Modern color gradient based on rank
    colors = [
        f"rgba({int(56 + i * 20)}, {int(189 - i * 15)}, 248, {0.9 - i * 0.08})"
        for i in range(len(probs))
    ]

    fig = go.Figure(go.Bar(
        x=probs,
        y=domains,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color="rgba(56, 189, 248, 0.4)", width=1),
            cornerradius=4
        ),
        text=[f"<b>{p:.1f}%</b>" for p in probs],
        textposition="outside",
        textfont=dict(color="#f8fafc", size=12, family="Plus Jakarta Sans"),
        hovertemplate="<b>%{y}</b><br>Confidence Probability: %{x:.2f}%<extra></extra>"
    ))

    fig.update_layout(
        title={
            "text": "<b>Top ML Career Domain Probabilities</b>",
            "font": {"size": 16, "color": "#f8fafc", "family": "Plus Jakarta Sans"}
        },
        xaxis=dict(
            title=dict(text="Probability Confidence (%)", font=dict(color="#94a3b8", size=12)),
            range=[0, 115],
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.06)",
            tickfont=dict(color="#94a3b8")
        ),
        yaxis=dict(
            tickfont=dict(size=12, color="#e2e8f0", family="Plus Jakarta Sans"),
            showgrid=False
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=10, r=25, t=50, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_skill_gap_bar(known_count: int, missing_count: int):
    """Renders a stacked composition bar chart of Mastered vs Missing skills."""
    fig = go.Figure(data=[
        go.Bar(
            name="Mastered Skills",
            x=["Requirements"],
            y=[known_count],
            marker_color="rgba(16, 185, 129, 0.85)",
            marker_line=dict(color="#10b981", width=1.5),
            text=[f"{known_count} Mastered"],
            textposition="inside",
            textfont=dict(color="#ffffff", size=12, family="Plus Jakarta Sans")
        ),
        go.Bar(
            name="Missing Skills",
            x=["Requirements"],
            y=[missing_count],
            marker_color="rgba(239, 68, 68, 0.85)",
            marker_line=dict(color="#ef4444", width=1.5),
            text=[f"{missing_count} Missing"],
            textposition="inside",
            textfont=dict(color="#ffffff", size=12, family="Plus Jakarta Sans")
        )
    ])

    fig.update_layout(
        barmode='stack',
        title={
            "text": "<b>Domain Skill Inventory Breakdown</b>",
            "font": {"size": 15, "color": "#f8fafc", "family": "Plus Jakarta Sans"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        height=240,
        margin=dict(l=10, r=10, t=40, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94a3b8", size=11)
        ),
        xaxis=dict(showgrid=False, tickfont=dict(color="#cbd5e1")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.06)", tickfont=dict(color="#94a3b8"))
    )
    st.plotly_chart(fig, use_container_width=True)


def render_overall_progress_chart(completion_pct: float):
    """Renders an interactive glowing donut chart of overall curriculum completion."""
    completion_pct = min(max(completion_pct, 0.0), 100.0)
    remaining = max(100.0 - completion_pct, 0.0)

    labels = ["Completed", "Remaining"]
    values = [completion_pct, remaining]
    colors = ["#38bdf8", "rgba(30, 41, 59, 0.6)"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.72,
        marker=dict(colors=colors, line=dict(color="#0f172a", width=2)),
        textinfo='none',
        hoverinfo='label+percent'
    )])

    fig.update_layout(
        annotations=[dict(
            text=f"<b>{completion_pct:.1f}%</b><br><span style='font-size:11px;color:#94a3b8;'>Progress</span>",
            x=0.5, y=0.5,
            font_size=26,
            font_color="#38bdf8",
            font_family="Plus Jakarta Sans",
            showarrow=False
        )],
        showlegend=True,
        legend=dict(
            font=dict(color="#94a3b8", size=11),
            orientation="h",
            xanchor="center",
            x=0.5,
            y=-0.1
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=10, r=10, t=10, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
