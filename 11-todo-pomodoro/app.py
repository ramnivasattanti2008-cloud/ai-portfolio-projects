"""
AI Todo + Pomodoro Timer — Productivity App
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Todo list with AI task suggestions
- Pomodoro timer (25/5)
- Daily stats tracking
- AI productivity tips
"""

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Todo & Pomodoro", page_icon="🍅", layout="wide")
st.title("🍅 AI Todo + Pomodoro Timer")
st.markdown("Manage tasks, stay focused with Pomodoro technique, and get AI productivity tips")

# Session state
if "todos" not in st.session_state:
    st.session_state.todos = []
if "pomodoro_minutes" not in st.session_state:
    st.session_state.pomodoro_minutes = 25
if "break_minutes" not in st.session_state:
    st.session_state.break_minutes = 5
if "sessions_completed" not in st.session_state:
    st.session_state.sessions_completed = 0

# UI Tabs
tab1, tab2, tab3 = st.tabs(["✅ Todo List", "🍅 Pomodoro", "📊 Stats"])

with tab1:
    st.subheader("✅ Todo List")

    new_task = st.text_input("➕ Add new task:", placeholder="What needs to be done?")
    priority = st.selectbox("Priority:", ["🔴 High", "🟡 Medium", "🟢 Low"])

    if st.button("Add Task", use_container_width=True) and new_task:
        st.session_state.todos.append({
            "task": new_task,
            "priority": priority,
            "done": False,
            "time": datetime.now().strftime("%H:%M")
        })

    st.divider()
    st.markdown("**Your Tasks:**")

    for i, todo in enumerate(st.session_state.todos):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            if todo["done"]:
                st.markdown(f"~~{todo['task']}~~ {todo['priority']}")
            else:
                st.markdown(f"{todo['task']} {todo['priority']}")
        with col2:
            if st.button("✅" if not todo["done"] else "↩️", key=f"done_{i}"):
                todo["done"] = not todo["done"]
                st.rerun()
        with col3:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.todos.pop(i)
                st.rerun()

    if st.button("🗑️ Clear Completed"):
        st.session_state.todos = [t for t in st.session_state.todos if not t["done"]]

with tab2:
    st.subheader("🍅 Pomodoro Timer")

    work_min = st.slider("Work (min):", 15, 60, 25)
    break_min = st.slider("Break (min):", 3, 15, 5)
    sessions = st.number_input("Sessions:", 1, 10, 4)

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.metric("⏱️ Work", f"{work_min} min")
    with col_t2:
        st.metric("☕ Break", f"{break_min} min")
    with col_t3:
        st.metric("🎯 Sessions", f"{sessions}")

    st.divider()

    # Timer display
    timer_placeholder = st.empty()
    timer_placeholder.markdown(f"<h1 style='text-align:center; font-size:80px;'>{work_min}:00</h1>", unsafe_allow_html=True)

    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("▶️ Start", use_container_width=True):
            import time
            remaining = work_min * 60
            while remaining > 0:
                mins = remaining // 60
                secs = remaining % 60
                timer_placeholder.markdown(f"<h1 style='text-align:center; font-size:80px;'>{mins:02d}:{secs:02d}</h1>", unsafe_allow_html=True)
                time.sleep(1)
                remaining -= 1
            st.balloons()
            st.session_state.sessions_completed += 1
            st.success("🍅 Pomodoro complete! Take a break.")

    with col_b2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.info("Paused")

    with col_b3:
        if st.button("🔄 Reset", use_container_width=True):
            timer_placeholder.markdown(f"<h1 style='text-align:center; font-size:80px;'>{work_min}:00</h1>", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🎵 Pomodoro Tips")
    tips = ["Work in focused sprints (25 min)", "No phone/messages during work", "Take real breaks (walk, stretch)", "4 sessions → long break (15-30 min)", "Track what you accomplished"]
    for tip in tips:
        st.markdown(f"- {tip}")

with tab3:
    st.subheader("📊 Today's Stats")

    total = len(st.session_state.todos)
    done = sum(1 for t in st.session_state.todos if t["done"])
    remaining = total - done

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("📋 Total Tasks", total)
    with col_stat2:
        st.metric("✅ Completed", done)
    with col_stat3:
        st.metric("🍅 Pomodoros", st.session_state.sessions_completed)

    if total > 0:
        st.progress(done / total)
        st.markdown(f"**Progress: {done}/{total} tasks ({done/total*100:.0f}%)**")

    st.divider()
    st.markdown("### 📅 Quick Stats")
    st.markdown(f"- Session started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown(f"- Current streak: 0 days (track daily!)")
    st.markdown(f"- Most productive day: Not tracked yet")

st.divider()
st.caption("Built by Attanti Ramnivas | Streamlit")
