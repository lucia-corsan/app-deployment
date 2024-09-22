import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from annotated_text import annotated_text
from streamlit_card import card

nltk.download('stopwords')

STOPWORDS_NLTK = set(stopwords.words('spanish'))

st.set_page_config(
        page_title="University and Careers: Analysis 2024",
        page_icon="👨‍🎓",
        layout="centered"
    )

st.sidebar.title("Index")

st.sidebar.markdown(
    """
    <style>
    a.custom-link {
        text-decoration: none;
        color: inherit;
        margin-bottom: 15px; /* Adds space between the links */
        display: block; /* Ensures each link is on its own line */
    }
    a.custom-link:hover {
        color: #ff6347; /* Change this color to your preferred hover color */
    }
    </style>
    <a href="#key-takeaways" class="custom-link">**💡 Key Takeaways**</a>
    <a href="#distribution-of-universities-and-degrees-by-region" class="custom-link">**🌍 Universities and Degrees by Region**</a>
    <a href="#analysis-of-words-and-lemmas-by-university" class="custom-link">**💬 Words and Lemmas by University**</a>
    <a href="#topic-decomposition-by-degree" class="custom-link">**🧩 Topic Decomposition by Degree**</a>
    <a href="#wordcloud-representation-by-university" class="custom-link">**☁️ Wordcloud Representation by University**</a>
    <a href="#wordcloud-representation-by-degree" class="custom-link">**☁️ Wordcloud Representation by Degree**</a>
    <a href="#job-recommendation-system-based-on-degree" class="custom-link">**🎯 Job Recommendation System by Degree**</a>
    """,
    unsafe_allow_html=True
)

# Código HTML y CSS adaptado para Streamlit
html_code = """

<head>    
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>

<p style="margin-top: 50px;"></p>

<p align="center" style="margin-top: -40px;">
    <img src="https://bestuc3m.es/wp-content/uploads/2022/10/Logo-UC3M-1024x329-1-1.png" height="55" class="img_hover">
</p>

<p style="margin-top: 30px;"></p>

<span class="st-emotion-cache-10trblm e1nzilvr1">
    <div class="row" style="text-align: center;">
        <div style="display: inline-block; font-size: 67px; font-family: 'Open Sans', sans-serif; font-weight: bold;">
            University & <span style="color: black; background-color: rgb(41, 181, 232); padding: 0 10px; font-size: 67px; font-family: 'Open Sans', sans-serif; font-weight: bold;">
                Careers</span>:
        </div>    
        <div style="display: inline-block;">
            <span style="display: inline-block; font-size: 70px; font-family: 'Open Sans', sans-serif; font-weight: bold;margin: -20px;">
                Analysis 2024
            </span>
            <img src="https://raw.githubusercontent.com/dataprofessor/thumbnail-image/master/Sno-Blue-Arrow.svg" height="70" align="center" style="margin-left: 30px; margin-top: -40px;">
        </div>
    </div>
</span>

<p align="center" style="font-family: 'Open Sans', sans-serif; font-size: 28px; line-height: 1.25; margin-top: 68px;">
    Explore the educational trends and find the best recommendations among 
    <span style="color: rgb(255, 189, 69);">
        <b>52,122</b>
    </span> 
    job offers and 
    <span style="color: rgb(255, 189, 69);">
        <b>12,087</b>
    </span> degrees and masters from Spanish universities.
</p>

<p style="text-align: center; font-family: 'Open Sans', sans-serif; font-size: 18px; margin: 20px 0;">
    <span style="color: rgb(255, 189, 69); font-weight: bold;">Contact me:</span>
    &nbsp;
    <a href="https://github.com/lucia-corsan" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit; margin: 0 10px;">
        <i class="fab fa-github" style="font-size: 24px;"></i>
    </a>
    <a href="https://www.linkedin.com/in/luciacordero/" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit; margin: 0 10px;">
        <i class="fab fa-linkedin-in" style="font-size: 24px;"></i>
    </a>
    </a>
    <a href="mailto:luciaa.corsan@gmail.com" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit; margin: 0 10px;">
        <i class="fa-solid fa-envelope" style="font-size: 24px;"></i>
    </a>
</p>
<p style="margin-top: 90px;"></p>

"""
st.markdown(html_code, unsafe_allow_html=True)

with st.expander('About this app'):
    st.write('This website is part of the results of my **Final Degree Project in Data Science and Engineering** in the 2023-2024 academic year.')
    st.write('This is a prototype, and the data obtained from the Tecnoempleo job portal have been provided under a non-commercial use clause in small-scale and controlled development environments.')
    st.write('Although the results presented in the report are limited to the Tecnoempleo.com portal and Spanish Registro de Universidades, it is important to highlight that the analysis methodology used is completely independent of the data source. This opens up the possibility of replicating the analysis with a second data source when available and with a sufficiently large time span. If you would like to see or use the project infrastructure with other data, please contact me.')

    st.markdown(
        """        
        ### Want to learn more?
        - Jump into our [Github repository](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
    
    """
    )

