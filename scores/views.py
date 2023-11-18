from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Score, Event, User, Criterion
from entries.models import Entry
from participants.models import Participant
from categories.models import Category
from django.shortcuts import get_object_or_404
from .serializers import ScoreSerializer
from django.db.models import Max
from entries.models import Entry
from categories.models import Category
from rest_framework import status


class ScoreEachEntryView(APIView):
    def post(self, request):
        score_value = request.data.get('score')
        event_id = request.data.get('event_id')
        entry_id = request.data.get('entry_id')
        user_id = request.data.get('user_id')
        criterion_id = request.data.get('criterion_id')
        if score_value is not None and event_id is not None and entry_id is not None and user_id is not None and criterion_id is not None:
            event = get_object_or_404(Event, pk=event_id)
            entry = get_object_or_404(Entry, pk=entry_id)
            user = get_object_or_404(User, pk=user_id)
            criterion = get_object_or_404(Criterion, pk=criterion_id)
            score = Score.objects.filter(event=event, entry=entry, user=user, criterion=criterion).first()
            if score is None:
                score = Score.objects.create(
                    score=score_value, 
                    event=event, 
                    entry=entry, 
                    user=user, 
                    criterion=criterion
                )
                return Response({'message': 'Score saved successfully!'}, status=201)
            else:
                return Response({'message': 'This record already exists!'}, status=200)
        else:
            return Response({'error': 'All fields are required!'}, status=400)


class CommentEachEntryView(APIView):
    def post(self, request):
        comment_text = request.data.get('comment')
        event_id = request.data.get('event_id')
        entry_id = request.data.get('entry_id')
        user_id = request.data.get('user_id')
        
        if comment_text is not None and event_id is not None and entry_id is not None and user_id is not None:
            event = get_object_or_404(Event, pk=event_id)
            entry = get_object_or_404(Entry, pk=entry_id)
            user = get_object_or_404(User, pk=user_id) 
            criterion = Criterion.objects.first()           
            comment, created = Score.objects.get_or_create(
                comment=comment_text, 
                event=event, 
                entry=entry, 
                user=user,
                criterion=criterion               
            )
            if created:
                return Response({'message': 'Comment saved successfully!'}, status=201)
            else:
                return Response({'message': 'This record already exists!'}, status=200)
        else:
            return Response({'error': 'All fields are required!'}, status=400)
        

class PlacementView(APIView):
    def get_winner(self, request):        
        event_id = request.data.get('event_id')
        category_id = request.data.get('category_id')        
        categories = Category.objects.filter(event_id=event_id)       
        entries = Entry.objects.filter(category_id=category_id, category_id__in=categories)        
        total_scores = Score.objects.filter(entry_id__in=entries).values('entry_id', 'entry__participant__first_name', 'entry__participant__last_name', 'entry__participant__participant_status').annotate(total_score=Sum('score'))        
        max_total_score_entry = total_scores.order_by('-total_score').first()
        return Response(max_total_score_entry)

    def get_second_place(self, request):        
        event_id = request.data.get('event_id')
        category_id = request.data.get('category_id')        
        categories = Category.objects.filter(event_id=event_id)       
        entries = Entry.objects.filter(category_id=category_id, category_id__in=categories)        
        total_scores = Score.objects.filter(entry_id__in=entries).values('entry_id', 'entry__participant__first_name', 'entry__participant__last_name', 'entry__participant__participant_status').annotate(total_score=Sum('score'))        
        second_place_entry = total_scores.order_by('-total_score')[1]
        return Response(second_place_entry)

    def get_third_place(self, request):        
        event_id = request.data.get('event_id')
        category_id = request.data.get('category_id')        
        categories = Category.objects.filter(event_id=event_id)       
        entries = Entry.objects.filter(category_id=category_id, category_id__in=categories)        
        total_scores = Score.objects.filter(entry_id__in=entries).values('entry_id', 'entry__participant__first_name', 'entry__participant__last_name', 'entry__participant__participant_status').annotate(total_score=Sum('score'))               
        if len(total_scores) >= 3:
            third_place_entry = total_scores.order_by('-total_score')[2]
            return Response(third_place_entry)
        else:
            return Response({"error": "Not enough entries for third place"}, status=400)

    
    def get_emerging_winner(self, request):        
        event_id = request.data.get('event_id')
        category_id = request.data.get('category_id')        
        categories = Category.objects.filter(event_id=event_id)       
        entries = Entry.objects.filter(category_id=category_id, category_id__in=categories, participant__participant_status='Emerging')        
        total_scores = Score.objects.filter(entry_id__in=entries).values('entry_id', 'entry__participant__first_name', 'entry__participant__last_name').annotate(total_score=Sum('score'))        
        max_total_score_entry = total_scores.order_by('-total_score').first()
        return Response(max_total_score_entry)


    def get_student_winner(self, request):        
        event_id = request.data.get('event_id')
        category_id = request.data.get('category_id')        
        categories = Category.objects.filter(event_id=event_id)       
        entries = Entry.objects.filter(category_id=category_id, category_id__in=categories, participant__participant_status='Student')        
        total_scores = Score.objects.filter(entry_id__in=entries).values('entry_id', 'entry__participant__first_name', 'entry__participant__last_name').annotate(total_score=Sum('score'))        
        max_total_score_entry = total_scores.order_by('-total_score').first()
        return Response(max_total_score_entry)

    
    def get(self, request):
        place = request.data.get('place')
        if place == 'winner':
            return self.get_winner(request)
        elif place == 'second':
            return self.get_second_place(request)
        elif place == 'third':
            return self.get_third_place(request)
        elif place == 'emerging':
            return self.get_emerging_winner(request)
        elif place == 'student':
            return self.get_student_winner(request)
        else:
            return Response({'error': 'Invalid place'}, status=400)


class TieAlertView(APIView):
    def get(self, request):        
        event_id = request.data.get('event_id')
        category_id = request.data.get('category_id')        
        categories = Category.objects.filter(event_id=event_id)       
        entries = Entry.objects.filter(category_id=category_id, category_id__in=categories)        
        total_scores = Score.objects.filter(entry_id__in=entries).values('entry_id', 'entry__participant__first_name', 'entry__participant__last_name', 'entry__participant__participant_status', 'entry__run_order').annotate(total_score=Sum('score'))        
        top_two_entries = total_scores.order_by('-total_score')[:2]

        if len(top_two_entries) < 2:
            return Response({"error": "Not enough entries for top two"}, status=status.HTTP_400_BAD_REQUEST)

        if top_two_entries[0]['total_score'] == top_two_entries[1]['total_score']:
            return Response({
                "alert": "The top two entries have the same total score!",
                "entries": top_two_entries
            })

        return Response(top_two_entries)
