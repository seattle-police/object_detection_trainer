from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    url(r'^$', 'object_detection_trainer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^get_coordinates/$', 'object_detection_trainer.views.get_coordinates'),
    url(r'^get_detections/$', 'object_detection_trainer.views.get_detections'),
    url(r'^get_frame_detections/(?P<frame>\d+_\d+\.png)/$', 'object_detection_trainer.views.get_frame_detections'),
    url(r'^add_to_training/$', 'object_detection_trainer.views.add_to_training'),
    url(r'^add_all_to_training/$', 'object_detection_trainer.views.add_all_to_training'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^train/$', 'object_detection_trainer.views.train'),
] + static("media/", document_root='/datadrive/')