st.markdown(
    """
    <style>
        .arrow-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }

        .arrow {
            box-sizing: border-box;
            height: 3vw;
            width: 3vw;
            border-style: solid;
            border-color: white;
            border-width: 0px 2px 2px 0px;
            transform: rotate(45deg);
            transition: all 150ms ease-in-out;
            cursor: pointer;
        }

        .arrow:hover {
            border-color: #FF9F36; /* Change color on hover */
            border-bottom-width: 5px; /* Increase thickness on hover */
            border-right-width: 5px; /* Increase thickness on hover */
        }

        .separator {
            border: 0;
            border-top: 2px solid #3498db;
            margin-top: -10px;
            margin-bottom: 20px;
        }

        .spacer {
            margin-top: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Arrow pointing to Key Takeaways section
st.markdown(
    """
    <div class="arrow-container">
        <div class="arrow" onclick="document.getElementById('first').scrollIntoView({ behavior: 'smooth' });"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Key Takeaways section
st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="key-takeaways">Key takeaways</h3>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    As of <strong><span style="color: orange;">August 01, 2024</span></strong>, the analysis about higher education in Spain revealed the following insights:
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <h3> <strong><span style="color: orange;">36%</span></strong> of university graduates are overqualified for their job</h2>
        <p>More targeted career guidance and alignment between academic programs and industry needs is required. 
        Addressing this issue is essential for an efficient job market and for improving the overall value of higher education.</p>
        <p><span style="color: orange;">Source</span></strong>: <a href="https://www.fundacioncyd.org/informe-cyd-2023-que-titulaciones-estudian-los-universitarios-en-espana-y-como-es-su-insercion-laboral/" target="_blank">Informe CYD 2023</a>.</p>

        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <h3><strong><span style="color: orange;">6 out of 10</span></strong> graduates feel unprepared for the job market</h2>
        <p> This highlights a critical gap in aligning educational outcomes with labor market demands, and the need for a tool that offers orientation about labor market opportunities based on educational background.</p>
        <p><span style="color: orange;">Source</span></strong>: <a href="https://elpais.com/educacion/2022-07-08/el-60-de-los-universitarios-no-se-ve-preparado-para-un-mercado-laboral-que-no-encuentra-los-perfiles-necesarios.html" target="_blank">El País</a>.</p>

        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <h3> Among university graduates,  <strong><span style="color: orange;">7.1%</span></strong> are unemployed (twice the EU)</h2>
        <p>Despite the investment in higher education, Spain has the second highest unemployment rate for higher education graduates just below Greece. The EU average graduate unemployment rate in 2023 was 3.5%.
        <strong></p>
        <p><span style="color: orange;">Source</span></strong>: <a href="https://www.fundacioncyd.org/informe-cyd-2023-que-titulaciones-estudian-los-universitarios-en-espana-y-como-es-su-insercion-laboral/" target="_blank">Informe CYD 2023</a>.</p>
        """,
        unsafe_allow_html=True
    )
    unsafe_allow_html=True


# Cargar el archivo Parquet
@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

ruct_final = load_data('/Users/lcsanchez/Desktop/TM_NLP/output/ruct_final.parquet')
ruct_raw = load_data('/Users/lcsanchez/Desktop/TM_NLP/output/ruct_preprocesado.parquet')
ruct_lemmas = pd.read_parquet('/Users/lcsanchez/Desktop/RUCT/ruct_lemmatized')
tecnoempleo_lemmas = pd.read_parquet('/Users/lcsanchez/Desktop/tecnoempleo_topicmodels/lemmas/tecnoempleo_lemmatized')

df_ruct_topics = pd.read_parquet('/Users/lcsanchez/Desktop/similarity/datasets/topic_analysis_ruct.parquet')
topic_coords = pd.read_csv('/Users/lcsanchez/Desktop/ruct_topicmodels/ex2_24tpc/TMmodel/tpc_coords.txt', delimiter='\t', header=None, names=['tpc_coordinates'])  # Asume que las coordenadas están separadas por tabulaciones
topic_names = pd.read_csv('/Users/lcsanchez/Desktop/ruct_topicmodels/ex2_24tpc/TMmodel/tpc_labels.txt', delimiter='\t', header=None, names=['tpc_names'])  # Asume que los nombres están separados por tabulaciones
similarity_bert_cosine = pd.read_parquet('/Users/lcsanchez/Desktop/similarity/cosine_sim_matrix_we_BERT.parquet')

st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="first">Distribution of Universities and Degrees by Region</h3>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)
# Diccionario de mapeo de universidades a comunidades autónomas
mapping = {
    "['Centros dependientes del Ministerio de Defensa']": 'Ministerio de Defensa',
    "['CUNEF Universidad']": 'Comunidad de Madrid',
    "['ESIC Universidad']": 'Comunidad de Madrid',
    "['IE Universidad']": 'Comunidad de Madrid',
    "['(Conjunto Internacional)']": 'Internacional',
    "['Mondragón Unibertsitatea']": 'País Vasco',
    "['Universidad a Distancia de Madrid']": 'Comunidad de Madrid',
    "['Universidad Alfonso X El Sabio']": 'Comunidad de Madrid',
    "['Universidad Antonio de Nebrija']": 'Comunidad de Madrid',
    "['Universidad Autónoma de Barcelona']": 'Cataluña',
    "['Universidad Autónoma de Madrid']": 'Comunidad de Madrid',
    "['Universidad Camilo José Cela']": 'Comunidad de Madrid',
    "['Universidad Cardenal Herrera-CEU']": 'Comunidad Valenciana',
    "['Universidad Carlos III de Madrid']": 'Comunidad de Madrid',
    "['Universidad Católica de Valencia San Vicente Mártir']": 'Comunidad Valenciana',
    "['Universidad Católica San Antonio']": 'Región de Murcia',
    "['Universidad Católica Santa Teresa de Jesús de Ávila']": 'Castilla y León',
    "['Universidad Complutense de Madrid']": 'Comunidad de Madrid',
    "['Universidad de A Coruña']": 'Galicia',
    "['Universidad de Alcalá']": 'Comunidad de Madrid',
    "['Universidad de Alicante']": 'Comunidad Valenciana',
    "['Universidad de Almería']": 'Andalucía',
    "['Universidad de Barcelona']": 'Cataluña',
    "['Universidad de Burgos']": 'Castilla y León',
    "['Universidad de Cádiz']": 'Andalucía',
    "['Universidad de Cantabria']": 'Cantabria',
    "['Universidad de Castilla-La Mancha']": 'Castilla-La Mancha',
    "['Universidad de Córdoba']": 'Andalucía',
    "['Universidad de Deusto']": 'País Vasco',
    "['Universidad de Diseño, Innovación y Tecnología (UDIT)']": 'Comunidad de Madrid',
    "['Universidad de Extremadura']": 'Extremadura',
    "['Universidad de Girona']": 'Cataluña',
    "['Universidad de Granada']": 'Andalucía',
    "['Universidad de Huelva']": 'Andalucía',
    "['Universidad de Jaén']": 'Andalucía',
    "['Universidad de La Laguna']": 'Canarias',
    "['Universidad de La Rioja']": 'La Rioja',
    "['Universidad de las Hespérides']": 'Canarias',
    "['Universidad de Las Palmas de Gran Canaria']": 'Canarias',
    "['Universidad de León']": 'Castilla y León',
    "['Universidad de Lleida']": 'Cataluña',
    "['Universidad de Málaga']": 'Andalucía',
    "['Universidad de Murcia']": 'Región de Murcia',
    "['Universidad de Navarra']": 'Navarra',
    "['Universidad de Oviedo']": 'Asturias',
    "['Universidad de Salamanca']": 'Castilla y León',
    "['Universidad de Santiago de Compostela']": 'Galicia',
    "['Universidad de Sevilla']": 'Andalucía',
    "['Universidad de Valladolid']": 'Castilla y León',
    "['Universidad de Vic-Universidad Central de Catalunya']": 'Cataluña',
    "['Universidad de Vigo']": 'Galicia',
    "['Universidad de Zaragoza']": 'Aragón',
    "['Universidad del Atlántico Medio']": 'Canarias',
    "['Universidad del País Vasco/Euskal Herriko Unibertsitatea']": 'País Vasco',
    "['Universidad Euneiz']": 'País Vasco',
    "['Universidad Europea de Canarias']": 'Canarias',
    "['Universidad Europea de Madrid']": 'Comunidad de Madrid',
    "['Universidad Europea de Valencia']": 'Comunidad Valenciana',
    "['Universidad Europea del Atlántico']": 'Cantabria',
    "['Universidad Europea Miguel de Cervantes']": 'Castilla y León',
    "['Universidad Fernando Pessoa-Canarias (UFP-C)']": 'Canarias',
    "['Universidad Francisco de Vitoria']": 'Comunidad de Madrid',
    "['Universidad Intercontinental de la Empresa']": 'Galicia',
    "['Universidad Internacional de Andalucía']": 'Andalucía',
    "['Universidad Internacional de la Empresa']": 'Galicia',
    "['Universidad Internacional de La Rioja']": 'La Rioja',
    "['Universitat de València (Estudi General)']": 'Comunidad Valenciana',
    "['Universitat Internacional de Catalunya']": 'Cataluña',
    "['Universitat Internacional Valenciana']": 'Comunidad Valenciana',
    "['Universitat Oberta de Catalunya']": 'Cataluña',
}

ruct_raw['CCAA'] = ruct_raw['Universidad'].map(mapping)

# Obtener todas las comunidades y añadir opción nacional
comunidades = ruct_raw['CCAA'].dropna().unique().tolist()
comunidades.insert(0, 'All (National Level)')

# Seleccionar por defecto la primera comunidad o una en particular (ejemplo: Madrid)
default_comunidad = 'Comunidad de Madrid'  # Aquí pones la comunidad/universidad por defecto que deseas
default_index = comunidades.index(default_comunidad) if default_comunidad in comunidades else 0

# Seleccionar la Comunidad Autónoma
selected_comunidad = st.selectbox('Select a region', comunidades, index=default_index)

# Filtrar datos según la selección
if selected_comunidad == 'All (National Level)':
    filtered_df = ruct_raw
else:
    filtered_df = ruct_raw[ruct_raw['CCAA'] == selected_comunidad]

# Calcular los valores para la región seleccionada
num_titulaciones = filtered_df.shape[0]
num_universidades = len(filtered_df['Universidad'].unique())

# Calcular la media nacional de titulaciones y universidades
national_avg_titulaciones = ruct_raw.groupby('CCAA').size().mean()
national_avg_universidades = ruct_raw['Universidad'].nunique() / len(ruct_raw['CCAA'].unique())

# Comparar con la media nacional
if selected_comunidad != 'All (National Level)':
    avg_titulaciones_region = filtered_df.groupby('CCAA').size().mean()
    avg_universidades_region = filtered_df['Universidad'].nunique() / len(filtered_df['CCAA'].unique())

    diff_titulaciones = num_titulaciones - national_avg_titulaciones
    diff_universidades = num_universidades - national_avg_universidades

    with st.container():
        # Crear un contenedor para las métricas
        col1, col2 = st.columns(2)

        # Mostrar las métricas en las columnas
        with col1:
            if diff_titulaciones > 0:
                st.metric(label="Number of degrees", value=f"{num_titulaciones:.0f}",
                          delta=f"+{diff_titulaciones:.0f} over the Spain's average", delta_color="normal")
            else:
                st.metric(label="Number of degrees", value=f"{num_titulaciones:.0f}",
                          delta=f"{diff_titulaciones:.0f} under the Spain's average", delta_color="normal",)

        with col2:
            if diff_universidades > 0:
                st.metric(label="Number of universities", value=f"{num_universidades:.0f}",
                          delta=f"+{diff_universidades:.0f} over the Spain's average", delta_color="normal")
            else:
                st.metric(label="Number of universities", value=f"{num_universidades:.0f}",
                          delta=f"{diff_universidades:.0f} under the Spain's average", delta_color="normal")

else:
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Number of degrees", value=f"{num_titulaciones:.0f}")

    with col2:
        st.metric(label="Number of universities", value=f"{num_universidades:.0f}")

st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h4 id="first">Evolution of degrees status over time by region</h4>
    """,
    unsafe_allow_html=True
)

