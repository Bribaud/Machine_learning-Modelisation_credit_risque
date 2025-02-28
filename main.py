import streamlit as st

from aide_prediction import predict

# Configuration de la page

st.set_page_config(

    page_title="Modélisation crédit risque",

    page_icon="📊",

    layout="wide",

)

# Header principal

st.markdown(

    """

    <div style="text-align: center; padding: 1rem 0; background-color: #f9f9f9; border-radius: 10px;">

        <h1 style="color: #4CAF50;">Modélisation crédit risque</h1>

        <p style="color: #888;">Analysez les risques de crédit en quelques clics</p>

    </div>

    """,

    unsafe_allow_html=True,

)

# Conteneur principal

with st.container():
    # Division en sections

    st.markdown("### Informations de base")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Âge (années)', min_value=18, step=1, max_value=100, value=28)

    with col2:
        income = st.number_input('Revenu annuel (en unités monétaires)', min_value=0, value=15000)

    with col3:
        loan_amount = st.number_input('Montant du prêt demandé', min_value=0, value=6000)

    # Ratio prêt/revenu

    loan_to_income_ratio = loan_amount / income if income > 0 else 0

    st.markdown(f"""

    **Ratio Prêt/Revenu:** 

    <div style="color: #4CAF50; font-size: 18px;">{loan_to_income_ratio:.2f}</div>

    """, unsafe_allow_html=True)

    # D'autres champs d'entrée

    st.markdown("### Détails du prêt")

    col4, col5, col6 = st.columns(3)

    with col4:
        loan_tenure_months = st.number_input('Durée du prêt (mois)', min_value=0, step=1, value=36)

    with col5:
        avg_dpd_per_delinquency = st.number_input('Retards moyens (jours)', min_value=0, value=20)

    with col6:
        delinquency_ratio = st.number_input('Ratio de défaillance (%)', min_value=0, max_value=100, step=1, value=30)

    col7, col8, col9 = st.columns(3)

    with col7:
        credit_utilization_ratio = st.number_input('Ratio d’utilisation du crédit (%)', min_value=0, max_value=100,
                                                   step=1, value=30)

    with col8:
        num_open_accounts = st.number_input('Nombre de comptes ouverts', min_value=1, max_value=4, step=1, value=2)

    with col9:
        residence_type = st.selectbox('Type de résidence', ['Propriétaire', 'Locataire', 'Hypothèque'])

    # Objectifs et types de prêt

    col10, col11 = st.columns(2)

    with col10:
        loan_purpose = st.selectbox('Objet du prêt', ['Éducation', 'Maison', 'Automobile', 'Personnel'])

    with col11:
        loan_type = st.selectbox('Type de prêt', ['Non sécurisé', 'Sécurisé'])

    # Bouton de calcul

    st.markdown("### Calcul des risques")

    if st.button('Calculer le risque'):
        # Appel de la fonction prédictive

        probability, credit_score, rating = predict(

            age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,

            delinquency_ratio, credit_utilization_ratio, num_open_accounts,

            residence_type, loan_purpose, loan_type

        )

        # Affichage des résultats

        st.success("Analyse terminée !")

        st.markdown(f"""

        **Probabilité de défaut :** {probability:.2%} 

        **Score de crédit :** {credit_score} 

        **Évaluation :** {rating}

        """, unsafe_allow_html=True)

# Footer

st.markdown(

    """

    <hr style="margin-top: 50px;">

    <div style="text-align: center; color: #aaa;">

        Projet personnel

    </div>

    """,

    unsafe_allow_html=True,

)