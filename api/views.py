from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserModel, Employer
from .serializers import SignUpSerializer, ProfileSerializer, EmployerSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class SignUp(APIView):
    def post(self, request):
        data = request.data
        serializers = SignUpSerializer(data = data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class SignIn(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = UserModel.objects.get(username = username)

        try:
            if user.check_password(password):
                token = Token.objects.get(user= user)
                return Response(
                    {
                        "token":token.key,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({
                    'message':"password invalid!"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            
        except UserModel.DoesNotExist:
            return Response(
                {'message':"username is not valid !"},
                status=status.HTTP_400_BAD_REQUEST
            )


class MyProfile(APIView):    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializers = ProfileSerializer(user)
        return Response(serializers.data, status=status.HTTP_200_OK)

class EmployerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user= request.user

        employees = Employer.objects.filter(user = user)
        
        serializers = EmployerSerializer(employees, many=True)
       
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serrializers = EmployerSerializer(data = data) 
        if serrializers.is_valid():
            serrializers.save()
            return Response(serrializers.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serrializers.errors, status=status.HTTP_400_BAD_REQUEST)
       




class EmployerDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            employee = Employer.objects.get(id = pk)
            if employee.user ==request.user:
                serializer = EmployerSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                   {
                        'message':'you are not the valid user for access the employee!'
                   },
                   status=status.HTTP_200_OK
                )
            
        except Employer.DoesNotExist:
            return Response({
                "message":"employee is not found"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request , pk):
        data = request.data
        data['user'] = request.user.id
        try:
            employee = Employer.objects.get(id = pk)
            if employee.user ==request.user:
                serializer = EmployerSerializer(instance = employee, data = data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                   {
                        'message':'you are not the valid user for access the employee!'
                   },
                   status=status.HTTP_200_OK
                )
            
        except Employer.DoesNotExist:
            return Response({
                "message":"employee is not found"
            },
            status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request , pk):
    
        try:
            employee = Employer.objects.get(id = pk)
            if employee.user ==request.user:
                employee.delete()
                return Response(
                    {
                        'message':'delete successfully!'
                    },
                    status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                   {
                        'message':'you are not the valid user for access the employee!'
                   },
                   status=status.HTTP_200_OK
                )
            
        except Employer.DoesNotExist:
            return Response({
                "message":"employee is not found"
            },
            status=status.HTTP_400_BAD_REQUEST
            )





class LogOut(APIView):    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token = Token.objects.get(user = user)
        token.delete()
        token = token.objects.create(user= user)
        token.save()
    
        return Response({
            'message':'logout success! token has been change!'
        }, status=status.HTTP_200_OK)