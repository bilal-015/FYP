
from django.urls import path
from . import views

urlpatterns = [

    # Register and Login urls

    path("", views.register, name='register'),
    path('register_candidate/', views.register_candidate, name='register_candidate'),
    path('send_email_verification/', views.send_email_verification, name='send_email_verification'),


    path("login/", views.login, name='login'),
    path("candidateLogin/", views.candidateLogin, name='candidateLogin'),
    path("logout/", views.logout_view, name='logout'),

    path('get_all_emails/', views.get_all_emails, name='get_all_emails'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path("set_new_password/", views.set_new_password, name="set_new_password"),

    path("forgotPassword/", views.forgot_password, name='forgotPassword'),


    path("dashboard/", views.dashboard, name='dashboard'),


    path("profile/", views.profile, name='profile'),
    path("updateProfile/", views.update_profile, name='updateProfile'),
    path("updateProfileImage/", views.update_profile_image, name = 'updateProfileImage'),


    path("interviewReports/", views.interview_reports, name='interviewReports'),
    path("interview_setup/", views.interview_setup, name='interviewSetup'),
    path("store_interview_setup/", views.store_interview_setup, name = 'store_interview_setup'),
    path("mcqs_page/", views.mcqs_page, name='mcqs_page'),
    path("api/mcqs/", views.get_mcqs, name="get_mcqs"),
    path("submit_mcqs/", views.submit_mcqs, name ="submit_mcqs"),


    path("get-coding-questions/", views.get_coding_questions, name="get_coding_questions"),
    path("coding_page/", views.coding_page, name='coding_page'),
    path("submit_coding_answers", views.submit_coding_answers, name='submit_coding_answers'),

    path("confidence_score_page/", views.confidence_score_page, name='confidence_score_page'),
    path("submit_confidence_assessment", views.submit_confidence_assessment, name = 'submit_confidence_assessment'),

    path("interview_report/<int:reportId>/", views.interview_report, name='interview_report'),

    path("reports/", views.interview_reports, name='reports'),




    # admin site
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),


    path("api/candidates/", views.admin_get_candidates, name="get_candidates"),
    path('candidates_management/', views.candidates_management, name='candidates_management'),
    path("delete-candidate/", views.delete_candidate, name="delete_candidate"),
    path("enable-candidate/", views.enable_candidate, name="enable_candidate"),
    path("disable-candidate/", views.disable_candidate, name="disable_candidate"),


    path('get_reports/', views.get_reports, name='get_reports'),
    path('reports_management/', views.reports_management, name='reports_management'),
    path("delete-report/", views.delete_report, name="delete_report"),


    path("store_log/", views.store_log, name="store_log"),
    path('logs_management/', views.logs_management, name='logs_management'),
    path("fetch_logs/", views.fetch_logs, name="fetch_logs"),


    path('candidate_detail', views.candidate_detail, name='candidate_detail'),
    path('report_detail/<int:reportId>/', views.report_detail, name='report_detail'),


    path('mcqs_management/', views.mcqs_management, name='mcqs_management'),
    path('add_mcq_to_database/', views.add_mcq_to_database, name='add_mcq_to_database'),


]

