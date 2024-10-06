from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import Patient, Pharmacist, Medication, PatientNote
from rest_framework import status

# 프론트에서 약물 사진 받아와서 분석 후 프론트로 분석 결과 전송
class AnalyzingMedicine(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        # ENDPOINT: 사진(picture), 환자 이름(patient)
        picture = request.data.get('picture')
        patient = request.data.get('patient')

        # TODO: AI 모델 연결하고 분석 결과 받는 코드
        medicine_list = [] # 분석 결과: 약물 이름 리스트

        # ENDPOINT: 분석 결과(약물 이름 리스트)
        # DB에 약물 정보 저장
        for medicine_name in medicine_list:
            Medication.objects.create(patient=patient, medicine_name=medicine_name)

        # TODO: 사진 분석 결과를 프론트로 다시 전송(Response)

# 프론트에서 입력한 약물 정보 받아와서 DB에 추가    
class AddMedicineInfo(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        # TODO: 받아온 약물 정보(이름)를 DB에 저장
        # ENDPOINT: 약물 정보(medicine_name), 환자 이름(patient)
        patient = request.data.get('patient')
        medicine_name = request.data.get('medicine_name') # 약물 이름
        Medication.objects.create(patient=patient, medicine_name=medicine_name)

# 약 이름 검색(MainPage, SearchDrugPage)
class SearchMedicine(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        # POST 보내기 실패
        pass

# DB(약사 소견 입력돼 있는 DB)에서 환자 이름과 일치하는 소견 데이터 불러와서 프론트로 전송
class PharmacistWithPatients(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        pharmacist_name = request.data.get('pharmacist')
        pharmacist = Pharmacist.objects.get(name=pharmacist_name)
        patients = pharmacist.patients.all()
        patients_names = [patient.name for patient in patients]

        return Response({'patient_names': patients_names}, status=status.HTTP_200_OK)


class PharmacistOpinion(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        patient_name = request.data.get('patient')
        patient = Patient.objects.get(name=patient_name)
        patient_note = PatientNote.objects.filter(patient=patient)
        note_list = [{'note': note.note, 'created_at': note.created_at} for note in patient_note]

        return Response({'note': note_list}, status=status.HTTP_200_OK)