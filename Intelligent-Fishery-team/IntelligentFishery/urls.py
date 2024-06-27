"""
URL configuration for IntelligentFishery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

from fishery.fish_views import get_data, fish_list, get_weight_data, water_list, get_water_data
from fishery.views import (
    login,
    register,
    homepage,
    user,
    illustration,
    main_info,
    underwater_system,
    data_center,
    intelligence_center,
    admin_management,
)


urlpatterns = [
    path("fishery/login/", login, name="login"),
    path("fishery/register/", register, name="register"),
    path("fishery/homepage/", homepage, name="homepage"),
    path("fishery/user/", user, name="user"),
    path("fishery/illustration/", illustration, name="illustration"),
    path("fishery/main_info/", main_info, name="main_info"),
    path("fishery/underwater_system/", underwater_system, name="underwater_system"),
    path("fishery/data_center/", data_center, name="data_center"),
    path(
        "fishery/intelligence_center/", intelligence_center, name="intelligence_center"
    ),
    path("fishery/admin_management/", admin_management, name="admin_management"),
    # fish
    path("fishery/fish_list/", fish_list, name="fish_list"),
    path("fishery/get_data/", get_data, name="get_data"),
    path("fishery/get_weight_data/", get_weight_data, name="get_weight_data"),
    # water
    path("fishery/water_list/", water_list, name="water_list"),
    path("fishery/get_water_data/", get_water_data, name="get_water_data"),
    path('', include('chat.urls')),  # 包含 chat 应用的 URLs
    path('', include('users.urls')),
]
