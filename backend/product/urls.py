from django.urls import path

from .views import (
    LatestProductsList,
    ProductDetail,
    CategoryDetail,
    CategoryList,
    Search,
)

urlpatterns = [
    path("latest-products/", LatestProductsList.as_view()),
    path("categories/", CategoryList.as_view()),
    path("products/search/", Search.as_view()),
    path(
        "products/<slug:category_slug>/<slug:product_slug>/",
        ProductDetail.as_view(),
    ),
    path("products/<slug:category_slug>/", CategoryDetail.as_view()),
]
