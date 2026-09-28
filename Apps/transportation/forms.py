from django import forms
from django.utils import timezone

from .models import (
    RouteStop,
    StudentTransport,
    TransportAttendance,
    TransportRoute,
    Vehicle,
)


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "name",
            "registration_number",
            "vehicle_type",
            "capacity",
            "driver_name",
            "driver_phone",
            "route_name",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "vehicle_type": forms.Select(attrs={"class": "form-select"}),
            "capacity": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "driver_name": forms.TextInput(attrs={"class": "form-control"}),
            "driver_phone": forms.TextInput(attrs={"class": "form-control"}),
            "route_name": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TransportRouteForm(forms.ModelForm):
    class Meta:
        model = TransportRoute
        fields = [
            "name",
            "description",
            "pickup_time",
            "drop_time",
            "fare",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "pickup_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "drop_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "fare": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class RouteStopForm(forms.ModelForm):
    class Meta:
        model = RouteStop
        fields = ["route", "name", "stop_order", "pickup_time"]
        widgets = {
            "route": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "stop_order": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "pickup_time": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
        }


class StudentTransportForm(forms.ModelForm):
    class Meta:
        model = StudentTransport
        fields = [
            "student",
            "route",
            "pickup_stop",
            "vehicle",
            "start_date",
            "end_date",
            "is_active",
        ]
        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "route": forms.Select(attrs={"class": "form-select"}),
            "pickup_stop": forms.Select(attrs={"class": "form-select"}),
            "vehicle": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["route"].queryset = TransportRoute.objects.filter(
            is_active=True
        )
        self.fields["vehicle"].queryset = Vehicle.objects.filter(
            is_active=True
        )
        self.fields["pickup_stop"].queryset = RouteStop.objects.filter(
            route__is_active=True
        )

        if not self.instance.pk and not self.initial.get("start_date"):
            self.initial["start_date"] = timezone.localdate()

    def clean(self):
        cleaned_data = super().clean()
        route = cleaned_data.get("route")
        pickup_stop = cleaned_data.get("pickup_stop")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if route and pickup_stop and pickup_stop.route_id != route.id:
            self.add_error(
                "pickup_stop",
                "Pickup stop must belong to the selected route.",
            )

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "End date cannot be earlier than the start date.",
            )

        return cleaned_data


class TransportAttendanceForm(forms.ModelForm):
    class Meta:
        model = TransportAttendance
        fields = ["assignment", "date", "status", "remarks"]
        widgets = {
            "assignment": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assignment"].queryset = StudentTransport.objects.filter(
            is_active=True
        )

        if not self.instance.pk and not self.initial.get("date"):
            self.initial["date"] = timezone.localdate()