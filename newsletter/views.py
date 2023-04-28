from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Newsletter, Subscriber
from .serializers import SubscriberSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SubscriberCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        
        # if email is not provided do this
        if not email:
            return Response({'email': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        # it performs a get() operation on d db obj using d parameters 
        # and if it doesn't exist, it performs a create operation
        subscriber, created = Subscriber.objects.get_or_create(email=email)
        
        if not subscriber.confirmed:
            subscriber.generate_confirmation_token()
            # to generate the absolute url of the confirmation endpoint
            confirmation_url = request.build_absolute_uri(f'/confirm/{subscriber.confirmation_token}')
            # send confirmation email
            message = Mail(
                from_email = 'balsacademy@gmail.com',
                to_emails = email,
                subject = 'Confirm your subscription',
                html_content = f'<p>Thank you for signing up to my email newsletter.' 
                    f'To confirm your subscription, please <a href="{confirmation_url}">click here</a>.</p>'
            )
            
            #     html_content = f'<p>Thank you for signing up for my email newsletter. To confirm your subscription,
            #     please <a href='{0}'>click here</a>.</p>'.
            #         format(request.build_absolute_uri('/confirm/{0}/'.
            #                                             format(subscriber.confirmation_token)))
            # )
            
            try:
                sg = SendGridAPIClient('SENDGRID_API_KEY')
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
                
        # subscriber is confirmed
        return Response({'success': 'You have suscessfully subscribed.'}, status=status.HTTP_201_CREATED)
    
class SubscriberDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    lookup_field = 'email'
    
    def delete(self, request, *args, **kwargs):
        # returns none if the obj does not exist
        email = kwargs.get['email', None]
        # email = kwargs['email']  it will raise a KeyError exception
        
        if not email:
            return Response({'email': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
        # if email exists
        subscriber = self.get_object()  # retrieves a single obj
        subscriber.delete()
        return Response({'success': 'You have successfully unsubscribed.'})
# work on this