import streamlit as st
import random
import time

# Page config
st.set_page_config(page_title="Mango Catch Game", layout="wide")

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
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = 50
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0

# Game configuration
PLAYERS = {
    "🏃‍♂️ Alex (Fast)": {"emoji": "🏃‍♂️", "color": "#FF6B6B"},
    "🏃‍♀️ Maya (Medium)": {"emoji": "🏃‍♀️", "color": "#4ECDC4"},
    "🏃 Sam (Slow)": {"emoji": "🏃", "color": "#45B7D1"},
    "🏃‍♂️ Rio (Very Fast)": {"emoji": "🏃‍♂️", "color": "#96CEB4"}
}

ITEMS = ["🥭", "🍎", "🍊", "🍌", "🥥", "🍑", "🍓"]

def create_new_round():
    """Create a new catching round"""
    st.session_state.game_round += 1
    
    # Create 3-5 items falling
    num_items = random.randint(3, 5)
    positions = random.sample(range(15, 85, 10), num_items)
    
    new_items = []
    for i, pos in enumerate(positions):
        new_items.append({
            'item': random.choice(ITEMS),
            'position': pos,
            'id': f"{st.session_state.game_round}_{i}"
        })
    
    st.session_state.mangos = new_items
    return new_items

def check_catches():
    """Check what the player caught"""
    caught = 0
    player_range = range(st.session_state.player_pos - 8, st.session_state.player_pos + 8)
    
    for mango in st.session_state.mangos:
        if mango['position'] in player_range:
            caught += 1
    
    missed = len(st.session_state.mangos) - caught
    
    st.session_state.score += caught * 10
    st.session_state.lives -= missed
    
    if st.session_state.lives <= 0:
        st.session_state.game_over = True
    
    return caught, missed

# Main game interface
st.title("🥭 Mango Catch Game!")

# Player selection
if not st.session_state.game_started:
    st.markdown("### Choose Your Player:")
    st.markdown("Each player has different catching abilities!")
    
    cols = st.columns(4)
    for i, (player_name, player_data) in enumerate(PLAYERS.items()):
        with cols[i]:
            if st.button(
                f"{player_data['emoji']}\n{player_name.split('(')[0].strip()}\n({player_name.split('(')[1]}",
                key=f"player_{i}",
                use_container_width=True,
                type="primary" if i == 0 else "secondary"
            ):
                st.session_state.player_choice = i
                st.session_state.game_started = True
                st.session_state.game_round = 0
                create_new_round()
                st.rerun()

