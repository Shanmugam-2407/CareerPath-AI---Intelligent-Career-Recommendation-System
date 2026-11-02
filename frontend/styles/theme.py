"""
Theme, CSS design system, and custom visual styling for CareerPath AI.
Implements a premium, modern SaaS-grade interface with glassmorphism,
micro-interactions, responsive typography, and glowing accents.
"""

def get_custom_css() -> str:
    """Returns the master CSS stylesheet for the application."""
    return """
    <style>
        /* ==================== GLOBAL FONTS & BASE THEME ==================== */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg-primary: #0b0f19;
            --bg-secondary: #0f172a;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(56, 189, 248, 0.3);
            --border-hover: rgba(99, 102, 241, 0.4);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --cyan-accent: #06b6d4;
            --sky-accent: #38bdf8;
            --indigo-accent: #6366f1;
            --purple-accent: #8b5cf6;
            --emerald-accent: #10b981;
            --amber-accent: #f59e0b;
            --rose-accent: #f43f5e;
            --glass-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
            --glow-cyan: 0 0 20px rgba(6, 182, 212, 0.25);
            --glow-indigo: 0 0 20px rgba(99, 102, 241, 0.25);
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            -webkit-font-smoothing: antialiased;
        }

        /* Container padding */
        .main .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1380px !important;
        }

        /* Gradient Headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: #ffffff !important;
        }

        .gradient-text {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }

        .gradient-text-emerald {
            background: linear-gradient(135deg, #34d399 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }

        /* ==================== TOP NAVIGATION / APP HEADER ==================== */
        .app-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(90deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.6) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 12px 20px;
            margin-bottom: 24px;
            backdrop-filter: blur(16px);
            box-shadow: var(--glass-shadow);
        }

        .app-branding {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .app-logo-badge {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            box-shadow: var(--glow-cyan);
        }

        .app-title-group h2 {
            margin: 0 !important;
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            line-height: 1.2 !important;
        }

        .app-title-group p {
            margin: 0 !important;
            font-size: 0.78rem !important;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .app-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            background: rgba(16, 185, 129, 0.12);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 8px #10b981;
            animation: pulse-animation 2s infinite;
        }

        @keyframes pulse-animation {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        /* ==================== WORKFLOW STEPPER BAR ==================== */
        .stepper-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 10px 16px;
            margin-bottom: 24px;
            overflow-x: auto;
        }

        .step-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-muted);
            white-space: nowrap;
        }

        .step-item.active {
            color: var(--sky-accent);
        }

        .step-item.completed {
            color: var(--emerald-accent);
        }

        .step-circle {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
        }

        .step-item.active .step-circle {
            background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
            border-color: #38bdf8;
            color: #ffffff;
            box-shadow: var(--glow-cyan);
        }

        .step-item.completed .step-circle {
            background: rgba(16, 185, 129, 0.2);
            border-color: #10b981;
            color: #34d399;
        }

        .step-divider {
            flex-grow: 1;
            height: 2px;
            background: rgba(255, 255, 255, 0.08);
            min-width: 14px;
        }

        .step-divider.filled {
            background: linear-gradient(90deg, #10b981, #38bdf8);
        }

        /* ==================== MODERN CARDS & CONTAINERS ==================== */
        .saas-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.7) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 20px;
            backdrop-filter: blur(14px);
            box-shadow: var(--glass-shadow);
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .saas-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
            box-shadow: 0 14px 28px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
        }

        .saas-card-glow {
            border: 1px solid rgba(56, 189, 248, 0.25);
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.08), var(--glass-shadow);
        }

        /* Metric cards */
        .metric-card-pro {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .metric-card-pro:hover {
            border-color: var(--border-accent);
            transform: translateY(-3px);
            box-shadow: var(--glass-shadow), 0 0 15px rgba(56, 189, 248, 0.15);
        }

        .metric-card-pro::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #38bdf8 0%, #6366f1 100%);
            border-radius: 4px 0 0 4px;
        }

        .metric-label-pro {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .metric-value-pro {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #ffffff;
            margin: 4px 0 8px 0;
            line-height: 1.1;
        }

        .metric-subtext-pro {
            font-size: 0.8rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* ==================== BUTTONS & INTERACTIVE CONTROLS ==================== */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.55rem 1.25rem !important;
            letter-spacing: 0.01em !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
        }

        .stButton>button:active {
            transform: translateY(0px) !important;
        }

        /* Primary Button */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            color: #ffffff !important;
            box-shadow: 0 4px 15px rgba(2, 132, 199, 0.3) !important;
        }

        .stButton>button[kind="primary"]:hover {
            background: linear-gradient(135deg, #0369a1 0%, #4338ca 100%) !important;
            border-color: #38bdf8 !important;
            box-shadow: 0 6px 24px rgba(2, 132, 199, 0.45) !important;
        }

        /* Secondary Button */
        .stButton>button[kind="secondary"] {
            background: rgba(30, 41, 59, 0.7) !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }

        .stButton>button[kind="secondary"]:hover {
            background: rgba(51, 65, 85, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.25) !important;
        }

        /* ==================== FORM INPUTS & SELECTS ==================== */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div,
        .stMultiSelect>div>div {
            border-radius: 10px !important;
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #f8fafc !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
        }

        /* Multiselect Tag styling */
        .stMultiSelect span[data-baseweb="tag"] {
            background-color: rgba(2, 132, 199, 0.25) !important;
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 6px !important;
            color: #e0f2fe !important;
            font-weight: 500 !important;
        }

        /* Sliders */
        .stSlider>div>div>div>div {
            color: #38bdf8 !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(15, 23, 42, 0.6) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: #f1f5f9 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            transition: all 0.2s ease !important;
        }

        .streamlit-expanderHeader:hover {
            border-color: var(--border-accent) !important;
            background: rgba(30, 41, 59, 0.8) !important;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #070b14 0%, #0c1220 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
        }

        /* Radio nav in sidebar */
        [data-testid="stSidebar"] .stRadio>div {
            gap: 6px !important;
        }

        [data-testid="stSidebar"] .stRadio label {
            background: rgba(15, 23, 42, 0.4) !important;
            padding: 8px 14px !important;
            border-radius: 8px !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }

        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(30, 41, 59, 0.6) !important;
            border-color: rgba(255, 255, 255, 0.08) !important;
        }

        /* Pills and Badges */
        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .pill-emerald {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.35);
        }

        .pill-rose {
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.35);
        }

        .pill-cyan {
            background: rgba(6, 182, 212, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(6, 182, 212, 0.35);
        }

        .pill-indigo {
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.35);
        }

        .pill-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.35);
        }

        /* Timeline Node styling */
        .timeline-month-badge {
            background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.85rem;
            display: inline-block;
            margin-bottom: 8px;
        }

        .week-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 14px;
            height: 100%;
            transition: all 0.2s ease;
        }

        .week-card:hover {
            border-color: rgba(56, 189, 248, 0.3);
            background: rgba(30, 41, 59, 0.7);
        }

        /* Preset Card Buttons */
        .preset-badge {
            display: inline-block;
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 6px 12px;
            margin: 4px;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .preset-badge:hover {
            border-color: var(--sky-accent);
            background: rgba(56, 189, 248, 0.15);
        }

        /* Smooth scrollbar */
        ::-webkit-scrollbar {
            width: 7px;
            height: 7px;
        }
        ::-webkit-scrollbar-track {
            background: #070b14;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }

        /* ==================== HIDE DEFAULT STREAMLIT MULTIPAGE NAVIGATION ==================== */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"],
        ul[data-testid="stSidebarNavItems"],
        div[data-testid="stSidebarNav"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }
    </style>
    """

