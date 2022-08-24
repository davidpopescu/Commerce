from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_Listing, name="create"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("watchList", views.watch, name="watchList"),
    path("addwatchList/<int:id>", views.addwatchList, name="addwatchList"),
    path("closed/<int:id>", views.closed, name="closed"),
    path("newComment/<int:id>", views.newComment, name="newComment"),
    path("category", views.category, name="category"),
    path("categories/<str:category>", views.categories, name="categories"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'auctions.views.handler404'