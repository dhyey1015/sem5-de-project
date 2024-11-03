from django.shortcuts import render
from .models import FAQ
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
import json

from django.shortcuts import render
from .models import FAQ

@csrf_exempt  # Snot included CSRF tokens
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the incoming JSON data
        user_query = data.get('query', '')  # Get the query from the POST request
        keywords = user_query.lower().split()

        faqs = FAQ.objects.all()
        matched_faq = None
        max_keywords_matches = 0

        for faq in faqs:
            faq_keywords = faq.question.lower().split()
            keyword_matches = sum(1 for keyword in keywords if keyword in faq_keywords)

            if keyword_matches > max_keywords_matches:
                max_keywords_matches = keyword_matches
                matched_faq = faq

        response = "I'm sorry, I don't have an answer for that."
        if matched_faq and max_keywords_matches > 0:
            response = matched_faq.answer

        return JsonResponse({'response': response})  # Return JSON response
    return render(request, 'index.html')
  
 # my logic   
# from django.shortcuts import render
# from .models import FAQ

# def chatbot_view(request):
#     response = None
#     if request.method == 'POST':
#         user_query = request.POST.get('query', '')
#         keywords = user_query.lower().split()
        
#         faqs = FAQ.objects.all()
#         for faq in faqs:
#             for keyword in keywords:
#                 if keyword in faq.question.lower():
#                     response = faq.answer
#                     break
#             if response:
#                 break
#         if not response:
#             response = "I'm sorry, I don't have an answer for that."
    
#     return render(request, 'chatbot/chat.html', {'response': response})

