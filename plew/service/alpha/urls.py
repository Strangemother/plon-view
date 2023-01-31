from trim import urls as t_urls
# from trim.models import grab_models

# from . import views
# urlpatterns = t_urls.paths_named(views,
#     # index=('IndexView', '',),
# )

app_name = 'alpha'


urlpatterns = t_urls.as_templates(
    index=('', 'alpha/index.html'),
)
