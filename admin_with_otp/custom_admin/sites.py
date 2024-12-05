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
    
    def verify_otp(self, request):
        if request.method == "POST":
            input_otp = request.POST.get('otp')

            session_otp_code = request.session.get('otp_code', None)
            otp_exp_date_str = request.session.get('otp_exp', None) # ISO format
            otp_attempts = request.session.get('otp_attempts', -1)

            if otp_attempts>MAX_OTP_TRIES:
                messages.add_message(request, messages.ERROR, "Too many attempts, try again later")
                request.session.flush()
                return redirect('admin:login')

            if session_otp_code is None or otp_exp_date_str is None or otp_attempts<0:
                messages.add_message(request, messages.ERROR, "Verification code expired, try Again")
                request.session.flush()
                return redirect('admin:login')

            # ISO to datetime
            otp_exp_date = timezone.datetime.fromisoformat(otp_exp_date_str)
            
            if timezone.now() > otp_exp_date:
                messages.add_message(request, messages.ERROR, "Verification code expired, try Again")
                request.session.flush()
                return redirect('admin:login')

            if input_otp==session_otp_code:
                # ! We saved user.pk in login state, 
                # ! we can retrieve the user record using this pk
                user_pk = request.session.get('login_state', None)
                
                if user_pk is not None:
                    user = get_user_model().objects.get(pk=user_pk)
                    
                    # sets the request.user object for next requests
                    auth_login(request, user) 
                    
                    request.session.pop('otp_attempts', None)
                    request.session.pop('login_state', None)
                    request.session.pop('otp_code', None)
                    request.session.pop('otp_exp', None)
                    
                    return redirect('admin:index') # Enjoy the Django Dashboard
                else:
                    # ! It will return to otp page
                    messages.add_message(request, messages.ERROR, "Verification code expired, try Again")
            else:
                # ! It will return to otp page
                request.session["otp_attempts"] = otp_attempts + 1
                messages.error(request, "Invalid Verification Code. Try Again")
        
        
        # ? show OTP Page (GET) to user, 
        # ? use the template inside templates dir (its path setup inside settings).
        return render(request, 'admin/2fa_verification.html')



    def cancel_otp(self, request):
        # request.session.pop('login_state', None)
        # request.session.pop('otp_code', None)
        # request.session.pop('otp_exp', None)
        request.session.flush()
        return redirect("admin:login")


admin_site = AdminSite(name='custom_admin')



