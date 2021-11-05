from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from users.permissions import Facilitator
from .models import Activity, Submission
from .serializers import SubmissionSerializer, ActivitySerializer
from rest_framework import status
from django.db.utils import IntegrityError


class View(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Facilitator]


    def post(self, request):
        data = request.data

        try:
            title = data['title']
            points = data['points']
            activity = Activity.objects.create(
                title=title,
                points=points
            )
            serialized = ActivitySerializer(activity)
            output_serialized = {**serialized.data}
            submissions = output_serialized.pop('submission_set')
            output_serialized['submissions'] = submissions

            return Response(output_serialized, status=status.HTTP_201_CREATED)
        
        except IntegrityError:
            return Response({'error': 'Activity with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        user = request.user

        if not user.is_staff:
            return Response('', status=status.HTTP_403_FORBIDDEN)
        
        activities = Activity.objects.all()
        serialized = ActivitySerializer(activities, many=True)

        list = []

        for item in serialized.data:
            object = {**item}
            submissions = object.pop('submission_set')
            object['submissions'] = submissions
            list.append(object)
        
        return Response(list, status=status.HTTP_200_OK)


class ViewById(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [Facilitator]


    def put(self, request, activity_id):
        data = request.data

        try:
            activity = Activity.objects.get(id=activity_id)
            title = data['title']
            points = data['points']

            if activity.submission_set.first():
                return Response({'error': 'You can not change an Activity with submissions'}, status=status.HTTP_400_BAD_REQUEST)
            
            activity.title = title
            activity.points = points
            activity.save()
            
            serialized = ActivitySerializer(activity)
            output_serialized = {**serialized.data}
            submissions = output_serialized.pop('submission_set')
            output_serialized['submissions'] = submissions

            return Response(output_serialized, status=status.HTTP_200_OK)
        
        except Activity.DoesNotExist:
            return Response({'error': 'Invalid activity_id'}, status=status.HTTP_404_NOT_FOUND)
        
        except KeyError:
            return Response({'errors': f"{str(KeyError)} it's missing"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        except IntegrityError:
            return Response({'error': 'Activity with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id)
            serialized = ActivitySerializer(activity)

            return Response(serialized.data, status=status.HTTP_200_OK)
        
        except Activity.DoesNotExist:
            return Response({'error': 'Invalid activity_id'}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, activity_id):
        try:
            activity = Activity.objects.get(id=activity_id)
            activity.delete()

            return Response('', status=status.HTTP_204_NO_CONTENT)
        
        except Activity.DoesNotExist:
            return Response({'error': 'Invalid activity_id'}, status=status.HTTP_404_NOT_FOUND)


class Create(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, activity_id):
        data = request.data
        user = request.user

        try:
            activity = Activity.objects.get(id=activity_id)
            
            if user.is_superuser or user.is_staff:
                return Response({'errors': 'Only students can apply submissions'}, status=status.HTTP_403_FORBIDDEN)
            repo = data['repo']
            submission = Submission.objects.create(
                user_id=user.id, 
                activity_id=activity.id, 
                repo=repo, 
                grade=None
            )
            serialized = SubmissionSerializer(submission)

            return Response(serialized.data, status=status.HTTP_201_CREATED)
        
        except Activity.DoesNotExist:
            return Response({'errors': 'Invalid course_id'}, status=status.HTTP_404_NOT_FOUND)
        
        except User.DoesNotExist:
            return Response({'errors': 'Invalid user_id list'}, status=status.HTTP_404_NOT_FOUND)
        
        except KeyError as e:
            return Response({'errors': f'{str(e)} is missing'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class SubmissionView(APIView):
    permission_classes = [IsAuthenticated, Facilitator]
    authentication_classes = [TokenAuthentication]


    def put(self, request, submission_id):
        data = request.data
        
        try:
            submission = Submission.objects.get(id=submission_id)
            grade = data['grade']

            submission.grade = grade
            submission.save()
            serialized = SubmissionSerializer(submission)

            return Response(serialized.data)

        except Submission.DoesNotExist:
            return Response({'errors': 'Invalid submission_id'}, status=status.HTTP_404_NOT_FOUND)    
        
        except KeyError as e:
            return Response({'errors': f'{str(e)} is missing'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ListSubmissions(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = request.user
        
        if not user.is_superuser and not user.is_staff:
            submissions = user.submission_set
            serialized = SubmissionSerializer(submissions, many=True)
            
            return Response(serialized.data, status=status.HTTP_200_OK)

        submissions = Submission.objects.all()
        serialized = SubmissionSerializer(submissions, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)
