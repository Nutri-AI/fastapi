from fastapi import APIRouter, HTTPException, status, UploadFile, File

from app_v2.domain.domain import NutrientsName

from app_v2.domain.domain import UserDomain, LogDomain, UserJoinModel, physique

class UserRouter:
    def __init__(self, domain: UserDomain):
        self.__domain= domain

    @property
    def router(self):
        api_router= APIRouter(prefix= '/user', tags= ['user'])

        @api_router.get('/')
        def root():
            return 'Welcome Here!'

        ####1 신규 유저 가입
        @api_router.post('/join')
        def join_user(request: UserJoinModel):
            try:
                return self.__domain.join_user(request)
            except:
                raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail= 'Please enter the appropriate format for the item')

        ####2 유저 정보 업데이트 - physique, RDI 수정
        @api_router.put('/update/{userid}')
        def update_user_physique(userid: str, physique: physique):
            return self.__domain.update_user_physique(userid, physique)

        ####3 유저 physique 정보 요청
        @api_router.get('/get/physique/{userid}')
        def get_user_physique(userid: str):
            return self.__domain.get_user_physique(userid)

        ####4 유저 정보 요청
        @api_router.get('/info/{userid}')
        def get_user(userid):
            try:
                return self.__domain.get_user(userid)
            except:
                raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'No exist userid')

        ####5 유저 정보 삭제
        @api_router.delete('/delete/{userid}')
        def delete_user(userid: str):
            return self.__domain.delete_user(userid)

        ####6 유저 RDI 정보 요청
        @api_router.get('/get/RDI/{userid}')
        def get_user_RDI(userid: str):
            return self.__domain.get_user_RDI(userid)

        ####7 nutr_suppl 수정 - 영양제 추가 등록 및 수정
        @api_router.put('/update/nutrients/{userid}')
        def update_user_nutr_suppl(userid: str, nutrsuppl: NutrientsName):
            return self.__domain.update_user_nutr_suppl(userid, nutrsuppl)
        
        ####8 유저 nutr_suppl 정보 요청
        @api_router.get('/get/nutr/suppl/{userid}')
        def get_user_nutr_suppl(userid: str):
            return self.__domain.get_user_nutr_suppl(userid)


        return api_router
        
class LogRouter:
    def __init__(self, domain: LogDomain):
        self.__domain= domain
    
    @property
    def router(self):
        api_router= APIRouter(prefix= '/log', tags= ['log'])

        ####1 이미지 S3로 업로드
        @api_router.post('/upload/image/{userid}')
        def upload_image(userid: str, image: UploadFile= File(...)):
            return self.__domain.upload_image(userid, image)

        ####2 음식 영양 성분 요청
        @api_router.get('/get/food/nutrients')
        def get_food_nutrients(food_cat: str, food_name: str):
            return self.__domain.get_food_nutrients(food_cat, food_name)

        ####3 유저 식단 섭취 로그 등록
        @api_router.post('/post/meal/log/{userid}')
        def post_meal_log(userid: str, image_key, food_list):
            return self.__domain.post_meal_log(userid, image_key, food_list)

        ####4 유저 식단 섭취 로그 정보 요청 - 특정 날
        @api_router.get('/get/meal/log/{userid}')
        def get_meal_log(userid: str, date):
            return self.__domain.get_meal_log(userid, date)

        ####5 유저 식단 섭취 로그 삭제 - 특정 시간(시기)
        @api_router.delete('/delete/meal/log/{userid}')
        def delete_meal_log(self, userid: str, datetime):
            return self.__domain.delete_meal_log(userid, datetime)
        
        ####6 영양제 영양성분 정보 요청
        @api_router.get('/get/nutr_suppl/nutrients')
        def get_nutr_suppl_nutrients(nutr_cat: str, product_code: str):
            return self.__domain.get_nutr_suppl_nutrients(nutr_cat, product_code)

        ####7 유저 영양제 섭취 로그 등록
        @api_router.post('/post/nutrtake/log/{userid}')
        def post_nutrtake_log(userid: str, nutr_suppl_list):
            return self.__domain.post_nutrtake_log(userid, nutr_suppl_list)

        ####8 유저 영양제 섭취 로그 정보 요청 - 특정 날
        @api_router.get('/get/nutrtake/log/{userid}')
        def get_nutrtake_log(userid: str, date):
            return self.__domain.get_nutrtake_log(userid, date)

        ####9 유저 영양제 섭취 로그 삭제 - 특정 시간(시기)
        @api_router.delete('/delete/nutrtake/log/{userid}')
        def delete_nutrtake_log(userid: str, datetime):
            return self.__domain.delete_nutrtake_log(userid, datetime)

        ####10 유저 영양 상태 식단 로그 입력 & 업데이트
        @api_router.put('/update/meal/nutr/log/{userid}')
        def update_user_meal_nutr_log(userid: str, nutrients):
            return self.__domain.update_user_meal_nutr_log(userid, nutrients)
        
        ####11 유저 영양 상태 영양제 로그 입력 & 업데이트
        @api_router.put('/update/nutrtake/nutr/log/{userid}')
        def update_user_nutrtake_nutr_log(userid: str, nutrients):
            return self.__domain.update_user_nutrtake_nutr_log(userid, nutrients)

        ####12 유저 영양 상태 로그 정보 요청 - 특정 날
        @api_router.get('/get/nutr/lod/{userid}')
        def get_user_nutr_log(userid: str, date):
            return self.__domain.get_user_nutr_log(userid, date)

        ####13 유저 영양제 추천
        @api_router.get('/recommend/nutrients/{userid}')
        def recommend_nutrients(userid: str, request):
            # request는 부족 영양소?
            return self.__domain.recommend_nutrients(userid, request)

        return api_router