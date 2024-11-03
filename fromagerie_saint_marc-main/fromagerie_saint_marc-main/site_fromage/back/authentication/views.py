from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import json
import requests
import os
import re

from .serializers import UserSerializer, ItemSerializer
from authentication.models import User, Item

@api_view(['POST'])
def signup(request):
	username = request.data.get('username', '').strip()
	password = request.data.get('password', '').strip()
	language = request.data.get('language', '')
	if username == '':
		raise ValidationError({'error': 'Username cannot be empty'})

	if User.objects.filter(username=username).exists():
		raise ValidationError({'error': 'Username is already taken'})

	if len(username) == 0 or len(username) > 20:
		raise ValidationError({'error': 'Username must be at least 1 and less than 20 characters long'})

	if len(password) < 8:
		raise ValidationError({'error': 'Password must be at least 8 characters long'})

	if re.search(r'[<>&"\'/\\()`,;]', username):
		raise ValidationError({'error': 'Username cannot contain the following characters: <, >, &, ", \', /, \\, (, ), `, ;'})

	request.data['username'] = username
	serialized = UserSerializer(data=request.data)

	if serialized.is_valid():
		user = User.objects.create_user(username=username, password=password, language=language)
		token = Token.objects.create(user=user)
		user.is_online = True
		user.save()
		serialized = UserSerializer(user)
		return JsonResponse({'Token': token.key, 'user': serialized.data})

	print(serialized.errors)
	return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def log_user(request):
	try:
		user = User.objects.get(username=request.data['username'])
	except User.DoesNotExist:
		raise AuthenticationFailed({'error': 'Username is incorrect.'})

	if user.is_student == True:
		raise AuthenticationFailed({'error': 'Please use authentication to log as this user'})
	if user.check_password(request.data['password']):
		token, created = Token.objects.get_or_create(user=user)
		user.is_online = True
		user.save()
		serialized = UserSerializer(user)
		return JsonResponse({'Token': token.key, 'user': serialized.data})

	raise AuthenticationFailed({'error': 'password is incorrect.'})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def logout(request):
	user = request.user
	user.is_online = False
	user.save()
	serialized = UserSerializer(user)
	return JsonResponse({'user': serialized.data})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_detail(request):
	user = request.user
	serialized = UserSerializer(user)
	return JsonResponse({'user': serialized.data})

@api_view(['GET'])
def get_user_by_id(request, user_id):
	try:
		user = User.objects.get(pk=user_id)
		serialized = UserSerializer(user)
		return Response(serialized.data)
	except User.DoesNotExist:
		return JsonResponse({'error': 'User user not found.'}, status=404)

@api_view(['GET'])
def all_users(request):
	users = User.objects.all()
	serialized = UserSerializer(users, many=True)
	return Response(serialized.data)

@api_view(['POST', 'GET'])
def ft_login(request):
	code = request.GET.get('code')
	if code:
		url = 'https://api.intra.42.fr/oauth/token'
		data = {
			'grant_type': 'authorization_code',
			'client_id': os.getenv('UID_KEY'),
			'client_secret': os.getenv('SECRET_KEY'),
			'code': code,
			'redirect_uri': 'https://localhost:3000/42_auth/'
		}
		response = requests.post(url, data=data)
		print(response.text)
	if response.status_code == 200:
			token = response.json().get('access_token')
			if token:
				user_response = requests.get('https://api.intra.42.fr/v2/me', headers={
					'Authorization': f'Bearer {token}'
				})

				if user_response.status_code == 200:
					user_data = user_response.json()
					username = user_data.get('login')
					email = user_data.get('email')
					user, created = User.objects.get_or_create(email=email, defaults={'username': username})
					if created:
						user.username = username
						profile_pic_data = user_data.get('image')
						if profile_pic_data:
							profile_pic_url = profile_pic_data.get('link')
							if profile_pic_url:
								response = requests.get(profile_pic_url)
								if response.status_code == 200:
									user.profile_pic.save(f'{username}_profile_pic.jpg', ContentFile(response.content))
						user.is_student = True
						user.save()
					elif user.is_student == False:
						raise AuthenticationFailed({'error': 'This username is not registered as a 42 student'})
					token, created = Token.objects.get_or_create(user=user)
					user.is_online = True
					serialized = UserSerializer(user)
					return JsonResponse({'Token': token.key, 'user': serialized.data})
	raise AuthenticationFailed({'error': '42 auth failed'})

# function to add item to user's inventory
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_item(request):
	try:
		print("1")
		user = request.user
		availability = True if request.POST.get('available', 'false') == 'true' else False
		item = Item.objects.create(name=request.POST.get('name', ''), description=request.POST.get('description', ''), owner=user, price=request.POST.get('price', 0), category=request.POST.get('category', ''), quantity=request.POST.get('quantity', 1), available=availability, images=request.FILES.get('images'))
		item.save()
		serialized = ItemSerializer(item)
		print("2")
		return JsonResponse({'item': serialized.data}, status=200)
	except Exception as e:
		print(e)
		return JsonResponse({'error': 'Item could not be added'}, status=418)

# function to get all items
@api_view(['POST', 'GET'])
def get_items(request):
	items = Item.objects.all()
	serialized = ItemSerializer(items, many=True)
	return Response(serialized.data)

@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def edit_item(request, item_id):
	item = get_object_or_404(Item, id=item_id)
	item.name = request.POST.get('name', item.name)
	item.description = request.POST.get('description', item.description)
	item.price = request.POST.get('price', item.price)
	item.category = request.POST.get('category', item.category)
	item.quantity = request.POST.get('quantity', item.quantity)
	item.available = True if request.POST.get('available', 'false') == 'true' else False
	item.images = request.FILES.get('images', item.images)
	item.save()
	serialized = ItemSerializer(item)
	return JsonResponse({'item': serialized.data})

@api_view(['GET'])
def item_detail(request, item_id):
	item = get_object_or_404(Item, id=item_id)
	serialized = ItemSerializer(item)
	return JsonResponse({'item': serialized.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_item(request, item_id):
	print(item_id)
	item = get_object_or_404(Item, id=item_id)
	item.delete()
	return JsonResponse({'success': 'Item deleted'}, status=204)