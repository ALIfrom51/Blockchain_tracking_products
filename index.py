import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
from blockchain import track_product, update_package_status, delete_product, reset_chain, get_chain, get_product_by_hash, trace_product, verify_hash, verify_block


icon_image = Image.open("a-vector-style-square-app-icon-featuring_pgOpjoI1TFGE-RYogOwFog_KdaVpDM6TXKByWgF7K9z9A_sd.jpeg")

# Load and convert technical background image to base64
def get_image_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

background_image_base64 = get_image_base64("a-technical-infographic-photograph-showi_ly5dvZHkT6ah8eCcU57-LQ_dBQhsEMzQkOu34WXDa0x-A_sd.jpeg")

st.set_page_config(
    page_title="Traçabilité colis sécurisée",
    page_icon=icon_image,
    layout="wide",
)

# Premium Theme with Technical Background Image
luxury_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
        letter-spacing: 0.01em;
    }}
    
    /* Premium Background with Technical Image */
    .stApp {{
        background-image: url('data:image/jpeg;base64,{background_image_base64}') !important;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        min-height: 100vh;
        position: relative;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(0, 26, 77, 0.75) 0%,
            rgba(13, 59, 13, 0.65) 25%,
            rgba(0, 0, 0, 0.8) 50%,
            rgba(10, 74, 122, 0.7) 75%,
            rgba(0, 26, 77, 0.75) 100%);
        pointer-events: none;
        z-index: 1;
    }}
    
    /* Ensure content appears over the overlay */
    [data-testid="stAppViewContainer"] {{
        position: relative;
        z-index: 2;
        background: transparent !important;
    }}
    
    /* Remove default streamlit background */
    [data-testid="stAppViewContainer"] > div {{
        background: transparent !important;
    }}
    
    [data-testid="stSidebar"] {{
        background: rgba(0, 26, 77, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid rgba(0, 212, 255, 0.3) !important;
    }}
    
    /* Premium Glass Panels - White semi-transparent */
    [data-testid="stMetricContainer"],
    [data-testid="stForm"],
    [data-testid="stExpander"],
    [data-testid="stAlert"],
    [data-testid="dataFrameContainer"] {{
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(25px) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
        border-radius: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 212, 255, 0.15), 
                    0 0 0 1px rgba(0, 212, 255, 0.1) inset !important;
    }}
    
    /* Typography - Poppins Geometric Sans-Serif */
    h1, h2, h3 {{
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        letter-spacing: -0.01em;
        background: linear-gradient(135deg, #00d084 0%, #0077be 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 10px rgba(0, 208, 132, 0.1);
    }}
    
    h1 {{
        font-size: 3rem !important;
        letter-spacing: -0.015em;
    }}
    
    h2 {{
        font-size: 2rem !important;
        letter-spacing: -0.01em;
    }}
    
    h3 {{
        font-size: 1.3rem !important;
        letter-spacing: -0.005em;
    }}
    
    /* Text styling */
    p, [data-testid="stMarkdownContainer"] {{
        color: #ffffff;
        font-weight: 400;
        line-height: 1.8;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }}
    
    /* Metric cards - Cyan & Green glow */
    [data-testid="metric-container"] {{
        background: rgba(0, 212, 255, 0.08) !important;
        border: 2px solid rgba(0, 212, 255, 0.4) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 
            0 8px 32px 0 rgba(0, 212, 255, 0.2),
            0 0 20px rgba(0, 208, 132, 0.15) inset,
            0 0 0 1px rgba(0, 212, 255, 0.2) inset !important;
        backdrop-filter: blur(20px);
    }}
    
    /* Pearlescent Buttons - Blue & Green */
    button {{
        background: linear-gradient(135deg, 
            rgba(0, 212, 255, 0.4) 0%,
            rgba(0, 208, 132, 0.5) 50%,
            rgba(10, 74, 122, 0.6) 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        border: 1.5px solid rgba(0, 212, 255, 0.6) !important;
        padding: 14px 28px !important;
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 
            0 8px 24px rgba(0, 212, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            inset 0 -1px 0 rgba(0, 208, 132, 0.2) !important;
    }}
    
    button:hover {{
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 
            0 12px 40px rgba(0, 212, 255, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.5),
            inset 0 -2px 5px rgba(0, 208, 132, 0.4) !important;
    }}
    
    button:active {{
        transform: translateY(-2px) scale(0.98) !important;
    }}
    
    /* Input fields */
    input, textarea, select {{
        background: rgba(0, 26, 77, 0.5) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        font-family: 'Poppins', sans-serif;
        font-size: 14px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.1) !important;
    }}
    
    input::placeholder, textarea::placeholder {{
        color: rgba(0, 212, 255, 0.5) !important;
    }}
    
    input:focus, textarea:focus, select:focus {{
        border-color: #00d084 !important;
        box-shadow: 
            0 0 30px rgba(0, 208, 132, 0.4),
            inset 0 0 10px rgba(0, 208, 132, 0.1) !important;
        background: rgba(0, 208, 132, 0.08) !important;
    }}
    
    /* Info/success/warning boxes */
    [data-testid="stAlert"] {{
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
        border-radius: 18px !important;
        color: #ffffff !important;
        backdrop-filter: blur(20px);
        padding: 16px 20px !important;
    }}
    
    /* Dataframe styling */
    [data-testid="dataFrameContainer"] {{
        background: rgba(0, 212, 255, 0.06) !important;
        border-radius: 20px !important;
        border: 1.5px solid rgba(0, 212, 255, 0.3) !important;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(0, 212, 255, 0.1) !important;
    }}
    
    /* Expander */
    [data-testid="stExpander"] {{
        border: 1.5px solid rgba(0, 212, 255, 0.35) !important;
        border-radius: 16px !important;
        background: rgba(0, 212, 255, 0.05) !important;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebarNav"] {{
        background: transparent;
    }}
    
    /* Radio button styling */
    [role="radiogroup"] {{
        background: rgba(0, 212, 255, 0.08) !important;
        padding: 16px !important;
        border-radius: 16px !important;
        border: 1.5px solid rgba(0, 212, 255, 0.3) !important;
        backdrop-filter: blur(15px);
    }}
    
    /* Horizontal line styling */
    hr {{
        border-color: rgba(0, 212, 255, 0.25) !important;
    }}
    
    /* Status Badges - Green, Blue, Navy, Black Palette */
    .status-ordered {{
        background: linear-gradient(135deg, #0077be 0%, #00a6d6 100%) !important;
        color: #fff;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(0, 119, 190, 0.4);
    }}
    
    .status-shipped {{
        background: linear-gradient(135deg, #001a4d 0%, #0077be 100%) !important;
        color: #fff;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(0, 26, 77, 0.4);
    }}
    
    .status-delivered {{
        background: linear-gradient(135deg, #00d084 0%, #1a5c1a 100%) !important;
        color: #fff;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(0, 208, 132, 0.4);
    }}
</style>
"""

st.markdown(luxury_css, unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image(icon_image, width=80)
with col2:
    st.title("Global Logistics Tracker")

st.markdown("---")
st.write(
    "🌿 Secure logistics tracking with blockchain technology. "
    "Professional green & blue interface with navy foundations and black accents for ultimate trust."
)
st.markdown("---")


def normalize_block(block):
    data = block.get("data")
    status = verify_block(block)
    if isinstance(data, dict):
        return {
            "index": block.get("index"),
            "timestamp": block.get("timestamp"),
            "package_id": data.get("product_id", "—"),
            "name": data.get("name", "—"),
            "quantity": str(data.get("quantity", "—")),
            "location": data.get("location", "—"),
            "status": data.get("status", data.get("note", data.get("reason", "—"))),
            "tracked_at": data.get("tracked_at", data.get("event_at", "—")),
            "hash": block.get("hash"),
            "previous_hash": block.get("previous_hash"),
            "hash_valid": "Valide" if status else "Invalide",
            "raw_data": data,
        }

    return {
        "index": block.get("index"),
        "timestamp": block.get("timestamp"),
        "package_id": "—",
        "name": "—",
        "quantity": "—",
        "location": "—",
        "tracked_at": "—",
        "hash": block.get("hash"),
        "previous_hash": block.get("previous_hash"),
        "hash_valid": "Valide" if status else "Invalide",
        "raw_data": data,
    }


def load_chain_data():
    chain = get_chain()
    normalized = [normalize_block(block) for block in chain]
    return pd.DataFrame(normalized)


def get_status_color(status):
    """Return HTML color badge for shipping status - Green, Blue, Navy, Black palette"""
    status_colors = {
        "Ordered": '<span style="background: linear-gradient(135deg, #0077be 0%, #00a6d6 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(0, 119, 190, 0.4);">📦 Ordered</span>',
        "Shipped": '<span style="background: linear-gradient(135deg, #001a4d 0%, #0077be 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(0, 26, 77, 0.4);">✈️ Shipped</span>',
        "Delivered": '<span style="background: linear-gradient(135deg, #00d084 0%, #1a5c1a 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(0, 208, 132, 0.4);">✅ Delivered</span>',
        "In transit": '<span style="background: linear-gradient(135deg, #0a4a7a 0%, #00b8d4 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(10, 74, 122, 0.4);">🚀 In Transit</span>',
        "Arrivé au centre de tri": '<span style="background: linear-gradient(135deg, #0d6b3a 0%, #00c869 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(13, 107, 58, 0.4);">📍 Hub</span>',
        "En cours de livraison": '<span style="background: linear-gradient(135deg, #00a6d6 0%, #0077be 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(0, 166, 214, 0.4);">🚗 On The Way</span>',
        "Livré": '<span style="background: linear-gradient(135deg, #00d084 0%, #1a5c1a 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(0, 208, 132, 0.4);">✅ Delivered</span>',
        "Retenu": '<span style="background: linear-gradient(135deg, #1a1a1a 0%, #0d3b0d 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 700; box-shadow: 0 4px 15px rgba(26, 26, 26, 0.4);">⚠️ On Hold</span>',
    }
    return status_colors.get(status, '<span style="color: #fff; padding: 8px 16px;">—</span>')


sidebar_page = st.sidebar.radio(
    "NAVIGATION",
    ["Tableau de bord", "Suivi de colis", "Mise à jour livraison", "Suppression de colis", "Réinitialisation", "Traçage par ID", "Vérification par hash", "Explorateur"],
    label_visibility="visible"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🟢 TRUSTED LOGISTICS")
st.sidebar.write(
    "Enterprise-grade package tracking secured by blockchain. "
    "Green & blue technology for verified, immutable supply chains."
)
st.sidebar.info(
    "🔐 Navy-black foundations with cyan accents for professional security and transparency."
)

if sidebar_page == "Tableau de bord":
    chain = get_chain()
    df = load_chain_data()
    st.markdown("### ADVANCED LOGISTICS DASHBOARD")
    st.markdown("")

    valid_blocks = len(df[df["hash_valid"] == "Valide"])
    invalid_blocks = len(df[df["hash_valid"] == "Invalide"])
    tracked_packages = len([b for b in chain if isinstance(b.get("data"), dict)])

    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.metric("Total Tracking", len(chain))
    with col2:
        st.metric("Active Shipments", tracked_packages)
    with col3:
        st.metric("Verified Blocks", valid_blocks)
    with col4:
        st.metric("Security Alerts", invalid_blocks)

    st.markdown("---")
    
    # Status Information
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown(get_status_color("Ordered"), unsafe_allow_html=True)
        st.caption("Order Placed")
    with col2:
        st.markdown(get_status_color("Shipped"), unsafe_allow_html=True)
        st.caption("🔵 In Transit")
    with col3:
        st.markdown(get_status_color("Delivered"), unsafe_allow_html=True)
        st.caption("🟢 Delivered")

    st.markdown("---")
    st.markdown("### 📊 Blockchain Integrity Report")
    st.info(
        "🔐 Invalid blocks indicate that shipment data no longer matches the stored hash. "
        "This alert may signal tampering or data entry errors."
    )

    st.markdown("### 📋 Recent Shipments")
    if len(df) > 1:
        st.dataframe(
            df.iloc[::-1].head(5)[["index", "timestamp", "package_id", "name", "quantity", "location", "status", "hash", "hash_valid"]],
            use_container_width=True
        )
    else:
        st.info("No shipments tracked yet. Start by registering your first package!")

    st.markdown("---")
    st.markdown("### Why Blockchain for Enterprise Logistics?")
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.write("🔐 **Immutability**\nOnce recorded, shipment data cannot be altered or manipulated.")
    with col2:
        st.write("🌐 **Total Transparency**\nReal-time visibility across the entire supply chain ecosystem.")
    with col3:
        st.write("✨ **Trusted Verification**\nCryptographic proof of delivery and authenticity for all parties.")

elif sidebar_page == "Suivi de colis":
    st.markdown("###  REGISTER NEW SHIPMENT")
    st.markdown("")
    with st.form("tracking_form"):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            package_id = st.text_input("🏷️ Shipment ID", max_chars=64)
            quantity = st.number_input("📊 Quantity", min_value=0, step=1, format="%d")
        with col2:
            name = st.text_input("📦 Shipment Name / Content")
            location = st.text_input("📍 Current Location (Origin)")
        recipient_location = st.text_input("🎯 Recipient Location")
        submitted = st.form_submit_button("🟢 Register Shipment")

    if submitted:
        if not package_id or not name or not location or not recipient_location:
            st.warning("Please fill all fields before registering a shipment.")
        else:
            block = track_product(package_id, name, quantity, location, recipient_location)
            st.success("Shipment registered successfully.")
            st.write("**Block Details:**")
            st.json(block)
            st.info(f"Hash registered: `{block['hash']}`")
            st.success("This hash allows you to verify later that the shipment has not been modified.")

elif sidebar_page == "Mise à jour livraison":
    st.markdown("### UPDATE SHIPMENT STATUS")
    st.markdown("")
    with st.form("delivery_update_form"):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            package_id = st.text_input("🏷️ Shipment ID", max_chars=64)
            status = st.selectbox(
                "📍 Shipment Status",
                ["En transit", "Arrivé au centre de tri", "En cours de livraison", "Livré", "Retenu"],
            )
        with col2:
            location = st.text_input("📌 Current Location")
            note = st.text_area("💬 Comments / Notes (Optional)")
        submitted = st.form_submit_button("Update Status")

    if submitted:
        if not package_id or not location:
            st.warning("Please enter the Shipment ID and current location.")
        else:
            block = update_package_status(package_id, status, location, note)
            st.success("Delivery update recorded.")
            st.write("**Event Details:**")
            st.json(block)
            st.info(f"Hash registered: `{block['hash']}`")
            st.success("This update is now traceable in the blockchain.")

elif sidebar_page == "Suppression de colis":
    st.markdown("### REMOVE SHIPMENT")
    st.markdown("")
    with st.form("deletion_form"):
        col1, col2 = st.columns(2, gap="large")
        with col1:
            package_id = st.text_input("🏷️ Shipment ID to Remove", max_chars=64)
        with col2:
            reason = st.selectbox(
                "⚠️ Deletion Reason",
                ["Annulé par le client", "Perdu en transit", "Endommagé", "Autre"],
            )
        submitted = st.form_submit_button("Remove Shipment")

    if submitted:
        if not package_id:
            st.warning("Please enter the Shipment ID to remove.")
        else:
            block = delete_product(package_id, reason)
            st.success("Removal recorded in the blockchain.")
            st.write("**Deletion Details:**")
            st.json(block)
            st.info(f"Hash registered: `{block['hash']}`")
            st.warning("The shipment is now marked as removed. This action is irreversible.")

elif sidebar_page == "Réinitialisation":
    st.markdown("### RESET BLOCKCHAIN")
    st.markdown("")
    st.warning("⚠️ **WARNING**: This action will delete ALL blockchain data and restart with an empty chain. Only the genesis block will be preserved.")
    st.markdown("")

    if st.button("Confirm Reset", type="primary"):
        reset_chain()
        st.success("Blockchain has been reset successfully.")
        st.info("All data has been deleted. You can now start fresh with new shipments.")
        st.rerun()

elif sidebar_page == "Traçage par ID":
    st.markdown("### TRACK BY SHIPMENT ID")
    st.markdown("")
    package_id = st.text_input("🏷️ Shipment ID to Search")
    if st.button("🔎 Search History"):
        if not package_id:
            st.warning("Please enter a Shipment ID.")
        else:
            history = trace_product(package_id)
            if not history:
                st.error("No history found for this Shipment ID.")
            else:
                st.success(f"{len(history)} block(s) found for shipment {package_id}.")
                for block in history:
                    status = "Valid" if verify_block(block) else "Invalid"
                    st.markdown(f"**Block #{block['index']} — Integrity: {status}**")
                    if status == "Invalid":
                        st.warning("This block appears to be altered. The data no longer matches the stored hash.")
                    st.json(block)
                    st.markdown("---")

elif sidebar_page == "Vérification par hash":
    st.markdown("### VERIFY BLOCK INTEGRITY")
    st.markdown("")
    hash_code = st.text_input("🔐 Block Hash Code")
    if st.button("Verify Block"):
        if not hash_code:
            st.warning("Please enter a hash code.")
        else:
            block = get_product_by_hash(hash_code)
            if block is None:
                st.error("No block found for this hash.")
            else:
                verified = verify_hash(hash_code)
                if verified:
                    st.success("Block is valid and has not been modified.")
                else:
                    st.error("Block has been tampered with: the hash no longer matches.")
                st.json(block)

else:
    st.markdown("### 🔗 BLOCKCHAIN EXPLORER")
    st.markdown("")
    df = load_chain_data()
    if df.empty:
        st.info("Blockchain is empty. Register your first shipment to begin tracking!")
    else:
        st.dataframe(df[["index", "timestamp", "package_id", "name", "quantity", "location", "hash", "hash_valid"]], use_container_width=True)
        with st.expander(" View Raw Blocks"):
            for block in get_chain():
                status = "Valid" if verify_block(block) else "Invalid"
                st.markdown(f"**Block #{block['index']} — Integrity: {status}**")
                if status == "Invalid":
                    st.warning("This block is suspicious: it may have been modified.")
                st.json(block)
                st.markdown("---")
