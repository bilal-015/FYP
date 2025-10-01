from django.contrib import admin
from .models import * 

# Register your models here.


admin.site.register(User)
admin.site.register(CandidateProfile)
admin.site.register(AdminProfile)
admin.site.register(SystemLog)
admin.site.register(InterviewReport)
admin.site.register(MCQ)