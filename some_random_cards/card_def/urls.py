from django.urls import path
from . import views

urlpatterns = [
    path('api/cards/', views.card_list_create, name='card-list-create'),\
    path('api/games/', views.game_list_create, name='game-list-create'),
    path('api/cards/<int:pk>/', views.card_detail, name='card-detail'),
    path('api/games/<int:game_id>/players/<int:player_id>/reveal/', views.reveal_cards, name='reveal-cards'),
    path('api/games/<int:game_id>/players/<int:player_id>/draw/<int:num_cards>/', views.draw_cards, name='draw-cards'),
    path('api/games/<int:game_id>/players/<int:player_id>/discard/<int:num_cards>/', views.discard_cards, name='discard-cards'),
]
