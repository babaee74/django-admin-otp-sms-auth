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
    



