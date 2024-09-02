from django.shortcuts import render
from .models import FAQ

# Create your views here.

def chatbot_view(request):
    response = None
    if request.method == 'POST':
        user_query = request.POST.get('query', '') #('query': "what is django")
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
            
    return render(request, 'chatbot/chat.html', {'response': response})
    
    
    
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

