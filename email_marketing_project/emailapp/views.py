from django.shortcuts import render
from .emailgen import EmailMarketingAssistant

def index(request):
    if request.method == 'POST':
        # Handle form submission and interact with the ML code
        assistant = EmailMarketingAssistant()

        mail_type = request.POST.get('mail_type')
        campaign_goal = request.POST.get('campaign_goal')

        details = {}

        # For e-commerce related prompts
        if mail_type == "e-commerce":
            details['product_name'] = request.POST.get('product_name', '')
            if campaign_goal in ['convince_to_buy']:
                details['product_description'] = request.POST.get('product_description', '')

        # For new customer related prompts
        elif mail_type == "people" and campaign_goal in ['welcome_new_user']:
            details['user_name'] = request.POST.get('user_name', '')
        elif mail_type == "people" and campaign_goal in ['congratulate_on_purchase']:
            details['user_name'] = request.POST.get('user_name', '')

        # For blog related prompts
        elif mail_type == "blog" and campaign_goal == "new_blog":
            details['post_title'] = request.POST.get('post_title', '')
            details['topic'] = request.POST.get('topic', '')

        website_url = request.POST.get('website_url')
        if website_url:
            company_description = assistant.get_company_description(website_url)
        else:
            company_description = "Website URL not provided."

        email_contents = assistant.get_sample_email(mail_type, campaign_goal, **details)

        # Convert email_contents to a list of tuples
        email_contents = [(i + 1, content) for i, content in enumerate(email_contents)]

        return render(request, 'emailapp/index.html', {'email_contents': email_contents, 'company_description': company_description})

    return render(request, 'emailapp/index.html')
