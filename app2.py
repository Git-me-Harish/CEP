import streamlit as st
import random
from gtts import gTTS
import os
import pandas as pd
import time
from io import BytesIO
import base64
import json
from datetime import datetime

# Enhanced session state initialization
def init_session_state():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 'Easy'
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'badges' not in st.session_state:
        st.session_state.badges = set()
    if 'total_time' not in st.session_state:
        st.session_state.total_time = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

def update_progress(activity, correct):
    """Update user progress and award badges"""
    if correct:
        st.session_state.streak += 1
        # Award badges based on streaks
        if st.session_state.streak == 5:
            st.session_state.badges.add("🌟 Quick Learner")
        elif st.session_state.streak == 10:
            st.session_state.badges.add("🏆 Master Listener")
    else:
        st.session_state.streak = 0

    # Record activity in history
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'activity': activity,
        'level': st.session_state.current_level,
        'result': 'correct' if correct else 'incorrect'
    })

def get_audio_html(text, slow=False):
    """Enhanced audio generation with speed control"""
    try:
        tts = gTTS(text=text, lang='en', slow=slow)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_str = base64.b64encode(audio_fp.getvalue()).decode()
        audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_str}"></audio>'
        return audio_html
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

def show_progress_dashboard():
    """Display user progress dashboard"""
    st.sidebar.header("📊 Progress Dashboard")
    
    # Display badges
    if st.session_state.badges:
        st.sidebar.subheader("🏅 Earned Badges")
        for badge in st.session_state.badges:
            st.sidebar.markdown(badge)
    
    # Display statistics
    st.sidebar.subheader("📈 Statistics")
    total_activities = len(st.session_state.history)
    if total_activities > 0:
        correct_activities = sum(1 for h in st.session_state.history if h['result'] == 'correct')
        accuracy = (correct_activities / total_activities) * 100
        st.sidebar.metric("Accuracy", f"{accuracy:.1f}%")
    
    st.sidebar.metric("Current Streak", st.session_state.streak)
    
    # Display recent activity
    if st.sidebar.checkbox("Show Recent Activity"):
        st.sidebar.subheader("Recent Activity")
        recent_history = st.session_state.history[-5:]  # Show last 5 activities
        for activity in recent_history:
            st.sidebar.markdown(
                f"**{activity['activity']}** ({activity['level']}) - {activity['result']}"
            )

def create_listening_module():
    st.title("🎧 Interactive English Learning Hub")
    init_session_state()
    
    # Enhanced sidebar navigation
    st.sidebar.header("Navigation")
    activity_type = st.sidebar.selectbox(
    "Choose Activity",
    ["Sound Recognition", "Word Listening", "Story Time", 
     "Following Instructions", "Phonetic Fun", "Sentence Practice",
     "Vocabulary Builder", "Comprehension Challenge", "Flash Cards"]  # Add this
)
    
    # Settings with additional options
    st.sidebar.header("⚙️ Settings")
    st.session_state.current_level = st.sidebar.selectbox(
        "Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )
    
    # Audio speed control
    slow_audio = st.sidebar.checkbox("Slow Audio Speed", value=False)
    
    # Display progress dashboard
    show_progress_dashboard()
    
    # Main content area with enhanced error handling
    try:
        if activity_type == "Sound Recognition":
            sound_recognition_game(slow_audio)
        elif activity_type == "Word Listening":
            word_listening_game(slow_audio)
        elif activity_type == "Story Time":
            interactive_story(slow_audio)
        elif activity_type == "Following Instructions":
            listening_instructions(slow_audio)
        elif activity_type == "Phonetic Fun":
            phonetic_practice(slow_audio)
        elif activity_type == "Vocabulary Builder":
            vocabulary_builder(slow_audio)
        elif activity_type == "Comprehension Challenge":
            comprehension_challenge(slow_audio)
        # In the main content area section
        elif activity_type == "Flash Cards":
            flash_cards(slow_audio)
        else:
            sentence_practice(slow_audio)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.button("Reset Activity", on_click=lambda: None)

def vocabulary_builder(slow_audio=False):
    st.subheader("📚 Vocabulary Builder")
    
    # Initialize session state for vocabulary builder
    if 'vocab_category' not in st.session_state:
        st.session_state.vocab_category = None
    if 'practice_word' not in st.session_state:
        st.session_state.practice_word = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    
    vocabulary_sets = {
        "Easy": {
            "colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink"],
            "animals": ["cat", "dog", "bird", "fish", "rabbit", "horse", "elephant"],
            "food": ["apple", "banana", "bread", "milk", "rice", "meat", "egg"]
        },
        "Medium": {
            "emotions": ["happy", "excited", "surprised", "worried", "confused", "tired", "proud"],
            "weather": ["sunny", "rainy", "cloudy", "windy", "stormy", "foggy", "snowy"],
            "activities": ["running", "swimming", "reading", "writing", "dancing", "singing", "playing"]
        },
        "Hard": {
            "abstract": ["freedom", "courage", "wisdom", "loyalty", "honesty", "patience", "kindness"],
            "academic": ["hypothesis", "analysis", "theory", "research", "conclusion", "evidence", "experiment"],
            "professional": ["collaborate", "implement", "negotiate", "coordinate", "facilitate", "delegate", "innovate"]
        }
    }
    
    # Category selection with state management
    new_category = st.selectbox(
        "Choose Category:", 
        list(vocabulary_sets[st.session_state.current_level].keys()),
        key='category_selector'
    )
    
    # Reset practice word when category changes
    if new_category != st.session_state.vocab_category:
        st.session_state.vocab_category = new_category
        st.session_state.practice_word = None
        st.session_state.current_audio = None
    
    if st.session_state.vocab_category:
        words = vocabulary_sets[st.session_state.current_level][st.session_state.vocab_category]
        
        # Word exploration mode with improved audio handling
        st.subheader("Explore Words")
        
        # Create a container for word display
        word_container = st.container()
        
        with word_container:
            for i, word in enumerate(words):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    # Generate unique key for each audio button
                    if st.button(f"🔊 Play", key=f"play_{word}_{i}"):
                        st.session_state.current_audio = get_audio_html(word, slow=slow_audio)
                    
                    # Display audio if available
                    if st.session_state.current_audio and st.session_state.practice_word == word:
                        st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{word}**")
                
                with col3:
                    if st.button(f"Practice", key=f"practice_{word}_{i}"):
                        st.session_state.practice_word = word
                        st.session_state.current_audio = get_audio_html(word, slow=slow_audio)
                        st.rerun()
        
        # Practice mode with improved state management
        if st.session_state.practice_word:
            st.markdown("---")
            st.subheader(f"Practice: {st.session_state.practice_word}")
            
            # Audio control for practice word
            if st.button("🔊 Hear Word Again", key="repeat_practice"):
                st.session_state.current_audio = get_audio_html(st.session_state.practice_word, slow=slow_audio)
                st.rerun()
            
            if st.session_state.current_audio:
                st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            # Practice input
            user_input = st.text_input(
                "Type what you hear:",
                key=f"practice_input_{st.session_state.practice_word}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Check", key="check_answer"):
                    if user_input.lower().strip() == st.session_state.practice_word.lower():
                        st.success("Perfect! 🎉")
                        update_progress("Vocabulary", True)
                        st.session_state.score += 1
                    else:
                        st.error(f"Try again! The word was: {st.session_state.practice_word}")
                        update_progress("Vocabulary", False)
            
            with col2:
                if st.button("New Word", key="new_word"):
                    # Choose a different word than the current one
                    available_words = [w for w in words if w != st.session_state.practice_word]
                    if available_words:
                        st.session_state.practice_word = random.choice(available_words)
                        st.session_state.current_audio = get_audio_html(st.session_state.practice_word, slow=slow_audio)
                        st.rerun()
        
        # Add a visual progress indicator
        st.markdown("---")
        progress = len([w for w in st.session_state.history if w['activity'] == 'Vocabulary' and w['result'] == 'correct'])
        st.progress(min(1.0, progress / 10))
        st.markdown(f"Words Mastered: {progress}")
        
