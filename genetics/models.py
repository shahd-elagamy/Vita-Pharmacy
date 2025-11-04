# نموذج الملف الجيني GeneticProfile
from django.db import models
from django.conf import settings

class GeneticProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dna_sequence = models.TextField()
    additional_info = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s Genetic Profile"

    class Meta:
        db_table = 'genetic_profile'  # تعيين اسم الجدول بشكل صريح

# نموذج التشخيص الإلكتروني OnlineDiagnosis
class OnlineDiagnosis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genetic_profile = models.ForeignKey(GeneticProfile, on_delete=models.CASCADE)
    diagnosis_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Diagnosis"

    class Meta:
        db_table = 'online_diagnosis'  # تعيين اسم الجدول بشكل صريح

# نموذج الأدوية المبنية على الحمض النووي DnaBasedMedicine
class DnaBasedMedicine(models.Model):
    medicine_name = models.CharField(max_length=255)
    description = models.TextField()
    recommended_for_genetic_profile = models.ForeignKey(GeneticProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.medicine_name

    class Meta:
        db_table = 'dna_based_medicine'  # تعيين اسم الجدول بشكل صريح

# نموذج الربط بين التشخيص والأدوية DiagnosisMedicine
class DiagnosisMedicine(models.Model):
    diagnosis = models.ForeignKey(OnlineDiagnosis, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(DnaBasedMedicine)  # استخدم ManyToManyField لربط الأدوية
    prescription_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.diagnosis.user.username}"

    class Meta:
        db_table = 'diagnosis_medicine'
