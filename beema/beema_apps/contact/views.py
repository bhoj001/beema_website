from django.shortcuts import render

# Create your views here.

def feedback(request):
    if request.method == 'GET':
        form = FeedBackForm()
    else:
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            location = form.cleaned_data['address']
            suggestion = form.cleaned_data['suggestion']
            html_message = """
                <p>From: {0}</p>
                <p>Location: {1}</p>
                <p>Sender Email: {2}</p>
                <p>Country: {3}</p>
                <br><br>
                <b>
                {4}
                </b>

            """.format(name, location, email, country, suggestion)
            try:
                # Call the celery tasks to send email. 
                message =  'From: {}\n Email: {} \n Location: {} \n Country: {}\n Message: {}'.format(name, email, location, country, suggestion )

                send_feedback_email_task.delay(
                    "Feedback Email",
                    message
                )

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect("/")
    return render(request, "static_pages/feedback.html", {'form': form})