tab1, tab2= st.tabs(["Line plot", "Horizontal bar plot"])

with tab1:
    # Grupos de estados
    extinguir_group = [
        "['Publicado en B.O.E.  (TITULACIÓN A EXTINGUIR)']",
        "['Publicado en B.O.E.  (TITULACIÓN A EXTINGUIR POR NO RENOVACIÓN)']"
    ]

    extinguida_group = [
        "['Publicado en B.O.E.  (TITULACIÓN EXTINGUIDA)']",
        "['Publicado en B.O.E.  (TITULACIÓN EXTINGUIDA POR NO RENOVACIÓN)']",
        "['Afectado por Resolución Judicial  (TITULACIÓN EXTINGUIDA)']"
    ]

    positive_group = [
        "['Publicado en B.O.E.  (TITULACIÓN RENOVADA)']",
        "['Publicado en B.O.E.  (TITULACIÓN RENOVADA POR ACREDITACIÓN INSTITUCIONAL)']",
        "['Publicado en B.O.E.']"
    ]

    # Filtrar el DataFrame para los estados deseados
    df_filtered_2 = filtered_df[filtered_df['Estado'].isin(extinguir_group + extinguida_group + positive_group)]

    # Agrupar por año y estado
    df_grouped_2 = df_filtered_2.groupby(['calendario', 'Estado']).size().unstack(fill_value=0)

    # Sumar las categorías según los grupos
    extinguir_group = [col for col in df_grouped_2.columns if col in extinguir_group]
    extinguida_group = [col for col in df_grouped_2.columns if col in extinguida_group]
    positive_group = [col for col in df_grouped_2.columns if col in positive_group]

    df_extinguir = df_grouped_2[extinguir_group].sum(axis=1)
    df_extinguida = df_grouped_2[extinguida_group].sum(axis=1)
    df_positive = df_grouped_2[positive_group].sum(axis=1)

    # Crear un DataFrame con los datos combinados para Altair
    df_combined = pd.DataFrame({
        'Año': df_extinguir.index,
        'Titulaciones a extinguir': df_extinguir.values,
        'Titulaciones extinguidas': df_extinguida.values,
        'Titulaciones renovadas': df_positive.values
    })

    # Convertir el DataFrame a formato largo para Altair
    df_melted = df_combined.melt('Año', var_name='Estado', value_name='Cantidad')

    # Crear una selección de hover
    hover = alt.selection_single(
        fields=["Año"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Crear el gráfico de líneas con puntos y tooltips
    lines = alt.Chart(df_melted).mark_line(point=True).encode(
        x=alt.X('Año:O', title='Año'),
        y=alt.Y('Cantidad:Q', title='Cantidad'),
        color=alt.Color('Estado:N', scale=alt.Scale(domain=[
            'Titulaciones a extinguir', 'Titulaciones extinguidas', 'Titulaciones renovadas'
        ], range=['#f2cc67', '#dd423e', '#8fd053'])),
        tooltip=['Año', 'Estado', 'Cantidad']
    ).properties(
        title=''
    )

    # Añadir puntos en la posición hover
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Añadir tooltips
    tooltips = alt.Chart(df_melted).mark_rule().encode(
        x='Año:O',
        y='Cantidad:Q',
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("Año:O", title="Año"),
            alt.Tooltip("Cantidad:Q", title="Cantidad"),
            alt.Tooltip("Estado:N", title="Estado"),
        ],
    ).add_selection(hover)

    # Añadir la línea vertical discontinua en 1999
    vertical_line = alt.Chart(pd.DataFrame({'Año': [1999]})).mark_rule(
        strokeDash=[4, 4],  # Línea discontinua
        color='#494d4b',  # Color blanco
        size=1.5  # Grosor de la línea
    ).encode(
        x='Año:O'
    )

    # Añadir la anotación con un emoji y el texto "FIRMA"
    annotation = alt.Chart(pd.DataFrame({
        'Año': [1999],
        'Cantidad': [df_melted[df_melted['Año'] == 1999]['Cantidad'].max()],
        'Text': ['✍️ Firma del Plan Bolonia']
    })).mark_text(
        align='left',
        dx=5,
        dy=-15,
        fontSize=12,
        color='white'
    ).encode(
        x='Año:O',
        y=alt.Y('Cantidad:Q'),
        text='Text:N'
    )

    # Combinar todo en el gráfico final
    final_chart = lines + points + tooltips + vertical_line + annotation

    # Mostrar el gráfico en Streamlit
    st.altair_chart(final_chart, use_container_width=True)

with tab2:
    # Define los grupos
    negative_groups = [
        "['Publicado en B.O.E.  (TITULACIÓN A EXTINGUIR)']",
        "['Publicado en B.O.E.  (TITULACIÓN EXTINGUIDA)']",
        "['Publicado en B.O.E.  (TITULACIÓN EXTINGUIDA POR NO RENOVACIÓN)']",
        "['Publicado en B.O.E.  (TITULACIÓN A EXTINGUIR POR NO RENOVACIÓN)']",
        "['Afectado por Resolución Judicial  (TITULACIÓN EXTINGUIDA)']"
    ]

    positive_groups = [
        "['Publicado en B.O.E.  (TITULACIÓN RENOVADA)']",
        "['Publicado en B.O.E.  (TITULACIÓN RENOVADA POR ACREDITACIÓN INSTITUCIONAL)']",
        "['Publicado en B.O.E.']"
    ]

    # Filtrar el DataFrame para los estados deseados
    df_filtered = filtered_df[filtered_df['Estado'].isin(negative_groups + positive_groups)]

    # Agrupar por año y estado
    df_grouped = df_filtered.groupby(['calendario', 'Estado']).size().unstack(fill_value=0)

    # Separar en grupos positivos y negativos
    df_negative = df_grouped.loc[:, [state for state in df_grouped.columns if state in negative_groups]]
    df_positive = df_grouped.loc[:, [state for state in df_grouped.columns if state in positive_groups]]

    # Multiplicar valores negativos por -1
    df_negative = -df_negative

    # Filtrar los datos para que comiencen en el año 2000
    df_negative = df_negative[df_negative.index >= 2000]
    df_positive = df_positive[df_positive.index >= 2000]

    # Combinar datos positivos y negativos en un solo DataFrame
    df_negative_melted = df_negative.reset_index().melt(id_vars='calendario', var_name='Estado', value_name='Cantidad')
    df_positive_melted = df_positive.reset_index().melt(id_vars='calendario', var_name='Estado', value_name='Cantidad')

    df_melted = pd.concat([df_negative_melted, df_positive_melted])

    # Renombrar los estados para mostrar solo la parte relevante
    rename_dict = {
        "['Publicado en B.O.E.  (TITULACIÓN A EXTINGUIR)']": 'Titulación a extinguir',
        "['Publicado en B.O.E.  (TITULACIÓN A EXTINGUIR POR NO RENOVACIÓN)']": 'Titulación a extinguir por no renovación',
        "['Publicado en B.O.E.  (TITULACIÓN EXTINGUIDA)']": 'Titulación extinguida',
        "['Publicado en B.O.E.  (TITULACIÓN EXTINGUIDA POR NO RENOVACIÓN)']": 'Titulación extinguida por no renovación',
        "['Afectado por Resolución Judicial  (TITULACIÓN EXTINGUIDA)']": 'Afectado por Resolución Judicial (Titulación extinguida)',
        "['Publicado en B.O.E.  (TITULACIÓN RENOVADA)']": 'Titulación renovada',
        "['Publicado en B.O.E.  (TITULACIÓN RENOVADA POR ACREDITACIÓN INSTITUCIONAL)']": 'Titulación renovada por acreditación institucional',
        "['Publicado en B.O.E.']": 'Titulación renovada (Publicado en B.O.E.)'
    }

    df_melted['Estado'] = df_melted['Estado'].map(rename_dict)

    # Definir colores para los estados
    color_scale = alt.Scale(domain=[
        'Titulación renovada',
        'Titulación renovada por acreditación institucional',
        'Titulación renovada (Publicado en B.O.E.)',
        'Titulación extinguida',
        'Titulación extinguida por no renovación',
        'Afectado por Resolución Judicial (Titulación extinguida)',
        'Titulación a extinguir',
        'Titulación a extinguir por no renovación'
    ], range=['#6fb02b', '#94d556', '#81c341', '#f25c54', '#f27059', '#f7b267', '#ffb703', '#ffd60a'])

    # Configuración de los rangos del eje x
    if selected_comunidad == 'All (National Level)':
        x_min = df_melted['Cantidad'].min() - 60
        x_max = df_melted['Cantidad'].max() + 350
    else:
        x_min = df_melted['Cantidad'].min() - 15
        x_max = df_melted['Cantidad'].max() + 30

    # Crear el gráfico de barras
    chart = alt.Chart(df_melted).mark_bar().encode(
        y=alt.Y('calendario:O', title='Year', sort=alt.EncodingSortField(field='calendario', order='ascending')),
        x=alt.X('Cantidad:Q', title='Count', scale=alt.Scale(domain=[x_min, x_max])),
        color=alt.Color('Estado:N', scale=color_scale),
        tooltip=['calendario', 'Estado', 'Cantidad']
    ).properties(
        title='',
        width=1000,  # Aumentar el ancho del gráfico
        height=600  # Aumentar la altura del gráfico
    )

    # Añadir una línea vertical en x=0
    vertical_line = alt.Chart(pd.DataFrame({'x': [0]})).mark_rule(color='black', strokeDash=[5, 5]).encode(
        x='x:Q'
    )

    # Configurar la leyenda para que los colores estén en líneas diferentes
    legend = alt.Legend(
        title='Status',
        orient='bottom',
        columns=3,  # Número de columnas en la leyenda
        direction='horizontal'
    )

    # Combinar el gráfico de barras con la línea vertical
    final_chart = chart + vertical_line

    # Añadir la leyenda
    final_chart = final_chart.encode(
        color=alt.Color('Estado:N', scale=color_scale, legend=legend)
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(final_chart, use_container_width=True)



st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="first">Analysis of Words and Lemmas by University</h3>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)

text = """
This grid of plots is a comparison of the number of total words in each degree (in blue), with respect to the lemmas in the same text (in pink)."""
st.markdown(text, unsafe_allow_html=True)

with st.expander('What is a lemma?'):
    st.markdown('A lemma is the **basic form of a word</strong**. It\'s the version you would look up in the dictionary.')
    st.write('When analysing language, computers want to analyse lemmas because they group similar meanings together. It avoids having many variations of the same word (and with the same meaning) in the text.')
    st.write('Let\'s see a quick example:')
    annotated_text(
        ("Cats", "noun (plural)", "#f77f00"),
        " ",
        ("are", "verb", "#55a630"),
        " ",
        ("chasing", "verb", "#55a630"),
        ' the ',
        ("mice", "noun (plural)", "#f77f00"))
    st.write("The lemmatised sentence would look like this:")
    annotated_text(
        ("Cat", "noun", "#f77f00"),
        " ",
        ("be", "infinitive", "#55a630"),
        " ",
        ("chase", "infinitive", "#55a630"),
        " the ",
        ("mouse", "noun", "#f77f00"),
    )


text = """
It is valuable to understand and analyse the information reflected by universities in the RUCT:

- If there are <strong><span style="color:orange">many terms but few lemmas</span></strong>, there may be redundant text that is not useful to understand the context in which the degree is framed.
- If <strong><span style="color:orange">the distribution of raw text and lemmas is similar</span></strong>, it may mean that there is more semantic value in the raw text, and that the information provided by the university is more concise.

The graph can show how lexical richness varies over time or between different documents. 
For example, greater length in documents may not always correspond to greater lemma density or greater vocabulary richness, which may indicate unnecessary repetition.
"""
st.markdown(text, unsafe_allow_html=True)

ruct_combined = pd.merge(ruct_lemmas, ruct_final[['id', 'Universidad', 'Nombre']], on='id', how='inner')

# Crear un selector de universidades
universidades = ruct_combined['Universidad'].unique()

# Establecer la universidad por defecto
default_universidad = "['Universidad Carlos III de Madrid']"

# Verificar si la universidad por defecto está en la lista de universidades y obtener su índice
default_index = list(universidades).index(default_universidad) if default_universidad in universidades else 0

# Crear el selector de universidades con la universidad por defecto
universidad_1 = st.selectbox('Select university:', universidades, index=default_index)

# Filtrar el DataFrame según las universidades seleccionadas
df_uni_1 = ruct_combined[ruct_combined['Universidad'] == universidad_1]

# Crear una lista con las columnas que queremos comparar
text_columns = {
    'Modules': 'Modulo_raw_text',
    'Matters': 'Materias_raw_text',
    'Subjects': 'Asignaturas_raw_text',
    'Contents': 'Contenidos_raw_text',
    'Competences': 'Competencias_Especificas_raw_text'
}

lemmas_columns = {
    'Modules': 'Modulo_lemmas',
    'Matters': 'Materias_lemmas',
    'Subjects': 'Asignaturas_lemmas',
    'Contents': 'Contenidos_lemmas',
    'Competences': 'Competencias_lemmas'
}

figures_uni_1 = []

# Initialize a list to store the charts
for key in text_columns:
    # Calcular conteos para la primera universidad
    df_uni_1['raw_word_count'] = df_uni_1[text_columns[key]].apply(lambda x: len(x.split()))
    df_uni_1['lemma_word_count'] = df_uni_1[lemmas_columns[key]].apply(lambda x: len(x.split()))

    # Crear el gráfico para la primera universidad
    fig_1 = go.Figure()
    fig_1.add_trace(go.Bar(
        x=df_uni_1.index,
        y=df_uni_1['raw_word_count'],
        name=f'{key} - Raw text',
        marker_color='#26558e',
        opacity=0.6
    ))
    fig_1.add_trace(go.Scatter(
        x=df_uni_1.index,
        y=df_uni_1['lemma_word_count'],
        mode='lines',
        name=f'{key} - Lemmas',
        fill='tozeroy',
        line=dict(color='#f8acff'),
        opacity=0.6
    ))
    fig_1.update_layout(
        title=f'{key}',
        xaxis_title='Documents',
        yaxis_title='Raw text  /  Lemmas Count',
        barmode='overlay',
        hovermode='x unified',
        height=400,  # Aumenta la altura del gráfico
        width=900,  # Aumenta el ancho del gráfico
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),  # Leyenda debajo del gráfico
        margin=dict(l=50, r=50, t=50, b=100),
    )
    figures_uni_1.append(fig_1)

