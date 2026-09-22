import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 페이지 설정
# ==================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# 제목
# ==================================================
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화들의 데이터를 그래프로 살펴봅니다.")


# ==================================================
# 데이터 불러오기
# ==================================================
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)

try:
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# ==================================================
# 데이터 전처리
# ==================================================

# 여러 장르가 있으면 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("기타")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 빈 장르는 기타로 처리
df.loc[
    df["genre_first"].isin(["", "nan", "None"]),
    "genre_first"
] = "기타"

# 제작 국가가 비어 있으면 기타로 처리
df["nation_clean"] = (
    df["nation"]
    .fillna("기타")
    .astype(str)
    .str.strip()
)

df.loc[
    df["nation_clean"].isin(["", "nan", "None"]),
    "nation_clean"
] = "기타"


# 숫자형으로 변환
df["total_audi_num"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)

df["first_scrn_num"] = pd.to_numeric(
    df["first_scrn"],
    errors="coerce"
)

df["first_week_audi_num"] = pd.to_numeric(
    df["first_week_audi"],
    errors="coerce"
)


# ==================================================
# 그래프 1
# 장르별 영화 편수 도넛 그래프
# ==================================================
st.divider()

st.subheader("📊 그래프 1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="영화 편수")
)

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=550,
    margin=dict(t=70, b=30, l=30, r=30),
    legend_title_text="장르"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프로 알 수 있는 내용을 적어 보세요."
)


# ==================================================
# 그래프 2
# 장르별 영화 트리맵
# ==================================================
st.divider()

st.subheader("🌳 그래프 2. 장르별 영화와 총 관객")

treemap_df = df.dropna(
    subset=[
        "total_audi_num",
        "movieNm",
        "genre_first"
    ]
).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi_num",
    title="장르 안에 들어 있는 영화별 총 관객"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=700,
    margin=dict(t=70, b=30, l=20, r=20)
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프로 알 수 있는 내용을 적어 보세요."
)


# ==================================================
# 그래프 3
# 총 관객 히스토그램
# ==================================================
st.divider()

st.subheader("📈 그래프 3. 영화별 총 관객 분포")

hist_df = df.dropna(
    subset=["total_audi_num"]
).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi_num",
    nbins=15,
    title="총 관객 수의 분포",
    labels={
        "total_audi_num": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=550,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=70, b=50, l=50, r=30)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# --------------------------------------------------
# 가장 많은 영화가 몰린 구간 계산
# --------------------------------------------------
bins = pd.cut(
    hist_df["total_audi_num"],
    bins=15,
    include_lowest=True
)

bin_counts = bins.value_counts().sort_index()

most_common_bin = bin_counts.idxmax()
most_common_count = bin_counts.max()


# --------------------------------------------------
# 가장 관객이 많은 영화 계산
# --------------------------------------------------
max_audi = hist_df["total_audi_num"].max()

top_movies = hist_df[
    hist_df["total_audi_num"] == max_audi
]

top_movie_names = ", ".join(
    top_movies["movieNm"].astype(str).tolist()
)


st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    f"대부분의 영화는 총 관객 수가 "
    f"**{most_common_bin.left:,.0f}명~"
    f"{most_common_bin.right:,.0f}명** 구간에 몰려 있으며, "
    f"이 구간에는 **{most_common_count}편**의 영화가 있습니다. "
    f"가장 관객이 많은 영화는 **{top_movie_names}**으로, "
    f"총 관객은 **{max_audi:,.0f}명**입니다."
)


# ==================================================
# 그래프 4
# 개봉일 스크린 수와 총 관객 산점도
# ==================================================
st.divider()

st.subheader("🔵 그래프 4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df.dropna(
    subset=[
        "first_scrn_num",
        "total_audi_num",
        "movieNm",
        "genre_first"
    ]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn_num",
    y="total_audi_num",
    color="genre_first",
    hover_name="movieNm",
    custom_data=["genre_first"],
    title="개봉일 스크린 수와 총 관객",
    labels={
        "first_scrn_num": "개봉일 스크린 수",
        "total_audi_num": "총 관객 수",
        "genre_first": "장르"
    }
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
    margin=dict(t=70, b=50, l=50, r=30)
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프로 알 수 있는 내용을 적어 보세요."
)


# ==================================================
# 그래프 5
# 장르별 총 관객 박스플롯
# ==================================================
st.divider()

st.subheader("📦 그래프 5. 장르별 총 관객 분포")

# 영화가 10편 이상인 장르만 선택
genre_movie_counts = df["genre_first"].value_counts()

valid_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

boxplot_df = df[
    df["genre_first"].isin(valid_genres)
].dropna(
    subset=[
        "total_audi_num",
        "movieNm",
        "genre_first"
    ]
).copy()

fig5 = px.box(
    boxplot_df,
    x="genre_first",
    y="total_audi_num",
    points="outliers",
    hover_name="movieNm",
    custom_data=["genre_first"],
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre_first": "장르",
        "total_audi_num": "총 관객 수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    margin=dict(t=70, b=50, l=50, r=30)
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프로 알 수 있는 내용을 적어 보세요."
)


# ==================================================
# 그래프 6
# 첫 주 관객을 점 크기로 넣은 버블 그래프
# ==================================================
st.divider()

st.subheader(
    "🫧 그래프 6. 개봉일 스크린 수와 총 관객 "
    "— 첫 주 관객 버블"
)

bubble_df = df.dropna(
    subset=[
        "first_scrn_num",
        "total_audi_num",
        "first_week_audi_num",
        "movieNm",
        "genre_first"
    ]
).copy()

fig6 = px.scatter(
    bubble_df,
    x="first_scrn_num",
    y="total_audi_num",
    size="first_week_audi_num",
    color="genre_first",
    hover_name="movieNm",
    custom_data=[
        "genre_first",
        "first_week_audi_num"
    ],
    size_max=55,
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn_num": "개봉일 스크린 수",
        "total_audi_num": "총 관객 수",
        "first_week_audi_num": "첫 주 관객",
        "genre_first": "장르"
    }
)

fig6.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{customdata[1]:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title_text="장르",
    margin=dict(t=70, b=50, l=50, r=30)
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프로 알 수 있는 내용을 적어 보세요."
)


# ==================================================
# 그래프 7
# 제작 국가 → 장르 선버스트
# ==================================================
st.divider()

st.subheader("☀️ 그래프 7. 제작 국가에서 장르로 내려가는 영화 구성")

sunburst_df = df[
    [
        "nation_clean",
        "genre_first"
    ]
].copy()

# 국가와 장르별 영화 편수를 계산
sunburst_counts = (
    sunburst_df
    .groupby(
        ["nation_clean", "genre_first"],
        as_index=False
    )
    .size()
    .rename(columns={"size": "영화 편수"})
)

fig7 = px.sunburst(
    sunburst_counts,
    path=["nation_clean", "genre_first"],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=700,
    margin=dict(t=70, b=30, l=20, r=20)
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    "이곳에 이 그래프로 알 수 있는 내용을 적어 보세요."
)


# ==================================================
# 원본 데이터 확인
# ==================================================
with st.expander("📋 사용한 데이터 확인하기"):
    st.dataframe(
        df[
            [
                "movieCd",
                "movieNm",
                "openDt",
                "genre",
                "genre_first",
                "nation",
                "first_scrn",
                "first_show",
                "first_week_audi",
                "total_audi",
                "days_in_top10"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
