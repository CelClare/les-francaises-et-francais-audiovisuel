import streamlit as st
from utils import inject_global_css

st.set_page_config(
    page_title="Analyse audiovisuelle automatisée",
    layout="wide",
)

inject_global_css()

st.title("Vers une analyse audiovisuelle automatisée")

st.markdown(
    '<div class="subtitle">Cette page présente la prochaine étape du projet : passer des données agrégées à une analyse directe des contenus audiovisuels, en combinant segmentation audio, genre vocal perçu, transcription et classification thématique.</div>',
    unsafe_allow_html=True,
)

st.info(
    "Objectif : relier une voix, une durée de parole et un sujet traité afin d’analyser plus finement la représentation femmes / hommes dans les médias audiovisuels."
)

st.divider()

# =========================================================
# CORPUS
# =========================================================
st.markdown(
    '<div class="section-title">Corpus envisagés</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="background:white; padding:18px; border-radius:18px; border:1px solid rgba(61,64,91,0.08); min-height:230px;">
            <div style="font-weight:700; font-size:1.1rem; color:#3D405B; margin-bottom:0.7rem;">InaGVAD · 2021-2022</div>
            <div style="color:#5E503F; line-height:1.7;">
                Corpus TV et radio annoté pour la détection d’activité vocale et la segmentation genrée de la parole.
                <br><br>
                <strong>Apport principal :</strong> mesurer automatiquement les durées de parole associées aux voix perçues comme féminines ou masculines.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="background:white; padding:18px; border-radius:18px; border:1px solid rgba(61,64,91,0.08); min-height:230px;">
            <div style="font-weight:700; font-size:1.1rem; color:#3D405B; margin-bottom:0.7rem;">is24_news_topic · 2023</div>
            <div style="color:#5E503F; line-height:1.7;">
                Corpus de sujets d’information TV et radio annotés selon 18 thématiques.
                <br><br>
                <strong>Apport principal :</strong> relier les contenus audiovisuels à des catégories éditoriales plus fines : politique, sport, santé, justice, économie, guerre, etc.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# =========================================================
# SCHÉMA
# =========================================================
st.markdown(
    '<div class="section-title">Pipeline cible</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="background:white; padding:22px; border-radius:18px; border:1px solid rgba(61,64,91,0.08);">
        <div style="display:flex; align-items:stretch; justify-content:space-between; gap:10px; text-align:center;">
            <div style="flex:1; padding:14px; border-radius:14px; background:#F4F1DE;">
                <strong>1. Audio / vidéo</strong><br>
                Extrait TV ou radio
            </div>
            <div style="align-self:center; font-size:1.5rem;">→</div>
            <div style="flex:1; padding:14px; border-radius:14px; background:#F4F1DE;">
                <strong>2. Segmentation</strong><br>
                Parole, musique, bruit
            </div>
            <div style="align-self:center; font-size:1.5rem;">→</div>
            <div style="flex:1; padding:14px; border-radius:14px; background:#F4F1DE;">
                <strong>3. Genre vocal perçu</strong><br>
                Voix femme / homme
            </div>
            <div style="align-self:center; font-size:1.5rem;">→</div>
            <div style="flex:1; padding:14px; border-radius:14px; background:#F4F1DE;">
                <strong>4. Sujet traité</strong><br>
                Classification thématique
            </div>
            <div style="align-self:center; font-size:1.5rem;">→</div>
            <div style="flex:1; padding:14px; border-radius:14px; background:#F4F1DE;">
                <strong>5. Indicateurs</strong><br>
                Temps de parole par thème
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# =========================================================
# QUESTION DATA
# =========================================================
st.markdown(
    '<div class="section-title">Question que cette approche permettra de traiter</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-note">
    Les pages précédentes montrent que les femmes parlent moins que les hommes et que ces écarts varient selon les chaînes,
    les horaires, les genres de programmes et les contextes thématiques. La limite actuelle est que les données restent agrégées :
    elles ne relient pas directement une voix, un segment de parole et un sujet précis.
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "La prochaine étape consiste donc à mesurer directement la part de parole féminine et masculine par sujet traité : politique, sport, santé, justice, économie, environnement, guerre, etc."
)

st.divider()

# =========================================================
# INDICATEURS CIBLES
# =========================================================
st.markdown(
    '<div class="section-title">Indicateurs visés</div>',
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(
        """
        <div class="section-note">
        <strong>Temps de parole par thème</strong><br>
        Comparer la part de parole féminine et masculine selon les sujets traités.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <div class="section-note">
        <strong>Écarts par type de média</strong><br>
        Observer les différences entre chaînes d’information, chaînes généralistes, radio et télévision.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown(
        """
        <div class="section-note">
        <strong>Autorité de parole</strong><br>
        Préparer une analyse ultérieure du rôle des intervenant·es : journaliste, expert·e, témoin, responsable politique.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

st.markdown(
    """
    <div class="section-note">
    <strong>À retenir :</strong> cette page marque le passage d’une analyse de données agrégées à une analyse automatique
    des contenus audiovisuels eux-mêmes. L’objectif n’est plus seulement de constater que les femmes parlent moins,
    mais d’identifier dans quels sujets, formats et positions de parole ces écarts se construisent.
    </div>
    """,
    unsafe_allow_html=True,
)