col1, col2= st.columns([1, 1])  # Igualar el ancho de las columnas

with col1:
    st.plotly_chart(figures_uni_1[1], use_container_width=True)

with col2:
    st.plotly_chart(figures_uni_1[2], use_container_width=True)

col3, col4= st.columns([1, 1])
with col3:
    st.plotly_chart(figures_uni_1[3], use_container_width=True)

with col4:
    st.plotly_chart(figures_uni_1[4], use_container_width=True)


st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="first">Topic Decomposition by Degree</h3>
    <hr class="separator">
    <p>Topic decomposition, also known as <strong><span style="color: orange;">topic modeling</span></strong>, is a way for computers to find hidden themes or topics in a large collection of text, like articles, books, etc. 
    <p>I have created and fine-tuned a topic model for Registro de Universidades dataset with all the contents, training systems, competences, modules and subjects for every degree and masters, so if you select a bachelor or masters, you will see its main topics.</p>
    """,
    unsafe_allow_html=True
)

#### estos datos son los que están procesados, es decir, los lematizados (que ya estaban filtrados, recalcar)
# ¿por qué de 5500 observaciones filtradas solo se han utilizado 2600 en el topic modeling?
# Crear un índice automático si no tienen índice
topic_coords['index'] = topic_coords.index
topic_names['index'] = topic_names.index

# Unir las bases de datos sobre el índice
topic_info = pd.merge(topic_names, topic_coords, on='index')
topic_info = topic_info.drop(columns=['index'])

topic_info['x'] = topic_info['tpc_coordinates'].apply(lambda coord: float(coord.strip("()").split(",")[0]))
topic_info['y'] = topic_info['tpc_coordinates'].apply(lambda coord: float(coord.strip("()").split(",")[1]))

df_ruct_topics['id'] = df_ruct_topics['id'].astype(int)
ruct_topics_info = pd.merge(ruct_final, df_ruct_topics[['id', 'tpc_decomposition']], on='id')

col1, col2= st.columns([1, 1])

with col1:

    # Filtrar la lista de universidades y grados
    universidades = ruct_topics_info['Universidad'].unique()
    # Establecer la universidad por defecto
    default_universidad = "['Universidad Carlos III de Madrid']"
    # Verificar si la universidad por defecto está en la lista de universidades y obtener su índice
    default_index = list(universidades).index(default_universidad) if default_universidad in universidades else 0

    selected_uni = st.selectbox('Select University', universidades, index=default_index)

with col2:
    grados = ruct_topics_info[ruct_topics_info['Universidad'] == selected_uni]['Nombre'].unique().tolist()
    selected_grado = st.selectbox('Select a degree (Bachelor or Masters)', grados)
    selected_data = ruct_topics_info[(ruct_topics_info['Universidad'] == selected_uni) & (ruct_topics_info['Nombre'] == selected_grado)]

selected_doc = selected_data.iloc[0]  # Seleccionar el primer documento
tpc_decomposition_list = selected_doc['tpc_decomposition']  # Obtener la lista de importancias

# Crear un DataFrame para la descomposición de tópicos
expanded_data = pd.DataFrame({
    'tpc_names': topic_info['tpc_names'],  # Nombres de los tópicos
    'x': topic_info['x'],  # Coordenada X
    'y': topic_info['y'],  # Coordenada Y
    'tpc_decomposition': tpc_decomposition_list  # Importancia del tópico
})

# Filtrar datos para eliminar tópicos con importancia cero
expanded_data = expanded_data[expanded_data['tpc_decomposition'] > 0]

tab1, tab2= st.tabs(["Bubble Chart", "Table (Topic Decomposition)"])
with tab1:

    # Paso 2: Crear el gráfico de burbujas
    fig = px.scatter(
        expanded_data,
        x='x',
        y='y',
        size='tpc_decomposition',  # Tamaño de la burbuja según la importancia del tópico
        hover_name='tpc_names',  # Nombre del tópico
        hover_data={'tpc_decomposition': True},  # Mostrar la importancia al pasar el ratón
        title=f'Topic modeling for: {selected_grado}',
        labels={'x': 'PCA 1', 'y': 'PCA 2'}
    )

    # Ajustar el tamaño de las burbujas
    max_decomposition = expanded_data['tpc_decomposition'].max()
    fig.update_traces(marker=dict(sizemode='area', sizeref=2.*max_decomposition/(100**2), line_width=2))
    fig.update_layout(showlegend=True)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

with tab2:
    # 'ruct_topics_info' contiene la descomposición de tópicos

    # Extraer la descomposición de tópicos para el primer documento en los datos seleccionados
    selected_doc_tpc = selected_data['tpc_decomposition'].values[0]  # Obtén el primer documento de los datos filtrados

    # Convertir la lista de descomposición de tópicos en un DataFrame
    expanded_data = pd.DataFrame({
        'tpc_names': topic_info['tpc_names'],  # Nombres de los tópicos
        'tpc_decomposition': selected_doc_tpc  # Importancia del tópico para el documento seleccionado
    })

    expanded_data_filtered = expanded_data[expanded_data['tpc_decomposition'] > 0]

    # Ordenar el DataFrame por la importancia del tópico en orden descendente
    expanded_data_sorted = expanded_data_filtered.sort_values(by='tpc_decomposition', ascending=False)

    # Mostrar la tabla en Streamlit con solo el nombre del tópico y la importancia
    st.dataframe(expanded_data_sorted[['tpc_names', 'tpc_decomposition']].reset_index(drop=True))


st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="first">Wordcloud Representation by University</h3>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)
# Selección de universidad
universidades = ruct_combined['Universidad'].unique()
selected_uni = st.selectbox('Select university', universidades, key='uni_selector')

# Filtrar los datos para la universidad seleccionada
selected_data = ruct_combined[ruct_combined['Universidad'] == selected_uni]

# Combinar todas las columnas de lemas en un solo texto
columns_to_include = ['Modulo_lemmas', 'Materias_lemmas', 'Asignaturas_lemmas', 'Contenidos_lemmas', 'Competencias_lemmas']
combined_text = ' '.join(selected_data[columns_to_include].astype(str).apply(lambda x: ' '.join(x), axis=1))

custom_stopwords = set(STOPWORDS).union(STOPWORDS_NLTK)  # Usar el conjunto de stopwords por defecto
custom_stopwords.update(['el', 'la', 'los', 'las', 'de', 'y', 'en', 'introducción', 'sistema', 'i', 'ii', 'iii',
                         'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xx', 'principale', 'módulo', 'materia', 'international',
                         'interacionale', 'content_course', 'description', 'course_description', 'eta', 'ámbito', 'sistemas', 'tema',
                         'concepto', 'tipo', 'introduction', 'system', 'alumno', 'alumnado','esta_asignatura', 'comprender', 'clases problemas',
                         'asignatura', 'estudiante', 'estudiantes', 'alumnos', 'herramienta', 'conceptos'])  # Añadir palabras específicas
# Generar el WordCloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='black',
    stopwords=custom_stopwords  # Pasar el conjunto de stopwords personalizado
).generate(combined_text)

# Mostrar el WordCloud en Streamlit
st.image(wordcloud.to_image(), caption=f'Lemmas WordCloud for {selected_uni}')

st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="first">Wordcloud Representation by Degree</h3>
    <hr class="separator">
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([1,1])

with col1:
    # Selección de universidad
    universidades = ruct_combined['Universidad'].unique()
    selected_uni = st.selectbox('Select university', universidades, key='uni2_selector')

with col2:
    grados = ruct_combined[ruct_combined['Universidad'] == selected_uni]['Nombre'].unique()
    selected_grado = st.selectbox('Select a degree (Bachelor or Masters)', grados,key='grado2_selector')

# Filtrar los datos para el grado seleccionado
selected_data = ruct_combined[(ruct_combined['Universidad'] == selected_uni) &
                                   (ruct_combined['Nombre'] == selected_grado)]

# Combinar todas las columnas de lemas en un solo texto
columns_to_include = ['Modulo_lemmas', 'Materias_lemmas', 'Asignaturas_lemmas', 'Contenidos_lemmas', 'Competencias_lemmas']
combined_text = ' '.join(selected_data[columns_to_include].astype(str).apply(lambda x: ' '.join(x), axis=1))

custom_stopwords = set(STOPWORDS).union(STOPWORDS_NLTK)  # Usar el conjunto de stopwords por defecto
custom_stopwords.update(['el', 'la', 'los', 'las', 'de', 'y', 'en', 'introducción', 'sistema', 'i', 'ii', 'iii',
                         'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xx', 'principale', 'módulo', 'materia', 'international',
                         'interacionale', 'content_course', 'description', 'course_description', 'eta', 'ámbito', 'sistemas', 'tema',
                         'concepto', 'tipo','introduction', 'system', 'alumno', 'alumnado','esta_asignatura', 'comprender', 'clases problemas',
                         'asignatura', 'estudiante', 'estudiantes', 'alumnos', 'herramienta', 'conceptos', 'contrato', 'práctica'])  # Añadir palabras específicas
# Generar el WordCloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='black',
    stopwords=custom_stopwords  # Pasar el conjunto de stopwords personalizado
).generate(combined_text)

# Mostrar el WordCloud en Streamlit
st.image(wordcloud.to_image(), caption=f'Lemmas WordCloud for {selected_grado}')

st.markdown(
    """
    <div class="spacer"></div> <!-- Espaciado superior -->
    <h3 id="first">Job Recommendation System based on Degree</h3>
    <hr class="separator">    
    <p>This recommendation system uses an advanced model to <strong><span style="color: orange;">find job vacancies that are most similar to a specific study</span></strong> (bachelor or masters).</p> 
    <p>It presents the user with the most relevant options and provides them with a visualisation of the key skills and topics associated with these vacancies. This can help students or graduates identify which jobs might best align with their studies and competences.</p>
    """,
    unsafe_allow_html=True
)

# do something
# Supongamos que tienes la matriz de similaridad como un DataFrame
# con los IDs de documentos de Tecnoempleo en las filas y documentos de RUCT en las columnas
# Supongamos que tienes un DataFrame con los nombres de los documentos de Tecnoempleo

tecnoempleo_lemmas = tecnoempleo_lemmas.drop_duplicates(subset=['title_translated_raw_text', 'skills_raw_text'])

container = st.container(border=True)
with container:
    col1, col2 = st.columns(2)

    with col1:
        # Filtrar la lista de universidades y grados para seleccionar un documento de RUCT
        universidades = ruct_topics_info['Universidad'].unique()
        # Establecer la universidad por defecto
        default_universidad = "['Universidad Carlos III de Madrid']"

        # Verificar si la universidad por defecto está en la lista de universidades y obtener su índice
        default_index = list(universidades).index(default_universidad) if default_universidad in universidades else 0

        # Crear el selector de universidades con la universidad por defecto
        selected_uni = st.selectbox('Select university', universidades, key='uni4_selector', index=default_index)
    with col2:

        grados = ruct_topics_info[ruct_topics_info['Universidad'] == selected_uni]['Nombre'].unique()
        selected_grado = st.selectbox('Select a degree (Bachelor or Masters)', grados, key='grado4_selector')

    # Filtrar los datos para el grado seleccionado
    selected_data = ruct_topics_info[(ruct_topics_info['Universidad'] == selected_uni) &
                                       (ruct_topics_info['Nombre'] == selected_grado)]

    selected_doc_id = str(selected_data['id'].values[0])

    # Convertir el índice a una columna y renombrarla a 'id'
    similarity_bert_cosine['id'] = similarity_bert_cosine.index
    similarities = similarity_bert_cosine.loc[:, ['id', selected_doc_id]]

    # Encontrar los 10 documentos más similares de Tecnoempleo
    top_10_similar = similarities.nlargest(10, selected_doc_id)  # Encuentra los 10 valores más grandes
    top_10_ids = top_10_similar['id'].tolist()

    filtered_10_df = tecnoempleo_lemmas[tecnoempleo_lemmas['id'].isin(top_10_ids)]

    # Obtener los nombres de los documentos de Tecnoempleo más similares
    top_10_names = filtered_10_df['title_translated_raw_text'].tolist()
    top_10_skills = filtered_10_df['skills_raw_text']

    #top_10_names.rename(columns={'name': 'Nombre del Documento'}, inplace=True)
    #top_10_skills.rename(columns={'name': 'Habilidades y softwares'}, inplace=True)

    data = {
        'Job': top_10_names,
        'Skills': top_10_skills
    }
    df = pd.DataFrame(data)

    # Mostrar los nombres en Streamlit
    st.write(f"**Most similar job vacancies to {selected_grado}**:")
    st.dataframe(df, width=3000)


    columns_to_include = ['title_translated_raw_text', 'skills_raw_text']
    combined_text = ' '.join(filtered_10_df[columns_to_include].astype(str).apply(lambda x: ' '.join(x), axis=1))

    custom_stopwords = set(STOPWORDS).union(STOPWORDS_NLTK)  # Usar el conjunto de stopwords por defecto
    custom_stopwords.update(['el', 'la', 'los', 'las', 'de', 'y', 'en', 'introducción', 'sistema', 'i', 'ii', 'iii',
                             'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xx', 'principale', 'módulo', 'materia', 'international',
                             'interacionale', 'content_course', 'description', 'course_description', 'eta', 'ámbito', 'sistemas', 'tema',
                             'concepto', 'tipo', 'Empleo', 'Becario', 'TelecomunicacionesElectronica'])  # Añadir palabras específicas
    # Generar el WordCloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='black',
        stopwords=custom_stopwords  # Pasar el conjunto de stopwords personalizado
    ).generate(combined_text)

    # Mostrar el WordCloud en Streamlit
    st.image(wordcloud.to_image(), caption=f'Lemmas WordCloud for {selected_grado}')

st.header("Steps to Derive the Recommendation System")

with st.expander('1. Selecting the Reference Document'):
    st.write("""
    - First, the user selects a specific document, which in this case is a university study.
    - This document is our starting point, and we want to find job vacancies that are similar to it in terms of content.
    """)

with st.expander('2. Calculating Similarity'):
    st.write("""
    - We have a table called `similarity_bert_cosine` that contains similarity scores between documents. These scores tell us how similar one study is to a job vacancy.
    - We use similarity based on `BERT` embeddings, an advanced natural language processing model that understands the meaning of the text, not just individual words.
    - We extract similarity scores between the selected document and other documents (in this case, job vacancies).
    """)

with st.expander('3. Selecting the Most Similar Documents'):
    st.write("""
    - We select the top 10 job vacancies that are most similar to the selected document.
    - We filter these documents from the database to focus only on them.
    """)

with st.expander('4. Visualizing the Results'):
    st.write("""
    - We display the titles of the 10 most similar job vacancies along with the skills required for each.
    - This allows the user to see which jobs are most aligned with the selected degree.
    """)

with st.expander('5. Generating the WordCloud'):
    st.write("""
    - A **WordCloud** is a visualization where words that appear more frequently in a text are shown larger.
    - We take the combined text from the job titles and the associated skills of these 10 similar documents.
    - We filter out common words that don't add value (like "the", "and", etc.) using a custom list of **stopwords**.
    - We generate and display a **WordCloud** to provide a visual representation of the most relevant skills and topics in these job vacancies.
    """)

