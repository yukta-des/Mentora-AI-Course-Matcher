import os
import json
import google.generativeai as genai
from config import Config

def init_gemini():
    api_key = Config.GEMINI_API_KEY or os.environ.get('GEMINI_API_KEY')
    if api_key:
        try:
            genai.configure(api_key=api_key)
            return True
        except Exception as e:
            print("Gemini config warning:", e)
    return False

def chat_with_advisor(user_message, conversation_history, courses_catalog):
    """
    AI Course Advisor Chatbot powered by Gemini API.
    Recommends exact courses from the database with personalized rationale.
    """
    has_api = init_gemini()
    
    # Prepare concise catalog summary for Gemini context
    catalog_summary = []
    for c in courses_catalog[:40]: # Send top 40 curated courses
        catalog_summary.append({
            "id": c.id,
            "title": c.title,
            "platform": c.platform,
            "level": c.level,
            "topic": c.topic,
            "is_free": c.is_free,
            "price_usd": c.price_usd,
            "duration_hours": c.duration_hours,
            "summary": c.summary
        })

    system_instruction = f"""
You are Mentora AI — a world-class AI Career & Course Advisor.
Your job is to help users find the exact right AI courses based on their background, career goals, available time, and budget.

Database of available courses:
{json.dumps(catalog_summary, indent=2)}

Guidelines:
1. Always be encouraging, clear, and structured.
2. Whenever you recommend a course, refer to its EXACT title and platform as listed in the database.
3. Provide a clear 1-2 sentence rationale for WHY this course fits their goal.
4. If the user gives a goal like "Become an ML engineer", outline a sequential step-by-step learning path (Step 1, Step 2, Step 3).
5. Highlight free alternatives if budget is a concern.
"""

    if not has_api:
        # Fallback intelligent advisory logic when API key is pending
        query_lower = user_message.lower()
        matched_courses = []
        for c in courses_catalog:
            if c.topic.lower() in query_lower or c.level.lower() in query_lower or any(word in c.title.lower() for word in query_lower.split()):
                matched_courses.append(c)
                if len(matched_courses) >= 3:
                    break
        if not matched_courses:
            matched_courses = courses_catalog[:3]

        fallback_text = f"🤖 **Mentora Advisor Recommendation**:\n\nBased on your query: *\"{user_message}\"*, here is your custom recommendation:\n\n"
        for idx, course in enumerate(matched_courses, 1):
            fallback_text += f"**Step {idx}: {course.title}** ({course.platform})\n"
            fallback_text += f"• **Level**: {course.level} | **Price**: {'FREE' if course.is_free else f'${course.price_usd}'} | **Duration**: ~{course.duration_hours}h\n"
            fallback_text += f"• **Why this fits**: Matches your target skill set in {course.topic}.\n\n"

        return {
            "status": "success",
            "reply": fallback_text,
            "recommended_course_ids": [c.id for c in matched_courses]
        }

    try:
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        
        # Build prompt from history
        chat_prompt = f"User asks: {user_message}"
        response = model.generate_content(chat_prompt)
        
        return {
            "status": "success",
            "reply": response.text
        }
    except Exception as e:
        print("Gemini API Error:", str(e))
        return {
            "status": "error",
            "reply": f"Mentora AI Advisor error: {str(e)}. (Make sure GEMINI_API_KEY is set in config.py or environment)."
        }


def generate_learning_path_roadmap(goal, courses_catalog):
    """
    Generates a structured multi-step roadmap for a career goal (e.g. 'ML Engineer', 'Chatbot Builder').
    """
    has_api = init_gemini()
    
    # Filter courses matching target goal
    goal_lower = goal.lower()
    step_courses = []
    
    # Pick beginner, intermediate, advanced progression
    beginners = [c for c in courses_catalog if c.level == 'Beginner']
    intermediates = [c for c in courses_catalog if c.level == 'Intermediate']
    advanceds = [c for c in courses_catalog if c.level == 'Advanced']
    
    step1 = next((c for c in beginners if any(w in c.topic.lower() for w in goal_lower.split())), beginners[0] if beginners else courses_catalog[0])
    step2 = next((c for c in intermediates if any(w in c.topic.lower() for w in goal_lower.split())), intermediates[0] if intermediates else courses_catalog[1])
    step3 = next((c for c in advanceds if any(w in c.topic.lower() for w in goal_lower.split())), advanceds[0] if advanceds else courses_catalog[2])

    steps = [
        {
            "step_number": 1,
            "phase": "Foundations",
            "course": step1.to_dict(),
            "milestone": f"Master basic terminology, syntax, and foundational concepts in {step1.topic}."
        },
        {
            "step_number": 2,
            "phase": "Core Skill Building",
            "course": step2.to_dict(),
            "milestone": f"Build real-world hands-on projects and fine-tune models in {step2.topic}."
        },
        {
            "step_number": 3,
            "phase": "Advanced Specialization",
            "course": step3.to_dict(),
            "milestone": f"Deploy production-grade systems, optimize performance, and master MLOps."
        }
    ]

    return {
        "status": "success",
        "goal": goal,
        "total_estimated_hours": step1.duration_hours + step2.duration_hours + step3.duration_hours,
        "steps": steps
    }
