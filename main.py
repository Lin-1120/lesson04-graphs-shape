import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화들의 데이터를 그래프로 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

try:
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# 데이터 전처리
# --------------------------------------------------

# 장르가 여러 개이면 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("기타")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 비어 있는 장르는 기타로 처리
df.loc[
    df["genre_first"].isin(["", "nan", "None"]),
    "genre_first"
] = "기타"

# 총 관객 수를 숫자로 변환
df["total_audi_num"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
)


# ==================================================
# 첫 번째 그래프
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
        "비율: %{percent}<extra></extra>"
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
# 두 번째 그래프
# ==================================================
st.divider()

st.subheader("🌳 그래프 2. 장르별 영화와 총 관객")

treemap_df = df.dropna(
    subset=["total_audi_num", "movieNm", "genre_first"]
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
# 세 번째 그래프
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
# 히스토그램에서 가장 많이 몰린 구간 계산
# --------------------------------------------------
min_audi = hist_df["total_audi_num"].min()
max_audi = hist_df["total_audi_num"].max()

# 히스토그램과 동일하게 15개 구간으로 나눔
bins = pd.cut(
    hist_df["total_audi_num"],
    bins=15,
    include_lowest=True
)

bin_counts = bins.value_counts().sort_index()

most_common_bin = bin_counts.idxmax()
most_common_count = bin_counts.max()

# 가장 관객이 많은 영화
max_audi = hist_df["total_audi_num"].max()

top_movies = hist_df[
    hist_df["total_audi_num"] == max_audi
]

top_movie_names = ", ".join(
    top_movies["movieNm"].astype(str).tolist()
)


# --------------------------------------------------
# 그래프로 알 수 있는 것
# --------------------------------------------------
st.markdown("#### 💡 이 그래프로 알 수 있는 것")

st.info(
    f"대부분의 영화는 총 관객 수가 "
    f"**{most_common_bin.left:,.0f}명~{most_common_bin.right:,.0f}명** "
    f"구간에 몰려 있으며, 이 구간에는 **{most_common_count}편**의 영화가 있습니다. "
    f"가장 관객이 많은 영화는 **{top_movie_names}**으로, "
    f"총 관객은 **{max_audi:,.0f}명**입니다."
)


# ==================================================
# 데이터 확인
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
