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

# ------------------------------------------------------------
# 2. 장르 안의 영화 - 트리맵 (칸 크기: 총 관객)
# ------------------------------------------------------------
st.header("2. 장르 안의 영화 (트리맵)")

fig_treemap = px.treemap(
    df,
    path=[px.Constant("전체"), "genre", "movieNm"],
    values="total_audi",
)
fig_treemap.update_traces(
    hovertemplate="%{label}<br>총 관객: %{value:,.0f}명<extra></extra>"
)
fig_treemap.update_layout(margin=dict(t=30, b=30, l=0, r=0))

st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 3. 총 관객 히스토그램
# ------------------------------------------------------------
st.header("3. 총 관객(total_audi) 히스토그램")

fig_hist = px.histogram(
    df,
    x="total_audi",
    nbins=30,
)
fig_hist.update_traces(
    hovertemplate="관객 구간: %{x}<br>영화 수: %{y}편<extra></extra>"
)
fig_hist.update_layout(
    xaxis_title="총 관객수",
    yaxis_title="영화 편수",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_hist, use_container_width=True)

# 가장 많이 몰려 있는 구간과 최다 관객 영화 계산
bin_series = pd.cut(df["total_audi"], bins=30)
top_bin = bin_series.value_counts().idxmax()
top_bin_count = bin_series.value_counts().max()

top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown(
    f"**이 그래프로 알 수 있는 것:** 영화는 대부분 총 관객 "
    f"약 {top_bin.left:,.0f}명 ~ {top_bin.right:,.0f}명 구간에 몰려 있으며 "
    f"({top_bin_count}편), 가장 많은 관객을 동원한 영화는 "
    f"**{top_movie_row['movieNm']}**"
    f"(총 관객 {top_movie_row['total_audi']:,.0f}명)입니다."
)

st.divider()

# ------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객 - 산점도
# ------------------------------------------------------------
st.header("4. 개봉일 스크린수와 총 관객의 관계 (산점도)")

fig_scatter = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
)
fig_scatter.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 5. 장르별 총 관객 - 상자 그림 (영화 10편 이상 장르만)
# ------------------------------------------------------------
st.header("5. 장르별 총 관객 분포 (상자 그림)")

genre_movie_counts = df["genre"].value_counts()
genres_10plus = genre_movie_counts[genre_movie_counts >= 10].index
df_box = df[df["genre"].isin(genres_10plus)]

fig_box = px.box(
    df_box,
    x="genre",
    y="total_audi",
    hover_data={"movieNm": True},
)
fig_box.update_traces(
    hovertemplate="%{customdata[0]}<br>총 관객: %{y:,.0f}명<extra></extra>"
)
fig_box.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객수",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 6. 개봉일 스크린수 vs 총 관객 - 버블 그래프 (크기: 첫 주 관객)
# ------------------------------------------------------------
st.header("6. 개봉일 스크린수와 총 관객의 관계 (버블 그래프)")

fig_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    size="first_week_audi",
    hover_name="movieNm",
    size_max=40,
)
fig_bubble.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객수",
    legend_title_text="장르",
    margin=dict(t=30, b=30, l=0, r=0),
)

st.plotly_chart(fig_bubble, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# ------------------------------------------------------------
# 7. 제작 국가 -> 장르 - 선버스트 (칸 크기: 영화 편수)
# ------------------------------------------------------------
st.header("7. 제작 국가에서 장르로 (선버스트)")

fig_sunburst = px.sunburst(
    df,
    path=["nation", "genre"],
)
fig_sunburst.update_traces(
    hovertemplate="%{label}<br>영화 수: %{value}편<extra></extra>"
)
fig_sunburst.update_layout(margin=dict(t=30, b=30, l=0, r=0))

st.plotly_chart(fig_sunburst, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()
