from django.db import models

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class ContactDetails(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    contact = models.CharField(max_length=200)

    def __str__(self):
        return f"Contact details for {self.patient}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_visited = models.DateField()
    medical_history = models.TextField()

    class Meta:
        unique_together = ('patient', 'date_visited')

    def __str__(self):
        return f"Medical history for {self.patient} on {self.date_visited}"
