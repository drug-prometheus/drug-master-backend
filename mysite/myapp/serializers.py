from rest_framework import serializers
from .models import Patient, Pharmacist, PatientNote, Medication, MedicationInfo
from .models import NoCombination

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name']

class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ['id', 'name']

class PatientNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNote
        fields = ['id', 'patient', 'pharmacist', 'note', 'created_at']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class MedicationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationInfo
        fields = '__all__'

class NoCombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoCombination
        fields = '__all__'