
import re
from xml import dom
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
import datetime
import jwt
from django.conf import settings
import uuid


def makeResponse(data):

    if data.get('code') == 200:
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


def isValidUuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def getSafeFromJson(json, key):
    try:
        return json[key]
    except KeyError:
        return None


def getDomainFromEmail(email):
    domain = re.search("@[\w.]+", email)
    print('domain', domain)
    if domain:
        return domain.group()
    return None


def generateFileName(self, filename):
    url = "media/docs/%s/%s" % (self.domain, filename)
    return url