# Game area
elif st.session_state.game_started and not st.session_state.game_over:
    # Game stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score", st.session_state.score)
    with col2:
        st.metric("Lives", "❤️" * st.session_state.lives)
    with col3:
        st.metric("Round", st.session_state.game_round)
    with col4:
        selected_player = list(PLAYERS.keys())[st.session_state.player_choice]
        st.metric("Player", selected_player.split('(')[0].strip())
    
    st.markdown("---")
    
    # Show current round items
    st.markdown("### Current Round - Position yourself to catch the items!")
    
    # Visual game area
    game_area = st.container()
    with game_area:
        # Show thrower bots
        st.markdown("**🤖 AI Throwers:** 🤖 Bot1 | 🤖 Bot2 | 🤖 Bot3")
        
        # Create a visual representation
        positions = [" "] * 10
        
        # Place items
        for mango in st.session_state.mangos:
            pos_index = min(9, max(0, mango['position'] // 10))
            if positions[pos_index] == " ":
                positions[pos_index] = mango['item']
            else:
                positions[pos_index] += mango['item']
        
        # Place player
        player_index = min(9, max(0, st.session_state.player_pos // 10))
        player_emoji = PLAYERS[list(PLAYERS.keys())[st.session_state.player_choice]]['emoji']
        
        # Display game field
        st.markdown("**Items falling:**")
        item_display = " | ".join([f"{pos if pos != ' ' else '   '}" for pos in positions])
        st.markdown(f"`{item_display}`")
        
        st.markdown("**Your position:**")
        player_positions = [" "] * 10
        player_positions[player_index] = player_emoji
        player_display = " | ".join([f"{pos if pos != ' ' else '   '}" for pos in player_positions])
        st.markdown(f"`{player_display}`")
        
        st.markdown("**Position scale:** 0 - 10 - 20 - 30 - 40 - 50 - 60 - 70 - 80 - 90")
    
    # Controls
    st.markdown("### Controls:")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("⏪⏪", help="Far left"):
            st.session_state.player_pos = max(5, st.session_state.player_pos - 30)
            st.rerun()
    with col2:
        if st.button("⏪", help="Move left"):
            st.session_state.player_pos = max(5, st.session_state.player_pos - 15)
            st.rerun()
    with col3:
        if st.button("◀️", help="Step left"):
            st.session_state.player_pos = max(5, st.session_state.player_pos - 8)
            st.rerun()
    with col4:
        if st.button("▶️", help="Step right"):
            st.session_state.player_pos = min(95, st.session_state.player_pos + 8)
            st.rerun()
    with col5:
        if st.button("⏩", help="Move right"):
            st.session_state.player_pos = min(95, st.session_state.player_pos + 15)
            st.rerun()
    with col6:
        if st.button("⏩⏩", help="Far right"):
            st.session_state.player_pos = min(95, st.session_state.player_pos + 30)
            st.rerun()
    
    # Catch button
    st.markdown("### Ready? Catch the items!")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 CATCH!", type="primary", use_container_width=True):
            caught, missed = check_catches()
            
            if caught > 0:
                st.success(f"🎉 Caught {caught} items! +{caught * 10} points!")
            if missed > 0:
                st.error(f"😔 Missed {missed} items! -{missed} lives!")
            
            if not st.session_state.game_over:
                time.sleep(1)
                create_new_round()
                st.rerun()
    
    with col2:
        if st.button("⏭️ Skip Round", help="Skip this round (lose a life)"):
            st.session_state.lives -= 1
            if st.session_state.lives <= 0:
                st.session_state.game_over = True
            else:
                create_new_round()
            st.rerun()

# Game over screen
elif st.session_state.game_over:
    st.markdown("# 🎮 Game Over!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Final Score", st.session_state.score)
    with col2:
        st.metric("Rounds Survived", st.session_state.game_round)
    with col3:
        efficiency = f"{(st.session_state.score // 10) / (st.session_state.game_round * 4) * 100:.1f}%" if st.session_state.game_round > 0 else "0%"
        st.metric("Catch Rate", efficiency)
    
    # Performance feedback
    if st.session_state.score >= 150:
        st.balloons()
        st.success("🏆 AMAZING! You're a mango-catching legend!")
    elif st.session_state.score >= 100:
        st.success("🎉 Excellent work! Great catching skills!")
    elif st.session_state.score >= 50:
        st.info("👍 Good job! Keep practicing to improve!")
    else:
        st.info("🎯 Don't give up! Try different positioning strategies!")
    
    # Restart options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again", type="primary", use_container_width=True):
            # Reset game state
            for key in ['game_started', 'player_choice', 'score', 'lives', 'game_over', 'mangos', 'game_round']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.player_pos = 50
            st.rerun()
    
    with col2:
        if st.button("🏠 Choose New Player", use_container_width=True):
            # Reset to player selection
            for key in ['game_started', 'player_choice', 'score', 'lives', 'game_over', 'mangos', 'game_round']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.player_pos = 50
            st.rerun()

# Instructions sidebar
with st.sidebar:
    st.markdown("## 📖 How to Play")
    st.markdown("""
    1. **Choose** your player character
    2. **Position** yourself using the movement buttons
    3. **Watch** where the items are falling
    4. **Click CATCH!** when you're in position
    5. **Score** 10 points per item caught
    6. **Survive** as long as possible!
    
    ### 🎯 Strategy Tips:
    - Look at item positions before moving
    - Try to position yourself to catch multiple items
    - Different players have different catching ranges
    - Don't rush - plan your moves!
    
    ### 🏆 Scoring:
    - 🥭 Each item = 10 points
    - Miss items = lose lives
    - Game ends at 0 lives
    """)
    
    if st.session_state.game_started and not st.session_state.game_over:
        st.markdown("---")
        st.markdown("### Current Status:")
        st.markdown(f"**Position:** {st.session_state.player_pos}")
        st.markdown(f"**Items this round:** {len(st.session_state.mangos)}")

st.markdown("---")
st.markdown("🎮 **Mango Catch Game** - Move strategically and catch them all!")
