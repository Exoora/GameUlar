import streamlit as st
import random

# --- Set page config ---
st.set_page_config("Snake Game", layout="wide")

# --- Session state initialization ---
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5)]
    st.session_state.food = (random.randint(0, 19), random.randint(0, 19))
    st.session_state.direction = (1, 0)
    st.session_state.score = 0
    st.session_state.game_over = False

# --- Title ---
st.title("🐍 Snake Game (Streamlit Edition)")

# --- Controls ---
cols = st.columns(4)
with cols[0]:
    if st.button("⬅️"):
        if st.session_state.direction != (1, 0):
            st.session_state.direction = (-1, 0)
with cols[1]:
    if st.button("⬆️"):
        if st.session_state.direction != (0, 1):
            st.session_state.direction = (0, -1)
with cols[2]:
    if st.button("⬇️"):
        if st.session_state.direction != (0, -1):
            st.session_state.direction = (0, 1)
with cols[3]:
    if st.button("➡️"):
        if st.session_state.direction != (-1, 0):
            st.session_state.direction = (1, 0)

# --- Game Loop ---
if not st.session_state.game_over:
    head_x, head_y = st.session_state.snake[0]
    dx, dy = st.session_state.direction
    new_head = (head_x + dx, head_y + dy)

    # Check for wall collision or self collision
    if (new_head in st.session_state.snake or
        new_head[0] < 0 or new_head[0] > 19 or
        new_head[1] < 0 or new_head[1] > 19):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, new_head)

        if new_head == st.session_state.food:
            st.session_state.food = (random.randint(0, 19), random.randint(0, 19))
            st.session_state.score += 1
        else:
            st.session_state.snake.pop()

# --- Draw the grid ---
grid = [['🟩' if (x, y) == st.session_state.food else
         '🟦' if (x, y) in st.session_state.snake else
         '⬛' for x in range(20)] for y in range(20)]

for row in grid:
    st.markdown("".join(row))

# --- Status ---
if st.session_state.game_over:
    st.error("💀 Game Over!")
    if st.button("Restart"):
        st.session_state.clear()
        st.experimental_rerun()
else:
    st.success(f"Score: {st.session_state.score}")
    st.experimental_rerun()  # Auto-loop the game
