from django.shortcuts import render
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser

from music.authentication import BearerAuthentication
from .models import Music, MusicCategory, ArtistScore, Artist, Profile
from .serializers import MusicSerializer, MusicCategorySerializer, ArtistScoreSerializer, ArtistSerializer, \
    UserProfileSerializer
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        })

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

class MusicCategoryList(generics.ListCreateAPIView):
    queryset = MusicCategory.objects.all()
    serializer_class = MusicCategorySerializer
    name = 'musiccategory-list'


class MusicCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MusicCategory.objects.all()
    serializer_class = MusicCategorySerializer
    name = 'musiccategory-detail'

# Profile view
class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-list'

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'profile-detail'



class MusicList(generics.ListCreateAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    name = 'music-list'

    @detail_route(methods=['post'])
    def upload_docs(request):
        try:
            file = request.data['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
    #parser_classes = (MultiPartParser,)

   # def post(self, request, format=None):
        # to access files
     #   print(request.FILES)
        # to access data
    #    print(request.data)
      #  return Response({'received data': request.data})
#
    authentication_classes = (BearerAuthentication,)
    #permission_classes = (
      #  permissions.IsAuthenticated,
     #   IsOwnerOrReadOnly,)
    #permission_classes = (
     #  permissions.IsAuthenticatedOrReadOnly,
     #  IsOwnerOrReadOnly, )

    def perform_create(self , serializer):
        # Pass an additional owner field to the create method
        # To Set the owner to the user received in the request
        serializer.save(owner=self.request.user)

#class FileUploadView(views.APIView):
 #   parser_classes = (FileUploadParser,)

 #   def post(self, request, filename, format=None):
   #     file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
   #     return Response(status=204)

class MusicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    name = 'music-detail'
    authentication_classes = (BearerAuthentication,)
    permission_classes = (
      permissions.IsAuthenticated,
       IsOwnerOrReadOnly,)
   # permission_classes = (
  #      permissions.IsAuthenticatedOrReadOnly,
   #     IsOwnerOrReadOnly,
   #  )


class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = 'artist-list'


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    name = 'artist-detail'


class ArtistScoreList(generics.ListCreateAPIView):
    queryset = ArtistScore.objects.all()
    serializer_class = ArtistScoreSerializer
    name = 'artistscore-list'

class ArtistScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArtistScore.objects.all()
    serializer_class = ArtistScoreSerializer
    name = 'artistscore-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'artist': reverse(ArtistList.name, request = request),
            'music-categories': reverse(MusicCategoryList.name, request = request),
            'musics': reverse(MusicList.name, request=request),
            'scores': reverse(ArtistScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
            'profiles': reverse(ProfileList.name, request=request)
        })


