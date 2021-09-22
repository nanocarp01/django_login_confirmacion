from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.core.mail import send_mail
from .forms import RegisterUserForm

def register(request):
    if request.user.is_authenticated:
        print('Already authenticated')
        return HttpResponseRedirect(reverse('logs:index'))
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            # RegisterUserForm is created from User model, all model field restrictions are checked to considerate it a valid form
            if form.is_valid():
                print('Valid form')
                # Save user to database but with is_active = False
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                # Send confirmation email
                current_site = get_current_site(request)
                subject = 'Activate Your ' + current_site.domain + ' Account'
                message = render_to_string('log/email_confirmation.html',
                    {
                        "domain": current_site.domain,
                        "user": user,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                    },
                )
                to_email = form.cleaned_data.get('email')
                send_mail(subject, message, 'fe@gmail.com', [to_email])

                # Redirect user to login
                messages.success(request, 'Please Confirm your email to complete registration before Login.')
                return HttpResponseRedirect(reverse('login'))
            else:
                #print('Invalid form: %s' % form.errors.as_data())
                #print(type(form.errors.as_data()))
                if form.errors:
                    #messages.info(request, 'Input field errors:')
                    for key, values in form.errors.as_data().items():
                        #print("Bad value: %s - %s" % (key, values))
                        if key == 'username':
                            messages.info(request, 'Error input fields')
                            break
                        else:
                            for error_value in values:
                                print(error_value)
                                #print(type(error_value))
                                messages.info(request, '%s' % (error_value.message))

                return HttpResponseRedirect(reverse('log:register'))
        else:
            form = RegisterUserForm()

            context = {
                'form': form
            }
            return render(request, 'log/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect user to login
        messages.success(request, 'Successful email confirmation, you can proceed to login.')
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Activation link is invalid!')

