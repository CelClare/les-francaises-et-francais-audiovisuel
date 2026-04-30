import streamlit as st
from utils import inject_global_css

st.set_page_config(
    page_title="Les Françaises et les Français face à l'information",
    layout="wide",
)

inject_global_css()

st.title("Les Françaises et les Français face à l'information")

st.markdown(
    """
    <div class="subtitle">
    Application d’analyse de la représentation femmes / hommes à la télévision française.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Dimensions de l'analyse")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Présence**\n\nÊtre visible à l’antenne")

with col2:
    st.info("**Parole**\n\nDisposer d’un temps d’expression")

with col3:
    st.info("**Autorité**\n\nÊtre reconnue comme experte, journaliste ou responsable")

st.divider()

st.markdown(
    """
    ### Objectif

    À partir de données ouvertes issues de l’INA, cette application explore les écarts de temps de parole entre femmes et hommes, mais aussi les contextes éditoriaux dans lesquels ces écarts apparaissent.

    L’objectif n’est pas seulement de mesurer **qui parle le plus**, mais d’interroger comment la parole est distribuée selon les chaînes, les thématiques et les formats de programmes.

    Cette application propose une lecture en quatre niveaux :

    - **Mesurer** les écarts de temps de parole entre femmes et hommes
    - **Comparer** les trajectoires des chaînes et leurs différences structurelles
    - **Contextualiser** ces écarts à partir des thématiques des journaux télévisés
    - **Interpréter** ce que les données montrent, suggèrent, et ne permettent pas encore de démontrer

    Les données mobilisées permettent de mesurer des écarts de parole, mais elles ne renseignent pas directement le rôle ou le statut des personnes qui s’expriment.

    Ainsi, une présence accrue des femmes à l’antenne ne signifie pas nécessairement une égalité de position ou d’autorité.

    L’application propose donc une lecture critique des indicateurs disponibles, en mettant en évidence leurs apports et leurs limites.

    Utilisez la navigation latérale pour explorer les différentes dimensions de l’analyse.
    """
)