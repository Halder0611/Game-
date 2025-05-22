import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime, timedelta

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'player_choice' not in st.session_state:
    st.session_state.player_choice = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'lives' not in st.session_state:
    st.session_state.lives = 3
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'mangos' not in st.session_state:
    st.session_state.mangos = []
if 'last_spawn' not in st.session_state:
    st.session_state.last_spawn = time.time()
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = 50  # Center position (0-100)

# Game configuration
PLAYERS = {
    "🏃‍♂️ Alex": {"color": "#FF6B6B", "speed": "Fast"},
    "🏃‍♀️ Maya": {"color": "#4ECDC4", "speed": "Medium"},
    "🏃 Sam": {"color": "#45B7D1", "speed": "Slow"},
    "🏃‍♂️ Rio": {"color": "#96CEB4", "speed": "Very Fast"}
}

THROWERS = ["🤖 Bot1", "🤖 Bot2", "🤖 Bot3"]
ITEMS = ["🥭", "🍎", "🍊", "🍌", "🥥"]

def spawn_mango():
    """Spawn a new mango from random thrower"""
    if time.time() - st.session_state.last_spawn > random.uniform(1, 3):
        thrower = random.choice(THROWERS)
        item = random.choice(ITEMS)
        position = random.randint(10, 90)
        
        st.session_state.mangos.append({
            'item': item,
            'thrower': thrower,
            'position': position,
            'fall_progress': 0,
            'id': random.randint(1000, 9999)
        })
        st.session_state.last_spawn = time.time()

def update_mangos():
    """Update mango positions"""
    for mango in st.session_state.mangos[:]:
        mango['fall_progress'] += 8
        
        # Check if caught
        if (mango['fall_progress'] >= 80 and mango['fall_progress'] <= 95 and
            abs(mango['position'] - st.session_state.player_pos) <= 8):
            st.session_state.score += 10
            st.session_state.mangos.remove(mango)
            st.success(f"Caught {mango['item']}! +10 points")
        
        # Check if missed
        elif mango['fall_progress'] >= 100:
            st.session_state.lives -= 1
            st.session_state.mangos.remove(mango)
            st.error(f"Missed {mango['item']}! -1 life")
            
            if st.session_state.lives <= 0:
                st.session_state.game_over = True

def draw_game():
    """Draw the game area"""
    # Game area
    game_html = f"""
    <div style="
        width: 100%; 
        height: 400px; 
        background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%);
        border: 3px solid #333;
        position: relative;
        overflow: hidden;
        border-radius: 10px;
    ">
        <!-- Throwers -->
        <div style="position: absolute; top: 10px; left: 20%; font-size: 24px;">🤖</div>
        <div style="position: absolute; top: 10px; left: 50%; font-size: 24px;">🤖</div>
        <div style="position: absolute; top: 10px; left: 80%; font-size: 24px;">🤖</div>
        
        <!-- Falling items -->
    """
    
    for mango in st.session_state.mangos:
        game_html += f"""
        <div style="
            position: absolute; 
            left: {mango['position']}%; 
            top: {mango['fall_progress']}%; 
            font-size: 20px;
        ">{mango['item']}</div>
        """
    
    # Player
    player_emoji = list(PLAYERS.keys())[st.session_state.player_choice].split()[0]
    game_html += f"""
        <!-- Player -->
        <div style="
            position: absolute; 
            left: {st.session_state.player_pos}%; 
            bottom: 10px; 
            font-size: 30px;
            transform: translateX(-50%);
        ">{player_emoji}</div>
    </div>
    """
    
    st.markdown(game_html, unsafe_allow_html=True)

# Main game interface
st.title("🥭 Mango Catch Game!")
st.markdown("Choose your player and catch the falling items thrown by AI bots!")

# Player selection
if not st.session_state.game_started:
    st.subheader("Choose Your Player:")
    
    cols = st.columns(4)
    for i, (player, stats) in enumerate(PLAYERS.items()):
        with cols[i]:
            if st.button(
                f"{player}\n🏃 Speed: {stats['speed']}", 
                key=f"player_{i}",
                use_container_width=True
            ):
                st.session_state.player_choice = i
                st.session_state.game_started = True
                st.rerun()

# Game area
elif st.session_state.game_started and not st.session_state.game_over:
    # Game stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", st.session_state.score)
    with col2:
        st.metric("Lives", st.session_state.lives)
    with col3:
        selected_player = list(PLAYERS.keys())[st.session_state.player_choice]
        st.metric("Player", selected_player.split()[1])
    
    # Game area
    draw_game()
    
    # Controls
    st.subheader("Controls:")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⏪", help="Move far left"):
            st.session_state.player_pos = max(5, st.session_state.player_pos - 20)
    with col2:
        if st.button("◀️", help="Move left"):
            st.session_state.player_pos = max(5, st.session_state.player_pos - 10)
    with col3:
        if st.button("🔄", help="Auto-play (refresh)"):
            pass  # Just refresh
    with col4:
        if st.button("▶️", help="Move right"):
            st.session_state.player_pos = min(95, st.session_state.player_pos + 10)
    with col5:
        if st.button("⏩", help="Move far right"):
            st.session_state.player_pos = min(95, st.session_state.player_pos + 20)
    
    # Game logic
    spawn_mango()
    update_mangos()
    
    # Auto-refresh for game loop
    time.sleep(0.1)
    st.rerun()

# Game over screen
elif st.session_state.game_over:
    st.subheader("🎮 Game Over!")
    st.metric("Final Score", st.session_state.score)
    
    if st.session_state.score >= 100:
        st.balloons()
        st.success("🏆 Excellent! You're a mango-catching master!")
    elif st.session_state.score >= 50:
        st.success("🎉 Great job! You caught quite a few!")
    else:
        st.info("🎯 Keep practicing to improve your catching skills!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again"):
            # Reset game state
            st.session_state.game_started = False
            st.session_state.player_choice = None
            st.session_state.score = 0
            st.session_state.lives = 3
            st.session_state.game_over = False
            st.session_state.mangos = []
            st.session_state.player_pos = 50
            st.rerun()
    
    with col2:
        if st.button("🏠 Main Menu"):
            # Reset to main menu
            st.session_state.game_started = False
            st.session_state.player_choice = None
            st.session_state.score = 0
            st.session_state.lives = 3
            st.session_state.game_over = False
            st.session_state.mangos = []
            st.session_state.player_pos = 50
            st.rerun()

# Instructions
with st.expander("📖 How to Play"):
    st.markdown("""
    1. **Choose your player** from the 4 available characters
    2. **Use the control buttons** to move left and right
    3. **Catch falling items** (🥭🍎🍊🍌🥥) thrown by the AI bots
    4. **Score points** for each item caught (+10 points)
    5. **Avoid missing items** - you lose a life for each miss
    6. **Game ends** when you run out of lives
    
    **Tips:**
    - Different players have different speeds
    - Items fall at different rates
    - Position yourself strategically to catch multiple items
    - Click the 🔄 button or wait for auto-refresh to see updates
    """)

# Footer
st.markdown("---")
st.markdown("🎮 **Mango Catch Game** - Built with Streamlit | Move fast and catch them all!")