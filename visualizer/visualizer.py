import streamlit as st
import redis
import pandas as pd
import time

REDIS_CONECTION = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

st.set_page_config(page_title="Visualizer", layout="wide")
st.title("Conteo palabras en repositorios de GitHub (Java/Python)")

top_n = st.sidebar.slider("Top N palabras", 5, 50, 15)
placeholder = st.empty()

while True:
    try:
        data = REDIS_CONECTION.zrevrange('word_count', 1, top_n - 1, withscores=True)
        if data:
            df = pd.DataFrame(data, columns=['Palabra', 'Frecuencia'])
            with placeholder.container():
                st.bar_chart(df.set_index('Palabra'))
                st.table(df)
        else:
            st.info("Esperando datos del Miner...")

    except Exception as e:
        st.error(f"Error de conexión: {e}")
    
    time.sleep(2)