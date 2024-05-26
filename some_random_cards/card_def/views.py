# some_random_cards/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game, Player, Card
from card_def.serializers import CardSerializer, GameSerializer

@api_view(['GET', 'POST'])
def card_list_create(request):
    if request.method == 'GET':
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def card_detail(request, pk):
    try:
        card = Card.objects.get(pk=pk)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CardSerializer(card)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def reveal_cards(request, game_id, player_id):
    try:
        player = Player.objects.get(id=player_id, game_id=game_id)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    revealed_cards = player.hand.all()  # Assuming Player has a hand field
    return Response({'revealed_cards': [card.name for card in revealed_cards]})

@api_view(['POST'])
def draw_cards(request, game_id, player_id, num_cards):
    try:
        player = Player.objects.get(id=player_id, game_id=game_id)
        game = Game.objects.get(id=game_id)
    except (Player.DoesNotExist, Game.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    deck = game.deck.first()  # Assuming Game has one deck
    if deck:
        drawn_cards = deck.draw(num_cards)  # Assuming Deck has a draw method
        player.hand.add(*drawn_cards)
        return Response({'drawn_cards': [card.name for card in drawn_cards]})
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def discard_cards(request, game_id, player_id, num_cards):
    try:
        player = Player.objects.get(id=player_id, game_id=game_id)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    cards_to_discard = player.hand.all()[:num_cards]  # Example logic
    player.hand.remove(*cards_to_discard)
    return Response({'discarded_cards': [card.name for card in cards_to_discard]})


@api_view(['GET', 'POST'])
def game_list_create(request):
    if request.method == 'GET':
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)