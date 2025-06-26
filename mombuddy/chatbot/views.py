from django.shortcuts import render
from .models import FAQ
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging
import spacy

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

logger = logging.getLogger(__name__)

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('query', '')
        
        # Process user query using spaCy
        doc = nlp(user_query)
        
        # Extract entities or keywords from the user's query to find the intent
        intent = detect_intent(doc)
        
        # Handle pregnancy-related FAQ or generate dynamic response based on detected intent
        if intent == 'pregnancy_faq':
            response = generate_dynamic_answer(user_query)
        else:
            response = handle_generic_response(user_query)
        
        # Log the query and response for debugging purposes
        logger.info(f"User query: {user_query}, Response: {response}")

        # Return the response as JSON
        return JsonResponse({'response': response})
    
    return render(request, 'index.html')


def detect_intent(doc):
    """Detect user intent based on the query, focusing on pregnancy-related topics."""
    
    # Define pregnancy-related keywords to detect intent
    pregnancy_keywords = ['pregnancy', 'food aversions', 'prenatal vitamins', 'exercise', 'bleeding', 'foods to avoid', 'sleep on my left side']
    
    # Check if any pregnancy-related keywords are mentioned in the query
    if any(keyword in doc.text.lower() for keyword in pregnancy_keywords):
        return 'pregnancy_faq'
    
    return 'generic'


def generate_dynamic_answer(user_query):
    """Generate a dynamic answer based on the question and context (using NLP and FAQ matching)."""
    
    # Process the query to extract meaningful entities or keywords
    doc = nlp(user_query)
    question = doc.text.lower()
    
    # Fetch all FAQs from the database
    faqs = FAQ.objects.all()
    faq_scores = []

    # Calculate semantic similarity between the user's query and each FAQ
    for faq in faqs:
        faq_doc = nlp(faq.question)  # Process FAQ question using spaCy
        similarity_score = doc.similarity(faq_doc)  # Calculate similarity score
        
        # Store the FAQ with its similarity score
        faq_scores.append((faq, similarity_score))

    # Sort FAQs by similarity score in descending order
    faq_scores.sort(key=lambda x: x[1], reverse=True)

    # If a relevant FAQ is found, return its answer
    if faq_scores and faq_scores[0][1] > 0.5:  # Adjust threshold based on testing
        matched_faq = faq_scores[0][0]
        return matched_faq.answer  # Provide the answer from the database
    else:
        return "I'm sorry, I couldn't find a relevant answer for that."


def handle_generic_response(user_query):
    """Generate a fallback response for queries that don't match any FAQ."""
    return "That's an interesting question! Could you please provide more details?"
