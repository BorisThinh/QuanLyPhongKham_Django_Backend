from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import patient, examination_schedule, receipt_medicine, medicine, receipt_medicine_detail, \
    category_medicine, bill, Comment, User, Like, Rating
from .serializers import PatientSerializer, ExaminationScheduleSerializer, ReceiptMedicineSerializer,\
    MedicineSerializer, ReceiptMedicineDetailSerializer, CategoryMedicineSerializer, BillSerializer,\
    CommentSerializer, CreateCommentsSerializer, UserSerializer, MedicineDetailSerializer
from django.conf import settings


def index(request):
    return HttpResponse("e-Clinic App")


class PatientViewSet(viewsets.ModelViewSet):
    queryset = patient.objects.filter(active=True)
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ExaminationScheduleViewSet(viewsets.ModelViewSet):
    queryset = examination_schedule.objects.filter(active=True)
    serializer_class = ExaminationScheduleSerializer
    # permission_classes = [permissions.IsAuthenticated]





class ReceiptMedicineViewSet(viewsets.ModelViewSet):
    queryset = receipt_medicine.objects.filter(active=True)
    serializer_class = ReceiptMedicineSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'get_medicine':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(str(patient__icontains=kw))

        id = self.request.query_params.get('id')
        if id:
            query = query.filter(id=id)

        return query

    @action(methods=['get'], detail=True, url_path='detail')
    def get_detail(self, request, pk):
        receipt_medicine_detail = self.get_object().detail

        return Response(data=ReceiptMedicineDetailSerializer(receipt_medicine_detail, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)



class MedicineViewSet(viewsets.ModelViewSet):
    queryset = medicine.objects.filter(active=True)
    serializer_class = MedicineDetailSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        medicines = medicine.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            medicines = medicines.filter(name__contains=q)


        return medicines


    def get_permissions(self):
        if self.action in ['like', 'rating']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        medicine = self.get_object()
        comments = medicine.comment.select_related('user').filter(active=True)

        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        medicine = self.get_object()
        user = request.user  # lấy user đã chứng thực đang đăng nhập

        l, _ = Like.objects.get_or_create(medicine=medicine, user=user)  # vừa update vừa tạo mới Like
        l.active = not l.active
        l.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        if 'rate' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        medicine = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(medicine=medicine, user=user)
        r.rate = request.data.get('rate')
        r.save()

        return Response(status=status.HTTP_201_CREATED)


class ReceiptMedicineDetailViewSet(viewsets.ModelViewSet):
    queryset = receipt_medicine_detail.objects.filter(active=True)
    serializer_class = ReceiptMedicineDetailSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'add_medicine':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


    @action(methods=['post'],detail=True,url_path='add-medicine')
    def add_medicine(self,request,pk):
        medicine = request.data.get('medicine')
        if medicine:
            n = medicine(medicine=medicine,receipt=self.get_object(),creator=request.user)

        return Response(MedicineSerializer(n).data,status=status.HTTP_201_CREATED)


        return Response(status=status.HTTP_400_BAD_REQUEST)






class CategoryMedicineViewSet(viewsets.ModelViewSet):
    queryset = category_medicine.objects.filter(active=True)
    serializer_class = CategoryMedicineSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)

        id = self.request.query_params.get('id')
        if id:
            query = query.filter(id=id)

        return query

    @action(methods=['get'], detail=True, url_path='medicine')
    def get_medicine(self, request, pk):
        medicines = self.get_object().medicine

        return Response(
            data=MedicineSerializer(medicines, many=True, context={'request': request}).data,
            status=status.HTTP_200_OK)


class BillViewSet(viewsets.ModelViewSet):
    queryset = bill.objects.filter(active=True)
    serializer_class = BillSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permission(self):
        if self.action in ['update', 'delete']:
            # request.user
            # request.data.user
            pass

        return [permissions.IsAuthenticated()]


class UserViewSet(viewsets.ViewSet,generics.CreateAPIView,generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser,]

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'],url_path="current-user",detail=False)
    def current_user(self,request):
        return Response(self.serializer_class(request.user,context={'request':request}).data,status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self,request):
        return Response(settings.OAUTH2_INFO,status=status.HTTP_200_OK)

