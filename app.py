from datetime import datetime

import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="내 메모장",
    page_icon="📝",
    layout="centered",
)


@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = get_supabase_client()


def add_note(title, content):
    supabase.table("notes").insert(
        {
            "title": title,
            "content": content,
        }
    ).execute()


def get_notes():
    result = (
        supabase.table("notes")
        .select("id, title, content, created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


def delete_note(note_id):
    supabase.table("notes").delete().eq("id", note_id).execute()

def check_password():
    if "password_ok" not in st.session_state:
        st.session_state.password_ok = False

    if st.session_state.password_ok:
        return True

    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.password_ok = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")

    return False


if not check_password():
    st.stop()

st.title("📝 내 메모장")

st.subheader("새 메모 작성")

title = st.text_input("제목")
content = st.text_area("내용", height=180)

if st.button("저장"):
    clean_title = title.strip()
    clean_content = content.strip()

    if not clean_title and not clean_content:
        st.warning("제목이나 내용을 입력해 주세요.")
    else:
        add_note(
            clean_title or "제목 없음",
            clean_content,
        )
        st.success("메모가 저장되었습니다.")
        st.rerun()

st.divider()

st.subheader("저장된 메모")

try:
    notes = get_notes()

    if not notes:
        st.info("아직 저장된 메모가 없습니다.")
    else:
        for note in notes:
            note_id = note["id"]
            note_title = note["title"]
            note_content = note["content"]
            created_at = note["created_at"]

            with st.container(border=True):
                st.markdown(f"### {note_title}")
                st.caption(created_at)
                st.write(note_content)

                if st.button("삭제", key=f"delete_{note_id}"):
                    delete_note(note_id)
                    st.success("메모가 삭제되었습니다.")
                    st.rerun()

except Exception as e:
    st.error("Supabase에서 메모를 불러오지 못했습니다.")
    st.exception(e)