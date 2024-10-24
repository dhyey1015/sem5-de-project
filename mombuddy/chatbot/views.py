from django.shortcuts import render
from .models import FAQ
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
import json

from django.shortcuts import render
from .models import FAQ

# Create your views here.

def chatbot_view1(request):
    response = None
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse the incoming JSON data
        user_query = data.get('query', '')
        # user_query = request.POST.get('query', '') #('query': "what is django")
        keywords = user_query.lower().split()
        
        faqs = FAQ.objects.all()
        matched_faq = None
        max_keywords_matches = 0
        
        for faq in faqs:
            faq_keywords = faq.question.lower().split()
            keyword_matches = sum(1 for keyword in keywords if keyword in faq_keywords)#<=========== don't know
            
            if keyword_matches > max_keywords_matches:
                max_keywords_matches = keyword_matches
                matched_faq = faq
                
        if matched_faq and max_keywords_matches > 0:
            response = matched_faq.answer
                
        elif (response):
            response = "I'm sorry, I don't have an answer for that."
            
    return render(request, 'index.html', {'response': response})

from django.http import JsonResponse
from .models import FAQ
import json

@csrf_exempt  # Since you're dealing with AJAX requests, make sure to handle CSRF tokens
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


# Create your views here.
# @csrf_exempt
# def chatbot_view(request):
#     response = None
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_query = data.get('message', '') #('query': "what is django")
#         keywords = user_query.lower().split()
        
#         faqs = FAQ.objects.all()
#         matched_faq = None
#         max_keywords_matches = 0
        
#         for faq in faqs:
#             faq_keywords = faq.question.lower().split()
#             keyword_matches = sum(1 for keyword in keywords if keyword in faq_keywords)#<=========== don't know
            
#             if keyword_matches > max_keywords_matches:
#                 max_keywords_matches = keyword_matches
#                 matched_faq = faq
                
#         if matched_faq and max_keywords_matches > 0:
#             response = matched_faq.answer
                
#         elif (response):
#             response = "I'm sorry, I don't have an answer for that."
            
#     return render(request, 'index.html', {'response': response})

# from django.http import JsonResponse
# import json

# @csrf_exempt
# def chatbot_view(request):
#     response = None
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_query = data.get('message', '')  # Expecting 'message' key in JSON body
#         keywords = user_query.lower().split()
        
#         faqs = FAQ.objects.all()
#         matched_faq = None
#         max_keywords_matches = 0
        
#         for faq in faqs:
#             faq_keywords = faq.question.lower().split()
#             keyword_matches = sum(1 for keyword in keywords if keyword in faq_keywords)
            
#             if keyword_matches > max_keywords_matches:
#                 max_keywords_matches = keyword_matches
#                 matched_faq = faq
                
#         if matched_faq and max_keywords_matches > 0:
#             response = matched_faq.answer
#         else:
#             response = "I'm sorry, I don't have an answer for that."
        
#         return JsonResponse({'response': response})

#     return JsonResponse({'response': "Invalid request method"}, status=400)



# def chatbot_view1(request, response=None):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON body of the request
#             data = json.loads(request.body)
#             user_query = data.get('message', '')  # This is the key sent by the front end
#             print(user_query)

#             # Break down the user's query into keywords
#             keywords = user_query.lower().split()

#             # Retrieve all FAQs from the database
#             faqs = FAQ.objects.all()
#             matched_faq = None
#             max_keywords_matches = 0

#             # Find the FAQ that has the most keyword matches
#             for faq in faqs:
#                 faq_keywords = faq.question.lower().split()
#                 keyword_matches = sum(1 for keyword in keywords if keyword in faq_keywords)

#                 if keyword_matches > max_keywords_matches:
#                     max_keywords_matches = keyword_matches
#                     matched_faq = faq

#             # Prepare the response based on the matched FAQ
#             if matched_faq and max_keywords_matches > 0:
#                 response = matched_faq.answer
#             else:
#                 response = "I'm sorry, I don't have an answer for that."
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     context = {
#         'response': response,
#     }
        
#     return render(request, 'index.html', context)
    

    #         # Return a JSON response with the chatbot answer
    #         return JsonResponse({'status': 'success', 'response': response}, status=200)

    #     except Exception as e:
    #         return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    # else:
    #     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    
    
    
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

