from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import Patient, Pharmacist, Medication, PatientNote
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout, login

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
        patient_name = request.data.get('patient')
        medicine_name = request.data.get('medicine_name') # 약물 이름
        pharmacist_name = '약사1'
        
        # Pharmacist DB에 해당 약사가 존재하는지 확인
        pharmacist, created = Pharmacist.objects.get_or_create(name=pharmacist_name)
        if created:
            print(f'[{pharmacist_name}] 약사가 새로 추가되었습니다.')
        else:
            print(f'[{pharmacist_name}] 약사는 이미 존재합니다.')

        # Patient DB에 해당 환자가 존재하는지 확인
        patient, created = Patient.objects.get_or_create(name=patient_name, pharmacist=pharmacist)
        if created:
            print(f'[{patient_name}] 환자가 새로 추가되었습니다.')
        else:
            print(f'[{patient_name}] 환자는 이미 존재합니다.')
            
        # Medication DB에 해당 약물이 존재하는지 확인
        medication, created = Medication.objects.get_or_create(patient=patient, medication_name=medicine_name)
        if created:
            print(f'[{patient_name}] 환자의 새 약물 [{medicine_name}]이(가) 성공적으로 추가되었습니다.')
            return Response({'message': f'{patient_name} 환자의 새 약물 {medicine_name}이(가) 성공적으로 추가되었습니다.'})
        else:
            print(f'[{patient_name}] 환자는 이미 [{medicine_name}] 약물을 복용 중입니다.')
            return Response({'message': f'[{patient_name}] 환자는 이미 [{medicine_name}] 약물을 복용 중입니다.'})

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

# 로그인    
class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request=request, user=user)

            return Response({
                'message': '로그인 성공'
            })
        
        return Response({'message': '로그인 실패'}, status=400)
    
# 로그아웃
class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request=request)

        return Response({'message': '로그아웃 성공'}, status=status.HTTP_200_OK)