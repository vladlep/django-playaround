from django.db import transaction
from rest_framework import serializers
from .models import CostLine, Cost


class CostLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostLine
        fields = ('amount', 'tax_rate')


class CostSerializerV2(serializers.ModelSerializer):
    """
    V2 CostSerializer.
    """
    number = serializers.CharField(max_length=50, required=False)
    cost_lines = CostLineSerializer(many=True, required=False)

    class Meta:
        model = Cost
        fields = ("id", 'number', "amount", "description", 'date', 'image', 'cost_lines')

    @staticmethod
    def _prepare_cost_lines(cost_lines, cost):
        line_objects = []
        line_fields = list(CostLineSerializer().fields.fields)
        for a_line in cost_lines:
            for key in a_line.keys():
                if key not in line_fields:
                    a_line.pop(key, None)
            a_object = CostLine(cost=cost, **a_line)
            line_objects.append(a_object)
        return line_objects

    @transaction.atomic
    def update(self, instance, validated_data):
        cost_lines = validated_data.pop('cost_lines', None)
        Cost.objects.filter(id=instance.id).update(**validated_data)
        instance = Cost.objects.get(id=instance.id) # get newly updated object
        if cost_lines:
            line_objects = CostSerializerV2._prepare_cost_lines(cost_lines, instance)
            CostLine.objects.filter(cost=instance).delete()
            CostLine.objects.bulk_create(line_objects)
        return instance

    @transaction.atomic
    def create(self, validated_data):
        cost_lines = validated_data.pop('cost_lines', None)
        cost = Cost.objects.create(**validated_data)
        if cost_lines:
            line_objects = CostSerializerV2._prepare_cost_lines(cost_lines, cost)
            CostLine.objects.bulk_create(line_objects)
        return cost