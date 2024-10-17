# views.py
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.forms import PasswordResetRequestForm




def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            try:
                user = User.objects.get(email=email_or_username)
            except User.DoesNotExist:
                # Handle case where user doesn't exist
                pass
            else:
                # Generate reset token and send email
                token = default_token_generator.make_token(user)
                reset_url = f"http://yourdomain.com/reset/{user.pk}/{token}/"
                send_mail(
                    "Password Reset",
                    f"Click the link to reset your password: {reset_url}",
                    "from@example.com",
                    [user.email],
                )
                # Redirect to a success page
                return redirect("password_reset_done")
    else:
        form = PasswordResetRequestForm()
    return render(request, "password_reset_form.html", {"form": form})




# views.py
def password_reset_confirm(request, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        
        pass
    else:
        if default_token_generator.check_token(user, token):
            
            return redirect("password_reset_complete")
        else:
            # Invalid token
            pass
    return redirect("password_reset_failed")

