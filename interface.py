import streamlit as st
import pandas as pd
from blockchain import track_product, update_package_status, delete_product, reset_chain, get_chain, get_product_by_hash, trace_product, verify_hash, verify_block


st.set_page_config(
    page_title="Traçabilité colis sécurisée",
    page_icon="🔐",
    layout="wide",
)

st.title("🔐 Traçabilité sécurisée des colis")
st.write(
    "Plateforme de cybersécurité pour une société de livraison : chaque colis est tracé, horodaté "
    "et vérifié avec la blockchain afin de détecter toute falsification."
)


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


sidebar_page = st.sidebar.radio(
    "Navigation",
    ["Tableau de bord", "Suivi de colis", "Mise à jour livraison", "Suppression de colis", "Réinitialisation", "Traçage par ID", "Vérification par hash", "Explorateur"],
)

st.sidebar.markdown("## Contexte cybersécurité")
st.sidebar.write(
    "Application de suivi de colis pour une société de livraison sécurisée. "
    "Chaque bloc contient les données d’un colis, le hash précédent et le hash actuel."
)
st.sidebar.info(
    "Ce système permet de détecter toute modification frauduleuse des données de livraison."
)

if sidebar_page == "Tableau de bord":
    chain = get_chain()
    df = load_chain_data()
    st.subheader("Tableau de bord")

    valid_blocks = len(df[df["hash_valid"] == "Valide"])
    invalid_blocks = len(df[df["hash_valid"] == "Invalide"])
    tracked_packages = len([b for b in chain if isinstance(b.get("data"), dict)])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de blocs", len(chain))
    col2.metric("Colis suivis", tracked_packages)
    col3.metric("Blocs valides", valid_blocks)
    col4.metric("Blocs suspects", invalid_blocks)

    st.markdown("---")
    st.info(
        "Un bloc invalide indique que les données du colis ne correspondent plus au hash stocké. "
        "Cette alerte peut signaler une falsification ou une erreur de saisie."
    )

    st.write("### Derniers colis ajoutés")
    if len(df) > 1:
        st.dataframe(
            df.iloc[::-1].head(5)[["index", "timestamp", "package_id", "name", "quantity", "location", "status", "hash", "hash_valid"]]
        )
    else:
        st.info("Aucun colis n’a encore été enregistré.")

    st.markdown("---")
    st.write("### Pourquoi la blockchain renforce la cybersécurité")
    st.markdown(
        "- Elle empêche la modification silencieuse des données de livraison.\n"
        "- Elle fournit une piste d’audit immuable pour chaque colis.\n"
        "- Elle améliore la confiance client et la conformité interne."
    )

elif sidebar_page == "Suivi de colis":
    st.subheader("Enregistrer un nouveau colis")
    with st.form("tracking_form"):
        package_id = st.text_input("ID du colis", max_chars=64)
        name = st.text_input("Nom du colis / contenu")
        quantity = st.number_input("Quantité", min_value=0, step=1, format="%d")
        location = st.text_input("Localisation actuelle (point de départ)")
        recipient_location = st.text_input("Localisation du destinataire")
        submitted = st.form_submit_button("Enregistrer le colis")

    if submitted:
        if not package_id or not name or not location or not recipient_location:
            st.warning("Veuillez remplir tous les champs avant d’enregistrer le colis.")
        else:
            block = track_product(package_id, name, quantity, location, recipient_location)
            st.success("Colis enregistré avec succès.")
            st.write("**Détails du bloc :**")
            st.json(block)
            st.info(f"Hash enregistré : `{block['hash']}`")
            st.success("Ce hash permet de vérifier ultérieurement que le colis n’a pas été modifié.")

