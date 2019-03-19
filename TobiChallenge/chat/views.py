from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from django.views.generic.base import View
from rest_framework.decorators import api_view

from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
from django.views import View

from django.views.decorators.csrf import csrf_exempt

import json
from botbuilder.schema import (Activity, ActivityTypes)
from botframework.connector import ConnectorClient
from botframework.connector.auth import (MicrosoftAppCredentials,
                                         JwtTokenValidation, SimpleCredentialProvider)

APP_ID = ''
APP_PASSWORD = ''

class ChatApiMessage(APIView):
    def get(self, *args, **kwargs):
        pass

    @staticmethod
    def __create_reply_activity(request_activity, text):
        return Activity(
            type=ActivityTypes.message,
            channel_id=request_activity.channel_id,
            conversation=request_activity.conversation,
            recipient=request_activity.from_property,
            from_property=request_activity.recipient,
            text=text,
            service_url=request_activity.service_url)

    def __handle_conversation_update_activity(self, activity):
        if activity.members_added[0].id != activity.recipient.id:
            credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
            reply = ChatApiMessage.__create_reply_activity(activity, 'Hello and welcome to the echo bot!')
            connector = ConnectorClient(credentials, base_url=reply.service_url)
            connector.conversations.send_to_conversation(reply.conversation.id, reply)
        return HttpResponse(status=202)

    def __handle_message_activity(self, activity):
        credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
        connector = ConnectorClient(credentials, base_url=activity.service_url)

        #call elaborate function [input: activity.text, output: to_send]

        to_send = 'You said: %s' % activity.text

        reply = ChatApiMessage.__create_reply_activity(activity, to_send)
        connector.conversations.send_to_conversation(reply.conversation.id, reply)
        return HttpResponse(status=200)


    def __unhandled_activity(self):
        return HttpResponse(status=404)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        
        activity = Activity.deserialize(body_data)

        if activity.type == ActivityTypes.conversation_update.value:
            return self.__handle_conversation_update_activity(activity)
        elif activity.type == ActivityTypes.message.value:
            return self.__handle_message_activity(activity)
        else:
            return self.__unhandled_activity()
