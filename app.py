# from datetime import datetime

# import streamlit as st
# from supabase import create_client


# st.set_page_config(
#     page_title="내 메모장",
#     page_icon="📝",
#     layout="centered",
# )


# @st.cache_resource
# def get_supabase_client():
#     url = st.secrets["SUPABASE_URL"]
#     key = st.secrets["SUPABASE_KEY"]
#     return create_client(url, key)


# supabase = get_supabase_client()


# def add_note(title, content):
#     supabase.table("notes").insert(
#         {
#             "title": title,
#             "content": content,
#         }
#     ).execute()


# def get_notes():
#     result = (
#         supabase.table("notes")
#         .select("id, title, content, created_at")
#         .order("created_at", desc=True)
#         .execute()
#     )
#     return result.data


# def delete_note(note_id):
#     supabase.table("notes").delete().eq("id", note_id).execute()

# def check_password():
#     if "password_ok" not in st.session_state:
#         st.session_state.password_ok = False

#     if st.session_state.password_ok:
#         return True

#     password = st.text_input("비밀번호", type="password")

#     if st.button("로그인"):
#         if password == st.secrets["APP_PASSWORD"]:
#             st.session_state.password_ok = True
#             st.rerun()
#         else:
#             st.error("비밀번호가 틀렸습니다.")

#     return False


# if not check_password():
#     st.stop()

# st.title("📝 내 메모장")

# st.subheader("새 메모 작성")

# title = st.text_input("제목")
# content = st.text_area("내용", height=180)

# if st.button("저장"):
#     clean_title = title.strip()
#     clean_content = content.strip()

#     if not clean_title and not clean_content:
#         st.warning("제목이나 내용을 입력해 주세요.")
#     else:
#         add_note(
#             clean_title or "제목 없음",
#             clean_content,
#         )
#         st.success("메모가 저장되었습니다.")
#         st.rerun()

# st.divider()

# st.subheader("저장된 메모")

# try:
#     notes = get_notes()

#     if not notes:
#         st.info("아직 저장된 메모가 없습니다.")
#     else:
#         for note in notes:
#             note_id = note["id"]
#             note_title = note["title"]
#             note_content = note["content"]
#             created_at = note["created_at"]

#             with st.container(border=True):
#                 st.markdown(f"### {note_title}")
#                 st.caption(created_at)
#                 st.write(note_content)

#                 if st.button("삭제", key=f"delete_{note_id}"):
#                     delete_note(note_id)
#                     st.success("메모가 삭제되었습니다.")
#                     st.rerun()

# except Exception as e:
#     st.error("Supabase에서 메모를 불러오지 못했습니다.")
#     st.exception(e)

import streamlit as st
from datetime import date
from supabase import create_client
import base64
from pathlib import Path