elif sidebar_page == "Mise à jour livraison":
    st.subheader("Mettre à jour l’état du colis")
    with st.form("delivery_update_form"):
        package_id = st.text_input("ID du colis", max_chars=64)
        status = st.selectbox(
            "Statut du colis",
            ["En transit", "Arrivé au centre de tri", "En cours de livraison", "Livré", "Retenu"],
        )
        location = st.text_input("Localisation actuelle")
        note = st.text_area("Commentaire / observation (optionnel)")
        submitted = st.form_submit_button("Ajouter une mise à jour")

    if submitted:
        if not package_id or not location:
            st.warning("Veuillez saisir l’ID du colis et la localisation.")
        else:
            block = update_package_status(package_id, status, location, note)
            st.success("Mise à jour de livraison enregistrée.")
            st.write("**Détails de l’événement :**")
            st.json(block)
            st.info(f"Hash enregistré : `{block['hash']}`")
            st.success("Cette mise à jour est maintenant traçable dans la blockchain.")

elif sidebar_page == "Suppression de colis":
    st.subheader("Supprimer un colis")
    with st.form("deletion_form"):
        package_id = st.text_input("ID du colis à supprimer", max_chars=64)
        reason = st.selectbox(
            "Raison de la suppression",
            ["Annulé par le client", "Perdu en transit", "Endommagé", "Autre"],
        )
        submitted = st.form_submit_button("Supprimer le colis")

    if submitted:
        if not package_id:
            st.warning("Veuillez saisir l’ID du colis à supprimer.")
        else:
            block = delete_product(package_id, reason)
            st.success("Suppression enregistrée dans la blockchain.")
            st.write("**Détails de la suppression :**")
            st.json(block)
            st.info(f"Hash enregistré : `{block['hash']}`")
            st.warning("Le colis est maintenant marqué comme supprimé. Cette action est irréversible.")

elif sidebar_page == "Réinitialisation":
    st.subheader("Réinitialiser la blockchain")
    st.warning("⚠️ Attention : Cette action va supprimer TOUTES les données de la blockchain et recommencer avec une chaîne vide.")
    st.write("Seul le bloc genesis sera conservé.")

    if st.button("Confirmer la réinitialisation", type="primary"):
        reset_chain()
        st.success("La blockchain a été réinitialisée avec succès.")
        st.info("Toutes les données ont été supprimées. Vous pouvez maintenant recommencer avec de nouveaux colis.")
        st.rerun()

elif sidebar_page == "Traçage par ID":
    st.subheader("Traçage d’un colis")
    package_id = st.text_input("ID du colis à rechercher")
    if st.button("Rechercher l’historique"):
        if not package_id:
            st.warning("Veuillez saisir un ID de colis.")
        else:
            history = trace_product(package_id)
            if not history:
                st.error("Aucun historique trouvé pour cet ID de colis.")
            else:
                st.success(f"{len(history)} bloc(s) trouvé(s) pour le colis {package_id}.")
                for block in history:
                    status = "Valide" if verify_block(block) else "Invalide"
                    st.markdown(f"**Bloc #{block['index']} — Intégrité : {status}**")
                    if status == "Invalide":
                        st.warning("Ce bloc semble altéré. La donnée ne correspond plus au hash stocké.")
                    st.json(block)
                    st.markdown("---")

elif sidebar_page == "Vérification par hash":
    st.subheader("Vérifier l’intégrité d’un bloc")
    hash_code = st.text_input("Hash du bloc")
    if st.button("Vérifier"):
        if not hash_code:
            st.warning("Veuillez saisir un hash.")
        else:
            block = get_product_by_hash(hash_code)
            if block is None:
                st.error("Aucun bloc trouvé pour ce hash.")
            else:
                verified = verify_hash(hash_code)
                if verified:
                    st.success("Le bloc est valide et n’a pas été modifié.")
                else:
                    st.error("Le bloc a été falsifié : le hash ne correspond plus.")
                st.json(block)

else:
    st.subheader("Explorateur de la blockchain")
    df = load_chain_data()
    if df.empty:
        st.info("La blockchain est vide. Enregistrez un colis pour commencer.")
    else:
        st.dataframe(df[["index", "timestamp", "package_id", "name", "quantity", "location", "hash", "hash_valid"]])
        with st.expander("Afficher les blocs bruts"):
            for block in get_chain():
                status = "Valide" if verify_block(block) else "Invalide"
                st.markdown(f"**Bloc #{block['index']} — Intégrité : {status}**")
                if status == "Invalide":
                    st.warning("Ce bloc est suspect : il a peut-être été modifié.")
                st.json(block)
                st.markdown("---")
