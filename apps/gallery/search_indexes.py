import datetime
from haystack import indexes
from models import Album,Photo


class AlbumIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    date = indexes.DateTimeField(model_attr='date')
#    photo_filename = indexes.CharField()

    def prepare_photo_filename(self,obj):
        print ("here : %s" % obj)
        return "Yeargh"
        photos = Photo.objects.order_by('order','photodate').filter(album=obj.id)
        if not photos:
            return None
        else:
            #return photos[0].filename
            return "Yeargh"

    def get_model(self):
        return Album

#    def index_queryset(self, using=None):
#        return self.get_model().objects.all().select_related('blog__tag')

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(datelastmodified__lte=datetime.datetime.now()).select_related('album__photos')