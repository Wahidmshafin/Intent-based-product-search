"""
Streamlit frontend for Intent-Based Product Search.

A modern, responsive UI that connects to the FastAPI backend
for hybrid semantic + keyword product search.
"""

import requests
import streamlit as st

# ─── Configuration ─────────────────────────────────────────────────────────────
API_BASE_URL = "http://127.0.0.1:8000/api"
SEARCH_ENDPOINT = f"{API_BASE_URL}/search/"
HISTORY_ENDPOINT = f"{API_BASE_URL}/search/history"
FEEDBACK_ENDPOINT = f"{API_BASE_URL}/search/feedback"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/product/upload"

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Intent Product Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Fonts ──────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Overrides ─────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #f8fafc;
    }

    /* ── Hero Section ─────────────────────────────────────────────────────── */
    .hero-container {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        font-weight: 400;
        letter-spacing: 0.02em;
    }

    /* ── Search Form styling ─────────────────────────────────────────────── */
    .stForm {
        border: none !important;
        padding: 0 !important;
    }

    /* ── Search Input ─────────────────────────────────────────────────────── */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.2rem !important;
        font-size: 1.05rem !important;
        color: #334155 !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }

    /* ── Product Card ─────────────────────────────────────────────────────── */
    .product-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
    }
    .product-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899);
        opacity: 0;
        transition: opacity 0.35s ease;
    }
    .product-card:hover {
        transform: translateY(-4px);
        border-color: #cbd5e1;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
    }
    .product-card:hover::before {
        opacity: 1;
    }

    .product-rank {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.6rem;
    }

    .product-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }

    .product-meta {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-bottom: 0.75rem;
    }

    .meta-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 0.25rem 0.7rem;
        font-size: 0.78rem;
        color: #475569;
        font-weight: 600;
    }

    .product-description {
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.65;
        font-weight: 400;
    }

    /* ── Sidebar ──────────────────────────────────────────────────────────── */
    /* Sidebar Toggle Buttons (Expand/Collapse) */
    [data-testid="collapsedControl"] svg, 
    [data-testid="stSidebar"] button[kind="header"] svg {
        width: 32px !important;
        height: 32px !important;
        stroke-width: 2.5 !important;
        color: #7c3aed !important;
    }
    
    [data-testid="collapsedControl"]:hover svg,
    [data-testid="stSidebar"] button[kind="header"]:hover svg {
        color: #ec4899 !important;
        transform: scale(1.1);
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #334155;
        letter-spacing: 0.03em;
    }

    .history-item {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.65rem 0.9rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.25s ease;
        color: #475569;
        font-size: 0.88rem;
    }
    .history-item:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
        color: #0f172a;
    }

    /* ── Results Header ───────────────────────────────────────────────────── */
    .results-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .results-header-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: #334155;
    }
    .results-count {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.55rem;
        border-radius: 12px;
    }

    /* ── Spinner / Status ─────────────────────────────────────────────────── */
    .search-status {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 0.95rem;
    }

    /* ── Empty State ──────────────────────────────────────────────────────── */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
    }
    .empty-state-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    .empty-state-text {
        color: #475569;
        font-size: 1rem;
        font-weight: 500;
    }
    .empty-state-hint {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }

    /* ── Button Overrides ─────────────────────────────────────────────────── */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(124,58,237,0.25) !important;
    }

    /* ── Feedback buttons ─────────────────────────────────────────────────── */
    .feedback-section {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.75rem;
        padding-top: 0.6rem;
        border-top: 1px solid #e2e8f0;
    }

    /* ── Debug info ───────────────────────────────────────────────────────── */
    .debug-info {
        background: #fff7ed;
        border: 1px solid #fdba74;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-top: 1rem;
        color: #c2410c;
        font-size: 0.82rem;
        font-family: 'Courier New', monospace;
    }

    /* ── Divider ──────────────────────────────────────────────────────────── */
    hr {
        border-color: #e2e8f0 !important;
    }

    /* ── Hide default Streamlit elements ──────────────────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ──────────────────────────────────────────────────────────

def search_products(query: str) -> tuple[list[dict] | None, dict]:
    """
    Send search query to the backend API.
    Returns (results, debug_info) tuple.
    """
    debug = {"url": SEARCH_ENDPOINT, "payload": {"query": query}}
    try:
        response = requests.post(
            SEARCH_ENDPOINT,
            json={"query": query},
            timeout=120,
        )
        debug["status_code"] = response.status_code
        debug["raw_response"] = response.text[:500]
        response.raise_for_status()
        return response.json(), debug
    except requests.exceptions.ConnectionError:
        debug["error"] = "Connection refused — backend not reachable"
        st.error("⚠️ Could not connect to the backend. Make sure the API server is running on `localhost:8000`.")
        return None, debug
    except requests.exceptions.Timeout:
        debug["error"] = "Request timed out after 120s"
        st.error("⏱️ The search request timed out. Please try again.")
        return None, debug
    except requests.exceptions.HTTPError as e:
        debug["error"] = f"HTTP {e.response.status_code}: {e.response.text[:300]}"
        st.error(f"🚨 API Error: {e.response.status_code} — {e.response.text}")
        return None, debug


def fetch_history(limit: int = 10) -> list[dict]:
    """Fetch recent search history from the backend."""
    try:
        response = requests.post(
            HISTORY_ENDPOINT,
            params={"limit": limit},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return []


def upload_products(limit: int = 50) -> tuple[bool, str]:
    """Trigger product data import from HuggingFace via the backend API."""
    try:
        response = requests.post(
            UPLOAD_ENDPOINT,
            params={"limit": limit},
            timeout=600,  # Large timeout — embedding generation is slow
        )
        response.raise_for_status()
        data = response.json()
        return True, data.get("response", "Done")
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to the backend. Is the API server running?"
    except requests.exceptions.Timeout:
        return False, "Import timed out (>10 min). The server may still be processing."
    except requests.exceptions.HTTPError as e:
        return False, f"API Error {e.response.status_code}: {e.response.text[:200]}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def submit_feedback(history_id: int, feedback: int) -> bool:
    """Submit feedback for a search result."""
    try:
        response = requests.put(
            FEEDBACK_ENDPOINT,
            params={"id": history_id, "feedback": feedback},
            timeout=10,
        )
        response.raise_for_status()
        return True
    except Exception:
        return False


def render_product_card(product: dict, rank: int) -> None:
    """Render a single product result card."""
    title = product.get("title") or "Untitled Product"
    category = product.get("category")
    brand = product.get("brand")
    description = product.get("description") or "No description available."

    # Build meta badges
    badges = ""
    if category:
        badges += f'<span class="meta-badge">📂 {category}</span>'
    if brand:
        badges += f'<span class="meta-badge">🏷️ {brand}</span>'
    badges += f'<span class="meta-badge">🆔 {product.get("id", "N/A")}</span>'

    # Truncate description for display
    desc_display = description
    if len(desc_display) > 350:
        desc_display = desc_display[:350] + "…"

    card_html = f"""
    <div class="product-card">
        <div class="product-rank">{rank}</div>
        <div class="product-title">{title}</div>
        <div class="product-meta">{badges}</div>
        <div class="product-description">{desc_display}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# ─── Session State Initialization ─────────────────────────────────────────────
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "debug_info" not in st.session_state:
    st.session_state.debug_info = None


# ─── Sidebar: Search History ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🕐 Recent Searches")
    st.markdown("---")

    history = fetch_history(limit=15)
    if history:
        with st.container(height=300):
            for item in history:
                query_text = item.get("query", "")
                if st.button(
                    f"🔎  {query_text}",
                    key=f"hist_{item.get('id', query_text)}",
                    use_container_width=True,
                ):
                    st.session_state.last_query = query_text
                    st.session_state.pending_search = query_text
                    st.rerun()
    else:
        st.markdown(
            '<div style="color:#6060a0; font-size:0.85rem; padding:1rem 0;">'
            "No search history yet.<br>Start searching to build your history!"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Data Import Section ────────────────────────────────────────────────
    st.markdown("## 📦 Import Data")
    st.caption(
        "Load product data from HuggingFace (`wdc/products-2017`) "
        "into the database. Imports cameras, watches, computers & shoes."
    )

    import_limit = st.number_input(
        "Products per category",
        min_value=10,
        max_value=500,
        value=50,
        step=10,
        help="Number of products to import from each of the 4 categories.",
    )

    if st.button("🚀 Import from HuggingFace", use_container_width=True):
        with st.status("Importing products…", expanded=True) as status:
            st.write(f"⏳ Importing {import_limit} products × 4 categories…")
            st.write("This may take a few minutes (embedding generation).")
            success, message = upload_products(limit=import_limit)
            if success:
                status.update(label="✅ Import complete!", state="complete")
                st.success(f"Successfully imported! Response: **{message}**")
            else:
                status.update(label="❌ Import failed", state="error")
                st.error(message)

    st.markdown("---")

    # Debug toggle
    show_debug = st.checkbox("🛠️ Show debug info", value=False)

    st.markdown(
        '<div style="color:#4a4a6a; font-size:0.75rem; text-align:center; padding-top:0.5rem;">'
        "Intent-Based Product Search v1.0<br>"
        "Powered by Hybrid RAG 🚀"
        "</div>",
        unsafe_allow_html=True,
    )


# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🔍 Intent Based Product Search</div>
    <div class="hero-subtitle">
        Discover products using natural language — powered by hybrid semantic &amp; keyword search
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Search Bar (wrapped in a form so Enter key submits) ─────────────────────
col_pad_l, col_center, col_pad_r = st.columns([1, 8, 1])

with col_center:
    with st.form(key="search_form", clear_on_submit=False):
        form_cols = st.columns([6, 1.2])
        with form_cols[0]:
            query = st.text_input(
                label="Search",
                value=st.session_state.last_query,
                placeholder="e.g., comfortable running shoes for men, lightweight laptop for students…",
                label_visibility="collapsed",
                key="search_input",
            )
        with form_cols[1]:
            submitted = st.form_submit_button("🔍 Search", use_container_width=True)


# ─── Check for pending search from sidebar history click ─────────────────────
pending = st.session_state.pop("pending_search", None)
if pending:
    submitted = True
    query = pending


# ─── Trigger Search ──────────────────────────────────────────────────────────
if submitted:
    search_query = query.strip() if query else ""

    if search_query:
        st.session_state.last_query = search_query

        # Custom loading animation
        loading_placeholder = st.empty()
        loading_placeholder.markdown(
            '<div class="search-status">'
            "🔮 Analyzing your intent and searching across products…"
            "</div>",
            unsafe_allow_html=True,
        )

        results, debug = search_products(search_query)
        loading_placeholder.empty()

        st.session_state.search_results = results
        st.session_state.debug_info = debug
    else:
        st.warning("Please enter a search query.")


# ─── Display Results ──────────────────────────────────────────────────────────
results = st.session_state.search_results

if results is not None:
    if len(results) > 0:
        # Results header
        st.markdown(
            f"""
            <div class="results-header">
                <span class="results-header-text">Search Results</span>
                <span class="results-count">{len(results)} found</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Render product cards
        for idx, product in enumerate(results, start=1):
            render_product_card(product, rank=idx)

            # Expandable details
            with st.expander(f"📋 Full details — {product.get('title', 'Product')}"):
                detail_cols = st.columns([1, 1])
                with detail_cols[0]:
                    st.markdown(f"**ID:** `{product.get('id', 'N/A')}`")
                    st.markdown(f"**Category:** {product.get('category') or '—'}")
                    st.markdown(f"**Brand:** {product.get('brand') or '—'}")
                with detail_cols[1]:
                    st.markdown("**Full Description:**")
                    st.markdown(
                        product.get("description") or "No description available."
                    )
    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <div class="empty-state-text">No products found for your query.</div>
                <div class="empty-state-hint">Try rephrasing or using different keywords.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    # Initial empty state
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-state-icon">🛍️</div>
            <div class="empty-state-text">Search for products using natural language</div>
            <div class="empty-state-hint">
                Try: "red sneakers for running", "wireless noise-cancelling headphones",
                "organic cotton t-shirt"
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─── Debug Panel (toggled from sidebar) ──────────────────────────────────────
if show_debug and st.session_state.debug_info:
    debug = st.session_state.debug_info
    st.markdown("---")
    st.markdown(
        f"""
        <div class="debug-info">
            <strong>🛠️ Debug Info</strong><br>
            <b>Endpoint:</b> {debug.get('url', 'N/A')}<br>
            <b>Payload:</b> {debug.get('payload', 'N/A')}<br>
            <b>Status Code:</b> {debug.get('status_code', 'N/A')}<br>
            <b>Raw Response:</b> {debug.get('raw_response', 'N/A')}<br>
            <b>Error:</b> {debug.get('error', 'None')}
        </div>
        """,
        unsafe_allow_html=True,
    )
