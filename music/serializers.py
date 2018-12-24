from rest_framework import serializers
from .models import ArtistScore, Artist, MusicCategory, Music, Profile
from django.contrib.auth.models import User


class UserMusicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Music
        fields = (
            'url',
            'name')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'url', 'pk','user', 'date_of_birth', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    musics = UserMusicSerializer(many=True, read_only=True)
    profiles = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'musics',
            'profiles',
            'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MusicCategorySerializer(serializers.HyperlinkedModelSerializer):
    musics = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='music-detail')

    class Meta:
        model = MusicCategory
        fields = ('url', 'pk','name', 'musics')

class MusicSerializer(serializers.HyperlinkedModelSerializer):
    # We just want to display the owner username (read-only)
    owner = serializers.ReadOnlyField(source='owner.username')
    # adding image
    image = serializers.ImageField(max_length=None, use_url=True)
    # adding video
    video = serializers.FileField(max_length=None, use_url=True)
    # Display category name instead of id
    music_category = serializers.SlugRelatedField(queryset=MusicCategory.objects.all(), slug_field='name')

    class Meta:
        model = Music
        fields = ('url', 'pk', 'owner', 'name', 'release_date', 'image', 'video', 'music_category' )

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # Display all details for music
    music = MusicSerializer()

    class Meta:
        model = ArtistScore
        fields = ('url', 'pk', 'score', 'score_date', 'music')

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Artist.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Artist
        fields = ('url', 'name', 'gender', 'gender_description', 'scores')

class ArtistScoreSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(queryset=Artist.objects.all(), slug_field='name')
    # display the music's name instead of id
    music = serializers.SlugRelatedField(queryset=Music.objects.all(), slug_field='name')

    class Meta:
        model = ArtistScore
        fields = ('url', 'pk','score', 'score_date', 'artist','music' )