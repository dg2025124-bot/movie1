import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    """
1년간 박스오피스 10위권에 든 영화 가운데, 해당 기간에 개봉한 216편의 데이터를 바탕으로
분포와 관계를 살펴보는 그래프 모음입니다.
"""
)


@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # genre 열에 세로막대 기호(|)로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    # openDt(여덟 자리 숫자)를 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    return df


df = load_data()

st.divider()

# ------------------------------------------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ------------------------------------------------------------
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.5,
)
fig_genre.update_traces(
    hovertemplate="%{label}<br>%{value}편<br>비율: %{percent}<extra></extra>"
)
fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()
