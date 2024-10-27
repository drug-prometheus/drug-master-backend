from django.contrib import admin
from django.urls import path
from myapp.views import AnalyzingMedicine, AddMedicineInfo, SearchMedicine, PharmacistOpinion
from myapp.views import PharmacistWithPatients, LoginView, LogoutView, SeeMediInfo, SavePharmacistOpinion
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyzing-medicine/', AnalyzingMedicine.as_view(), name='analyzing-medicine'), # 사진 업로드하면 약물 분석
    path('add-medicine-info/', AddMedicineInfo.as_view(), name='add-medicine-info'), # 약물 정보 받아서 DB에 저장
    path('search-medicine/', SearchMedicine.as_view(), name='search-medicine'), # 약물 검색
    path('pharmacist-opinion/', PharmacistOpinion.as_view(), name='pharmacist-opinion'), # 약사 소견
    path('pharmacist-with-patients/', PharmacistWithPatients.as_view(), name='pharmacist-with-patients'), # 약사가 관리하는 환자 이름들
    path('login/', LoginView.as_view(), name='login'), # login
    path('logout/', LogoutView.as_view(), name='logout'), # logout
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('see-medi-info/', SeeMediInfo.as_view(), name='see-medi-info'), # 메인 화면에서 약물 정보 보기
    path('save-pharmacist-opinion/', SavePharmacistOpinion.as_view(), name='save-pharmacist-opinion'), # 약사 소견 DB에 저장
]
