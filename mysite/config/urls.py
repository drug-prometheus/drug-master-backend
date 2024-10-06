from django.contrib import admin
from django.urls import path
from myapp.views import AnalyzingMedicine, AddMedicineInfo, SearchMedicine, PharmacistOpinion
from myapp.views import PharmacistWithPatients

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyzing-medicine/', AnalyzingMedicine.as_view(), name='analyzing-medicine'), # 사진 업로드하면 약물 분석
    path('add-medicine-info/', AddMedicineInfo.as_view(), name='add-medicine-info'), # 약물 정보 받아서 DB에 저장
    path('search-medicine/', SearchMedicine.as_view(), name='search-medicine'), # 약물 검색
    path('pharmacist-opinion/', PharmacistOpinion.as_view(), name='pharmacist-opinion'), # 약사 소견
    path('pharmacist-with-patients/', PharmacistWithPatients.as_view(), name='pharmacist-with-patients'), # 약사가 관리하는 환자 이름들
]
