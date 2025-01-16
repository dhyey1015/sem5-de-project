from django.shortcuts import render
from .models import FAQ
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging
from transformers import pipeline

logger = logging.getLogger(__name__)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('query', '').lower()
        faqs = FAQ.objects.all()

        # Simple keyword filtering to reduce context size
        relevant_faqs = [faq for faq in faqs if any(keyword in faq.question.lower() for keyword in user_query.split())]
        
        # If no relevant FAQ is found, fall back to all FAQs (prevent empty context)
        if not relevant_faqs:
            relevant_faqs = faqs  

        # Prepare context using only relevant FAQs
        context = " ".join([f"{faq.question}: {faq.answer}" for faq in relevant_faqs])

        # Ensure the context fits the model's token limit
        if len(context.split()) > 500:
            context = " ".join(context.split()[:500])  # Trim context to avoid token overflow

        # Perform question answering with refined context
        result = qa_pipeline(question=user_query, context=context)
        response = result['answer']
        confidence = result['score']

        # Confidence threshold to avoid incorrect answers
        # if confidence < 0.5:
        #     response = "I'm not sure about that. Please consult a healthcare professional."

        logger.info(f"User query: {user_query}, Response: {response}, Confidence: {confidence}")
        return JsonResponse({'response': response})
        
    return render(request, 'index.html')



# from django.shortcuts import render
# from .models import FAQ
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json
# import logging
# from transformers import pipeline

# logger = logging.getLogger(__name__)

# # Load the transformer model once for efficiency
# qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")

# @csrf_exempt
# def chatbot_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_query = data.get('query', '')
#         faqs = FAQ.objects.all()

#         # Prepare context by concatenating all FAQs
#         context = " ".join([f"{faq.question}: {faq.answer}" for faq in faqs])

#         # Use the transformer for question answering
#         result = qa_pipeline(question=user_query, context=context)
#         confidence = result['score']
#         response = result['answer']

#         # # Set a confidence threshold to avoid incorrect responses
#         # if confidence < 0.5:  
#         #     response = "I'm sorry, I don't have an answer for that."

#         logger.info(f"User query: {user_query}, Response: {response}, Confidence: {confidence}")
#         return JsonResponse({'response': response})
        
#     return render(request, 'index.html')





# from django.shortcuts import render
# from .models import FAQ
# from django.views.decorators.csrf import csrf_exempt 
# from django.http import JsonResponse
# import json

# from django.shortcuts import render
# from .models import FAQ
# import logging

# logger = logging.getLogger(__name__)

# @csrf_exempt  # Snot included CSRF tokens
# def chatbot_view(request):
#     if request.method == 'POST':

#         data = json.loads(request.body)  # Parse the incoming JSON data
#         user_query = data.get('query', '')  # Get the query from the POST request
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

#         response = "I'm sorry, I don't have an answer for that."
#         if matched_faq and max_keywords_matches > 0:
#             response = matched_faq.answer
            
#         logger.info(f"User query: {user_query}, Response: {response}")

#         return JsonResponse({'response': response})  # Return JSON response
#     return render(request, 'index.html')
  
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