def add_otter_background():
    otter_path = Path("images/otter.png")

    if not otter_path.exists():
        st.warning("수달 이미지 파일을 찾을 수 없습니다: images/otter.png")
        return

    encoded = base64.b64encode(otter_path.read_bytes()).decode()

    st.markdown(
        f"""
        <style>
        .otter-bg {{
            position: fixed;
            left: -160px;
            bottom: 40px;
            width: 130px;
            height: 130px;
            background-image: url("data:image/png;base64,{encoded}");
            background-size: contain;
            background-repeat: no-repeat;
            opacity: 0.22;
            z-index: 0;
            pointer-events: none;
            animation: otter-walk 18s linear infinite;
        }}

        @keyframes otter-walk {{
            0% {{
                transform: translateX(-160px) scaleX(1);
            }}
            45% {{
                transform: translateX(calc(100vw + 160px)) scaleX(1);
            }}
            50% {{
                transform: translateX(calc(100vw + 160px)) scaleX(-1);
            }}
            95% {{
                transform: translateX(-160px) scaleX(-1);
            }}
            100% {{
                transform: translateX(-160px) scaleX(1);
            }}
        }}

        .block-container {{
            position: relative;
            z-index: 2;
        }}
        </style>

        <div class="otter-bg"></div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# Supabase 연결
# =========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================
# 앱 비밀번호 확인
# =========================
def password_gate():
    if "password_ok" not in st.session_state:
        st.session_state["password_ok"] = False

    if st.session_state["password_ok"]:
        return True

    st.title("체크리스트 앱")

    password = st.text_input("앱 비밀번호", type="password")

    if st.button("입장"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state["password_ok"] = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")

    return False


# =========================
# 역할 선택 화면
# =========================
def role_select_screen():
    st.title("누가 사용할까요?")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("관리자", use_container_width=True):
            st.session_state["role"] = "admin"
            st.rerun()

    with col2:
        if st.button("율하", use_container_width=True):
            st.session_state["role"] = "율하"
            st.rerun()

    with col3:
        if st.button("서하", use_container_width=True):
            st.session_state["role"] = "서하"
            st.rerun()


def back_to_role_select():
    if st.button("처음 화면으로"):
        if "role" in st.session_state:
            del st.session_state["role"]
        st.rerun()


# =========================
# 관리자 화면
# =========================
def admin_screen():
    st.title("관리자 화면")
    back_to_role_select()

    st.divider()

    st.subheader("체크리스트 만들기")

    child_name = st.selectbox(
        "누구의 체크리스트인가요?",
        ["율하", "서하"]
    )

    category = st.selectbox(
        "분류",
        ["공부", "독서", "생활", "운동", "집안일", "기타"]
    )

    description = st.text_input("설명")

    point = st.number_input(
        "점수",
        min_value=0,
        max_value=100,
        value=1,
        step=1
    )

    if st.button("추가하기"):
        if not description.strip():
            st.warning("설명을 입력하세요.")
        else:
            supabase.table("checklist_items").insert({
                "child_name": child_name,
                "category": category,
                "description": description.strip(),
                "point": int(point),
                "is_active": True,
            }).execute()

            st.success("체크리스트가 추가되었습니다.")
            st.rerun()

    st.subheader("등록된 체크리스트")

    items = (
        supabase.table("checklist_items")
        .select("*")
        .order("child_name", desc=False)
        .order("category", desc=False)
        .order("created_at", desc=False)
        .execute()
        .data
    )

    if not items:
        st.info("아직 등록된 체크리스트가 없습니다.")

    for item in items:
        col1, col2, col3 = st.columns([6, 1, 1])

        with col1:
            status = "사용 중" if item["is_active"] else "숨김"
            st.write(
                f"**{item['child_name']} / {item['category']} / {item['point']}점**"
            )
            st.caption(f"{item['description']} / {status}")

        with col2:
            if item["is_active"]:
                if st.button("숨김", key=f"hide_{item['id']}"):
                    supabase.table("checklist_items").update({
                        "is_active": False
                    }).eq("id", item["id"]).execute()
                    st.rerun()
            else:
                if st.button("복구", key=f"show_{item['id']}"):
                    supabase.table("checklist_items").update({
                        "is_active": True
                    }).eq("id", item["id"]).execute()
                    st.rerun()

        with col3:
            if st.button("삭제", key=f"delete_{item['id']}"):
                supabase.table("checklist_items").delete().eq("id", item["id"]).execute()
                st.rerun()

    st.subheader("점수 현황")

    for child_name in ["율하", "서하"]:
        total = calculate_total_score(child_name)
        st.metric(child_name, f"{total}점")


# =========================
# 아이 화면
# =========================
def child_screen(child_name):
    if child_name == "율하":
        add_otter_background()

    st.title(f"{child_name} 체크리스트")
    back_to_role_select()

    selected_date = st.date_input("날짜", value=date.today())

    st.divider()

    items = (
        supabase.table("checklist_items")
        .select("*")
        .eq("is_active", True)
        .eq("child_name", child_name)
        .order("category", desc=False)
        .order("created_at", desc=False)
        .execute()
        .data
    )

    if not items:
        st.info(f"{child_name}에게 할당된 체크리스트가 없습니다.")
        return

    header_cols = st.columns([1.3, 4, 1, 1.2, 3, 1])
    header_cols[0].markdown("**분류**")
    header_cols[1].markdown("**설명**")
    header_cols[2].markdown("**점수**")
    header_cols[3].markdown("**체크**")
    header_cols[4].markdown("**메모**")
    header_cols[5].markdown("**저장**")

    st.divider()

    today_score = 0

    for item in items:
        existing = (
            supabase.table("checklist_records")
            .select("*")
            .eq("child_name", child_name)
            .eq("item_id", item["id"])
            .eq("record_date", str(selected_date))
            .limit(1)
            .execute()
            .data
        )

        if existing:
            record = existing[0]
            default_done = record["is_done"]
            default_memo = record.get("memo") or ""
        else:
            record = None
            default_done = False
            default_memo = ""

        row = st.columns([1.3, 4, 1, 1.2, 3, 1])

        with row[0]:
            st.write(item["category"])

        with row[1]:
            st.write(item["description"])

        with row[2]:
            st.write(f"{item['point']}점")

        with row[3]:
            done = st.checkbox(
                "완료",
                value=default_done,
                key=f"done_{child_name}_{item['id']}_{selected_date}",
                label_visibility="collapsed"
            )

        with row[4]:
            memo = st.text_input(
                "메모",
                value=default_memo,
                key=f"memo_{child_name}_{item['id']}_{selected_date}",
                label_visibility="collapsed"
            )

        with row[5]:
            save_clicked = st.button(
                "저장",
                key=f"save_{child_name}_{item['id']}_{selected_date}"
            )

        if done:
            today_score += item["point"]

        if save_clicked:
            data = {
                "child_name": child_name,
                "item_id": item["id"],
                "record_date": str(selected_date),
                "is_done": done,
                "memo": memo,
            }

            if record:
                supabase.table("checklist_records").update(data).eq("id", record["id"]).execute()
            else:
                supabase.table("checklist_records").insert(data).execute()

            st.success("저장되었습니다.")
            st.rerun()

    st.divider()

    st.metric("오늘 점수", f"{today_score}점")

    total_score = calculate_total_score(child_name)
    st.metric("누적 점수", f"{total_score}점")

# =========================
# 점수 계산
# =========================
def calculate_total_score(child_name):
    records = (
        supabase.table("checklist_records")
        .select("is_done, checklist_items(point)")
        .eq("child_name", child_name)
        .eq("is_done", True)
        .execute()
        .data
    )

    total = 0

    for record in records:
        item = record.get("checklist_items")
        if item:
            total += item.get("point", 0)

    return total


# =========================
# 메인
# =========================
def main():
    st.set_page_config(
        page_title="체크리스트 앱",
        page_icon="✅",
        layout="centered"
    )

    if not password_gate():
        return

    if "role" not in st.session_state:
        role_select_screen()
        return

    role = st.session_state["role"]

    if role == "admin":
        admin_screen()
    elif role in ["율하", "서하"]:
        child_screen(role)
    else:
        st.error("잘못된 사용자입니다.")
        del st.session_state["role"]
        st.rerun()


if __name__ == "__main__":
    main()