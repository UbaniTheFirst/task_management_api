from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Task(models.Model):
    """
    Task model representing a user's task with priority and status tracking.
    """
    
    # Priority choices
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    
    # Fields
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    def clean(self):
        """Validate that due_date is in the future."""
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError({'due_date': 'Due date must be in the future.'})
    
    def mark_complete(self):
        """Mark task as completed and set completed_at timestamp."""
        self.status = 'Completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        """Mark task as incomplete and clear completed_at timestamp."""
        self.status = 'Pending'
        self.completed_at = None
        self.save()