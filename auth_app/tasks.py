# from celery import shared_task
# from django.core.mail import send_mail


# @shared_task
# def send_verification_email( email, verification_url,):

#     send_mail(
#         subject="Verify your email address",

#         message=(
#             f"Welcome!\n\n"
#             f"Please verify your email address by clicking "
#             f"the link below:\n\n"
#             f"{verification_url}\n\n"
#             f"If you did not create this account, "
#             f"you can ignore this email."
#         ),

#         from_email="noreply@example.com",

#         recipient_list=[email],

#         fail_silently=False,
#     )