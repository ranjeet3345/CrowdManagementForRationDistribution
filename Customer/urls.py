
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('signup/', views.signup_view, name='signup'),
    path('staffForm/',views.editStaffProfile,name='staff_complete_profile'),
    path('customerForm/',views.editCustomerProfile,name='customer_complete_profile'),
    path('profile/', views.view_profile, name='view_profile'),
    path('bookToken/<int:staff_id>/', views.book_token, name='book_token'),
    path('allStaffList/',views.allStaffView,name="allStaffList"),
    path('allCustomerList/',views.allCustomerView,name="allCustomerList"),
    path('showStaffDashboard/<int:staff_id>',views.showStaffDashBoard,name='showStaffDashboard'),
    path('showStaffDashboard1/<int:token_id>',views.customerInQueue,name='showStaffDashboard1'),
    path('showStaffDashboard2/<int:token_id>',views.haveTakenRation,name='showStaffDashboard2'),


]
