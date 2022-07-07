from rest_framework.serializers import ModelSerializer
from employer.models import Jobs


class JobsSerializers(ModelSerializer):


    class Meta:
        model=Jobs

