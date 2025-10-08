from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
import json
from datetime import date
import pandas as pd
from django.db.models import Avg, Count,Max, Min
from django.core.mail import send_mail
from .models import *
from .util import *
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.utils import timezone
from .utils.scraping_script import MCQScraper
import pandas as pd




@csrf_exempt
def send_email_verification(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            code = data.get("code")

            send_mail(
                subject="Your Email Verification Code",
                message=f"Your  email verification code is: {code}",
                from_email="interviewaiplatform@gmail.com",   
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})








@csrf_exempt
def register_candidate(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        degree = request.POST.get('degree')
        job_domain = request.POST.get('job_domain')
        experience = request.POST.get('experience')
        password = request.POST.get('password')
        image = request.FILES.get('profileImage')

        if not all([full_name, email, phone, degree, job_domain, experience, password]):
            return JsonResponse({'success': False, 'message': 'Missing required fields.'})

        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already registered.'})

        
        user = User.objects.create(
            email=email,
            password=make_password(password),
            user_type="candidate",
        )

       
        CandidateProfile.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            degree=degree,
            job_domain=job_domain,
            experience=int(experience),
            image=image if image else 'candidate_images/default_profile.png'
        )

        return JsonResponse({'success': True, 'message': 'Candidate registered successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




# This is the view to handle candidate login

def candidateLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            # if check_password(password,candidate.password):
            if(check_password(password, user.password)):

                if(user.user_type == "candidate"):
                    # Login successful
                    candidate = CandidateProfile.objects.get(user=user)
                    request.session["candidate_id"] = user.id
                    request.session["candidate_name"] = candidate.full_name
                    request.session["candidate_email"] = user.email  
                    request.session["candidate_phone"] = candidate.phone  
                    request.session["candidate_degree"] = candidate.degree  
                    request.session["candidate_job_domain"] = candidate.job_domain  
                    request.session["candidate_experience"] = candidate.experience  
                    request.session["candidate_image"] = candidate.image.url  
                    request.session["interview_Completed"] = False


                    messages.success(request, "Login successful!")
                    save_log("logged in", f"{candidate.full_name} logged in.", user.id)
                    return redirect("dashboard")
                elif(user.user_type == "admin"):
                    admin = AdminProfile.objects.get(user=user)

                    request.session["admin_id"] = user.id
                    request.session["admin_email"] = user.email
                    request.session["admin_full_name"] =admin.full_name
                    request.session["admin_image"] =admin.image.url
                    messages.success(request, "Login successful!")
                    
                    return redirect("admin_dashboard")  

            else:
                messages.error(request, "Incorrect password.")
                return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect("login")
    return redirect("login")




def logout_view(request):
    logout(request)  # ends the session & logs out
    return redirect('login')


@require_POST
def update_profile(request):
    try:
        data = json.loads(request.body)
        

        # Find the candidate by email stored in session
        candidate_email = request.session.get('candidate_email')
        
        if not candidate_email:
            return JsonResponse({"error": "Not logged in"}, status=401)

        try:
            
            user = User.objects.get(email=candidate_email)
        except User.DoesNotExist:
            return JsonResponse({"error": "Candidate not found"}, status=404)

        
        candidate = CandidateProfile.objects.get(user=user)
        
        # Update the database
        candidate.full_name = data['fullName']
        candidate.phone = data['phone']
        candidate.degree = data['degree']
        candidate.experience = int(data['experience'])
        candidate.job_domain = data['jobDomain']
        candidate.save()

        
        # Update the session too
        request.session['candidate_name'] = candidate.full_name
        request.session['candidate_phone'] = candidate.phone
        request.session['candidate_degree'] = candidate.degree
        request.session['candidate_experience'] = candidate.experience
        request.session['candidate_job_domain'] = candidate.job_domain
        

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# view for to upload the new profile photo

@require_POST
def update_profile_image(request):
    profile_image = request.FILES.get('image')

    if not profile_image:
        return JsonResponse({'error': 'No image provided'}, status=400)

    candidate_email = request.session.get('candidate_email')
    if not candidate_email:
        return JsonResponse({'error': 'Not logged in'}, status=403)

    try:
        user = User.objects.get(email=candidate_email)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Candidate not found'}, status=404)
    candidate = CandidateProfile.objects.get(user=user)
    candidate.image = profile_image
    candidate.save()

    request.session['candidate_image'] = candidate.image.url

    return JsonResponse({
        'message': 'Profile image updated successfully',
        'image_url': candidate.image.url
    })



def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')


def get_all_emails(request):
    emails = list(User.objects.values_list('email', flat=True))
    return JsonResponse({'emails': emails})

def forgot_password(request):
    return render(request, 'forgot_password.html')


def send_verification_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            code = data.get("code")

            send_mail(
                subject="Your Verification Code",
                message=f"Your verification code is: {code}",
                from_email="interviewaiplatform@gmail.com",   
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})



@csrf_exempt
def set_new_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_password = data.get("password")
            email = data.get("email")

            if not new_password or not email:
                return JsonResponse({"success": False, "error": "Email and password are required"})

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"success": False, "error": "Email not found"})
            
            user.password = make_password(new_password)
            user.save()

            return JsonResponse({"success": True, "message": "Password updated successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method"})


