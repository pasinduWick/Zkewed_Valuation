from django.urls import path

from . import views

urlpatterns = [ path("", views.valuation, name="valuation"),
                path("valuation", views.valuation, name="valuation"),
                # path("verification", views.Verification, name="verification"),
                # path("RPA", views.RPA, name="RPA"),
                # path("moderate", views.moderate, name = "moderate")
                
                ]