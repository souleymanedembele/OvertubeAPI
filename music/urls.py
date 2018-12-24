from django.conf.urls import url
from music import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   url(r'^music-categories/$',
    views.MusicCategoryList.as_view(),
    name=views.MusicCategoryList.name),

    url(r'^music-categories/(?P<pk>[0-9]+)/$',
        views.MusicCategoryDetail.as_view(),
        name=views.MusicCategoryDetail.name),

    url(r'^music/$',
        views.MusicList.as_view(),
        name=views.MusicList.name),

    url(r'^music/(?P<pk>[0-9]+)/$',
        views.MusicDetail.as_view(),
        name=views.MusicDetail.name),

    url(r'^artist/$',
        views.ArtistList.as_view(),
        name=views.ArtistList.name),

    url(r'^artist/(?P<pk>[0-9]+)/$',
        views.ArtistDetail.as_view(),
        name=views.ArtistDetail.name),

    url(r'^artist-scores/$',
        views.ArtistScoreList.as_view(),
        name=views.ArtistScoreList.name),

    url(r'^artist-score/(?P<pk>[0-9]+)/$',
        views.ArtistScoreDetail.as_view(),
        name=views.ArtistScoreDetail.name),

    url(r'^users/$',
        views.UserList.as_view(),
        name=views.UserList.name),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name=views.UserDetail.name),

      url(r'^profile/$',
          views.ProfileList.as_view(),
          name=views.ProfileList.name),

      url(r'^profile/(?P<pk>[0-9]+)/$',
          views.ProfileDetail.as_view(),
          name=views.ProfileDetail.name),

    url(r'^$', views.ApiRoot.as_view(), name=views.ApiRoot.name)
]+ static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)