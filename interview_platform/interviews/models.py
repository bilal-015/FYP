
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class Candidates(models.Model):
    
#     cid = models.AutoField(primary_key=True)  # Auto-incrementing candidate ID
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15)
#     password = models.CharField(max_length=128)  # Store hashed password
#     degree = models.CharField(max_length=100)
#     job_domain = models.CharField(max_length=100)
#     experience = models.PositiveIntegerField(help_text="Experience in years")
#     image = models.ImageField(
#         upload_to='candidate_images/',
#         null=True,
#         blank=True,
#         default='candidate_images/default_profile.png'
#     )
    
#     def __str__(self):
#         return f"{self.full_name}"



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type="candidate", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, user_type="admin", **extra_fields)


class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ("admin", "Admin"),
        ("candidate", "Candidate"),
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="candidate")
    created_at = models.DateTimeField(auto_now_add=True)

    # Required by Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.user_type})"


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    degree = models.CharField(max_length=100)
    job_domain = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to="candidate_images/",
        default="candidate_images/default_profile.png",
    )

    def __str__(self):
        return self.full_name


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile")
    full_name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="candidate_images/",
        default="candidate_images/default_profile.png",
    )

    def __str__(self):
        return self.full_name


    

class SystemLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    

class InterviewReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")

    # Basic info
    date = models.DateField()
    duration_minutes = models.CharField(max_length=20)
    technology = models.CharField(max_length=100)  
    difficulty = models.CharField(max_length=50)   

    # Overall performance
    overall_score = models.PositiveIntegerField()
    performance_text = models.TextField()

    # Metrics
    technical_knowledge = models.PositiveIntegerField()
    problem_solving = models.PositiveIntegerField()
    code_quality = models.PositiveIntegerField()
    confidence = models.PositiveIntegerField()

    # MCQ test
    mcq_correct = models.PositiveIntegerField()
    mcq_total = models.PositiveIntegerField()
    mcq_time_taken = models.CharField(max_length=20)
    mcq_accuracy = models.PositiveIntegerField()
    strong_areas = models.CharField(max_length=255)
    improvement_areas = models.CharField(max_length=255)

    # Coding test
    coding_problems_solved = models.PositiveIntegerField()
    coding_problems_total = models.PositiveIntegerField()
    coding_test_cases_passed = models.PositiveIntegerField()
    coding_test_cases_total = models.PositiveIntegerField()
    coding_avg_time_per_problem = models.CharField(max_length=20)
    coding_code_quality = models.PositiveIntegerField()
    best_solution = models.CharField(max_length=255)
    optimization_needed = models.CharField(max_length=255)

    # Confidence assessment
    overall_confidence = models.PositiveIntegerField()
    eye_contact = models.PositiveIntegerField()
    voice_clarity = models.PositiveIntegerField()
    facial_expressions = models.PositiveIntegerField()
    strengths = models.CharField(max_length=255)
    suggestions = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Safely show candidate full name if available
        if hasattr(self.user, "candidate_profile"):
            return f"Report {self.report_id} - {self.user.candidate_profile.full_name} ({self.date})"
        return f"Report {self.report_id} - {self.user.email} ({self.date})"




class MCQ(models.Model):
    q_no = models.AutoField(primary_key=True)  # Auto-incremented ID for each question
    question = models.TextField()
    code_part = models.TextField(blank=True, null=True)

    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()

    # Store correct answer as a single character (a, b, c, d)
    answer = models.CharField(max_length=1, choices=[
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D'),
    ])

    # New fields from CSV
    difficulty = models.CharField(
    max_length=20,
    choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ],
    blank=True,
    null=True
    )
    topics = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"Q{self.q_no}: {self.question[:50]}..."
