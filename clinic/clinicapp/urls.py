from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(prefix='patient', viewset=views.PatientViewSet, basename="patient")
router.register(prefix='examination_schedule', viewset=views.ExaminationScheduleViewSet, basename='examination_schedule')
router.register(prefix='receipt_medicine', viewset=views.ReceiptMedicineViewSet, basename='receipt_medicine')
router.register(prefix='medicine', viewset=views.MedicineViewSet, basename='medicine')
router.register(prefix='receipt_medicine_detail', viewset=views.ReceiptMedicineDetailViewSet, basename='reciept_medicine_detail')
router.register(prefix='category_medicine', viewset=views.CategoryMedicineViewSet, basename='category_medicine')
router.register(prefix='bill', viewset=views.BillViewSet, basename='bill')
router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')
router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/',views.AuthInfo.as_view()),

]