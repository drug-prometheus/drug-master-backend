from django.db import models

# 약사 리스트
class Pharmacist(models.Model):
    name = models.CharField(max_length=100) # 약사 이름

    def __str__(self):
        return self.name

# 환자 리스트
class Patient(models.Model):
    name = models.CharField(max_length=100) # 환자 이름
    pharmacist = models.ForeignKey(Pharmacist, related_name='patients', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 환자의 복약 리스트
# 입력한 약물 정보 저장
# 사진을 통해 분석한 결과 저장
class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) # 환자 이름
    medication_name = models.CharField(max_length=100) # 약 이름

    def __str__(self):
        return f'{self.medication_name} for {self.patient.name}'
    
# 약사 소견서
class PatientNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE) # 환자
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE) # 약사
    note = models.TextField() # 소견서
    created_at = models.DateTimeField(auto_now=True) # 작성한 날짜(자동 기입)

    def __str__(self):
        return f'Note by {self.pharmacist.name} for {self.patient.name} on {self.created_at}'