def comprehension_challenge(slow_audio=False):
    st.subheader("🎯 Comprehension Challenge")
    
    # Initialize session states
    if 'current_passage' not in st.session_state:
        st.session_state.current_passage = None
    if 'show_questions' not in st.session_state:
        st.session_state.show_questions = False
    if 'answers_submitted' not in st.session_state:
        st.session_state.answers_submitted = False
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    
    passages = {
        "Easy": [
            {
                "title": "My Pet Dog",
                "text": "I have a pet dog named Max. He is brown and white. Max loves to play with his ball. He also likes to run in the garden. Every morning, he wakes me up to go for a walk.",
                "questions": [
                    {"question": "What is the dog's name?", "answer": "Max"},
                    {"question": "What color is Max?", "answer": "brown and white"},
                    {"question": "What does Max like to play with?", "answer": "ball"},
                    {"question": "Where does Max like to run?", "answer": "garden"},
                    {"question": "What happens every morning?", "answer": "Max wakes up the owner for a walk"}
                ]
            }
        ],
        "Medium": [
            {
                "title": "The School Garden",
                "text": "Our school started a garden project last spring. Each class planted different vegetables and flowers. We learned about soil, water, and sunlight. By summer, we had tomatoes, carrots, and beautiful sunflowers. The garden helps us learn about nature and healthy food.",
                "questions": [
                    {"question": "When did the garden project start?", "answer": "last spring"},
                    {"question": "What did the classes plant?", "answer": "vegetables and flowers"},
                    {"question": "What did students learn about?", "answer": "soil, water, and sunlight"},
                    {"question": "What grew in the garden?", "answer": "tomatoes, carrots, and sunflowers"},
                    {"question": "What does the garden help students learn about?", "answer": "nature and healthy food"}
                ]
            }
        ],
        "Hard": [
            {
                "title": "The History of Flight",
                "text": "Humans have always dreamed of flying like birds. The Wright brothers made this dream come true in 1903 with their first powered flight. Their airplane, the Wright Flyer, stayed in the air for 12 seconds and covered 120 feet. This historic achievement changed transportation forever and led to modern aviation.",
                "questions": [
                    {"question": "Who made powered flight possible?", "answer": "Wright brothers"},
                    {"question": "When was the first powered flight?", "answer": "1903"},
                    {"question": "What was the name of their airplane?", "answer": "Wright Flyer"},
                    {"question": "How long did the first flight last?", "answer": "12 seconds"},
                    {"question": "How far did the first flight go?", "answer": "120 feet"}
                ]
            }
        ]
    }
    
    # Create containers for better organization
    header_container = st.container()
    passage_container = st.container()
    question_container = st.container()
    
    with header_container:
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🔄 Start New Challenge", key="new_challenge"):
                st.session_state.current_passage = random.choice(passages[st.session_state.current_level])
                st.session_state.show_questions = False
                st.session_state.answers_submitted = False
                st.session_state.current_audio = None
                st.rerun()
    
    if st.session_state.current_passage:
        with passage_container:
            st.markdown(f"## 📖 {st.session_state.current_passage['title']}")
            
            # Audio controls
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🔊 Listen to Passage", key="play_audio"):
                    st.session_state.current_audio = get_audio_html(
                        st.session_state.current_passage['text'], 
                        slow=slow_audio
                    )
            
            if st.session_state.current_audio:
                st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            # Display passage in a styled container
            st.markdown("""
            <style>
            .passage-container {
                background-color: #f8f9fa;
                border-left: 3px solid #1e88e5;
                padding: 20px;
                border-radius: 5px;
                margin: 10px 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="passage-container">
                {st.session_state.current_passage['text']}
            </div>
            """, unsafe_allow_html=True)
            
            if not st.session_state.show_questions:
                if st.button("📝 Ready for Questions", key="show_questions"):
                    st.session_state.show_questions = True
                    st.rerun()
    
        if st.session_state.show_questions:
            with question_container:
                st.markdown("---")
                st.markdown("## ❓ Questions")
                
                # Create a form for questions
                with st.form(key="question_form"):
                    user_answers = {}
                    for q in st.session_state.current_passage['questions']:
                        user_answers[q['question']] = st.text_input(
                            q['question'],
                            key=f"q_{hash(q['question'])}"
                        )
                    
                    submit_button = st.form_submit_button("📤 Submit Answers")
                    
                    if submit_button and not st.session_state.answers_submitted:
                        correct_count = 0
                        feedback = []
                        
                        for q in st.session_state.current_passage['questions']:
                            user_ans = user_answers[q['question']].lower().strip()
                            correct_ans = q['answer'].lower()
                            
                            if user_ans == correct_ans:
                                correct_count += 1
                                feedback.append(f"✅ {q['question']}: Correct!")
                            else:
                                feedback.append(f"❌ {q['question']}: The correct answer was '{q['answer']}'")
                        
                        score_percentage = (correct_count / len(st.session_state.current_passage['questions'])) * 100
                        
                        # Display results
                        st.success(f"Score: {correct_count}/{len(st.session_state.current_passage['questions'])} ({score_percentage:.1f}%)")
                        
                        # Show detailed feedback
                        with st.expander("See Detailed Feedback"):
                            for fb in feedback:
                                st.markdown(fb)
                        
                        # Update progress
                        update_progress("Comprehension", score_percentage >= 80)
                        st.session_state.score += correct_count
                        st.session_state.answers_submitted = True
                
                # Show progress
                if hasattr(st.session_state, 'history'):
                    comprehension_attempts = len([x for x in st.session_state.history 
                                               if x['activity'] == 'Comprehension'])
                    if comprehension_attempts > 0:
                        success_rate = len([x for x in st.session_state.history 
                                          if x['activity'] == 'Comprehension' 
                                          and x['result'] == 'correct']) / comprehension_attempts
                        st.progress(success_rate)
                        st.markdown(f"Overall Success Rate: {success_rate*100:.1f}%")