@never_cache
def dashboard(request):
    
    recent_activities = [["Completed Technical Interview", "Software Engineering - Advanced Level", "2 hours ago"],
                       ["Generated Interview Report", "View your performance analysis and feedback", "1 day ago"],
                       ["Updated Profile", "Changed preferred interview domains", "3 days ago"]]
    
    # Get the candidate
    user = User.objects.get(id=request.session["candidate_id"], user_type="candidate")

    # Query all reports for this candidate
    reports = InterviewReport.objects.filter(user=user)

    # Count of interviews
    interview_count = reports.count()

    # Average overall score
    avg_overall_score = reports.aggregate(avg_score=Avg("overall_score"))["avg_score"] or 0



    average_score = int(avg_overall_score)
    total_interviews = interview_count

    interview_info = {
        "average_score": average_score,
        "total_interviews": total_interviews,
        }
    
    params = {
        "interview_info": interview_info,
        "recent_activities": recent_activities
        }
    
    request.session["interview_Completed"] = True
    request.session.modified = True


    return render(request, 'dashboard.html', params)

def profile(request):

    # Get the candidate
    user = User.objects.get(id=request.session["candidate_id"], user_type="candidate")

    # Query all reports for this candidate
    reports = InterviewReport.objects.filter(user = user)

    # Count of interviews
    interview_count = reports.count()

    # Average overall score
    avg_overall_score = reports.aggregate(avg_score=Avg("overall_score"))["avg_score"] or 0




    no_of_interviews = interview_count
    average_score = int(avg_overall_score)

    params = {
        "no_of_interviews": no_of_interviews,
        "average_score": average_score
    }
    
    return render(request, 'profile.html',params)  


def interview_reports(request):
    request.session["interview_Completed"] = False
    request.session.modified = True
    user = User.objects.get(id=request.session["candidate_id"], user_type="candidate")
    reports = InterviewReport.objects.filter(user=user).order_by("-date").values(
    "report_id", "date", "technology", "difficulty", "overall_score"
)


    # Convert queryset into list of dicts
    params = list(reports)

    return render(request, 'interview_reports.html',{"reports": params})

def interview_setup(request):
    request.session["interview_Completed"] = False
    request.session.modified = True
    return render(request, 'interview_setup.html')


def store_interview_setup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        language = data.get("language").capitalize()
        difficulty = data.get("difficulty").capitalize()

        request.session["language"] = language
        request.session["difficulty_level"] = difficulty
        request.session["topics"] = data.get("topics")
        request.session["mcqs_source"] = data.get("source")

        


        return redirect("mcqs_page")


