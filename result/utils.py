from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.template.exceptions import TemplateDoesNotExist
from assessment.models import Assessment
from users.models import User


def get_result_text(answers):
    negative_answers = [question for question, answer in answers.items() if answer == 'NO']
    if negative_answers:
        return ("ACT EARLY: Talk with your child's professional if you answered 'NO' for any questions.\n"
                "It is important to act early by talking with your child's professional.\n"
                "Use the resources provided in our App to learn more on how to support your child's growth.")
    else:
        return "Great job! Your child seems to be meeting all their milestones."

def get_detailed_result(answers):
    detailed_results = []
    for question, answer in answers.items():
        question_obj = Assessment.objects.filter(question=question).first()
        if question_obj:
            detailed_results.append(f"{question_obj.category}: {question_obj.question} - Your answer: {answer}")
        else:
            detailed_results.append(f"Question: {question} - Your answer: {answer} (No matching question found)")
    return "\n".join(detailed_results)

def send_results_email(answers, recipient_email):
    try:
        user = User.objects.get(email=recipient_email)
        detailed_result = get_detailed_result(answers)
        result_text = get_result_text(answers)
    except Exception as e:
        return f"Error generating results: {e}"

    try:
        html_content = render_to_string('email.html', {
            'parent_first_name': user.first_name,
            'detailed_results': detailed_result.split("\n"),
            'result_text': result_text
        })
    except Exception as e:
        return f"Error rendering template: {e}"

    try:
        send_mail(
            subject="Milestone Assessment Result",
            message='',
            html_message=html_content,
            from_email='TotoSteps <totostepsciphers@gmail.com>',            
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return "Email sent successfully"
    except Exception as e:
        return str(e)
