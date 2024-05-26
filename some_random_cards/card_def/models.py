from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
    hand = models.ManyToManyField('Card', related_name='players_hand', blank=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ability_type = models.CharField(max_length=100)  # e.g., 'reveal', 'draw', etc.
    ability_value = models.IntegerField(null=True, blank=True)  # e.g., number of cards to draw
    game = models.ForeignKey(Game, related_name='cards', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Deck(models.Model):
    game = models.ForeignKey(Game, related_name='deck', on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, related_name='decks')

    def draw(self, num_cards):
        drawn_cards = self.cards.all()[:num_cards]
        self.cards.remove(*drawn_cards)
        return drawn_cards

    def __str__(self):
        return f"{self.game.name} Deck"
