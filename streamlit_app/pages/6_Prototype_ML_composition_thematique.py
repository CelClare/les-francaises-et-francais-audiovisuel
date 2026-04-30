import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from utils import inject_global_css, load_data, beautify_plot

st.set_page_config(
    page_title="Prototype ML : composition thématique",
    layout="wide",
)

inject_global_css()

(
    gender_year_channel,
    gender_year_public_private,
    gender_year_category,
    gender_public_private_global,
    jt_year_channel_theme,
    jt_year_theme,
    jt_topics_global,
    theme_gender_proxy,
    theme_gender_proxy_by_theme,
    jt_theme_volatility,
    jt_editorial_composition,
    gender_by_hour,
    csa_program_genres,
) = load_data()

st.title("Prototype ML : composition thématique et part féminine")

st.markdown(
    '<div class="subtitle">Cette page teste une question exploratoire : la composition thématique des JT permet-elle d’expliquer une partie des variations de la part féminine moyenne selon les chaînes et les années ?</div>',
    unsafe_allow_html=True,
)

st.info(
    "Ce prototype n’est pas un modèle prédictif fiable. Il sert à tester l’existence éventuelle d’un signal statistique dans les données."
)

# Jointure thème × genre
df = jt_editorial_composition.merge(
    gender_year_channel[["year", "channel_name", "avg_female_share"]],
    on=["year", "channel_name"],
    how="inner",
)

# Pivot : thèmes en colonnes
features = df.pivot_table(
    index=["year", "channel_name"],
    columns="theme",
    values="theme_share_subjects",
    fill_value=0,
).reset_index()

target = (
    df[["year", "channel_name", "avg_female_share"]]
    .drop_duplicates()
)

ml_df = features.merge(
    target,
    on=["year", "channel_name"],
    how="inner",
)

st.write("Nombre d'observations utilisées :", ml_df.shape[0])
st.write("Nombre de variables thématiques :", ml_df.shape[1] - 3)

X = ml_df.drop(columns=["year", "channel_name", "avg_female_share"])
y = ml_df["avg_female_share"]

if len(ml_df) < 10:
    st.warning("Pas assez d’observations pour entraîner un modèle exploitable.")
    st.stop()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

col1, col2 = st.columns(2)
col1.metric("Erreur moyenne absolue", f"{mae:.1%}")
col2.metric("R² exploratoire", f"{r2:.2f}")

results = pd.DataFrame({
    "Part féminine réelle": y_test,
    "Part féminine prédite": y_pred,
})

fig = px.scatter(
    results,
    x="Part féminine réelle",
    y="Part féminine prédite",
    title="Part féminine réelle vs prédite",
)

fig.update_xaxes(tickformat=".0%")
fig.update_yaxes(tickformat=".0%")

fig = beautify_plot(fig)
st.plotly_chart(fig, width="stretch")