import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="생활기록부 바이트 계산기", layout="centered")
st.title("🧾 생활기록부 바이트 계산기")

st.markdown("""
생활기록부 입력 내용을 **바이트 기준**으로 계산합니다.  
(교육청 시스템과 동일한 방식)
""")

# -----------------------------
# 기준 설정
# -----------------------------
MAX_BYTES = st.selectbox(
    "📌 항목별 바이트 기준 선택",
    [500, 1000, 1500, 2000],
    index=2
)

# -----------------------------
# 텍스트 입력
# -----------------------------
text = st.text_area(
    "✏️ 생활기록부 내용을 입력하세요",
    height=250,
    placeholder="예) 수업에 성실히 참여하며 개념 이해도가 높고..."
)

# -----------------------------
# 바이트 계산 함수
# -----------------------------
def calculate_bytes(text):
    total = 0
    for ch in text:
        if ord(ch) <= 127:
            total += 1      # 영문, 숫자, 특수문자
        else:
            total += 3      # 한글, 한자, 기타 유니코드
    return total

current_bytes = calculate_bytes(text)

# -----------------------------
# 결과 출력
# -----------------------------
st.subheader("📊 바이트 계산 결과")

col1, col2 = st.columns(2)

col1.metric("현재 바이트", f"{current_bytes} byte")
col2.metric("기준 바이트", f"{MAX_BYTES} byte")

progress = min(current_bytes / MAX_BYTES, 1.0)
st.progress(progress)

# -----------------------------
# 상태 메시지
# -----------------------------
if current_bytes < MAX_BYTES:
    st.success(f"✅ {MAX_BYTES - current_bytes} byte 남았습니다.")
elif current_bytes == MAX_BYTES:
    st.warning("⚠️ 정확히 기준 바이트에 도달했습니다.")
else:
    st.error(f"❌ {current_bytes - MAX_BYTES} byte 초과했습니다.")

# -----------------------------
# 추가 정보
# -----------------------------
with st.expander("ℹ️ 바이트 계산 기준 안내"):
    st.markdown("""
- 한글 / 한자 / 대부분의 특수문자: **3 byte**
- 영문 / 숫자 / 기본 특수문자: **1 byte**
- 실제 교육행정정보시스템(NEIS) 기준과 동일
""")




import streamlit as st
import re

st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("📘 생활기록부 자동 분류 & 바이트 계산기")

# ======================
# 입력
# ======================
text = st.text_area(
    "생활기록부 문장을 입력하세요 (태그·줄바꿈 없어도 됩니다)",
    height=200,
    placeholder=(
        "수업 중 문제를 변형하여 풀이 전략을 설명함."
        "친구들이 이해하기 어려워했기 때문임."
        "개념 이해와 의사소통 능력이 향상됨."
        "교과서 p.132, 추가 자료를 설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# ======================
# 바이트 계산
# ======================
def calc_bytes(s):
    return len(s.encode("utf-8"))

# ======================
# 문장 분해 + 의미 기반 분류
# ======================
def classify_sentences(text):
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    result = {
        "행동": "",
        "동기": "",
        "결론": "",
        "참고": "",
        "느낀점": ""
    }

    for s in sentences:
        if any(k in s for k in ["수업", "설명", "풀이", "활동", "발표", "수행","보고서","토론","시연","시뮬레이션","나타냄","증명","참여"]):
            result["행동"] += s + ". "
        elif any(k in s for k in ["때문", "이유", "어려워", "동기", "하므로","이므로","위해","위해서","필요"]):
            result["동기"] += s + ". "
        elif any(k in s for k in ["향상", "성장", "깨달", "이해", "결론","결과","도출","능력"]):
            result["결론"] += s + ". "
        elif any(k in s for k in ["교과서", "자료", "논문", "p.","도서", "페이지"]):
            result["참고"] += s + ". "
        else:
            result["느낀점"] += s + ". "

    return result

# ======================
# 처리
# ======================
if text:
    st.divider()

    classified = classify_sentences(text)
    total_bytes = calc_bytes(text)

    st.info(f"📏 전체 바이트 수: **{total_bytes} byte**")
    st.divider()

    icons = {
        "행동": "🔵 [행동]",
        "동기": "🔴 [동기]",
        "결론": "🟢 [결론]",
        "참고": "🟣 [참고]",
        "느낀점": "🟠 [느낀점]"
    }

    for key in ["행동", "동기", "결론", "참고", "느낀점"]:
        content = classified[key].strip()
        if content:
            st.markdown(f"**{icons[key]}** {content}")
            st.caption(f"➡️ 바이트 수: {calc_bytes(content)} byte")

    st.divider()

    if total_bytes > 1500:
        st.error("⚠️ 생활기록부 권장 바이트 수를 초과했습니다.")
    else:
        st.success("✅ 생활기록부 바이트 기준에 적절합니다.")
