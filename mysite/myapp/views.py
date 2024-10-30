from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from .models import Patient, Pharmacist, Medication, PatientNote, MedicationInfo, NoCombination
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
import torch
import cv2
import pathlib
from io import BytesIO

# 절대 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 프론트에서 약물 사진 받아와서 분석 후 프론트로 분석 결과 전송
class AnalyzingMedicine(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        temp = pathlib.PosixPath
        pathlib.PosixPath = pathlib.WindowsPath

        model_path = os.path.abspath(os.path.join(BASE_DIR, 'yolo_model_weight', 'best.pt'))
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

        test_sample = os.path.abspath(os.path.join(BASE_DIR, 'test_sample'))

        pill_name = [
            'ApurtranTablet150mg(Irbesartan)',
            'BalsanTablet80mg(Valsartan)',
            'BalthrepTablet160mg(Valsartan)',
            'DiosartanTablet160mg(Valsartan)',
            'EscitalTablet5mg(EscitalopramOxalate)',
            'ExbanTablet80mg(Valsartan)',
            'FeratracTablet2.5mg(Letrozole)',
            'GasbetTablet5mg(MosaprideCitrateHydrate)',
            'GasdialTablet50mg(DimethiconeMagnesium)',
            'GasprenTablet(MosaprideCitrateDihydrate)',
            'GasridTablet5mg(MosaprideCitrateHydrate)',
            'LipinonTablet80mg(AtorvastatinCalciumTrihydrate)',
            'NumentaminSustainedReleaseCapsule8mg(GalantamineBromide)',
            'RosorodTablet10mg(RosuvastatinCalcium)',
            'SarvaltanTablet160mg(Valsartan)',
            'SurosinDTablet(TamsulosinHydrochloride)',
            'ValsartanTablet(Valsartan)',
            'ValsartelTablet160mg(Valsartan)',
            'ValsartelTablet80mg(Valsartan)',
            'ZolpidemSustainedReleaseTablet(ZolpidemTartrate)'
        ]

        pill_name_kor = {
            'ApurtranTablet150mg(Irbesartan)': '아푸르탄정150밀리그램(이르베사르탄)',
            'BalsanTablet80mg(Valsartan)': '발산정80밀리그램(발사르탄)',
            'BalthrepTablet160mg(Valsartan)': '발트렙정160밀리그램(발사르탄)',
            'DiosartanTablet160mg(Valsartan)': '디오살탄정160밀리그램(발사르탄)',
            'EscitalTablet5mg(EscitalopramOxalate)': '에스시탈정5밀리그램(에스시탈로프람옥살산염)',
            'ExbanTablet80mg(Valsartan)': '엑스반정80밀리그램(발사르탄)',
            'FeratracTablet2.5mg(Letrozole)': '페라트라정2.5밀리그램(레트로졸)',
            'GasbetTablet5mg(MosaprideCitrateHydrate)': '가스베트정5밀리그램(모사프리드시트르산염수화물)',
            'GasdialTablet50mg(DimethiconeMagnesium)': '가스디알정50밀리그램(디메크로틴산마그네슘)',
            'GasprenTablet(MosaprideCitrateDihydrate)': '가스프렌정(모사프리드시트르산염이수화물)',
            'GasridTablet5mg(MosaprideCitrateHydrate)': '가스리드정5mg(모사프리드시트르산염수화물)',
            'LipinonTablet80mg(AtorvastatinCalciumTrihydrate)': '리피논정80밀리그램(아토르바스타틴칼슘삼수화물)',
            'NumentaminSustainedReleaseCapsule8mg(GalantamineBromide)': '뉴멘타민서방캡슐8밀리그램(갈란타민브롬화수소산염)',
            'RosorodTablet10mg(RosuvastatinCalcium)': '로수로드정10밀리그램(로수바스타틴칼슘)',
            'SarvaltanTablet160mg(Valsartan)': '사르발탄정160밀리그램(발사르탄)',
            'SurosinDTablet(TamsulosinHydrochloride)': '수로신디정(탐스로신염산염)',
            'ValsartanTablet(Valsartan)': '바르탄정(발사르탄)',
            'ValsartelTablet160mg(Valsartan)': '발사르텔정160밀리그램(발사르탄)',
            'ValsartelTablet80mg(Valsartan)': '발사르텔정80밀리그램(발사르탄)',
            'ZolpidemSustainedReleaseTablet(ZolpidemTartrate)': '졸뎀속붕정(졸피뎀타르타르산염)'
        }


        detected_pills = []
        bounding_boxs = []
        output_image_path = test_sample + '/merge_img_1.jpg'

        def draw_bboxes(image_path, bounding_boxs_, output_path=None):
            # image = cv2.imread(image_path)

            image_path.seek(0)
            image_data = np.frombuffer(image_path.read(), np.uint8)
            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            if image is None:
                print("Image could not be read.")

            h, w, _ = image.shape
            
            for i, line in enumerate(bounding_boxs_):
                x1, y1, x2, y2 = line
                
                color = (0, 255, 0)  # 초록색 바운딩 박스
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.putText(image, f'{detected_pills[i]}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            if output_path:
                cv2.imwrite(output_path, image)
            else:
                cv2.imshow('Image with Bounding Boxes', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        def delete_images_in_folder(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                try:
                    if os.path.isfile(file_path) and file_name.endswith(('.jpg', '.jpeg', '.png')):
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

        def test_backend(img_dir):
            from tensorflow.keras.models import load_model

            model_path = os.path.abspath(os.path.join(BASE_DIR, 'Pill_image_mobile_net.h5'))
            model = load_model(model_path)

            image = Image.open(img_dir)
            image = image.resize((100, 100))
            image = np.array(image)
            image = image/255.
            
            plt.imshow(image)
            plt.show()
            
            image = np.reshape(image, (1, 100, 100, 3))
            
            prediction = model.predict(image)
            prediction.shape
            pred_class = np.argmax(prediction, axis=-1)

            print(pill_name[int(pred_class)])
            return pill_name[int(pred_class)][:]
        
        def detect_and_crop_objects(image_path):
            # img = cv2.imread(image_path)

            image_path.seek(0)
            image_data = np.frombuffer(image_path.read(), np.uint8)
            img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

            if img is None:
                print("Image could not be read.")

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = model(img_rgb)

            bbox_list = results.xyxy[0].cpu().numpy()
            cropped_images = []

            print(len(bbox_list))

            for idx, bbox in enumerate(bbox_list):
                xmin, ymin, xmax, ymax, confidence, cls = map(int, bbox)
                
                cropped_img = img[ymin:ymax, xmin:xmax]
                cropped_images.append(cropped_img)  

                crop_output_path = test_sample
                os.makedirs(crop_output_path, exist_ok=True)
                crop_file_path = os.path.join(crop_output_path, f"{os.path.basename(image_path.name).split('.')[0]}_crop_{idx}.jpg")
                cv2.imwrite(crop_file_path, cropped_img)

                bounding_boxs.append([xmin, ymin, xmax, ymax])
                
                pills = test_backend(crop_file_path)
                print(pills)
                detected_pills.append(pills)

        picture = request.FILES.get('picture')
        patient_name = request.POST.get('patient')
        # patient_name이 None이라서 임시로.
        # patient_name = '정윤성'
        patient = Patient.objects.get(name=patient_name)

        detect_and_crop_objects(picture)
        draw_bboxes(picture, bounding_boxs, output_image_path)

        # 분석 결과: 약물 이름 리스트
        medicine_list = []
        for pill in detected_pills:
            medicine_list.append(pill_name_kor[pill])
        print(medicine_list)

        # 사진 분석 과정에서 생성된 사진 삭제
        delete_images_in_folder(test_sample)

        # DB에 약물 정보 저장
        for medicine_name in medicine_list:
            Medication.objects.create(patient=patient, medication_name=medicine_name)

        # 병용금기 약물 리스트
        no_combination_list = []

        for medi_name in medicine_list:
            try:
                medication = MedicationInfo.objects.get(medication_name=medi_name)
                no_combination_info = NoCombination.objects.filter(medication_name=medication)

                if no_combination_info.exists():
                    serializer = NoCombinationSerializer(no_combination_info, many=True)
                    mix_medication_names = [item['mix_medication_name'] for item in serializer.data]
                    no_combination_list.extend(mix_medication_names)
            except MedicationInfo.DoesNotExist:
                continue

        no_combination_list = list(set(no_combination_list))

        # TODO: 사진 분석 결과를 프론트로 다시 전송(Response)
        return Response({'medication_list': medicine_list, 'no_combination_list': no_combination_list})

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
        medication_name = request.data.get('medication_name').rstrip() # 약물 이름
        medication = MedicationInfo.objects.get(medication_name=medication_name)

        no_combination_info = NoCombination.objects.filter(medication_name=medication)
        serializer = NoCombinationSerializer(no_combination_info, many=True)
        mix_medication_names = [item['mix_medication_name'] for item in serializer.data]

        return Response({'no_mixture': mix_medication_names}, status=status.HTTP_200_OK)

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
