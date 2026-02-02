import streamlit as st
import re

# ======================
# 페이지 설정
# ======================
st.set_page_config(page_title="생활기록부 자가 점검", layout="centered")
st.title("📘 생활기록부 self 점검")

st.markdown("""
한 번만 입력하면  
📏 바이트 계산+🧠 문장 자동 분류+🖍️ 구조 점검
  
""")

# ======================
# 기준 선택
# ======================
MAX_BYTES = st.selectbox(
    "📌 바이트 기준 선택",
    [500, 1000, 1500, 2000],
    index=2
)

# ======================
# 입력 (★ 단 하나 ★)
# ======================
text = st.text_area(
    "✏️ 생활기록부 줄글 입력",
    height=260,
    placeholder=(
        "수업 중 문제를 변형하여 풀이 전략을 설명함."
        "친구들이 이해하기 어려워했기 때문임."
        "개념 이해와 의사소통 능력이 향상됨."
        "설명하는 과정에서 나도 더 깊이 이해하게 됨."
    )
)

# ======================
# 바이트 계산 (NEIS 기준)
# ======================
def calc_bytes(text):
    total = 0
    for ch in text:
        total += 1 if ord(ch) <= 127 else 3
    return total

# ======================
# 문장 분해 + 분류
# ======================
def classify(text):
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    result = {
        "동기": [],
        "행동": [],
        "결론": [],
        "느낀점": []
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
# 실행 (입력 1번 → 전부)
# ======================
if text.strip():
    st.divider()

    total_bytes = calc_bytes(text)
    classified = classify(text)

    # ---------- 요약 ----------
    st.subheader("📊 요약")

    col1, col2 = st.columns(2)
    col1.metric("글자 수", len(text))
    col2.metric("바이트 수", total_bytes)

    st.progress(min(total_bytes / MAX_BYTES, 1.0))

    if total_bytes > MAX_BYTES:
        st.error(f"❌ {total_bytes - MAX_BYTES} byte 초과")
    else:
        st.success(f"✅ {MAX_BYTES - total_bytes} byte 여유")

    st.divider()

    # ---------- 분류 결과 ----------
    st.subheader("🧠 자동 분류 결과")

    icons = {
        "동기": "🔴 [동기]",
        "행동": "🔵 [행동]",
        "결론": "🟢 [결론]",
        "느낀점": "🟠 [느낀점]"
    }

    for k in ["동기", "행동", "결론", "느낀점"]:
        if classified[k]:
            content = ". ".join(classified[k]) + "."
            st.markdown(f"**{icons[k]}** {content}")
            st.caption(f"바이트: {calc_bytes(content)}")

