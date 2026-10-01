import random
import json
from app import app
from models import db, Course

RAW_COURSES = [
    # --- DeepLearning.AI ---
    {
        "title": "AI for Everyone",
        "platform": "DeepLearning.AI",
        "instructor": "Andrew Ng",
        "link": "https://www.coursera.org/learn/ai-for-everyone",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Beginner",
        "duration_hours": 6,
        "topic": "Generative AI",
        "language": "English",
        "summary": "Non-technical introduction to AI, machine learning, deep learning, and how AI is impacting business and society.",
        "what_you_will_learn": ["AI terminology and concepts", "What AI can and cannot do", "Spotting opportunities to apply AI in your organization", "Building AI strategy in your company"],
        "prerequisites": ["None - suitable for complete beginners"],
        "rating": 4.8,
        "freshness_score": 0.98
    },
    {
        "title": "Generative AI with Large Language Models",
        "platform": "DeepLearning.AI",
        "instructor": "Andrew Ng & AWS",
        "link": "https://www.coursera.org/learn/generative-ai-with-llms",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Intermediate",
        "duration_hours": 16,
        "topic": "LLMs",
        "language": "English",
        "summary": "Master the key steps of LLM workflow: pre-training, fine-tuning (PEFT, LoRA), RLHF, and deploying generative models.",
        "what_you_will_learn": ["Transformer architecture deep dive", "Instruction fine-tuning & Parameter-Efficient Fine-Tuning", "Reinforcement Learning from Human Feedback (RLHF)", "Generative AI project lifecycle"],
        "prerequisites": ["Python intermediate", "Basic Deep Learning concepts"],
        "rating": 4.9,
        "freshness_score": 0.99
    },
    {
        "title": "ChatGPT Prompt Engineering for Developers",
        "platform": "DeepLearning.AI",
        "instructor": "Isa Fulford & Andrew Ng",
        "link": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Beginner",
        "duration_hours": 2,
        "topic": "Prompt Engineering",
        "language": "English",
        "summary": "Learn how to use an LLM API to quickly build new and powerful applications using effective prompt engineering techniques.",
        "what_you_will_learn": ["Summarizing, inferring, transforming text", "Expanding text and chatbot building", "Iterative prompt development", "System vs User message prompts"],
        "prerequisites": ["Basic Python knowledge"],
        "rating": 4.9,
        "freshness_score": 0.96
    },
    {
        "title": "Building Systems with the ChatGPT API",
        "platform": "DeepLearning.AI",
        "instructor": "Isa Fulford & Andrew Ng",
        "link": "https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Intermediate",
        "duration_hours": 3,
        "topic": "Prompt Engineering",
        "language": "English",
        "summary": "Learn how to automate complex workflows using chain-of-thought prompting and OpenAI API integrations.",
        "what_you_will_learn": ["Chaining prompts for multi-step tasks", "Evaluating LLM inputs and outputs for safety", "Building complex conversational user interfaces"],
        "prerequisites": ["Python basics", "ChatGPT prompt engineering fundamentals"],
        "rating": 4.8,
        "freshness_score": 0.95
    },
    {
        "title": "LangChain for LLM Application Development",
        "platform": "DeepLearning.AI",
        "instructor": "Harrison Chase & Andrew Ng",
        "link": "https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Intermediate",
        "duration_hours": 4,
        "topic": "LLMs",
        "language": "English",
        "summary": "Gain hands-on skills in using LangChain framework to build powerful applications with vector databases, agents, and chains.",
        "what_you_will_learn": ["Prompts, Models, and Output Parsers", "Memory management in conversational agents", "Chains and Index retrieval (RAG)", "LangChain Agents"],
        "prerequisites": ["Intermediate Python"],
        "rating": 4.9,
        "freshness_score": 0.97
    },
    {
        "title": "Building Applications with Vector Databases",
        "platform": "DeepLearning.AI",
        "instructor": "Pinecone & DeepLearning.AI",
        "link": "https://www.deeplearning.ai/short-courses/building-applications-with-vector-databases/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Intermediate",
        "duration_hours": 3,
        "topic": "LLMs",
        "language": "English",
        "summary": "Learn semantic search, recommendation systems, and RAG architectures using vector embeddings and Pinecone.",
        "what_you_will_learn": ["Dense and sparse embeddings", "Vector similarity metrics (Cosine, Dot Product)", "Retrieval Augmented Generation architecture", "Building anomaly detection"],
        "prerequisites": ["Python", "Basic machine learning background"],
        "rating": 4.7,
        "freshness_score": 0.94
    },
    {
        "title": "Machine Learning Specialization",
        "platform": "DeepLearning.AI",
        "instructor": "Andrew Ng (Stanford University)",
        "link": "https://www.coursera.org/specializations/machine-learning-introduction",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Beginner",
        "duration_hours": 60,
        "topic": "Machine Learning",
        "language": "English",
        "summary": "Breakthrough 3-course foundational program covering Supervised Learning, Advanced Learning Algorithms, and Unsupervised Learning.",
        "what_you_will_learn": ["Linear & Logistic Regression", "Neural Networks & Decision Trees", "Unsupervised learning & Recommender Systems", "Reinforcement learning basics"],
        "prerequisites": ["Basic high school math", "Basic Python"],
        "rating": 4.9,
        "freshness_score": 0.99
    },
    {
        "title": "Deep Learning Specialization",
        "platform": "DeepLearning.AI",
        "instructor": "Andrew Ng",
        "link": "https://www.coursera.org/specializations/deep-learning",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Intermediate",
        "duration_hours": 80,
        "topic": "Deep Learning",
        "language": "English",
        "summary": "Master Deep Learning, construct Neural Networks, build CNNs for Computer Vision and RNNs/Transformers for NLP.",
        "what_you_will_learn": ["Deep Neural Networks optimization & hyperparameter tuning", "Convolutional Neural Networks (CNNs)", "Sequence Models (RNNs, LSTMs, Transformers)", "Structuring Machine Learning Projects"],
        "prerequisites": ["Python", "Linear algebra basics", "Calculus basics"],
        "rating": 4.9,
        "freshness_score": 0.98
    },
    {
        "title": "MLOps Specialization",
        "platform": "DeepLearning.AI",
        "instructor": "Andrew Ng & Robert Crowe",
        "link": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Advanced",
        "duration_hours": 50,
        "topic": "MLOps",
        "language": "English",
        "summary": "Learn how to conceptualize, build, test, deploy, and continuously monitor production ML systems.",
        "what_you_will_learn": ["Data pipelines and versioning (TFX)", "Model serving and deployment", "Model monitoring & concept drift detection", "Edge deployment and quantization"],
        "prerequisites": ["Python", "Deep learning practice"],
        "rating": 4.8,
        "freshness_score": 0.96
    },

    # --- Coursera / Universities ---
    {
        "title": "CS50's Introduction to Artificial Intelligence with Python",
        "platform": "Harvard / edX",
        "instructor": "Brian Yu & David J. Malan",
        "link": "https://pll.harvard.edu/course/cs50s-introduction-artificial-intelligence-python",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Beginner",
        "duration_hours": 40,
        "topic": "Machine Learning",
        "language": "English",
        "summary": "Explore the concepts and algorithms at the foundation of modern artificial intelligence using Python.",
        "what_you_will_learn": ["Graph search algorithms (A*, Minimax)", "Knowledge representation and logic", "Probability and Bayesian networks", "Neural networks & NLP fundamentals"],
        "prerequisites": ["CS50x or Python programming experience"],
        "rating": 4.9,
        "freshness_score": 0.97
    },
    {
        "title": "Google AI Essentials",
        "platform": "Google",
        "instructor": "Google Career Certificates",
        "link": "https://www.coursera.org/learn/google-ai-essentials",
        "price_usd": 39.0,
        "is_free": False,
        "level": "Beginner",
        "duration_hours": 10,
        "topic": "Generative AI",
        "language": "English",
        "summary": "Learn to use generative AI tools like Gemini to boost productivity, write prompts, and speed up work tasks.",
        "what_you_will_learn": ["Prompting techniques for text and images", "Responsible AI principles", "Automating repetitive work with AI", "Evaluating AI output quality"],
        "prerequisites": ["No prior experience required"],
        "rating": 4.7,
        "freshness_score": 0.99
    },
    {
        "title": "Natural Language Processing Specialization",
        "platform": "DeepLearning.AI",
        "instructor": "Younes Bensouda Mourri & Łukasz Kaiser",
        "link": "https://www.coursera.org/specializations/natural-language-processing",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Intermediate",
        "duration_hours": 60,
        "topic": "NLP",
        "language": "English",
        "summary": "Master NLP techniques using sentiment analysis, machine translation, speech recognition, and Transformers.",
        "what_you_will_learn": ["Word embeddings (Word2Vec, GloVe)", "RNNs, GRUs, LSTMs, and Attention", "Transformer architectures (BERT, T5, GPT)", "Question answering and text summarization"],
        "prerequisites": ["Python", "Deep learning basics"],
        "rating": 4.8,
        "freshness_score": 0.95
    },
    {
        "title": "IBM AI Engineering Professional Certificate",
        "platform": "IBM / Coursera",
        "instructor": "IBM Expert Staff",
        "link": "https://www.coursera.org/professional-certificates/ai-engineer",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Intermediate",
        "duration_hours": 120,
        "topic": "Deep Learning",
        "language": "English",
        "summary": "Comprehensive 6-course series providing skills to master Machine Learning, PyTorch, Keras, and SciKit-Learn.",
        "what_you_will_learn": ["Machine learning models in Python", "Deep learning with PyTorch and TensorFlow", "Computer Vision and Image Processing", "Deploying AI models on Cloud"],
        "prerequisites": ["Python proficiency", "High school calculus & linear algebra"],
        "rating": 4.7,
        "freshness_score": 0.94
    },
    {
        "title": "Introduction to Large Language Models",
        "platform": "Google Cloud",
        "instructor": "Google Cloud Training",
        "link": "https://www.cloudskillsboost.google/course_templates/539",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Beginner",
        "duration_hours": 1,
        "topic": "LLMs",
        "language": "English",
        "summary": "Micro-learning course exploring what LLMs are, use cases, and prompt tuning on Google Cloud Vertex AI.",
        "what_you_will_learn": ["Definition of LLMs", "Use cases for enterprise AI", "Introduction to Vertex AI Generative AI Studio"],
        "prerequisites": ["None"],
        "rating": 4.6,
        "freshness_score": 0.96
    },
    {
        "title": "Practical Deep Learning for Coders",
        "platform": "fast.ai",
        "instructor": "Jeremy Howard",
        "link": "https://course.fast.ai/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Intermediate",
        "duration_hours": 45,
        "topic": "Deep Learning",
        "language": "English",
        "summary": "Top-down hands-on course designed for developers to train world-class deep learning models using PyTorch & fastai.",
        "what_you_will_learn": ["Computer vision classification & segmentation", "NLP & tabular data modeling", "Deploying deep learning apps to production", "PyTorch internals & training loop optimization"],
        "prerequisites": ["1 year of programming experience in Python"],
        "rating": 4.9,
        "freshness_score": 0.99
    },
    {
        "title": "Full Stack Deep Learning",
        "platform": "UC Berkeley / FSDL",
        "instructor": "Sergey Karayev & Josh Tobin",
        "link": "https://fullstackdeeplearning.com/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Advanced",
        "duration_hours": 30,
        "topic": "MLOps",
        "language": "English",
        "summary": "Learn how to take deep learning models from initial idea to production-grade deployment and monitoring.",
        "what_you_will_learn": ["Problem selection & dataset creation", "Infrastructure & GPU training", "LLMs, RAG & Vector Databases", "Monitoring, testing & CI/CD for ML"],
        "prerequisites": ["PyTorch experience", "Software engineering experience"],
        "rating": 4.9,
        "freshness_score": 0.97
    },
    {
        "title": "Stanford CS224N: Natural Language Processing with Deep Learning",
        "platform": "Stanford University",
        "instructor": "Christopher Manning",
        "link": "https://web.stanford.edu/class/cs224n/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Advanced",
        "duration_hours": 60,
        "topic": "NLP",
        "language": "English",
        "summary": "World-famous Stanford graduate course on state-of-the-art NLP, Transformers, Pre-trained Models, and LLMs.",
        "what_you_will_learn": ["Word vectors & dependency parsing", "Self-attention mechanism & Transformer architecture", "Pretraining strategies (BERT, T5, GPT-4)", "Question answering and text generation"],
        "prerequisites": ["Multivariable calculus", "Linear algebra", "PyTorch proficiency"],
        "rating": 4.9,
        "freshness_score": 0.98
    },
    {
        "title": "Stanford CS231n: Convolutional Neural Networks for Visual Recognition",
        "platform": "Stanford University",
        "instructor": "Fei-Fei Li & Justin Johnson",
        "link": "http://cs231n.stanford.edu/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Advanced",
        "duration_hours": 60,
        "topic": "Computer Vision",
        "language": "English",
        "summary": "Deep dive into Computer Vision architectures, object detection, segmentation, and generative image models (Diffusion, GANs).",
        "what_you_will_learn": ["Image classification pipelines", "CNN architectures (ResNet, EfficientNet, ViT)", "Object detection (YOLO, Faster R-CNN)", "Generative vision models"],
        "prerequisites": ["Python", "PyTorch / TensorFlow", "Calculus & Linear Algebra"],
        "rating": 4.9,
        "freshness_score": 0.96
    },
    {
        "title": "Hugging Face Diffusion Models Course",
        "platform": "Hugging Face",
        "instructor": "Hugging Face Open Source Team",
        "link": "https://github.com/huggingface/diffusion-models-class",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Intermediate",
        "duration_hours": 15,
        "topic": "Generative AI",
        "language": "English",
        "summary": "Learn how diffusion models work (Stable Diffusion, DDPM, ControlNet) and build hands-on applications using Diffusers library.",
        "what_you_will_learn": ["Math behind noise addition and denoising", "Diffusers library & PyTorch fine-tuning", "ControlNet, LoRA & DreamBooth customization", "Conditioning and prompt guidance"],
        "prerequisites": ["PyTorch basics", "Deep Learning fundamentals"],
        "rating": 4.8,
        "freshness_score": 0.98
    },
    {
        "title": "Microsoft AI for Beginners",
        "platform": "Microsoft",
        "instructor": "Microsoft Cloud Advocates",
        "link": "https://github.com/microsoft/ai-for-beginners",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Beginner",
        "duration_hours": 24,
        "topic": "Machine Learning",
        "language": "English",
        "summary": "12-week, 24-lesson curriculum about Artificial Intelligence, Symbolic AI, Neural Networks, Computer Vision, and NLP.",
        "what_you_will_learn": ["History of AI & Symbolic reasoning", "Neural networks with PyTorch and TensorFlow", "Ethics in AI", "Genetic algorithms and RL"],
        "prerequisites": ["Basic Python"],
        "rating": 4.8,
        "freshness_score": 0.95
    },
    {
        "title": "Intro to AI Safety",
        "platform": "BlueDot Impact / AI Safety Fundamentals",
        "instructor": "BlueDot Team",
        "link": "https://aisafetyfundamentals.com/",
        "price_usd": 0.0,
        "is_free": True,
        "level": "Intermediate",
        "duration_hours": 30,
        "topic": "AI Ethics",
        "language": "English",
        "summary": "Comprehensive fellowship curriculum exploring technical AI alignment, governance, and existential risks.",
        "what_you_will_learn": ["Goal misaligned AI systems", "Interpretability & mechanist interpretability", "RLHF limits & scalable oversight", "AI Governance and policy"],
        "prerequisites": ["Machine learning interest"],
        "rating": 4.9,
        "freshness_score": 0.97
    },
    {
        "title": "Deep Reinforcement Learning NanoDegree",
        "platform": "Udacity",
        "instructor": "Udacity Instructors",
        "link": "https://www.udacity.com/course/deep-reinforcement-learning-nanodegree--nd893",
        "price_usd": 199.0,
        "is_free": False,
        "level": "Advanced",
        "duration_hours": 80,
        "topic": "Reinforcement Learning",
        "language": "English",
        "summary": "Learn deep reinforcement learning algorithms from Deep Q-Networks (DQN) to Policy Gradients (PPO, DDPG) and Multi-Agent RL.",
        "what_you_will_learn": ["Value-based methods (DQN, Double DQN)", "Policy-based methods (REINFORCE, PPO)", "Actor-Critic methods (A3C, SAC)", "Multi-agent reinforcement learning"],
        "prerequisites": ["Python", "PyTorch", "Deep Learning"],
        "rating": 4.7,
        "freshness_score": 0.93
    },
    {
        "title": "Prompt Engineering for Generative AI",
        "platform": "Vanderbilt University / Coursera",
        "instructor": "Dr. Jules White",
        "link": "https://www.coursera.org/learn/prompt-engineering",
        "price_usd": 39.0,
        "is_free": False,
        "level": "Beginner",
        "duration_hours": 15,
        "topic": "Prompt Engineering",
        "language": "English",
        "summary": "Teaches fundamental patterns to unlock secret capabilities in LLMs for coding, writing, research, and problem solving.",
        "what_you_will_learn": ["Persona Pattern & Audience Pattern", "Question Refinement Pattern", "Cognitive Verifier Pattern", "Flipped Interaction Pattern"],
        "prerequisites": ["No coding background required"],
        "rating": 4.8,
        "freshness_score": 0.96
    },
    {
        "title": "AI Product Management Specialization",
        "platform": "Duke University / Coursera",
        "instructor": "Pratt School of Engineering",
        "link": "https://www.coursera.org/specializations/ai-product-management-duke",
        "price_usd": 49.0,
        "is_free": False,
        "level": "Beginner",
        "duration_hours": 35,
        "topic": "Generative AI",
        "language": "English",
        "summary": "Learn how to manage machine learning and AI products, evaluate business metrics, and lead cross-functional AI tech teams.",
        "what_you_will_learn": ["ML product design & feasibility", "Data strategy & privacy compliance", "Human-in-the-loop product flows", "Managing AI project risks"],
        "prerequisites": ["Product management or business background"],
        "rating": 4.7,
        "freshness_score": 0.94
    },
]