def flash_cards(slow_audio=False):
    st.subheader("💡 Interactive Flash Cards")
    
    # Flash card data organized by difficulty
    flash_cards_data = {
        "Easy": {
            "Basic Vocabulary": [
                {"front": "Hello", "back": "A common greeting", "example": "Hello, how are you?"},
                {"front": "Book", "back": "Something we read", "example": "I love reading this book"},
                {"front": "Sun", "back": "Bright star in the sky", "example": "The sun is shining"},
                {"front": "Tree", "back": "Plant with trunk and leaves", "example": "Birds live in the tree"},
                {"front": "House", "back": "Place where people live", "example": "My house is blue"}
            ],
            "Numbers": [
                {"front": "One", "back": "The first number", "example": "I have one apple"},
                {"front": "Two", "back": "Double of one", "example": "Two birds are flying"},
                {"front": "Three", "back": "After two", "example": "Three little pigs"}
            ]
        },
        "Medium": {
            "Action Words": [
                {"front": "Running", "back": "Moving fast on feet", "example": "She is running in the park"},
                {"front": "Dancing", "back": "Moving to music", "example": "They are dancing at the party"},
                {"front": "Swimming", "back": "Moving through water", "example": "Fish are swimming in the pond"}
            ],
            "Emotions": [
                {"front": "Happy", "back": "Feeling good", "example": "The children are happy"},
                {"front": "Excited", "back": "Very enthusiastic", "example": "We are excited about the party"},
                {"front": "Peaceful", "back": "Calm and quiet", "example": "The garden is peaceful"}
            ]
        },
        "Hard": {
            "Advanced Words": [
                {"front": "Phenomenal", "back": "Extraordinary, exceptional", "example": "The performance was phenomenal"},
                {"front": "Serendipity", "back": "Lucky discovery", "example": "Finding this book was serendipity"},
                {"front": "Resilient", "back": "Able to recover quickly", "example": "She is very resilient"}
            ],
            "Idioms": [
                {"front": "Break a leg", "back": "Good luck", "example": "Break a leg at your performance!"},
                {"front": "Piece of cake", "back": "Very easy", "example": "The test was a piece of cake"},
                {"front": "Under the weather", "back": "Feeling sick", "example": "I'm feeling under the weather"}
            ]
        }
    }
    
    # Category selection
    category = st.selectbox(
        "Choose Category:",
        list(flash_cards_data[st.session_state.current_level].keys())
    )
    
    if category:
        cards = flash_cards_data[st.session_state.current_level][category]
        
        # Initialize card index in session state if not present
        if 'card_index' not in st.session_state:
            st.session_state.card_index = 0
        if 'show_back' not in st.session_state:
            st.session_state.show_back = False
            
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous") and st.session_state.card_index > 0:
                st.session_state.card_index -= 1
                st.session_state.show_back = False
        with col3:
            if st.button("Next ➡️") and st.session_state.card_index < len(cards) - 1:
                st.session_state.card_index += 1
                st.session_state.show_back = False
                
        # Display current card
        current_card = cards[st.session_state.card_index]
        
        # Create a card-like container
        st.markdown("""
        <style>
        .flash-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        .flash-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .card-content {
            font-size: 24px;
            color: #333;
            margin: 20px 0;
        }
        .example-text {
            font-size: 18px;
            color: #666;
            font-style: italic;
            margin-top: 15px;
        }
        .progress-indicator {
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Card container
        card_container = st.container()
        with card_container:
            st.markdown(f"""
            <div class="flash-card" id="flashcard">
                <div class="card-content">
                    {current_card['back'] if st.session_state.show_back else current_card['front']}
                </div>
                {f'<div class="example-text">{current_card["example"]}</div>' if st.session_state.show_back else ''}
            </div>
            <div class="progress-indicator">
                Card {st.session_state.card_index + 1} of {len(cards)}
            </div>
            """, unsafe_allow_html=True)
            
        # Flip button
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔄 Flip Card"):
                st.session_state.show_back = not st.session_state.show_back
        
        # Audio button
        audio_text = current_card['front'] + ". " + current_card['example']
        audio_html = get_audio_html(audio_text, slow=slow_audio)
        if audio_html:
            st.markdown(audio_html, unsafe_allow_html=True)
        
        # Practice section
        st.write("---")
        st.write("Practice:")
        user_input = st.text_input("Type the word/phrase you learned:")
        
        if st.button("Check"):
            if user_input.lower().strip() == current_card['front'].lower():
                st.success("Perfect! 🎉")
                update_progress("Flash Cards", True)
                st.session_state.score += 1
            else:
                st.error(f"Keep practicing! The correct answer is: {current_card['front']}")
                update_progress("Flash Cards", False)
def sound_recognition_game(slow_audio=False):
    st.subheader("👂 Sound Recognition Game")
    
    # Initialize session states
    if 'current_sound' not in st.session_state:
        st.session_state.current_sound = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'current_category' not in st.session_state:
        st.session_state.current_category = None
    if 'answer_submitted' not in st.session_state:
        st.session_state.answer_submitted = False
    
    sounds_data = {
        "Easy": {
            "animal_sounds": {
                "cat": "meow sound",
                "dog": "barking sound",
                "cow": "mooing sound",
                "bird": "chirping sound",
                "duck": "quacking sound",
                "horse": "neighing sound",
                "sheep": "baaing sound"
            }
        },
        "Medium": {
            "nature_sounds": {
                "rain": "rain falling",
                "wind": "wind blowing",
                "thunder": "thunder cracking",
                "waves": "ocean waves",
                "fire": "fire crackling",
                "leaves": "leaves rustling",
                "stream": "water flowing"
            }
        },
        "Hard": {
            "instrument_sounds": {
                "piano": "piano notes",
                "guitar": "guitar strumming",
                "drums": "drum beats",
                "violin": "violin playing",
                "flute": "flute melody",
                "trumpet": "trumpet sound",
                "xylophone": "xylophone notes"
            }
        }
    }
    
    # Create containers for better organization
    header_container = st.container()
    game_container = st.container()
    feedback_container = st.container()
    
    with header_container:
        category = sounds_data[st.session_state.current_level]
        sound_type = random.choice(list(category.keys()))
        
        # Display current category with styling
        st.markdown(f"""
        <div style='
            background-color: #f0f7ff;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #1e88e5;
            margin: 10px 0;
        '>
            <h3 style='margin:0; color: #1e88e5;'>
                {sound_type.replace('_', ' ').title()}
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    with game_container:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🎵 Play New Sound", key="new_sound"):
                # Reset states for new sound
                sound_pair = random.choice(list(category[sound_type].items()))
                st.session_state.current_sound = sound_pair
                st.session_state.current_audio = get_audio_html(sound_pair[1], slow=slow_audio)
                st.session_state.current_category = sound_type
                st.session_state.answer_submitted = False
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_game"):
                st.session_state.current_sound = None
                st.session_state.current_audio = None
                st.session_state.answer_submitted = False
                st.rerun()
    
        if st.session_state.current_sound and st.session_state.current_audio:
            # Display audio player
            st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            # Create a styled container for options
            st.markdown("""
            <style>
            .stRadio > label {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0;
                transition: all 0.3s ease;
            }
            .stRadio > label:hover {
                background-color: #e3f2fd;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display options
            options = list(category[sound_type].keys())
            user_answer = st.radio(
                "What made this sound?",
                options,
                key=f"answer_{hash(str(st.session_state.current_sound))}"
            )
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button("✅ Check Answer", key="check_answer") and not st.session_state.answer_submitted:
                    st.session_state.answer_submitted = True
                    if user_answer == st.session_state.current_sound[0]:
                        st.success("Correct! 🎉")
                        update_progress("Sound Recognition", True)
                        st.session_state.score += 1
                    else:
                        st.error(f"Not quite! The correct answer was {st.session_state.current_sound[0]}")
                        update_progress("Sound Recognition", False)
            
            with col2:
                if st.button("🔊 Play Again", key="play_again"):
                    st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            with col3:
                if st.button("➡️ Next", key="next_sound"):
                    # Reset for next sound
                    sound_pair = random.choice(list(category[sound_type].items()))
                    st.session_state.current_sound = sound_pair
                    st.session_state.current_audio = get_audio_html(sound_pair[1], slow=slow_audio)
                    st.session_state.answer_submitted = False
                    st.rerun()
    
    with feedback_container:
        if hasattr(st.session_state, 'history'):
            # Show progress
            sound_attempts = len([x for x in st.session_state.history 
                                if x['activity'] == 'Sound Recognition'])
            if sound_attempts > 0:
                success_rate = len([x for x in st.session_state.history 
                                  if x['activity'] == 'Sound Recognition' 
                                  and x['result'] == 'correct']) / sound_attempts
                
                st.markdown("### Your Progress")
                st.progress(success_rate)
                st.markdown(f"Success Rate: {success_rate*100:.1f}%")
                
                # Display streak if available
                if hasattr(st.session_state, 'streak'):
                    st.markdown(f"Current Streak: {st.session_state.streak} 🔥")

def word_listening_game(slow_audio=False):
    st.subheader("🎯 Word Listening Challenge")
    
    # Initialize session states
    if 'current_word' not in st.session_state:
        st.session_state.current_word = None
    if 'current_pair' not in st.session_state:
        st.session_state.current_pair = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'answer_checked' not in st.session_state:
        st.session_state.answer_checked = False
    
    word_pairs = {
        "Easy": [
            ("cat", "hat"),
            ("pen", "pin"),
            ("ship", "sheep"),
            ("bed", "bad"),
            ("fit", "feet"),
            ("hit", "heat"),
            ("sit", "seat")
        ],
        "Medium": [
            ("through", "threw"),
            ("weight", "wait"),
            ("peace", "piece"),
            ("hear", "here"),
            ("write", "right"),
            ("there", "their"),
            ("wear", "where")
        ],
        "Hard": [
            ("affect", "effect"),
            ("principal", "principle"),
            ("stationary", "stationery"),
            ("complement", "compliment"),
            ("desert", "dessert"),
            ("patient", "patience"),
            ("weather", "whether")
        ]
    }
    
    # Create containers for better organization
    header_container = st.container()
    game_container = st.container()
    feedback_container = st.container()
    
    with header_container:
        # Display level and progress
        st.markdown(f"""
        <div style='
            background-color: #f0f7ff;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #1e88e5;
            margin: 10px 0;
        '>
            <h3 style='margin:0; color: #1e88e5;'>
                Level: {st.session_state.current_level}
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    with game_container:
        current_pairs = word_pairs[st.session_state.current_level]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔊 New Word", key="new_word"):
                # Get a new word pair
                pair = random.choice(current_pairs)
                word = random.choice(pair)
                
                # Update session state
                st.session_state.current_word = word
                st.session_state.current_pair = pair
                st.session_state.current_audio = get_audio_html(word, slow=slow_audio)
                st.session_state.answer_checked = False
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_game"):
                st.session_state.current_word = None
                st.session_state.current_pair = None
                st.session_state.current_audio = None
                st.session_state.answer_checked = False
                st.rerun()
        
        if st.session_state.current_word and st.session_state.current_audio:
            # Display audio player with styling
            st.markdown("""
            <div style='
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
            '>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Style radio buttons
            st.markdown("""
            <style>
            .stRadio > label {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0;
                transition: all 0.3s ease;
            }
            .stRadio > label:hover {
                background-color: #e3f2fd;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display options
            user_answer = st.radio(
                "Which word did you hear?",
                st.session_state.current_pair,
                key=f"answer_{st.session_state.current_word}"
            )
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button("✅ Check Answer", key="check_answer") and not st.session_state.answer_checked:
                    st.session_state.answer_checked = True
                    if user_answer == st.session_state.current_word:
                        st.success("Correct! 🎉")
                        update_progress("Word Listening", True)
                        st.session_state.score += 1
                    else:
                        st.error(f"Not quite! The correct word was '{st.session_state.current_word}'")
                        update_progress("Word Listening", False)
            
            with col2:
                if st.button("🔊 Listen Again", key="listen_again"):
                    st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            with col3:
                if st.button("➡️ Next", key="next_word"):
                    # Get a new word pair
                    new_pair = random.choice([p for p in current_pairs if p != st.session_state.current_pair])
                    new_word = random.choice(new_pair)
                    
                    # Update session state
                    st.session_state.current_word = new_word
                    st.session_state.current_pair = new_pair
                    st.session_state.current_audio = get_audio_html(new_word, slow=slow_audio)
                    st.session_state.answer_checked = False
                    st.rerun()
    
    with feedback_container:
        if hasattr(st.session_state, 'history'):
            # Show progress
            word_attempts = len([x for x in st.session_state.history 
                               if x['activity'] == 'Word Listening'])
            if word_attempts > 0:
                success_rate = len([x for x in st.session_state.history 
                                  if x['activity'] == 'Word Listening' 
                                  and x['result'] == 'correct']) / word_attempts
                
                st.markdown("### Your Progress")
                st.progress(success_rate)
                st.markdown(f"Success Rate: {success_rate*100:.1f}%")
                
                # Display streak if available
                if hasattr(st.session_state, 'streak'):
                    st.markdown(f"Current Streak: {st.session_state.streak} 🔥")
                
                # Display tips
                with st.expander("💡 Tips for Similar-Sounding Words"):
                    st.markdown("""
                    - Listen carefully to the vowel sounds
                    - Pay attention to word endings
                    - Try to visualize the word's meaning
                    - Practice the minimal pairs regularly
                    - Focus on the subtle differences in pronunciation
                    """)
                
def listening_instructions(slow_audio=False):
    st.subheader("🎮 Following Instructions Game")
    
    instructions = {
        "Easy": [
            "Touch your nose and count to three",
            "Raise both hands and wave",
            "Stand up, turn around, and sit down",
            "Clap your hands three times",
            "Point to the door and then to the window",
            "Pat your head and rub your stomach",
            "Jump twice and say 'hello'"
        ],
        "Medium": [
            "First touch your toes, then jump twice, and finally clap once",
            "Draw a circle in the air, point to your eyes, then wave goodbye",
            "Stand up, spin around twice, then sit and raise your right hand",
            "Pat your head three times, then your shoulders twice, then clap once",
            "Touch your left ear with your right hand, then reverse",
            "Make a triangle shape with your fingers, then point to three objects",
            "Hop on one foot, switch to the other foot, then clap twice"
        ],
        "Hard": [
            "Touch your nose, right ear, left shoulder, and then clap twice in that exact order",
            "Stand up, turn clockwise, touch the floor, jump once, and sit down",
            "Draw a square in the air, then a triangle, then a circle, using the same hand",
            "Count to five while touching each finger to your thumb in sequence",
            "Pat your head while rubbing your stomach, then switch actions without stopping",
            "Point to something red, then blue, then green, then clap for each color",
            "Make a star shape with your fingers, then trace it in the air with your elbow"
        ]
    }
    
    # Instructions container
    instruction_container = st.container()
    
    # Action buttons in columns
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 New Instruction"):
            # Select random instruction based on current level
            instruction = random.choice(instructions[st.session_state.current_level])
            st.session_state.current_instruction = instruction
            st.session_state.instruction_started = True
            st.session_state.instruction_complete = False
            
            # Generate and store audio
            audio_html = get_audio_html(instruction, slow=slow_audio)
            if audio_html:
                st.session_state.current_audio = audio_html
    
    with col2:
        if st.button("🔄 Repeat Instruction") and hasattr(st.session_state, 'current_audio'):
            st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
    
    # Display current instruction and progress
    if hasattr(st.session_state, 'instruction_started') and st.session_state.instruction_started:
        with instruction_container:
            # Stylized instruction display
            st.markdown("""
            <style>
            .instruction-box {
                background-color: #f0f7ff;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-left: 5px solid #1e88e5;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .instruction-text {
                font-size: 20px;
                color: #1e88e5;
                margin-bottom: 15px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="instruction-box">
                <div class="instruction-text">{st.session_state.current_instruction}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Play initial audio
            if hasattr(st.session_state, 'current_audio'):
                st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            # Progress tracking
            steps_completed = st.checkbox("✅ I have completed all the steps!")
            
            if steps_completed and not st.session_state.instruction_complete:
                st.session_state.instruction_complete = True
                st.success("Great job following the instructions! 🌟")
                st.session_state.score += 1
                update_progress("Instructions", True)
                
                # Level-based feedback
                if st.session_state.current_level == "Easy":
                    st.info("💡 Try the Medium level for more challenge!")
                elif st.session_state.current_level == "Medium":
                    st.info("💫 You're doing great! Ready for Hard level?")
                else:
                    st.info("🏆 Excellent work at the highest level!")
            
            # Tips expander
            with st.expander("📝 Tips for Better Listening"):
                st.markdown("""
                - 👂 Listen to the complete instruction before starting
                - 🔍 Break down complex instructions into smaller steps
                - 🎯 Visualize each action as you hear it
                - ⏰ Take your time to complete each step correctly
                - 🔄 Use the repeat button if needed
                - ✨ Practice makes perfect!
                """)
            
            # Progress tracking
            st.markdown("""
            <style>
            .progress-bar {
                width: 100%;
                background-color: #f0f0f0;
                border-radius: 10px;
                margin: 10px 0;
            }
            .progress-text {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Show current level progress
            level_progress = min(100, (st.session_state.score / 10) * 100)  # Assuming 10 points per level
            st.markdown(f"""
            <div class="progress-bar">
                <div style="width: {level_progress}%; height: 20px; background-color: #1e88e5; 
                     border-radius: 10px; transition: width 0.5s ease-in-out;">
                </div>
            </div>
            <div class="progress-text">Level Progress: {level_progress:.0f}%</div>
            """, unsafe_allow_html=True)
            
def interactive_story(slow_audio=False):
    st.subheader("📚 Interactive Story Time")
    
    # Initialize session states
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'answers_submitted' not in st.session_state:
        st.session_state.answers_submitted = False
    if 'story_started' not in st.session_state:
        st.session_state.story_started = False
    
    stories = {
        "Easy": [
            {
                "title": "The Kind Lion",
                "text": "Once there was a kind lion. He helped all the animals in the forest. One day, he found a little mouse in trouble. The lion helped the mouse. Later, the mouse helped the lion too. They became good friends.",
                "questions": [
                    "Who is the main character?",
                    "What did the lion do?",
                    "Who did the lion help?",
                    "Did the mouse help the lion too?",
                    "Where does the story take place?",
                    "What is the moral of the story?"
                ],
                "keywords": ["lion", "mouse", "help", "forest", "friends", "kindness"]
            }
        ],
        "Medium": [
            {
                "title": "The Magic Garden",
                "text": "In Sarah's backyard, there was a special garden. Every night, the flowers would sing sweet lullabies. Butterflies would dance in the moonlight. One day, Sarah discovered that her garden was magical because she had been taking such good care of it.",
                "questions": [
                    "Where was the special garden?",
                    "What did the flowers do at night?",
                    "What did the butterflies do?",
                    "Why was the garden magical?",
                    "Who is Sarah?",
                    "What is the message of this story?"
                ],
                "keywords": ["garden", "flowers", "butterflies", "magic", "care", "Sarah"]
            }
        ],
        "Hard": [
            {
                "title": "The Time Machine",
                "text": "Professor Smith invented a remarkable time machine in his basement laboratory. After years of careful calculations and experiments, he finally completed his creation. However, when he tested it for the first time, something unexpected happened. Instead of traveling through time, he traveled through different dimensions!",
                "questions": [
                    "What did Professor Smith invent?",
                    "Where did he build his invention?",
                    "How long did it take to complete?",
                    "What happened during the test?",
                    "Was the result what he expected?",
                    "What genre is this story?"
                ],
                "keywords": ["time machine", "professor", "invention", "dimensions", "experiment", "laboratory"]
            }
        ]
    }
    
    # Create containers for better organization
    header_container = st.container()
    story_container = st.container()
    question_container = st.container()
    feedback_container = st.container()
    
    with header_container:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("📖 Start New Story", key="new_story"):
                story = random.choice(stories[st.session_state.current_level])
                st.session_state.current_story = story
                st.session_state.current_audio = get_audio_html(story['text'], slow=slow_audio)
                st.session_state.answers_submitted = False
                st.session_state.story_started = True
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_story"):
                st.session_state.current_story = None
                st.session_state.current_audio = None
                st.session_state.answers_submitted = False
                st.session_state.story_started = False
                st.rerun()
    
    if st.session_state.story_started and st.session_state.current_story:
        with story_container:
            # Style the story display
            st.markdown("""
            <style>
            .story-container {
                background-color: #00060CFF;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #1e88e5;
                margin: 10px 0;
            }
            .story-title {
                color: #1e88e5;
                font-size: 24px;
                margin-bottom: 15px;
            }
            .keywords {
                background-color: #00080EFF;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="story-container">
                <div class="story-title">{st.session_state.current_story['title']}</div>
                {st.session_state.current_story['text']}
            </div>
            """, unsafe_allow_html=True)
            
            # Audio controls
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.session_state.current_audio:
                    st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            with col2:
                if st.button("🔊 Listen Again", key="listen_again"):
                    st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            # Display keywords
            st.markdown(f"""
            <div class="keywords">
                <strong>Keywords:</strong> {', '.join(st.session_state.current_story['keywords'])}
            </div>
            """, unsafe_allow_html=True)
        
        with question_container:
            st.markdown("### 📝 Answer these questions:")
            
            # Create a form for questions
            with st.form(key='story_questions'):
                answers = {}
                for question in st.session_state.current_story['questions']:
                    answers[question] = st.text_input(
                        question,
                        key=f"q_{hash(question)}"
                    )
                
                submit_button = st.form_submit_button("📤 Submit Answers")
                
                if submit_button and not st.session_state.answers_submitted:
                    correct_count = sum([1 for ans in answers.values() if ans.strip() != ""])
                    percentage = (correct_count / len(st.session_state.current_story['questions'])) * 100
                    st.session_state.score += correct_count
                    
                    # Show results
                    if percentage >= 80:
                        st.success(f"🌟 Excellent! You answered {correct_count} out of {len(st.session_state.current_story['questions'])} questions correctly!")
                        update_progress("Story Time", True)
                    else:
                        st.warning(f"📚 Good try! You answered {correct_count} out of {len(st.session_state.current_story['questions'])} questions. Keep practicing!")
                        update_progress("Story Time", False)
                    
                    st.session_state.answers_submitted = True
    
    with feedback_container:
        if hasattr(st.session_state, 'history'):
            story_attempts = len([x for x in st.session_state.history 
                                if x['activity'] == 'Story Time'])
            if story_attempts > 0:
                success_rate = len([x for x in st.session_state.history 
                                  if x['activity'] == 'Story Time' 
                                  and x['result'] == 'correct']) / story_attempts
                
                st.markdown("### 📊 Your Progress")
                st.progress(success_rate)
                st.markdown(f"Success Rate: {success_rate*100:.1f}%")
                
                # Reading tips
                with st.expander("💡 Reading Comprehension Tips"):
                    st.markdown("""
                    - Read the story carefully at least twice
                    - Pay attention to the keywords
                    - Try to visualize the story as you read
                    - Look for cause and effect relationships
                    - Think about the main message or moral
                    - Use context clues to understand new words
                    """)

def sentence_practice(slow_audio=False):
    st.subheader("🗣️ Sentence Practice")
    
    # Initialize session states
    if 'current_sentence' not in st.session_state:
        st.session_state.current_sentence = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'answer_checked' not in st.session_state:
        st.session_state.answer_checked = False
    if 'current_accuracy' not in st.session_state:
        st.session_state.current_accuracy = 0
    
    sentences = {
        "Easy": [
            "The cat sits on the mat.",
            "I like to play in the park.",
            "The sun is bright today.",
            "She has a red book.",
            "They are going to school.",
            "The dog runs fast.",
            "We eat breakfast every morning."
        ],
        "Medium": [
            "The children are playing in the garden after lunch.",
            "Yesterday, I went to the museum with my family.",
            "The beautiful butterfly landed on the yellow flower.",
            "She enjoys reading books under the big tree.",
            "The teacher explained the lesson carefully.",
            "They built a sandcastle at the beach.",
            "The stars twinkle brightly in the night sky."
        ],
        "Hard": [
            "Although it was raining heavily, they continued their journey through the forest.",
            "The scientist discovered a remarkable new species of butterfly in the Amazon rainforest.",
            "Despite the challenging circumstances, she persevered and achieved her goals.",
            "The ancient manuscript revealed secrets about the forgotten civilization.",
            "The spectacular aurora borealis illuminated the northern sky.",
            "The innovative technology revolutionized the way people communicate.",
            "The symphony orchestra performed a magnificent concert at the grand hall."
        ]
    }
    
    # Create containers for better organization
    header_container = st.container()
    practice_container = st.container()
    feedback_container = st.container()
    
    with header_container:
        # Display level and controls
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔄 New Sentence", key="new_sentence"):
                # Get a new sentence different from the current one
                available_sentences = [s for s in sentences[st.session_state.current_level] 
                                    if s != st.session_state.current_sentence]
                sentence = random.choice(available_sentences)
                st.session_state.current_sentence = sentence
                st.session_state.current_audio = get_audio_html(sentence, slow=slow_audio)
                st.session_state.answer_checked = False
                st.session_state.current_accuracy = 0
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_practice"):
                st.session_state.current_sentence = None
                st.session_state.current_audio = None
                st.session_state.answer_checked = False
                st.session_state.current_accuracy = 0
                st.rerun()
    
    if st.session_state.current_sentence:
        with practice_container:
            # Style the practice area
            st.markdown("""
            <style>
            .practice-container {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #1e88e5;
                margin: 10px 0;
            }
            .sentence-length {
                color: #666;
                font-size: 14px;
                margin-top: 5px;
            }
            .accuracy-meter {
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
                background-color: #e3f2fd;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Audio player
            if st.session_state.current_audio:
                st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
            
            # Display sentence length info
            st.markdown(f"""
            <div class="sentence-length">
                Words: {len(st.session_state.current_sentence.split())} | 
                Characters: {len(st.session_state.current_sentence)}
            </div>
            """, unsafe_allow_html=True)
            
            # Input form
            with st.form(key="sentence_form"):
                user_input = st.text_input(
                    "Type what you heard:",
                    key=f"input_{hash(st.session_state.current_sentence)}"
                )
                
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    submit_button = st.form_submit_button("✅ Check")
                with col2:
                    listen_button = st.form_submit_button("🔊 Listen Again")
                with col3:
                    next_button = st.form_submit_button("➡️ Next")
                
                if submit_button and not st.session_state.answer_checked:
                    accuracy = calculate_sentence_accuracy(user_input, st.session_state.current_sentence)
                    st.session_state.current_accuracy = accuracy
                    st.session_state.answer_checked = True
                    
                    if accuracy >= 90:
                        st.success(f"Perfect match! 🎉 Accuracy: {accuracy:.1f}%")
                        update_progress("Sentence Practice", True)
                        st.session_state.score += 2
                    else:
                        st.warning(f"Almost there! Accuracy: {accuracy:.1f}%")
                        # Show difference highlighting
                        show_difference_highlighting(user_input, st.session_state.current_sentence)
                        update_progress("Sentence Practice", False)
                
                if listen_button:
                    st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
                
                if next_button:
                    available_sentences = [s for s in sentences[st.session_state.current_level] 
                                        if s != st.session_state.current_sentence]
                    new_sentence = random.choice(available_sentences)
                    st.session_state.current_sentence = new_sentence
                    st.session_state.current_audio = get_audio_html(new_sentence, slow=slow_audio)
                    st.session_state.answer_checked = False
                    st.session_state.current_accuracy = 0
                    st.rerun()
    
    with feedback_container:
        if hasattr(st.session_state, 'history'):
            # Show progress
            sentence_attempts = len([x for x in st.session_state.history 
                                   if x['activity'] == 'Sentence Practice'])
            if sentence_attempts > 0:
                success_rate = len([x for x in st.session_state.history 
                                  if x['activity'] == 'Sentence Practice' 
                                  and x['result'] == 'correct']) / sentence_attempts
                
                st.markdown("### 📊 Your Progress")
                st.progress(success_rate)
                st.markdown(f"Success Rate: {success_rate*100:.1f}%")
                
                # Practice tips
                with st.expander("💡 Tips for Better Sentence Practice"):
                    st.markdown("""
                    - Listen carefully to the entire sentence before typing
                    - Pay attention to punctuation marks
                    - Break long sentences into smaller chunks
                    - Practice with different speeds
                    - Focus on challenging words
                    - Use context clues to understand meaning
                    """)

def show_difference_highlighting(user_input, correct_sentence):
    """Show differences between user input and correct sentence"""
    import difflib
    
    d = difflib.Differ()
    diff = list(d.compare(user_input.lower(), correct_sentence.lower()))
    
    st.markdown("### Difference Analysis:")
    st.markdown("""
    <style>
    .diff-added { color: #4caf50; font-weight: bold; }
    .diff-removed { color: #f44336; font-weight: bold; text-decoration: line-through; }
    </style>
    """, unsafe_allow_html=True)
    
    diff_html = []
    for token in diff:
        if token.startswith('+'):
            diff_html.append(f'<span class="diff-added">{token[2:]}</span>')
        elif token.startswith('-'):
            diff_html.append(f'<span class="diff-removed">{token[2:]}</span>')
        elif token.startswith(' '):
            diff_html.append(token[2:])
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px;">
        {''.join(diff_html)}
    </div>
    """, unsafe_allow_html=True)

def calculate_sentence_accuracy(user_input, correct_sentence):
    """Calculate accuracy percentage between user input and correct sentence"""
    if not user_input:
        return 0
    
    user_words = user_input.lower().split()
    correct_words = correct_sentence.lower().split()
    
    # Word-level accuracy
    correct_word_count = sum(1 for u, c in zip(user_words, correct_words) if u == c)
    word_accuracy = (correct_word_count / len(correct_words)) * 100
    
    # Character-level accuracy
    import difflib
    sequence_matcher = difflib.SequenceMatcher(None, user_input.lower(), correct_sentence.lower())
    char_accuracy = sequence_matcher.ratio() * 100
    
    # Combined accuracy score
    return (word_accuracy + char_accuracy) / 2

def calculate_sentence_accuracy(user_input, correct_sentence):
    """Calculate the accuracy percentage of the user's input"""
    user_words = user_input.lower().strip().split()
    correct_words = correct_sentence.lower().strip().split()
    
    if not user_words:
        return 0
    
    correct_count = sum(1 for u, c in zip(user_words, correct_words) if u == c)
    total_words = max(len(user_words), len(correct_words))
    
    return (correct_count / total_words) * 100

def phonetic_practice(slow_audio=False):
    st.subheader("🔤 Phonetic Fun")
    
    # Initialize session states
    if 'selected_phoneme' not in st.session_state:
        st.session_state.selected_phoneme = None
    if 'practice_word' not in st.session_state:
        st.session_state.practice_word = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'practice_count' not in st.session_state:
        st.session_state.practice_count = 0
    
    phonemes = {
        "Easy": {
            "th": ["this", "that", "three", "thank", "think", "thumb", "throat"],
            "sh": ["ship", "shop", "shell", "share", "shake", "shoe", "shine"],
            "ch": ["chair", "cheese", "church", "chest", "chain", "child", "chips"]
        },
        "Medium": {
            "ph": ["phone", "photo", "phrase", "phantom", "physics", "phonics", "pharmacy"],
            "wh": ["what", "where", "when", "which", "whale", "wheel", "whistle"],
            "ck": ["back", "black", "clock", "duck", "kick", "stick", "truck"]
        },
        "Hard": {
            "ough": ["though", "through", "thought", "rough", "cough", "enough", "bought"],
            "tion": ["action", "motion", "station", "fiction", "nation", "section", "portion"],
            "ight": ["light", "night", "right", "sight", "fight", "bright", "flight"]
        }
    }
    
    # Create containers for better organization
    header_container = st.container()
    practice_container = st.container()
    word_container = st.container()
    feedback_container = st.container()
    
    with header_container:
        st.markdown("""
        <style>
        .phoneme-header {
            background-color: #000000FF;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #1e88e5;
            margin: 10px 0;
        }
        .word-card {
            background-color: #070000FF;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.2s;
        }
        .word-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .practice-area {
            background-color: #00070EFF;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_phoneme = st.selectbox(
                "Choose a sound to practice:",
                list(phonemes[st.session_state.current_level].keys()),
                key='phoneme_selector'
            )
            
            if new_phoneme != st.session_state.selected_phoneme:
                st.session_state.selected_phoneme = new_phoneme
                st.session_state.practice_word = None
                st.session_state.current_audio = None
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset", key="reset_practice"):
                st.session_state.practice_word = None
                st.session_state.current_audio = None
                st.session_state.practice_count = 0
                st.rerun()
    
    if st.session_state.selected_phoneme:
        with practice_container:
            st.markdown(f"""
            <div class="phoneme-header">
                <h3>Words with '{st.session_state.selected_phoneme}' sound</h3>
                <p>Click on any word to practice!</p>
            </div>
            """, unsafe_allow_html=True)
            
            current_words = phonemes[st.session_state.current_level][st.session_state.selected_phoneme]
            
            # Display words in a grid
            cols = st.columns(3)
            for idx, word in enumerate(current_words):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="word-card">
                        <h4>{word}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"🔊 Practice", key=f"practice_{word}"):
                        st.session_state.practice_word = word
                        st.session_state.current_audio = get_audio_html(word, slow=slow_audio)
                        st.rerun()
        
        if st.session_state.practice_word:
            with word_container:
                st.markdown("""
                <div class="practice-area">
                """, unsafe_allow_html=True)
                
                st.markdown(f"### Practicing: {st.session_state.practice_word}")
                
                # Audio controls
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.session_state.current_audio:
                        st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
                with col2:
                    if st.button("🔊 Repeat", key="repeat_audio"):
                        st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
                
                # Practice form
                with st.form(key="practice_form"):
                    user_input = st.text_input(
                        "Type what you hear:",
                        key=f"input_{st.session_state.practice_word}"
                    )
                    
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        submit = st.form_submit_button("✅ Check")
                    with col2:
                        listen = st.form_submit_button("🔊 Listen")
                    with col3:
                        next_word = st.form_submit_button("➡️ Next")
                    
                    if submit:
                        if user_input.lower().strip() == st.session_state.practice_word.lower():
                            st.success("Correct spelling! 🎉")
                            update_progress("Phonetic Practice", True)
                            st.session_state.score += 1
                            st.session_state.practice_count += 1
                        else:
                            st.error(f"The correct spelling is: {st.session_state.practice_word}")
                            show_difference_highlighting(user_input, st.session_state.practice_word)
                            update_progress("Phonetic Practice", False)
                    
                    if listen:
                        st.markdown(st.session_state.current_audio, unsafe_allow_html=True)
                    
                    if next_word:
                        available_words = [w for w in current_words if w != st.session_state.practice_word]
                        if available_words:
                            new_word = random.choice(available_words)
                            st.session_state.practice_word = new_word
                            st.session_state.current_audio = get_audio_html(new_word, slow=slow_audio)
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    with feedback_container:
        if hasattr(st.session_state, 'history'):
            # Show progress
            phonetic_attempts = len([x for x in st.session_state.history 
                                   if x['activity'] == 'Phonetic Practice'])
            if phonetic_attempts > 0:
                success_rate = len([x for x in st.session_state.history 
                                  if x['activity'] == 'Phonetic Practice' 
                                  and x['result'] == 'correct']) / phonetic_attempts
                
                st.markdown("### 📊 Your Progress")
                st.progress(success_rate)
                st.markdown(f"Success Rate: {success_rate*100:.1f}%")
                
                # Tips expander
                with st.expander("💡 Phonetic Practice Tips"):
                    st.markdown("""
                    - Listen carefully to the sound patterns
                    - Pay attention to similar sounds
                    - Practice saying the words out loud
                    - Break down complex sounds
                    - Notice patterns in spelling
                    - Use the slow audio option for difficult words
                    """)

if __name__ == "__main__":
    create_listening_module()