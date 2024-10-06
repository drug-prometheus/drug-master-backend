from django.contrib import admin
from django.urls import path
from myapp.views import AnalyzingMedicine, AddMedicineInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyzing-medicine/', AnalyzingMedicine.as_view(), name='analyzing-medicine'), # 사진 업로드하면 약물 분석
    path('add-medicine-info/', AddMedicineInfo.as_view(), name='add-medicine-info'), # 약물 정보 받아서 DB에 저장
    
]
