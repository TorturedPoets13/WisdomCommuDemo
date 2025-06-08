#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
from django.db.models import Count, F
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.filters import BaseFilterBackend
from api.serializers.bank import BankCreateModelSerializer, BankListModelSerializer, StatisticsListSerializer, \
    ActivityModelListSerializer, GoodsListSerializer
from api import models
from rest_framework.pagination import LimitOffsetPagination


class BankView(ListAPIView, CreateAPIView, DestroyAPIView):
    queryset = models.UserInfo.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BankCreateModelSerializer
        return BankListModelSerializer

    def delete(self, request, *args, **kwargs):
        user_object = self.get_object()
        from utils import ai
        ai.delete(user_object.uid, user_object.face_token)
        response = super().delete(request, *args, **kwargs)
        return response


class StatisticsView(ListAPIView):
    queryset = models.UserInfo.objects.values('create_date').annotate(count=Count('create_date')).order_by(
        "-create_date") # 其实就是在做一个group by 解释在笔记文件夹--》小程序--》笔记txt
    serializer_class = StatisticsListSerializer


class FaceView(APIView):
    """
    人脸检测，用户提交图片，后台根据图片进行人脸搜索。
    """

    def post(self, request, *args, **kwargs):
        avatar_object = request.data.get('avatar')
        if not avatar_object:
            return Response({"msg": "未提交图像", "status": False})
        from utils import ai
        result = ai.search(avatar_object)
        print(result)

        score = 0
        if result["error_code"] == 0:
            user_id = result["result"]['user_list'][0]['user_id']
            obj = models.UserInfo.objects.filter(uid=user_id).first()
            score = obj.score

        return Response({"content": result, "status": True, 'score': score})


class VoiceView(APIView):
    def post(self, request, *args, **kwargs):
        voice_object = request.data.get('voice')
        from utils import ai
        result = ai.speed(voice_object)
        # {'corpus_no': '6847771638436561158', 'result': ['今天天气很好呢，一起去散步吧'], 'sn': '15921476781594371078', 'err_msg': 'success.', 'err_no': 0}
        return Response(result)


from rest_framework.filters import BaseFilterBackend


class PullDownFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get("max_id")
        if max_id:
            # [9, 8, 7 ]   [7,8,9]
            queryset = queryset.filter(id__gt=max_id)
            # queryset = queryset.filter(id__gt=max_id).reverse()
        return queryset


class ReachBottomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get("min_id")
        if min_id:
            queryset = queryset.filter(id__lt=min_id)
        return queryset

class MineFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        uid = request.query_params.get("user_id")
        if not uid:
            return queryset

        user_object = models.UserInfo.objects.filter(uid=uid).first()
        if not user_object:
            return queryset.none()

        # queryset = models.Activity.objects.filter(xxx=user_object)
        queryset = queryset.filter(ac__user=user_object)
        return queryset


from rest_framework.pagination import LimitOffsetPagination


class DemoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2

    def get_offset(self, request):
        return 0

    def get_paginated_response(self, data):
        return Response(data)


class ActivityView(ListAPIView):
    queryset = models.Activity.objects.all().order_by('-id')
    serializer_class = ActivityModelListSerializer
    filter_backends = [MineFilter, PullDownFilter, ReachBottomFilter]
    pagination_class = DemoLimitOffsetPagination

    def paginate_queryset(self, queryset):
        max_id = self.request.query_params.get("max_id")
        if max_id:
            return
        return super().paginate_queryset(queryset)


class GoodsView(ListAPIView):
    queryset = models.Goods.objects.all().order_by('-id')
    serializer_class = GoodsListSerializer


from rest_framework import serializers


class ApplyCreateSerializer(serializers.Serializer):
    user_uid = serializers.CharField()
    activity_id = serializers.IntegerField()

    def validate_user_uid(self, value):
        user_object = models.UserInfo.objects.filter(uid=value).first()
        if not user_object:
            raise exceptions.ValidationError("用户不存在")
        return value

    def validate_activity_id(self, value):
        activity_object = models.Activity.objects.filter(id=value).first()
        if not activity_object:
            raise exceptions.ValidationError("活动不存在")
        return value


class ApplyView(CreateAPIView):
    serializer_class = ApplyCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        activity_id = serializer.data.get('activity_id')
        user_uid = serializer.data.get('user_uid')

        exists = models.JoinRecord.objects.filter(activity_id=activity_id, user__uid=user_uid).exists()
        if exists:
            return Response({"status": False, 'error': "此用户已报名"})

        user_object = models.UserInfo.objects.filter(uid=user_uid).first()
        models.JoinRecord.objects.create(
            activity_id=activity_id,
            user=user_object
        )

        models.Activity.objects.filter(id=activity_id).update(count=F("count") + 1)

        return Response({"status": True, 'msg': "报名成功"})


class ExchangeView(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        activity_id = request.query_params.get('activity_id')
        user_object = models.UserInfo.objects.filter(uid=user_id).first()
        record_object = models.JoinRecord.objects.filter(user=user_object, activity_id=activity_id).first()
        if not record_object:
            return Response({'status': False, "error": "数据不存在"})

        if record_object.exchange:
            return Response({'status': False, "error": "已申请，不能重复申请"})

        record_object.exchange = True
        record_object.save()

        user_object.score = user_object.score + record_object.activity.score
        user_object.save()

        return Response({'status': True, "msg": "申请成功", "score": user_object.score})

