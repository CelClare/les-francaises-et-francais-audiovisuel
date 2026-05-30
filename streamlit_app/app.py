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
    Application d’analyse de la représentation femmes / hommes dans l’audiovisuel français,
    à partir de données ouvertes de l’INA.
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "Cette application explore qui parle, quand, sur quelles chaînes, dans quels formats "
    "et dans quels contextes éditoriaux."
)

st.divider()

st.markdown("### Ce que l’application analyse")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Temps de parole**\n\nMesurer les écarts entre femmes et hommes.")

with col2:
    st.info("**Contextes éditoriaux**\n\nComparer chaînes, horaires, thématiques et genres de programmes.")

with col3:
    st.info("**Limites et prolongements**\n\nPréparer une analyse plus fine par audio, segmentation et transcription.")

st.divider()

st.markdown("### Parcours d’analyse")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        <div class="section-note">
        <strong>1. Mesurer</strong><br>
        Observer les écarts globaux de temps de parole et leur évolution.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <div class="section-note">
        <strong>2. Comparer</strong><br>
        Identifier les différences entre chaînes, catégories et horaires de diffusion.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown(
        """
        <div class="section-note">
        <strong>3. Contextualiser</strong><br>
        Relier les écarts observés aux thématiques des JT et aux genres de programmes.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    """
    ### Objectif

    L’objectif n’est pas seulement de mesurer **qui parle le plus**, mais d’interroger
    les conditions de visibilité de cette parole : à quel moment, sur quelles chaînes,
    dans quels sujets et dans quels formats.

    Les données mobilisées permettent de mesurer des écarts de parole, mais elles ne
    renseignent pas encore directement le rôle ou le statut des personnes qui s’expriment.
    Ainsi, une présence accrue des femmes à l’antenne ne signifie pas nécessairement
    une égalité de position ou d’autorité.

    L’application propose donc une lecture critique des indicateurs disponibles, et ouvre
    vers une analyse plus fine des contenus audiovisuels par segmentation audio,
    transcription et classification thématique.
    """
)