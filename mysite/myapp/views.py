from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from .models import Patient, Pharmacist, Medication, PatientNote, MedicationInfo
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout, login
from .serializers import MedicationInfoSerializer, NoCombinationSerializer, MedicationSerializer
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import io

# 프론트에서 약물 사진 받아와서 분석 후 프론트로 분석 결과 전송
class AnalyzingMedicine(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        def test_backend(img_dir):
            model = load_model(r'Pill_image_mobile_net.h5')

            image = Image.open(io.BytesIO(img_dir.read()))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            print(image)
            image = image.resize((100, 100))
            image = np.array(image)
            image = image/255.
            
            image = np.reshape(image, (1, 100, 100, 3))
            
            prediction = model.predict(image)
            prediction.shape
            pred_class = np.argmax(prediction, axis=-1)
            print(pred_class)
            
            return pred_class

        picture = request.POST.get('picture')
        patient = request.POST.get('patient')

        # 분석 결과: 약물 이름 리스트
        medicine_list = test_backend(picture)

        # ENDPOINT: 분석 결과(약물 이름 리스트)
        # DB에 약물 정보 저장
        for medicine_name in medicine_list:
            Medication.objects.create(patient=patient, medicine_name=medicine_name)

        # TODO: 사진 분석 결과를 프론트로 다시 전송(Response)
        return Response({'medication_list': medicine_list})

# 프론트에서 입력한 약물 정보 받아와서 DB에 추가    
class AddMedicineInfo(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        patient_name = request.data.get('patient') # 환자 이름
        medicine_name = request.data.get('medicine_name') # 약물 이름
        
        # Patient DB에서 해당 환자를 검색하여 담당 약사를 알아냄
        try:
            patient = Patient.objects.get(name=patient_name)
            pharmacist_name = patient.pharmacist.name
            print(f'[{patient_name}] 환자의 담당 약사는 [{pharmacist_name}] 약사입니다.')
        except Patient.DoesNotExist:
            return Response({'message': f'[{patient_name}] 환자가 존재하지 않습니다.'}, status=404)
            
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

    # DB에 저장된 약물 정보 모두 전송
    def get(self, request, format=None):
        medications = MedicationInfo.objects.all()
        serializer = MedicationInfoSerializer(medications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 약물 리스트에서 클릭했을 때 병용금기 정보가 뜸
    def post(self, request, format=None):
        medication_name = request.data.get('medication_name') # 약물 이름
        medication = Medication.objects.get(medication_name=medication_name)
        serializer = NoCombinationSerializer(medication, many=True)

        return Response({'no_mixture': serializer}, status=status.HTTP_200_OK)

# DB(약사 소견 입력돼 있는 DB)에서 환자 이름과 일치하는 소견 데이터 불러와서 프론트로 전송
class PharmacistWithPatients(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        pharmacist_name = request.data.get('pharmacist')
        pharmacist = Pharmacist.objects.get(name=pharmacist_name)
        patients = pharmacist.patients.all()
        patients_names = [patient.name for patient in patients]

        return Response({'patient_names': patients_names}, status=status.HTTP_200_OK)

# 약사 소견 데이터를 DB에서 불러와서 프론트로 전송
class PharmacistOpinion(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        patient_name = request.data.get('patient')
        patient = Patient.objects.get(name=patient_name)
        patient_note = PatientNote.objects.filter(patient=patient)
        note_list = [{'note': note.note, 'created_at': note.created_at} for note in patient_note]

        return Response({'note': note_list}, status=status.HTTP_200_OK)

# 프론트에서 작성한 약사 소견서 DB에 저장
class SavePharmacistOpinion(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        patient_name = request.data.get('patient').rstrip()
        opinion = request.data.get('opinion')
        
        patient = Patient.objects.get(name=patient_name)
        pharmacist_name = patient.pharmacist.name

        patient_note = PatientNote.objects.create(
            patient=patient,
            pharmacist=patient.pharmacist,
            note=opinion
        )
        
        return Response({'message': f'약사 소견이 저장되었습니다.\n약사: {pharmacist_name}\n환자:{patient_name}'})

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
    
# 약물 정보 보기 (메인 화면)
class SeeMediInfo(APIView):
    def post(self, request, format=None):
        patient_name = request.data.get('patient_name') # 환자 이름름

        if patient_name is None:
            return Response({'error': '환자 이름이 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            patient = Patient.objects.get(name=patient_name)
        except Patient.DoesNotExist:
            return Response({'error': '환자가 DB에 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 환자에 해당하는 Medication 리스트 가져오기
        medications = Medication.objects.filter(patient=patient)

        serializer = MedicationSerializer(medications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