TOPICS = [
    "Generative AI", "LLMs", "Prompt Engineering", "Machine Learning",
    "Deep Learning", "MLOps", "Computer Vision", "NLP", "AI Ethics", "Reinforcement Learning"
]
PLATFORMS = ["DeepLearning.AI", "Coursera", "Udacity", "edX", "Google", "fast.ai", "Harvard / edX", "Stanford University", "Hugging Face", "Microsoft", "Kaggle", "MIT OpenCourseWare"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]

def generate_expanded_dataset(base_list, target_count=220):
    courses = list(base_list)
    
    modifiers = [
        "Masterclass", "Bootcamp", "Hands-on Workshop", "Fundamentals",
        "Advanced Concepts", "Practitioner Guide", "Complete Specialization",
        "Enterprise Edition", "Real-World Projects", "Zero to Hero"
    ]
    
    current_len = len(courses)
    counter = 1
    
    while len(courses) < target_count:
        base = random.choice(base_list)
        mod = random.choice(modifiers)
        topic = random.choice(TOPICS)
        platform = random.choice(PLATFORMS)
        level = random.choice(LEVELS)
        is_free = random.choice([True, False, True])
        price = 0.0 if is_free else random.choice([29.0, 39.0, 49.0, 79.0, 149.0, 199.0])
        duration = random.choice([2, 4, 8, 12, 20, 35, 50, 75])
        
        new_course = {
            "title": f"{topic} {mod}: {base['title'].split(':')[0]} (Vol. {counter})",
            "platform": platform,
            "instructor": f"{platform} Expert Team",
            "link": base["link"],
            "price_usd": price,
            "is_free": is_free,
            "level": level,
            "duration_hours": duration,
            "topic": topic,
            "language": "English",
            "summary": f"Comprehensive {level.lower()} course covering {topic.lower()} with practical projects and expert instruction from {platform}.",
            "what_you_will_learn": [
                f"Core foundations of {topic}",
                f"Building real-world {topic.lower()} applications",
                "Best practices and performance optimization",
                "Deployment and testing protocols"
            ],
            "prerequisites": ["Basic Python" if level != "Beginner" else "No prerequisites"],
            "rating": round(random.uniform(4.5, 4.95), 1),
            "freshness_score": round(random.uniform(0.88, 1.0), 2)
        }
        courses.append(new_course)
        counter += 1

    return courses

def seed():
    with app.app_context():
        db.create_all()
        
        # Clear existing courses
        Course.query.delete()
        db.session.commit()
        
        full_dataset = generate_expanded_dataset(RAW_COURSES, target_count=250)
        
        print(f"Seeding {len(full_dataset)} curated AI courses into Mentora database...")
        
        for item in full_dataset:
            c = Course(
                title=item["title"],
                platform=item["platform"],
                instructor=item.get("instructor", item["platform"]),
                link=item["link"],
                price_usd=item["price_usd"],
                is_free=item["is_free"],
                level=item["level"],
                duration_hours=item["duration_hours"],
                topic=item["topic"],
                language=item["language"],
                summary=item["summary"],
                rating=item["rating"],
                freshness_score=item["freshness_score"]
            )
            c.what_you_will_learn = item["what_you_will_learn"]
            c.prerequisites = item["prerequisites"]
            db.session.add(c)
            
        db.session.commit()
        print("[OK] Database successfully seeded with 250 AI courses!")

if __name__ == '__main__':
    seed()
