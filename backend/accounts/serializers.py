from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "valuer_license_no"]

    def validate(self, attrs):
        role = attrs.get("role")
        license_no = (attrs.get("valuer_license_no") or "").strip()

        # ✅ لازم رخصة إذا role=valuer
        if role == User.ROLE_VALUER:
            if not license_no or len(license_no) < 5:
                raise serializers.ValidationError({
                    "valuer_license_no": "رقم رخصة المقيم مطلوب (5 أحرف أو أكثر)."
                })
        else:
            attrs["valuer_license_no"] = None

        # ✅ خلي الإيميل مرتب
        attrs["email"] = (attrs.get("email") or "").lower().strip()
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "valuer_license_no"]


# ✅ Login by Email + Password (JWT)
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # بدل username نخليها email
    username_field = "email"

    def validate(self, attrs):
        email = (attrs.get("email") or "").lower().strip()
        password = attrs.get("password")

        user = User.objects.filter(email__iexact=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Email أو كلمة المرور غير صحيحة")

        if not user.is_active:
            raise serializers.ValidationError("هذا الحساب غير مفعل")

        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": MeSerializer(user).data,  # ✅ يرجّع بيانات المستخدم مع التوكن
        }
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # (اختياري) نحط role داخل التوكن
        token["role"] = user.role
        return token
