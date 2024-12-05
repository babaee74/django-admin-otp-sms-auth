from django.contrib import admin
from django.urls import path
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render 
from custom_admin.utils import get_otp_code
from django.utils import timezone
from datetime import timedelta
from admin_with_otp.settings import OTP_DURATION, MAX_OTP_TRIES




class AdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()

        custom_patterns = [
            path("2fa-otp/", self.verify_otp, name="2fa-otp"),
            path("cancel-otp/", self.cancel_otp, name="cancel-otp"),
        ]

        # ! NOTE: order here is super important
        # ! because Django router checks each URL against the request url
        # ! and finds the first match.
        return custom_patterns + urls
    
    def login(self, request, extra_context=None):
        """
        Use default login procedure for all methods other than POST (mainly GET).
        """
        if request.method == "POST":
            mobile = request.POST.get("username")
            password = request.POST.get("password")
            # print("Admin Login Creds:", mobile, password)

            if mobile is None or password is None:
                messages.add_message(request, messages.ERROR, "Username or Password is empty!")
            
            user = authenticate(request=request, mobile=mobile, password=password)
            if user is not None:
                # TODO: implement SMS OTP
                otp_code = get_otp_code(user.mobile)
                
                if otp_code is not None:
                    # TODO: handle session vars
                    # * We will create a session variable to store these:
                    # ! OTP code, OTP code exp date, login state
                    request.session["otp_attempts"] = 0
                    request.session["login_state"] = user.pk
                    request.session['otp_code'] = otp_code
                    request.session['otp_exp'] = (timezone.now() + timedelta(minutes=OTP_DURATION)).isoformat()
                    return redirect("/admin/2fa-otp/")
                
                else:
                    messages.add_message(request, messages.ERROR, "Something went wrong, please report this problem.")

                
            else:
                messages.add_message(request, messages.ERROR, "Wrong Username or Password!")
        
        return super().login(request, extra_context=extra_context)
