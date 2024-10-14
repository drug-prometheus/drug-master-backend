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
    
# 약물 정보
# 약물 검색 시 활용
class MedicationInfo(models.Model):
    medication_name = models.CharField(max_length=100) # 약 이름
    properties_classification = models.CharField(max_length=100) # 약효분류
    medical_properties = models.TextField() # 효능효과
    usage_capacity = models.TextField() # 용법용량
    side_effects = models.TextField() # 부작용, 주의사항
    prohibition = models.TextField() # 금기

    def __str__(self):
        return f'Information of {self.medication_name}'
    
# 병용금기 정보조회
class NoCombination(models.Model):
    medication_name = models.ForeignKey(MedicationInfo, on_delete=models.CASCADE) # 약물 이름
    mix_medication_name = models.CharField(max_length=100) # 병용금기 약물 이름
    mix_enterprise_name = models.CharField(max_length=100) # 병용금기 약물 판매 회사
    mix_etc_otc_name = models.CharField(max_length=100) # 병용금기 약물 전문의약품/일반의약품 이름
    prohibit_content = models.CharField(max_length=100) # 병용 시 발생 가능한 증상

    def __str__(self):
        return f'Do not eat {self.mix_medication_name} with {self.medication_name}'