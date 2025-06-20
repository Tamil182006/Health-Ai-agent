import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 💅 Modern UI Styling - Only Visual Changes, No Logic Touched
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f5f9ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    body {
        background-color: #f5f9ff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #2e8b57;
        color: white;
        font-weight: 600;
        border: none;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #276747;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .custom-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #e6fffa;
        border: 1px solid #81e6d9;
        margin-bottom: 1rem;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #fffaf0;
        border: 1px solid #fbd38d;
        margin-bottom: 1rem;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
    }
    h1, h2, h3 {
        color: #2e8b57;
        font-weight: 700;
    }
    .section-box {
        background: linear-gradient(to right, #d4fc79, #96e6a1);
        padding: 1rem;
        border-radius: 12px;
        color: #003300;
        font-weight: bold;
        margin-bottom: 1.5rem;
        font-size: 1.05rem;
    }
    </style>
""", unsafe_allow_html=True)

def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        st.markdown(f"""
        <div class="custom-card">
            <h3>🌟 Why this plan works</h3>
            <p>{plan_content.get("why_this_plan_works", "Information not available")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="custom-card">
            <h3>🍽️ Meal Plan</h3>
            <p>{plan_content.get("meal_plan", "Plan not available").replace('\n', '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

        considerations = plan_content.get("important_considerations", "").split('\n')
        if any(c.strip() for c in considerations):
            st.markdown("""
            <div class="custom-card">
                <h3>⚠️ Important Considerations</h3>
                <ul>
            """, unsafe_allow_html=True)
            for consideration in considerations:
                if consideration.strip():
                    st.markdown(f"<li>{consideration.strip()}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        st.markdown(f"""
        <div class="custom-card">
            <h3>🌟 Goals</h3>
            <p>{plan_content.get("goals", "Goals not specified")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="custom-card">
            <h3>🏋️‍♂️ Exercise Routine</h3>
            <p>{plan_content.get("routine", "Routine not available").replace('\n', '<br>')}</p>
        </div>
        """, unsafe_allow_html=True)

        tips = plan_content.get("tips", "").split('\n')
        if any(t.strip() for t in tips):
            st.markdown("""
            <div class="custom-card">
                <h3>💡 Pro Tips</h3>
                <ul>
            """, unsafe_allow_html=True)
            for tip in tips:
                if tip.strip():
                    st.markdown(f"<li>{tip.strip()}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)

# Keep rest of your logic (main(), etc.) unchanged. This is the enhanced CSS + display blocks.


def main():
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    st.title("🏋️‍♂️ AI Health & Fitness Planner")

    st.markdown("""
        <div class='section-box'>
            Get personalized dietary and fitness plans tailored to your goals and preferences.
            Our AI-powered system considers your unique profile to create the perfect plan for you.
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("🔑 API Configuration")
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Gemini API key to access the service"
        )

        if not gemini_api_key:
            st.warning("⚠️ Please enter your Gemini API Key to proceed")
            st.markdown("[Get your API key here](https://aistudio.google.com/apikey)")
            return

        st.success("API Key accepted!")

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-2.5-flash-preview-05-20", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Error initializing Gemini model: {e}")
            return

        st.header("👤 Your Profile")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
            activity_level = st.selectbox(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                help="Choose your typical activity level"
            )
            dietary_preferences = st.selectbox(
                "Dietary Preferences",
                options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
                help="Select your dietary preference"
            )

        with col2:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
            fitness_goals = st.selectbox(
                "Fitness Goals",
                options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
                help="What do you want to achieve?"
            )

        if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
            with st.spinner("Creating your perfect health and fitness routine..."):
                try:
                    dietary_agent = Agent(
                        name="Dietary Expert",
                        role="Provides personalized dietary recommendations",
                        model=gemini_model,
                        instructions=[
                            "Consider the user's input, including dietary restrictions and preferences.",
                            "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                            "Provide a brief explanation of why the plan is suited to the user's goals.",
                            "Focus on clarity, coherence, and quality of the recommendations.",
                        ]
                    )

                    fitness_agent = Agent(
                        name="Fitness Expert",
                        role="Provides personalized fitness recommendations",
                        model=gemini_model,
                        instructions=[
                            "Provide exercises tailored to the user's goals.",
                            "Include warm-up, main workout, and cool-down exercises.",
                            "Explain the benefits of each recommended exercise.",
                            "Ensure the plan is actionable and detailed.",
                        ]
                    )

                    user_profile = f"""
                    Age: {age}
                    Weight: {weight}kg
                    Height: {height}cm
                    Sex: {sex}
                    Activity Level: {activity_level}
                    Dietary Preferences: {dietary_preferences}
                    Fitness Goals: {fitness_goals}
                    """

                    dietary_plan_response = dietary_agent.run(user_profile)
                    dietary_plan = {
                        "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                        "meal_plan": dietary_plan_response.content,
                        "important_considerations": """
                        - Hydration: Drink plenty of water throughout the day
                        - Electrolytes: Monitor sodium, potassium, and magnesium levels
                        - Fiber: Ensure adequate intake through vegetables and fruits
                        - Listen to your body: Adjust portion sizes as needed
                        """
                    }

                    fitness_plan_response = fitness_agent.run(user_profile)
                    fitness_plan = {
                        "goals": "Build strength, improve endurance, and maintain overall fitness",
                        "routine": fitness_plan_response.content,
                        "tips": """
                        - Track your progress regularly
                        - Allow proper rest between workouts
                        - Focus on proper form
                        - Stay consistent with your routine
                        """
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    st.session_state.qa_pairs = []

                    display_dietary_plan(dietary_plan)
                    display_fitness_plan(fitness_plan)

                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

        if st.session_state.plans_generated:
            st.header("❓ Questions about your plan?")
            question_input = st.text_input("What would you like to know?")

            if st.button("Get Answer"):
                if question_input:
                    with st.spinner("Finding the best answer for you..."):
                        dietary_plan = st.session_state.dietary_plan
                        fitness_plan = st.session_state.fitness_plan

                        context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}"
                        full_context = f"{context}\nUser Question: {question_input}"

                        try:
                            agent = Agent(model=gemini_model, show_tool_calls=True, markdown=True)
                            run_response = agent.run(full_context)

                            if hasattr(run_response, 'content'):
                                answer = run_response.content
                            else:
                                answer = "Sorry, I couldn't generate a response at this time."

                            st.session_state.qa_pairs.append((question_input, answer))
                        except Exception as e:
                            st.error(f"❌ An error occurred while getting the answer: {e}")

            if st.session_state.qa_pairs:
                st.header("💬 Q&A History")
                for question, answer in st.session_state.qa_pairs:
                    st.markdown(f"**Q:** {question}")
                    st.markdown(f"**A:** {answer}")

if __name__ == "__main__":
    main()
