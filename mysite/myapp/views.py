from rest_framework.views import APIView
from rest_framework.response import Response

# 프론트에서 약물 사진 받아와서 분석 후 프론트로 분석 결과 전송
class AnalyzingMedicine(APIView):

    def post(self, request, format=None):
        # TODO: 프론트에서 업로드한 사진 받아오기
        # TODO: 약물 사진 업로드하면 분석해주는 AI 모델 연결해서 사진 분석
        # TODO: 사진 분석 결과를 프론트로 다시 전송(Response)

        # ENDPOINT: 사진
        # ENDPOINT: 분석 결과(약물 이름 리스트, 약물 개수)

        return Response()

# 프론트에서 입력한 약물 정보 받아와서 DB에 추가    
class AddMedicineInfo(APIView):

    def post(self, request, format=None):
        # TODO: 받아온 약물 정보(이름, 복약 횟수 등)을 DB에 저장

        # ENDPOINT: 약물 정보(이름, 복약 횟수, ???)

        pass

# 약 이름 검색(MainPage, SearchDrugPage)
class SearchMedicine(APIView):

    def post(self, request, format=None):
        # TODO: DB에서 약 이름과 일치하는 데이터 가져와서 프론트로 보내기

        # ENDPOINT: 약 데이터(약물 이름, ???)

        pass

# DB(약사 소견 입력돼 있는 DB)에서 환자 이름과 일치하는 소견 데이터 불러와서 프론트로 전송
class PharmacistOpinion(APIView):

    def post(self, request, format=None):
        # 여기서 말하는 DB는 약사 소견 입력돼 있는 DB
        # TODO: DB에서 환자 이름과 일치하는 소견 데이터 불러와서 프론트로 전송

        # ENDPOINT: 약사 소견?

        pass