def get_mcqs(request):
    
    mcqs = generate_mcqs(request.session["language"],request.session["difficulty_level"],request.session["topics"],request.session["mcqs_source"])
    return JsonResponse(mcqs, safe=False)

    



def mcqs_page(request):
    
    return render(request, 'mcqs_page.html')


@csrf_exempt  
def submit_mcqs(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Extract data
            answers = data.get('answers', [])
            time_taken = data.get('time_taken')
            correct_count = data.get('correct_count')
            incorrect_count = data.get('incorrect_count')
            percentage = data.get('percentage')
            score = data.get('score')
            total_questions = data.get('total_questions')
            
            
            # # Example: Save each answer
            # for answer in answers:
            #     question_id = answer.get('question_id')
            #     selected = answer.get('selected_answer')
            #     correct = answer.get('correct_answer')
            #     is_correct = answer.get('is_correct')
                
               
            result = evaluate_mcqs(answers)


            request.session["mcqs_result"] = {
                "total_questions" : total_questions,
                "correct_answers" : correct_count,
                "incorrect_answers" : incorrect_count,
                "time_taken" : time_taken,
                "accuracy" : percentage,
                "strong_areas" : result["strong_areas"],
                "improvement_areas" : result["improvement_areas"]
            }

            
            return JsonResponse({
                'success': True,
                'message': 'Results saved successfully',
                'score': score,
                'percentage': percentage
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)



def get_coding_questions(request):

    questions = generate_coding_questions(request.session["language"],request.session["difficulty_level"])
    
    return JsonResponse(questions, safe=False)



def coding_page(request):
    return render(request, 'coding_page.html')


@csrf_exempt
def submit_coding_answers(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Process the data
            responses = data.get('responses', [])
            total_questions = data.get('total_questions')
            solved_count = data.get('solved_count')
            total_time = data.get('total_time')
            avg_time_per_problem = data.get('avg_time_per_problem')
            solved_percentage = data.get('solved_percentage')
            language = data.get('language')
            
            result = process_coding_answers(responses)


            


            request.session["coding_result"] = {
                "total_questions" : total_questions,
                "problems_solved" : solved_count,
                "total_testcases" : result["total_testcases"],
                "test_cases_passed" : result["test_cases_passed"],
                "average_time" : avg_time_per_problem,
                "total_time" : total_time,
                "code_quality" : result["code_quality"],
                "best_solution" : result["best_solution"],
                "optimization_needed" : result["optimization_needed"]
            }
            
            
            return JsonResponse({
                'success': True,
                'message': 'Coding responses saved successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)



def confidence_score_page(request):
    return render(request, 'confidence_score_page.html')

@csrf_exempt
def submit_confidence_assessment(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # assessment = data.get("assessment")

            result = process_confidence_data(data)

            time_taken = 200


            result["time_taken"] = time_taken  

            request.session["confidence_assessment_result"] = result


            request.session["overall_performance"] = evaluate_overall_performance()


            # total seconds from all parts
            totalseconds = (
                            int(request.session["mcqs_result"]["time_taken"])
                            + int(request.session["coding_result"]["total_time"])
                            + int(request.session["confidence_assessment_result"]["time_taken"])
                        )


            


            # convert to minutes and seconds
            minutes= int(totalseconds / 60)
            seconds = int(totalseconds % 60)

            duration = f"{minutes}:{seconds:02d}"

            mcqs_minutes = int(request.session["mcqs_result"]["time_taken"] / 60)
            mcqs_seconds = int(request.session["mcqs_result"]["time_taken"] % 60)

            mcqs_time = f"{mcqs_minutes}:{mcqs_seconds:02d}"

            avg_minutes = int(request.session["coding_result"]["average_time"] / 60)
            avg_seconds = int(request.session["coding_result"]["average_time"] % 60)

            avg_time = f"{avg_minutes}:{avg_seconds:02d}"



            today_date = date.today().strftime("%Y-%m-%d")
            if isinstance(today_date, str):
                today_date = date.fromisoformat(today_date)
        


            reportData = {
                "candidate_name" : request.session['candidate_name'],
                "interview_date" : today_date,
                "duration" :  duration,
                "technology" : request.session["language"],
                "difficulty" : request.session["difficulty_level"],

                "overall_score" : request.session["overall_performance"]["score"],
                "overall_description" : request.session["overall_performance"]["description"],
                "technical_knowledge" : request.session["overall_performance"]["technical_knowledge"],
                "problem_solving" : request.session["overall_performance"]["problem_solving"],
                "code_quality" : request.session["coding_result"]["code_quality"],
                "overall_confidence" : request.session["confidence_assessment_result"]["overallConfidence"],

                "total_mcqs" : request.session["mcqs_result"]["total_questions"],
                "correct_mcqs" : request.session["mcqs_result"]["correct_answers"],
                "mcqs_time_taken" : mcqs_time,
                "mcqs_accuracy" : request.session["mcqs_result"]["accuracy"],
                "mcqs_strong_areas" : request.session["mcqs_result"]["strong_areas"],
                "mcqs_improvement_areas" : request.session["mcqs_result"]["improvement_areas"],

                "total_coding_questions" : request.session["coding_result"]["total_questions"],
                "solved_questions" : request.session["coding_result"]["problems_solved"],
                "total_test_cases" : request.session["coding_result"]["total_testcases"],
                "test_cases_passed" : request.session["coding_result"]["test_cases_passed"],
                "average_time" : avg_time,
                "code_quality" : request.session["coding_result"]["code_quality"],
                "best_solution" : request.session["coding_result"]["best_solution"],
                "optimization_needed" : request.session["coding_result"]["optimization_needed"],
                
                "eye_contact" :  request.session["confidence_assessment_result"]["eye_contact"],
                "voice_clarity" :  request.session["confidence_assessment_result"]["voice_clarity"],
                "facial_expressions" :  request.session["confidence_assessment_result"]["facialExpressions"],
                "strengths" :  request.session["confidence_assessment_result"]["strengths"],
                "suggestions" :  request.session["confidence_assessment_result"]["suggestions"]
            }


            response = save_interview_report(request.session["candidate_id"], reportData)

            if(response == False):
               raise Exception("Something went wrong!")
            
            else:
                keys_to_clear = [
                                "language", "difficulty_level", "overall_performance", "coding_result",
                                "mcqs_result", "confidence_assessment_result"
                                ]

                for key in keys_to_clear:
                    if key in request.session:
                        del request.session[key]
                            
            
                           



            return JsonResponse({
                'success': True,
                'message': 'Confidence assessment responses saved successfully',
                'report_id' : response
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)


    


def interview_report(request, reportId):
    # Mark interview as completed in session
    request.session["interview_Completed"] = True
    request.session.modified = True

    # Fetch report from DB
    report = get_object_or_404(InterviewReport, report_id=reportId)


    # Convert model instance to dict (all fields)
    params = {
        field.name: getattr(report, field.name)
        for field in report._meta.fields
    }

    params["incorrect_mcqs"] = params["mcq_total"] - params["mcq_correct"]
    params["full_name"] = request.session.get("candidate_name")

    
    
    # Send to template
    return render(request, "new_report.html",params)







## -------------------------------ADMIN SITE---------------------------------

def admin_dashboard(request):

    admin_data = {"name": request.session["admin_full_name"],
                  "email": request.session["admin_email"],
                  "image": request.session["admin_image"]}
    
        # Get the candidate
    total_candidates = User.objects.filter(user_type="candidate").count()


    # Query all reports for this candidate
    interviews_count = InterviewReport.objects.count()

    logs = SystemLog.objects.count()

    # fetch recent 4 interviews (from all candidates)
    recent_reports = InterviewReport.objects.select_related("user__candidate_profile").order_by("-created_at")[:4]

    # now extract candidate details from these reports
    candidates_data = []
    for report in recent_reports:
        candidates_data.append({
            "name": report.user.candidate_profile.full_name,
            "image": report.user.candidate_profile.image.url,
            "date": report.date,
            "technology": report.technology,
            "score": report.overall_score
        })

    recent_logs = SystemLog.objects.all().order_by("-created_at")[:3]

    params = {
        "admin_data": admin_data,
        "total_candidates": total_candidates,
        "interviews_count": interviews_count,
        "logs": logs,
        "candidates_data": candidates_data,
        "recent_logs": recent_logs
    }





    return render(request, 'admin/dashboard.html',params)



def admin_get_candidates(request):
    candidates = CandidateProfile.objects.select_related("user").all()
    data = []
    for candidate in candidates:
        data.append({
            "id": candidate.user.id,
            "is_active": candidate.user.is_active,
            "name": candidate.full_name,
            "email": candidate.user.email,
            "phone": candidate.phone,
            "degree": candidate.degree,
            "domain": candidate.job_domain,
            "experience": candidate.experience,
            "image": candidate.image.url,
        })
    return JsonResponse(data, safe=False)


def candidates_management(request):
    return render(request, 'admin/candidates.html')

@csrf_exempt 
def delete_candidate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("id")

            user = User.objects.get(id=user_id)
            user.delete()

            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Candidate not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt 
def enable_candidate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("id")

            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Candidate not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt 
def disable_candidate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("id")

            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()

            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Candidate not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


def get_reports(request):
    reports = InterviewReport.objects.select_related("user__candidate_profile").order_by("-created_at")
    
    
    data = []
    for report in reports:
        data.append({
            "id": report.report_id,
            "candidate": report.user.candidate_profile.full_name,
            "date": report.date,
            "technology": report.technology,
            "difficulty": report.difficulty,
            "score": report.overall_score,
        })

    return JsonResponse(data, safe=False, status=200)

def reports_management(request):
    return render(request, 'admin/reports.html')

@csrf_exempt 
def delete_report(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            report_id = data.get("id")

            report = InterviewReport.objects.get(report_id=report_id)
            report.delete()

            return JsonResponse({"success": True})
        except InterviewReport.NotExist:
            return JsonResponse({"success": False, "error": "Report not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


def fetch_logs(request):
    print("Fetching logs...")
    logs = SystemLog.objects.select_related("user").order_by("-created_at")
    
    logs_data = []

    for log in logs:
        # Handle candidate/admin/system gracefully
        if hasattr(log.user, "candidate_profile"):
            candidate_name = log.user.candidate_profile.full_name
        elif hasattr(log.user, "admin_profile"):
            candidate_name = log.user.admin_profile.full_name
        local_time = timezone.localtime(log.created_at, timezone.get_fixed_timezone(300))
        logs_data.append({
            "id": log.log_id,
            "title": log.title,
            "candidate": candidate_name,
            "email": log.user.email,
            "description": log.description,
            "datetime": DateFormat(local_time).format("M. j, Y, P"),
        })
        print(logs_data[-1])

    return JsonResponse(logs_data, safe=False, status=200)



@csrf_exempt  
def store_log(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        user_id = request.POST.get("user_id")


        if title and description and user_id:
            save_log(title, description, user_id)
            return HttpResponse("Log saved")
        
    return HttpResponse("Invalid request")


def logs_management(request):
    return render(request, 'admin/logs.html')

def candidate_detail(request):

    user_id = request.GET.get("id")
    user = get_object_or_404(User, id=user_id)
    candidate = get_object_or_404(CandidateProfile, user=user)
    reports = InterviewReport.objects.filter(user=user).order_by("-created_at")
    logs = SystemLog.objects.filter(user=user).order_by("-created_at")

    # Fetch highest and lowest score for candidate
    report_stats = InterviewReport.objects.filter(user=user).aggregate(
        highest_score=Max("overall_score"),
        lowest_score=Min("overall_score")
    )

    highest_report = InterviewReport.objects.filter(
        user=user, overall_score=report_stats["highest_score"]
    ).first()

    lowest_report = InterviewReport.objects.filter(
        user=user, overall_score=report_stats["lowest_score"]
    ).first()

    strength = {
        "technology": highest_report.technology if highest_report else None,
        "score": report_stats["highest_score"],
    }
    weakness_score = report_stats["lowest_score"]
    weakness_technology = lowest_report.technology if lowest_report else None

    # If both scores are the same, set weakness score to 0
    if report_stats["highest_score"] == report_stats["lowest_score"]:
        weakness_score = 0
        weakness_technology = None

    weakness = {
        "technology": weakness_technology,
        "score": weakness_score,
    }


    performance_summary = {
        "total_interviews": reports.count(),
        "average_score": int(reports.aggregate(Avg("overall_score"))["overall_score__avg"] or 0),
        "strength": strength,
        "weakness": weakness,   
    }

    params = {
        "user": user,
        "candidate": candidate,
        "performance_summary": performance_summary,
        "reports": reports,
        "logs": logs
    }



    return render(request, 'admin/candidate_detail.html', params)

def report_detail(request, reportId):
        # Fetch report from DB
    report = get_object_or_404(InterviewReport, report_id=reportId)
    candidate_profile = CandidateProfile.objects.get(user=report.user)


    # Convert model instance to dict (all fields)
    params = {
        field.name: getattr(report, field.name)
        for field in report._meta.fields
    }

    params["incorrect_mcqs"] = params["mcq_total"] - params["mcq_correct"]
    params["full_name"] = candidate_profile.full_name

    return render(request, 'admin/interview_report.html', params)


def mcqs_management(request):
    return render(request, 'admin/mcqs_management.html')

@csrf_exempt
def add_mcq_to_database(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)

        # Prepare MCQ data dictionary
        mcq_data = {
            "question": data.get('question'),
            "code_part": data.get('code_part'),
            "option_a": data.get('option_a'),
            "option_b": data.get('option_b'),
            "option_c": data.get('option_c'),
            "option_d": data.get('option_d'),
            "answer": (data.get('answer') or '').lower(),
            "domain": (data.get('domain') or '').lower(),
            "difficulty": (data.get('difficulty') or 'easy').lower(),
            "topics": (data.get('topic') or '').lower()
        }


        # Add MCQ
        if add_mcq(mcq_data):
            return JsonResponse({'success': True, 'message': 'MCQ added successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'MCQ already exists'}, status=409)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt   
@require_POST
def scrape_mcqs(request):
    try:
        data = json.loads(request.body)
        domain = data.get("domain")
        print(f"Requested domain for scraping: {domain}")

        if not domain:
            return JsonResponse({
                "success": False,
                "message": "Domain not provided."
            }, status=400)

        scraper = MCQScraper(driver_path="D:\\FYP\\datasets\\chromedriver-win64\\chromedriver.exe")
        print("Initialized MCQScraper")

        df = None
        if domain.lower() == "python":
            print("Scraping Python MCQs...")
            hrefs = scraper.get_links("https://www.sanfoundry.com/python-mcqs-tuples/")
            df = scraper.scrape_mcqs(hrefs)
        elif domain.lower() == "java":
            hrefs = scraper.get_links("https://www.sanfoundry.com/java-mcqs-arithmetic-operators/")
            df = scraper.scrape_mcqs(hrefs)
        elif domain.lower() == "c++":
            hrefs = scraper.get_links("https://www.sanfoundry.com/c-plus-plus-interview-questions-answers-types/")
            df = scraper.scrape_mcqs(hrefs)

        if df is None or df.empty:
            print("No MCQs scraped or DataFrame is empty")
            return JsonResponse({
                "success": False,
                "message": "No MCQs found during scraping."
            }, status=404)

        print(f"Scraped {len(df)} MCQs")
        mcqs = df.to_dict(orient="records")

        return JsonResponse({
            "success": True,
            "mcqs": mcqs
        }, safe=False)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            "success": False,
            "message": f"Error occurred: {str(e)}"
        }, status=500)