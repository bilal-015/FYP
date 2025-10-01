import requests

payload = {
    "language": "Cyber Security",
    "topics": [
        "Application Layer",
        "Basics of Networking",
        "Information Networks and Technology Review",
        "Cyber Security",
        "Phases of Security",
        "Understanding Attack Vectors",
        "Understanding Network Models for Securit",
        "Introduction to Ethical Hacking",
        "Security Tools",
        "Bugs and Vulnerabilities"
    ],
    "difficulty": "hard",
    "num_return_sequences": 1
}

res = requests.post("http://127.0.0.1:8001/generate", json=payload)
print(res.json())
