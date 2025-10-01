import csv
import os
import django

# --- Setup Django environment ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interview_platform.settings')
django.setup()

from interviews.models import MCQ


def import_mcqs_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Reads header from CSV automatically
        for row in reader:
            mcq, created = MCQ.objects.update_or_create(
                question=row['Question'],  # match by question text
                defaults={
                    "code_part": row['Code_Part'] if row['Code_Part'] else None,
                    "option_a": row['Option_A'],
                    "option_b": row['Option_B'],
                    "option_c": row['Option_C'],
                    "option_d": row['Option_D'],
                    "answer": row['Answer'].lower() if row['Answer'] else "a",
                    "difficulty": row['Difficulty'].lower() if row['Difficulty'] else "easy",
                    "topics": row['Topics'].lower() if row['Topics'] else "general",
                }
            )
            if created:
                print(f"✅ Added: {row['Question'][:50]}...")
            else:
                print(f"🔄 Updated: {row['Question'][:50]}...")

    print("🎉 Import finished!")


if __name__ == "__main__":
    import_mcqs_from_csv("mcqs.csv")  # <-- put your CSV file name here
