import streamlit as st
import streamlit.components.v1 as components
import notes_extractor
import flashcard_generator
import flashcard_formatter

# Page Setup
st.set_page_config(page_title="Notes to Flashcards", page_icon="📝")

if "deck" not in st.session_state:
    st.session_state.deck = None
if "elements" not in st.session_state:
    st.session_state.elements = []
if "flashcard_mode" not in st.session_state:
    st.session_state.flashcard_mode = "Auto"

# Sidebar Info
st.sidebar.markdown("# 📝 Notes to Flashcards")
st.sidebar.write(
    "An AI-powered study tool that converts raw notes and files into customized flashcards, "
    "which can be exported directly to platforms like Quizlet and Knowt."
)

# Sidebar Buttons
youtube_svg = '<svg style="width: 24px; height: 17px; margin-right: 10px;" viewBox="0 0 24 24" fill="red"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
github_svg = '<svg style="width: 20px; height: 20px; margin-right: 10px; fill: var(--text-color);" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>'

button_style = "background-color: var(--secondary-background-color); color: var(--text-color); padding: 0.5rem 1rem; border-radius: 0.5rem; display: flex; align-items: center; border: 1px solid rgba(128, 128, 128, 0.4); font-family: sans-serif; font-size: 14px; font-weight: 500;"

st.sidebar.markdown(
    f"""
    <a href="https://youtu.be/O4EYNBXZeUk" target="_blank" style="text-decoration: none; display: block; margin-bottom: 10px;">
        <div style="{button_style}">{youtube_svg}Watch Video Demo</div>
    </a>
    <a href="https://github.com/git-ishaan-kumar/notes-to-flashcards" target="_blank" style="text-decoration: none; display: block;">
        <div style="{button_style}">{github_svg}Open in GitHub</div>
    </a>
    """,
    unsafe_allow_html=True
)

# Main Interface
if st.session_state.deck is None:
    
    # Input Sources
    st.subheader("1. Provide Source Material")
    uploaded_files = st.file_uploader("Upload files (.txt, .pdf, .docx) - Max 3", type=["txt", "pdf", "docx"], accept_multiple_files=True)
    pasted_text = st.text_area("Or paste your notes directly from your clipboard here:", height=150)
    
    st.divider()
    
    # Settings
    st.subheader("2. Configure Flashcards")
    
    col1, col2 = st.columns(2)
    with col1:
        options = ["Auto"] + list(range(1, 21))
        num_cards_val = st.select_slider("Number of Cards", options=options, value="Auto")
            
    with col2:
        flashcard_mode = st.selectbox("Flashcard Mode", ["Auto", "Terms & Definitions", "Practice Test", "Fill-in-the-Blank"])
    
    st.divider()
    
    # Formatting Separators
    st.subheader("3. Format & Export Settings")
    format_choice = st.selectbox("Export Format Separators", ["Tab Separated (Default)", "Comma & Semicolon", "Custom"])
    
    # Default Mappings
    format_type = "tab"
    custom_term_sep = "\t"
    custom_card_sep = ""
    
    if format_choice == "Comma & Semicolon":
        format_type = "comma"
    elif format_choice == "Custom":
        format_type = "custom"
        c1, c2 = st.columns(2)
        with c1:
            custom_term_sep = st.text_input("Between Term & Definition", value="|")
        with c2:
            custom_card_sep = st.text_input("Between Cards", value="***")
            
    # Save Formatting Settings
    st.session_state.format_type = format_type
    st.session_state.custom_term_sep = custom_term_sep
    st.session_state.custom_card_sep = custom_card_sep

    # Generation Trigger
    if st.button("🚀 Generate Flashcards", type="primary", use_container_width=True):
        elements = []
        try:
            if uploaded_files:
                if len(uploaded_files) > 3:
                    st.warning("Maximum of 3 files allowed. Only processing the first 3.")
                    files_to_process = uploaded_files[:3]
                else:
                    files_to_process = uploaded_files
                    
                for file in files_to_process:
                    elements.extend(notes_extractor.process_document(file))
                    
            if pasted_text.strip():
                elements.append(pasted_text.strip())
                
            if not elements:
                st.error("Please provide some notes or upload a file first!")
            else:
                with st.spinner("🧠 AI is analyzing your notes and generating flashcards..."):
                    st.session_state.elements = elements
                    st.session_state.flashcard_mode = flashcard_mode
                    
                    deck = flashcard_generator.generate_cards(
                        extracted_elements=elements,
                        num_cards=num_cards_val,
                        flashcard_mode=flashcard_mode
                    )
                    
                    if deck:
                        st.session_state.deck = deck
                        st.rerun()
                    else:
                        st.error("❌ Failed to generate flashcards. Please try again.")
        except Exception as e:
            st.error(f"❌ An error occurred during file processing: {e}")

