from django.db import models


class SearchHistory(models.Model):
    """Model to store search history"""
    query_type = models.CharField(max_length=20, choices=[
        ('recipe', 'Recipe Name'),
        ('ingredients', 'Ingredients')
    ])
    query_text = models.TextField()
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Search Histories'

    def __str__(self):
        return f"{self.query_type}: {self.query_text[:50]}"
