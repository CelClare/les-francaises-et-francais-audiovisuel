import streamlit as st
from utils import inject_global_css

st.set_page_config(
    page_title="Les Françaises et Français face à l'information",
    layout="wide",
)

inject_global_css()

st.title("Les Françaises et Français face à l'information")
st.markdown(
    '<div class="subtitle">Application d’exploration des données INA sur la représentation femmes / hommes dans l’audiovisuel télévisé français, éclairée par les contextes éditoriaux des journaux télévisés.</div>',
    unsafe_allow_html=True,
)

st.divider()

st.markdown(
    """
    ### Bienvenue

    Cette application s’organise autour de quatre questions :

    - **Y a-t-il des écarts globaux de représentation femmes / hommes dans l’audiovisuel télévisé français ?**
    - **Ces écarts se retrouvent-ils de la même manière selon les chaînes, ou observe-t-on des trajectoires différentes ?**
    - **Dans quels environnements thématiques ces écarts prennent-ils forme ?**
    - **Peut-on commencer à rapprocher structure éditoriale et représentation femmes / hommes ?**

    La démarche part d’un **diagnostic global**, puis descend à une échelle plus fine en observant les **chaînes**, les **journaux télévisés** et enfin un **croisement exploratoire** entre structure thématique et représentation moyenne.

    L’objectif n’est pas seulement de décrire des écarts, mais de mieux comprendre **dans quels contextes éditoriaux** ils prennent forme et comment ils peuvent être interprétés.

    Utilisez la navigation latérale de Streamlit pour parcourir les différentes pages.
    """
)