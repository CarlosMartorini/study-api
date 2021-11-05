from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import Course
from django.contrib.auth.models import User
from users.permissions import Instructor
from .serializers import CourseSerializer
from rest_framework import status
from django.db.utils import IntegrityError


class View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Instructor]


    def get(self, request):
        courses = Course.objects.all()
        serialized = CourseSerializer(courses, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        try:
            name = data['name']
            course = Course.objects.create(name=name)
            serialized = CourseSerializer(course)

            return Response(serialized.data, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({'error': 'Course with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError:
            return Response({'error': f"{str(KeyError)} it's missing!"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ViewById(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Instructor]


    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            serialized = CourseSerializer(course)

            return Response(serialized.data, status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response({'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND)

    
    def put(self, request, course_id):
        data = request.data

        try:
            course = Course.objects.get(id=course_id)
            new_name = data['name']
            course.name = new_name
            course.save()
            serialized = CourseSerializer(course)

            return Response(serialized.data, status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response({'error': 'Course not founded!'}, status=status.HTTP_404_NOT_FOUND)
        
        except KeyError:
            return Response({'error', f"{str(KeyError)} it's missing"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        except IntegrityError:
            return Response({'error': 'Course with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            
            return Response('', status=status.HTTP_204_NO_CONTENT)
        
        except Course.DoesNotExist:
            return Response({'error': 'Course not founded!'}, status=status.HTTP_404_NOT_FOUND)


class Create(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Instructor]


    def put(self, request, course_id):
        data = request.data

        try:
            course = Course.objects.get(id=course_id)
            user_ids = data['user_ids']

            if type(user_ids) != list:
                return Response({'errors': 'user_ids is not a list'}, status=status.HTTP_400_BAD_REQUEST)

            course.users.set([])

            for item in user_ids:
                user = User.objects.get(id=item)
                if not user:
                    return Response({'errors': 'invalid user_id list'})
                if user.is_superuser or user.is_staff:
                    return Response({'errors': 'Only students can be enrolled in the course.'}, status=status.HTTP_400_BAD_REQUEST)
                course.users.add(user)
            
            course.save()
            serialized = CourseSerializer(course)

            return Response(serialized.data, status=status.HTTP_200_OK)
        
        except Course.DoesNotExist:
            return Response({'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND)

        except User.DoesNotExist:
            return Response({'errors': 'Only students can be enrolled in the course.'}, status=status.HTTP_404_NOT_FOUND)

