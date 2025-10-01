

from .models import *
from datetime import date
import requests














def generate_mcqs(language,difficulty,topics,source):
        mcqs = [
        {
            "id": 1,
            "category": "data types, variables, arrays, operators, control structures, functions",
            "text": "Which of the following is NOT a valid Java access modifier?",
            "options": [
                { "id": "A", "text": "public" },
                { "id": "B", "text": "protected" },
                { "id": "C", "text": "internal" },
                { "id": "D", "text": "private" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 2,
            "category": "JavaScript Concepts",
            "text": "What does the 'this' keyword refer to in JavaScript?",
            "options": [
                { "id": "A", "text": "The function itself" },
                { "id": "B", "text": "The window object" },
                { "id": "C", "text": "The object that the function belongs to" },
                { "id": "D", "text": "The parent object of the function" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 3,
            "category": "Python Syntax",
            "text": "Which of the following is used to create a virtual environment in Python?",
            "options": [
                { "id": "A", "text": "venv" },
                { "id": "B", "text": "pipenv" },
                { "id": "C", "text": "virtualenv" },
                { "id": "D", "text": "All of the above" }
            ],
            "correctAnswer": "D"
        },
        {
            "id": 4,
            "category": "Database Concepts",
            "text": "Which SQL clause is used to filter the results of a query?",
            "options": [
                { "id": "A", "text": "GROUP BY" },
                { "id": "B", "text": "ORDER BY" },
                { "id": "C", "text": "WHERE" },
                { "id": "D", "text": "HAVING" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 5,
            "category": "Data Structures",
            "text": "Which data structure uses a LIFO (Last-In-First-Out) approach?",
            "options": [
                { "id": "A", "text": "Queue" },
                { "id": "B", "text": "Stack" },
                { "id": "C", "text": "Linked List" },
                { "id": "D", "text": "Tree" }
            ],
            "correctAnswer": "B"
        },
        {
            "id": 6,
            "category": "Web Development",
            "text": "What does CSS stand for?",
            "options": [
                { "id": "A", "text": "Computer Style Sheets" },
                { "id": "B", "text": "Creative Style System" },
                { "id": "C", "text": "Cascading Style Sheets" },
                { "id": "D", "text": "Colorful Style Sheets" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 7,
            "category": "Algorithms",
            "text": "Which algorithm is used to find the shortest path between two nodes?",
            "options": [
                { "id": "A", "text": "Bubble Sort" },
                { "id": "B", "text": "Dijkstra's Algorithm" },
                { "id": "C", "text": "Binary Search" },
                { "id": "D", "text": "Quick Sort" }
            ],
            "correctAnswer": "B"
        },
        {
            "id": 8,
            "category": "Object-Oriented Programming",
            "text": "Which OOP concept allows one class to inherit properties and methods from another?",
            "options": [
                { "id": "A", "text": "Encapsulation" },
                { "id": "B", "text": "Abstraction" },
                { "id": "C", "text": "Inheritance" },
                { "id": "D", "text": "Polymorphism" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 9,
            "category": "Operating Systems",
            "text": "What is the main purpose of an operating system?",
            "options": [
                { "id": "A", "text": "To manage computer hardware resources" },
                { "id": "B", "text": "To provide a user interface" },
                { "id": "C", "text": "To execute and provide services for applications" },
                { "id": "D", "text": "All of the above" }
            ],
            "correctAnswer": "D"
        },
        {
            "id": 10,
            "category": "Networking",
            "text": "What protocol is used to transfer web pages over the internet?",
            "options": [
                { "id": "A", "text": "FTP" },
                { "id": "B", "text": "HTTP" },
                { "id": "C", "text": "SMTP" },
                { "id": "D", "text": "TCP" }
            ],
            "correctAnswer": "B"
        },
        {
            "id": 11,
            "category": "Cloud Computing",
            "text": "Which service model provides virtual machines to users?",
            "options": [
                { "id": "A", "text": "SaaS (Software as a Service)" },
                { "id": "B", "text": "PaaS (Platform as a Service)" },
                { "id": "C", "text": "IaaS (Infrastructure as a Service)" },
                { "id": "D", "text": "FaaS (Function as a Service)" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 12,
            "category": "Security",
            "text": "What type of attack involves tricking users into revealing sensitive information?",
            "options": [
                { "id": "A", "text": "DDoS" },
                { "id": "B", "text": "Phishing" },
                { "id": "C", "text": "Brute Force" },
                { "id": "D", "text": "SQL Injection" }
            ],
            "correctAnswer": "B"
        },
        {
            "id": 13,
            "category": "Version Control",
            "text": "Which command is used to create a new branch in Git?",
            "options": [
                { "id": "A", "text": "git branch <branch-name>" },
                { "id": "B", "text": "git create <branch-name>" },
                { "id": "C", "text": "git new <branch-name>" },
                { "id": "D", "text": "git checkout -b <branch-name>" }
            ],
            "correctAnswer": "A"
        }
        ,
        {
            "id": 14,
            "category": "Mobile Development",
            "text": "Which programming language is primarily used for iOS development?",
            "options": [
                { "id": "A", "text": "Java" },
                { "id": "B", "text": "Kotlin" },
                { "id": "C", "text": "Swift" },
                { "id": "D", "text": "Objective-C" }
            ],
            "correctAnswer": "C"
        },
        {
            "id": 15,
            "category": "Machine Learning",
            "text": "What is the process of converting categorical data into numerical data called?",
            "options": [
                { "id": "A", "text": "Normalization" },
                { "id": "B", "text": "Standardization" },
                { "id": "C", "text": "Encoding" },
                { "id": "D", "text": "Feature Scaling" }
            ],
            "correctAnswer": "C"
        }
    ];


        return mcqs


def evaluate_mcqs(mcqs):
      mcqs = mcqs

      result = {
            "strong_areas" : "OOP, Algorithms",
            "improvement_areas" : "Data Structures, System Design"
      }

      return result



def generate_coding_questions(langauge,difficulty):
      language = langauge
      difficulty = difficulty
      questions = [
        {
            "title": "Two Sum Problem",
            "description": "Given an array of integers and a target, find two numbers that add up to the target.",
            "tags": ["Arrays", "Hash Map", "Algorithms"],
            "constraints": [
                "2 ≤ nums.length ≤ 10⁴",
                "-10⁹ ≤ nums[i] ≤ 10⁹",
                "-10⁹ ≤ target ≤ 10⁹",
                "Only one valid answer exists"
            ],
            "example": ""
        },
        {
            "title": "Reverse Linked List",
            "description": "Reverse a singly linked list in-place.",
            "tags": ["Linked List", "Pointers"],
            "constraints": [
                "The number of nodes in the list is in the range [0, 5000]",
                "-5000 ≤ Node.val ≤ 5000"
            ],
            "example": "Input: 1->2->3->4->5\nOutput: 5->4->3->2->1"
        },
        {
            "title": "Binary Tree Inorder Traversal",
            "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
            "tags": ["Binary Tree", "Recursion", "Stack"],
            "constraints": [
                "The number of nodes in the tree is in the range [0, 100]",
                "-100 ≤ Node.val ≤ 100"
            ],
            "example": "Input: [1,null,2,3]\nOutput: [1,3,2]"
        }
    ]
      
      return questions
      
      
def process_coding_answers(responses):
    responses = responses

      
    result = {
                "total_testcases" : 30,
                "test_cases_passed" : 20,
                "code_quality" : 90,
                "best_solution" : "two sum Problem",
                "optimization_needed" : "binary tree traversal"
            }
    
    return result
      


def process_confidence_data(data):
    # do your manipulation here
    result = {
        "overallConfidence" : 80,
        "eye_contact" : 85,
        "voice_clarity" : 72,
        "facialExpressions" : 85,
        "strengths" : "Clear articulation, Good posture",
        "suggestions" : "Improve eye contact consistency"
    }
    return result


def evaluate_overall_performance():
      
    overall_performance = {
         "score" : 86,
         "description" : "this is the description",
         "technical_knowledge" : 80,
         "problem_solving"  : 70
         

    }

    return overall_performance



def save_interview_report(candidate_id, reportData):
    try:
        user = User.objects.get(id=candidate_id, user_type="candidate")

        report = InterviewReport.objects.create(
            user=user,
            
            # Basic info
            date=reportData["interview_date"],
            duration_minutes=reportData["duration"],
            technology=reportData["technology"],
            difficulty=reportData["difficulty"],

            # Overall performance
            overall_score=reportData["overall_score"],
            performance_text=reportData["overall_description"],

            # Metrics
            technical_knowledge=reportData["technical_knowledge"],
            problem_solving=reportData["problem_solving"],
            code_quality=reportData["code_quality"],
            confidence=reportData["overall_confidence"],

            # MCQ test
            mcq_correct=reportData["correct_mcqs"],
            mcq_total=reportData["total_mcqs"],
            mcq_time_taken=reportData["mcqs_time_taken"],
            mcq_accuracy=reportData["mcqs_accuracy"],
            strong_areas=reportData["mcqs_strong_areas"],
            improvement_areas=reportData["mcqs_improvement_areas"],

            # Coding test
            coding_problems_solved=reportData["solved_questions"],
            coding_problems_total=reportData["total_coding_questions"],
            coding_test_cases_passed=reportData["test_cases_passed"],
            coding_test_cases_total=reportData["total_test_cases"],
            coding_avg_time_per_problem=reportData["average_time"],
            coding_code_quality=reportData["code_quality"],
            best_solution=reportData["best_solution"],
            optimization_needed=reportData["optimization_needed"],

            # Confidence assessment
            overall_confidence=reportData["overall_confidence"],
            eye_contact=reportData["eye_contact"],
            voice_clarity=reportData["voice_clarity"],
            facial_expressions=reportData["facial_expressions"],
            strengths=reportData["strengths"],
            suggestions=reportData["suggestions"]
        )

        return report.report_id
        

    except User.DoesNotExist:
         return False

def save_log(title, description, userId):
    try:
        user = User.objects.get(id=userId)

        log = SystemLog.objects.create(
            user=user,
            title=title,
            description=description
        )

        return True

    except User.DoesNotExist:
         return False
    

def mcq_exists(questions,code):
    # for q in questions:
    #     if q.id == code:
    #         return True
    return False


def add_mcq(mcq_data):
    if(mcq_exists(mcq_data["question"],mcq_data.get("code_part"))):
        return False

    try:

        mcq = MCQ.objects.create(
        question=mcq_data["question"],
        code_part=mcq_data.get("code_part"),
        option_a=mcq_data["option_a"],
        option_b=mcq_data["option_b"],
        option_c=mcq_data["option_c"],
        option_d=mcq_data["option_d"],
        answer=mcq_data["answer"],
        domain=mcq_data.get("domain"),
        difficulty=mcq_data.get("difficulty"),
        topics=mcq_data.get("topics")
    )
        return True
    except Exception as e:
        print(f"Error adding MCQ: {e}")
        return False
    




def get_prompt(language, topics, difficulty,num_mcqs):
    payload = {
        "language": language,
        "topics": topics,
        "difficulty": difficulty,
        "num_return_sequences": 1,
        "num_mcqs": num_mcqs
    }
    response = requests.post("http://127.0.0.1:8001/generate", json=payload)
    return response.json()["prompt"]