# Output Interface
else:
    st.markdown("<div id='deck-start'></div>", unsafe_allow_html=True)
    
    deck = st.session_state.deck
    
    scroll_script = f"""
    <script>
        var parent = window.parent;
        var scrollCount = 0;
        var scrollInterval = setInterval(function() {{
            if (parent) {{
                var anchor = parent.document.getElementById('deck-start');
                if (anchor) {{
                    anchor.scrollIntoView({{behavior: 'auto', block: 'start'}});
                }} else {{
                    parent.scrollTo(0, 0);
                    var viewContainer = parent.document.querySelector('[data-testid="stAppViewContainer"]');
                    if (viewContainer) viewContainer.scrollTo(0, 0);
                }}
            }}
            scrollCount++;
            if (scrollCount >= 20) {{
                clearInterval(scrollInterval); // Stop trying after 2 seconds
            }}
        }}, 100);
    </script>
    <!-- trigger id: {len(deck.cards)} -->
    """
    components.html(scroll_script, height=0)
    
    st.success(f"Successfully created {len(deck.cards)} flashcards!")
    
    # Retrieve Formatter Settings
    format_type = st.session_state.get("format_type", "tab")
    c_term = st.session_state.get("custom_term_sep", "\t")
    c_card = st.session_state.get("custom_card_sep", "")
    
    # Generate Formatted String
    formatted_text = flashcard_formatter.format_flashcards(
        deck=deck,
        format_type=format_type,
        custom_term_sep=c_term,
        custom_card_sep=c_card
    )
    
    # Code Block Output
    st.code(formatted_text, language="text")
    
    # Determine Display Names
    if format_type == "tab":
        term_display = "Tab"
        card_display = "New Line"
    elif format_type == "comma":
        term_display = "Comma"
        card_display = "Semicolon"
    else:
        term_display = f"'{c_term}'"
        card_display = f"'{c_card}'"
        
    st.divider()
    st.subheader("📥 How to Import")
    
    # Import Instruction Toggles
    tab1, tab2 = st.tabs(["🟦 Quizlet", "🦉 Knowt"])
    
    with tab1:
        st.markdown(f"""
        **Steps to import to Quizlet:**
        1. Go to Quizlet and click **Create a new study set**.
        2. Scroll down and click the **Import from Word, Excel, Google Docs, etc.** button.
        3. Copy the formatted text from the code box above (use the clipboard icon in the top right!).
        4. Paste the text into the Quizlet import box.
        5. Make sure **Between term and definition** is set to: `{term_display}`.
        6. Make sure **Between cards** is set to: `{card_display}`.
        7. Click **Import**.
        """)
        
    with tab2:
        st.markdown(f"""
        **Steps to import to Knowt:**
        1. Go to Knowt and create a new set, then click **Import**.
        2. Copy the formatted text from the code box above.
        3. Paste your text into the import box.
        4. Make sure **Between term and definition** is set to: `{term_display}`.
        5. Make sure **Between rows** is set to: `{card_display}`.
        6. Click **Add to bottom** or **Replace entire set**.
        """)
        
    st.divider()
    
    # Expand Deck Section
    st.subheader("➕ Expand Deck")
    add_count = st.slider("Number of additional cards to generate:", min_value=1, max_value=20, value=10)
    
    # Bottom Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"➕ Generate {add_count} More Cards", type="primary", use_container_width=True):
            with st.spinner(f"🧠 Generating {add_count} more distinct cards..."):
                existing_fronts = [c.front for c in deck.cards]
                avoid_prompt = f"CRITICAL: Do not generate cards for the following concepts you already covered: {existing_fronts}"
                new_elements = st.session_state.elements + [avoid_prompt]
                
                new_deck = flashcard_generator.generate_cards(
                    extracted_elements=new_elements,
                    num_cards=add_count,
                    flashcard_mode=st.session_state.flashcard_mode
                )
                
                if new_deck:
                    st.session_state.deck.cards.extend(new_deck.cards)
                    st.rerun()
                else:
                    st.error("❌ Failed to generate more flashcards. Please try again.")
                    
    with col2:
        if st.button("🔄 Create a New Flashcard Deck", type="secondary", use_container_width=True):
            st.session_state.deck = None
            st.session_state.elements = []
            st.rerun()