import streamlit as st
from utils import inject_global_css

st.set_page_config(
    page_title="Segmentation audio et analyse automatisée",
    layout="wide",
)

inject_global_css()

st.title("Vers une analyse audiovisuelle automatisée")

st.markdown(
    '<div class="subtitle">Cette page présente la suite logique du projet : passer des données agrégées à une analyse plus fine des contenus audiovisuels eux-mêmes, à partir de l’audio, de la segmentation et de la transcription.</div>',
    unsafe_allow_html=True,
)

st.info(
    "Les pages précédentes montrent des écarts de représentation. "
    "Cette étape vise à comprendre plus précisément qui parle, dans quel rôle, à quel moment et dans quel sujet."
)

st.divider()

st.markdown(
    '<div class="section-title">Pipeline envisagé</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.info("**1. Vidéo / audio**\n\nExtrait de JT ou de programme")

with col2:
    st.info("**2. Segmentation**\n\nDétection des zones de parole")

with col3:
    st.info("**3. Genre perçu**\n\nVoix femme / homme selon l’outil")

with col4:
    st.info("**4. Transcription**\n\nTexte du segment parlé")

with col5:
    st.info("**5. Analyse**\n\nThème, rôle, durée, statut")

st.divider()

st.markdown(
    '<div class="section-title">Ce que cette approche permettrait de mesurer</div>',
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        <div class="section-note">
        <strong>Temps de parole par sujet</strong><br>
        Mesurer directement la part de parole féminine et masculine à l’intérieur d’un sujet précis.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <div class="section-note">
        <strong>Rôle des intervenant·es</strong><br>
        Distinguer journalistes, expert·es, témoins, responsables politiques ou anonymes.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown(
        """
        <div class="section-note">
        <strong>Autorité de parole</strong><br>
        Ne plus seulement compter la présence, mais analyser la position occupée dans le récit médiatique.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    '<div class="section-title">Pourquoi cette étape est nécessaire</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-note">
    Les données utilisées dans les pages précédentes permettent de mesurer des tendances fortes, mais elles restent agrégées.
    Elles ne disent pas encore si les femmes parlent comme expertes, journalistes, témoins, invitées politiques ou simples personnes concernées.
    Pour répondre à cette limite, il faut descendre au niveau du segment audiovisuel.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-note">
    <strong>À retenir :</strong> la prochaine étape du projet consiste à relier directement un sujet, une voix, une durée de parole,
    une transcription et un rôle. C’est à ce niveau que la question de l’autorité de parole pourra être réellement analysée.
    </div>
    """,
    unsafe_allow_html=True,
)