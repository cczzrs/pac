from django.db import models
###########################################
####### python manage.py inspectdb ########
###########################################


class OperationRecord(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    hash_id = models.CharField(max_length=64, blank=True, null=True)
    resolve_date_begin = models.DateTimeField(blank=True, null=True)
    resolve_date_end = models.DateTimeField(blank=True, null=True)
    run_time = models.DateTimeField(blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    base_sources = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        ret = {}
        for n in dir(self.read()):
            if n.find('_') == 0:
                continue
            print(n+'='+str(getattr(self, n)))
            ret[n] = str(getattr(self, n))
        return str(ret)

    class Meta:
        managed = False
        db_table = 'operation_record'

    class read(object):
        id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
        hash_id = models.CharField(max_length=64, blank=True, null=True)
        resolve_date_begin = models.DateTimeField(blank=True, null=True)
        resolve_date_end = models.DateTimeField(blank=True, null=True)
        run_time = models.DateTimeField(blank=True, null=True)
        service_type = models.CharField(max_length=100, blank=True, null=True)
        update_time = models.DateTimeField(blank=True, null=True)
        base_sources = models.CharField(max_length=5000, blank=True, null=True)


class SpidersBaseSource(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    hash_id = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=500, blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    url_source = models.CharField(max_length=500, blank=True, null=True)
    url_type = models.CharField(max_length=2, blank=True, null=True)
    resolve_type = models.CharField(max_length=2, blank=True, null=True)
    resolve_rule = models.CharField(max_length=50, blank=True, null=True)
    resolve_source = models.CharField(max_length=5000, blank=True, null=True)
    resolve_sources = models.CharField(max_length=5000, blank=True, null=True)
    resolve_next_page = models.CharField(max_length=500, blank=True, null=True)
    resolve_page_wait = models.CharField(max_length=500, blank=True, null=True)
    run_time = models.DateTimeField(blank=True, null=True)
    run_count = models.IntegerField(blank=True, null=True)
    content_page_rule = models.CharField(max_length=5000, blank=True, null=True)
    bz1 = models.CharField(max_length=255, blank=True, null=True)
    bz2 = models.CharField(max_length=255, blank=True, null=True)

    def tfilter(**p):
        return list(SpidersBaseSource.objects.exclude(url_type=0).filter(**p))

    def get(**p):
        return SpidersBaseSource.objects.exclude(url_type=0).get(**p)

    def get_by_resolve_key(resolve_key):
        p = eval(resolve_key)
        return SpidersBaseSource.tfilter(url_type='2', service_type=p[0], tags=p[1])

    def updateBy_RK_URLS_to_status(resolve_key, urlse):
        p = eval(resolve_key)
        ret = 0
        for url in urlse:
            print("updateBy_RK_URLS_to_status url=" + url)
            ret += SpidersBaseSource.objects.filter(url_source=url, url_type='2', service_type=p[0], tags=p[1]).update(url_type='-2', bz1=urlse[url])
        return ret

    def __str__(self):
        ret = {}
        for n in dir(self.read()):
            if n.find('_') == 0:
                continue
            # print(n+'='+str(getattr(self, n)))
            ret[n] = str(getattr(self, n))
        return str(ret)

    class Meta:
        managed = False
        db_table = 'spiders_base_source'

    class read(object):
        id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
        hash_id = models.CharField(max_length=64, blank=True, null=True)
        city = models.CharField(max_length=100, blank=True, null=True)
        province = models.CharField(max_length=100, blank=True, null=True)
        area = models.CharField(max_length=500, blank=True, null=True)
        service_type = models.CharField(max_length=100, blank=True, null=True)
        tags = models.CharField(max_length=255, blank=True, null=True)
        update_time = models.DateTimeField(blank=True, null=True)
        url_source = models.CharField(max_length=500, blank=True, null=True)
        url_type = models.CharField(max_length=2, blank=True, null=True)
        resolve_type = models.CharField(max_length=2, blank=True, null=True)
        resolve_rule = models.CharField(max_length=50, blank=True, null=True)
        resolve_source = models.CharField(max_length=5000, blank=True, null=True)
        resolve_sources = models.CharField(max_length=5000, blank=True, null=True)
        resolve_next_page = models.CharField(max_length=500, blank=True, null=True)
        resolve_page_wait = models.CharField(max_length=500, blank=True, null=True)
        run_time = models.DateTimeField(blank=True, null=True)
        run_count = models.IntegerField(blank=True, null=True)
        content_page_rule = models.CharField(max_length=5000, blank=True, null=True)
        bz1 = models.CharField(max_length=255, blank=True, null=True)
        bz2 = models.CharField(max_length=255, blank=True, null=True)


class SpidersNews(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    hash_id = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    news_title = models.TextField(blank=True, null=True)
    news_type = models.CharField(max_length=255, blank=True, null=True)
    news_date = models.DateTimeField(blank=True, null=True)
    url_source = models.CharField(max_length=255, blank=True, null=True)
    url_type = models.CharField(max_length=255, blank=True, null=True)
    resolve_type = models.CharField(max_length=255, blank=True, null=True)
    resolve_rule = models.CharField(max_length=255, blank=True, null=True)
    resolve_source = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    bz1 = models.CharField(max_length=255, blank=True, null=True)
    bz2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spiders_news'


class SpidersNewsContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    hash_id = models.CharField(max_length=64, blank=True, null=True)
    news_content = models.TextField(blank=True, null=True)
    news_type = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    url_source = models.CharField(max_length=255, blank=True, null=True)
    url_type = models.CharField(max_length=255, blank=True, null=True)
    bz1 = models.CharField(max_length=255, blank=True, null=True)
    bz2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spiders_news_content'

