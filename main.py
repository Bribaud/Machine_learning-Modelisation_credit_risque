import streamlit as st
from aide_prediction import predict

# Configuration de la page
st.set_page_config(
    page_title="Modélisation du Risque de Crédit",
    page_icon="📈",
    layout="centered"
)


# Initialisation des variables dans session_state si elles n'existent pas
def init_session_state():
    for key, value in {
        "age": 28, "income": 15000, "loan_amount": 6000,
        "loan_tenure_months": 36, "avg_dpd_per_delinquency": 20,
        "delinquency_ratio": 30, "credit_utilization_ratio": 30,
        "num_open_accounts": 2, "residence_type": "Propriétaire",
        "loan_purpose": "Éducation", "loan_type": "Non sécurisé",
        "ready_to_predict": False
    }.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# Sidebar pour la navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Aller à", ["🏠 Accueil", "📊 Entrée des données", "🔎 Résultats"])

# Accueil
if page == "🏠 Accueil":
    st.title("Modélisation du Risque de Crédit")
    st.write(
        "Bienvenue dans l'outil d'analyse des risques de crédit. Remplissez les informations et obtenez une évaluation instantanée.")
    st.image("artifacts/im.png")

# Entrée des données
elif page == "📊 Entrée des données":
    st.title("📊 Informations du Demandeur")

    st.session_state["age"] = st.slider("Âge", 18, 100, st.session_state["age"])
    st.session_state["income"] = st.number_input("Revenu annuel", min_value=0, value=st.session_state["income"],
                                                 step=1000)
    st.session_state["loan_amount"] = st.number_input("Montant du prêt demandé", min_value=0,
                                                      value=st.session_state["loan_amount"], step=500)

    st.subheader("📌 Caractéristiques du Prêt")
    st.session_state["loan_tenure_months"] = st.slider("Durée du prêt (mois)", 6, 120,
                                                       st.session_state["loan_tenure_months"])
    st.session_state["avg_dpd_per_delinquency"] = st.number_input("Retards moyens (jours)", min_value=0,
                                                                  value=st.session_state["avg_dpd_per_delinquency"])
    st.session_state["delinquency_ratio"] = st.slider("Ratio de défaillance (%)", 0, 100,
                                                      st.session_state["delinquency_ratio"])
    st.session_state["credit_utilization_ratio"] = st.slider("Ratio d’utilisation du crédit (%)", 0, 100,
                                                             st.session_state["credit_utilization_ratio"])
    st.session_state["num_open_accounts"] = st.slider("Nombre de comptes ouverts", 1, 10,
                                                      st.session_state["num_open_accounts"])
    st.session_state["residence_type"] = st.selectbox("Type de résidence", ["Propriétaire", "Locataire", "Hypothèque"],
                                                      index=["Propriétaire", "Locataire", "Hypothèque"].index(
                                                          st.session_state["residence_type"]))
    st.session_state["loan_purpose"] = st.selectbox("Objet du prêt", ["Éducation", "Maison", "Automobile", "Personnel"],
                                                    index=["Éducation", "Maison", "Automobile", "Personnel"].index(
                                                        st.session_state["loan_purpose"]))
    st.session_state["loan_type"] = st.selectbox("Type de prêt", ["Non sécurisé", "Sécurisé"],
                                                 index=["Non sécurisé", "Sécurisé"].index(
                                                     st.session_state["loan_type"]))

    if st.button("Valider et Analyser"):
        st.session_state["ready_to_predict"] = True

# Résultats
elif page == "🔎 Résultats":
    st.title("🔎 Résultat de l'Analyse")
    if st.session_state["ready_to_predict"]:
        probability, credit_score, rating = predict(
            st.session_state["age"], st.session_state["income"], st.session_state["loan_amount"],
            st.session_state["loan_tenure_months"], st.session_state["avg_dpd_per_delinquency"],
            st.session_state["delinquency_ratio"], st.session_state["credit_utilization_ratio"],
            st.session_state["num_open_accounts"], st.session_state["residence_type"],
            st.session_state["loan_purpose"], st.session_state["loan_type"]
        )

        st.metric("📉 Probabilité de défaut", f"{probability:.2%}")
        st.metric("💳 Score de crédit", credit_score)
        st.metric("🔍 Évaluation", rating)

        st.success("Analyse terminée avec succès !")
    else:
        st.warning("Veuillez d'abord entrer les données dans l'onglet 'Entrée des données'.")

# Footer
st.sidebar.markdown("""
---
© 2025 - Analyse du Risque de Crédit
""")
