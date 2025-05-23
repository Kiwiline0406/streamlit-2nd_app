import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Définition d'un titre
st.title("Manipulation de données et création de graphiques")

# Import des datasets
names_dataset_list = ['anagrams', 'anscombe', 'attention', 'brain_networks', 'car_crashes',
                      'diamonds', 'dots', 'dowjones', 'exercise', 'flights',
                      'fmri', 'geyser', 'glue', 'healthexp', 'iris',
                      'mpg', 'penguins', 'planets', 'seaice', 'taxis',
                      'tips', 'titanic']

datasets_dico = {}

for item in names_dataset_list:
    url = f"https://raw.githubusercontent.com/mwaskom/seaborn-data/master/{item}.csv"
    try:
        df = pd.read_csv(url)
        datasets_dico[item] = df
    except Exception as e:
        st.warning(f"Erreur pour {item} : {e}")

choice = st.selectbox(
    "Quel dataset t'intéresse ?",
    names_dataset_list,
    placeholder="Il y a sûrement quelque chose qui te plaît ici, regarde bien..."
)

if choice:
    st.badge("Dataset chargé avec succès", icon=":material/check:", color="green")
    st.subheader("Aperçu du dataset :chart_with_upwards_trend:", divider=True)
    dataset_user = datasets_dico[choice]
    st.dataframe(dataset_user)

    # Vérifier unicité des colonnes
    if dataset_user.columns.duplicated().any():
        st.error("⚠️ Ce dataset contient des colonnes en double. Impossible de générer un graphique avec.")
        st.write("Colonnes dupliquées :", dataset_user.columns[dataset_user.columns.duplicated()].tolist())
    else:
        st.subheader("Crée ton propre graphique :art:", divider=True)
        colonnes_list = dataset_user.columns.tolist()
        x_axis = st.selectbox("Choisis la colonne X : ", colonnes_list)
        y_axis = st.selectbox("Choisis la colonne Y : ", colonnes_list)

        graphs_list = ['scatter_chart', 'bar_chart', 'line_chart']
        graph_user = st.selectbox("Quel type de graphique tu souhaites ? ", graphs_list)

        if graph_user and x_axis and y_axis:
            df_chart = dataset_user[[x_axis, y_axis]].dropna()
            try:
                chart_func = getattr(st, graph_user)
                chart_func(data=df_chart, x=x_axis, y=y_axis)
            except Exception as e:
                st.error(f"Erreur lors de l'affichage du graphique : {e}")

        agree = st.checkbox("Afficher la matrice de corrélation")
        col_num = dataset_user.select_dtypes(include='number')
        if agree and not col_num.empty:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = col_num.corr()
            sns.heatmap(corr,
                        cmap='PuOr',
                        vmin=-1.0, vmax=1.0,
                        square=True, ax=ax)
            st.pyplot(fig)
