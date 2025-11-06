from django.db import models
from django.contrib.auth.models import User  # ✅ Use Django's built-in User model

# ============================================================
# ✅ CUSTOM MODELS — the only ones you actually need
# ============================================================

class Case(models.Model):
    # Link each case to a registered user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')

    image = models.ImageField(upload_to='cases/')
    condition = models.CharField(max_length=100)
    confidence = models.FloatField()
    risk_level = models.CharField(max_length=50)
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cases'
        managed = True

    def __str__(self):
        return f"Case {self.id} - {self.condition} ({self.user.username})"


class FollowUp(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='followups')
    image = models.ImageField(upload_to='followups/')
    condition = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(blank=True, null=True)
    risk_level = models.CharField(max_length=50, blank=True)
    advice = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'followups'
        managed = True

    def __str__(self):
        return f"Follow-Up for Case {self.case.id}"
