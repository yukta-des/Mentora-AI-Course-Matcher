import os
import sys
import webbrowser
import threading
import time

def open_browser():
    """Wait 1.5 seconds for Flask server to start, then open default web browser directly."""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

def main():
    print("=" * 60)
    print("  🚀 MENTORA: AI-Powered Course Recommendation Web App")
    print("=" * 60)

    # Step 1: Ensure database exists and is seeded
    db_file = os.path.join(os.path.dirname(__file__), 'mentora.db')
    if not os.path.exists(db_file):
        print("\n📦 First-time setup detected: Seeding 250 curated AI courses into database...")
        from seed_courses import seed
        seed()
    else:
        print("\n✅ Database (mentora.db) detected and ready.")

    # Step 2: Inform user about Gemini API Key
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("\nℹ️  GEMINI_API_KEY environment variable is not set.")
        print("   Mentora AI Advisor will run in demo fallback mode.")
    else:
        print("🤖 Gemini API Key configured for AI Advisor & Learning Paths!")

    # Step 3: Open browser automatically in background thread
    print("\n🌐 Opening Mentora in your web browser directly...")
    threading.Thread(target=open_browser, daemon=True).start()

    # Step 4: Run Flask Web Server
    print("   Running on http://127.0.0.1:5000\n")
    print("Press CTRL+C to stop the server.")
    print("=" * 60 + "\n")

    from app import app
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

if __name__ == '__main__':
    main()
