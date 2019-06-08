FROM alpine:latest
MAINTAINER CCZZRS <cczzrs@aliyun.com>

ARG TZ="Asia/Shanghai"

# Update apk repositories
#RUN echo "http://dl-2.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories
#RUN echo "http://dl-2.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
#RUN echo "http://dl-2.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

ENV LANG=C.UTF-8
ENV TZ ${TZ}


# ### insert glibc
# Here we install GNU libc (aka glibc) and set C.UTF-8 locale as default.
RUN ALPINE_GLIBC_BASE_URL="https://github.com/sgerrand/alpine-pkg-glibc/releases/download" && \
    ALPINE_GLIBC_PACKAGE_VERSION="2.27-r0" && \
    ALPINE_GLIBC_BASE_PACKAGE_FILENAME="glibc-$ALPINE_GLIBC_PACKAGE_VERSION.apk" && \
    ALPINE_GLIBC_BIN_PACKAGE_FILENAME="glibc-bin-$ALPINE_GLIBC_PACKAGE_VERSION.apk" && \
    ALPINE_GLIBC_I18N_PACKAGE_FILENAME="glibc-i18n-$ALPINE_GLIBC_PACKAGE_VERSION.apk" && \
    apk add --no-cache --virtual=.build-dependencies wget ca-certificates && \
    echo \
        "-----BEGIN PUBLIC KEY-----\
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApZ2u1KJKUu/fW4A25y9m\
        y70AGEa/J3Wi5ibNVGNn1gT1r0VfgeWd0pUybS4UmcHdiNzxJPgoWQhV2SSW1JYu\
        tOqKZF5QSN6X937PTUpNBjUvLtTQ1ve1fp39uf/lEXPpFpOPL88LKnDBgbh7wkCp\
        m2KzLVGChf83MS0ShL6G9EQIAUxLm99VpgRjwqTQ/KfzGtpke1wqws4au0Ab4qPY\
        KXvMLSPLUp7cfulWvhmZSegr5AdhNw5KNizPqCJT8ZrGvgHypXyiFvvAH5YRtSsc\
        Zvo9GI2e2MaZyo9/lvb+LbLEJZKEQckqRj4P26gmASrZEPStwc+yqy1ShHLA0j6m\
        1QIDAQAB\
        -----END PUBLIC KEY-----" | sed 's/   */\n/g' > "/etc/apk/keys/sgerrand.rsa.pub" && \
    wget \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_I18N_PACKAGE_FILENAME" && \
    apk add --no-cache \
        "$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_I18N_PACKAGE_FILENAME" && \
    \
    rm "/etc/apk/keys/sgerrand.rsa.pub" && \
    /usr/glibc-compat/bin/localedef --force --inputfile POSIX --charmap UTF-8 "$LANG" || true && \
    echo "export LANG=$LANG" > /etc/profile.d/locale.sh && \
    \
    apk del glibc-i18n && \
    \
    rm "/root/.wget-hsts" && \
    apk del .build-dependencies && \
    rm \
        "$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_I18N_PACKAGE_FILENAME"
# ### inserted glibc
		
		
# ### insert chrome
# https://pkgs.alpinelinux.org/package/edge/community/x86_64/chromium
RUN apk update && apk add --no-cache bash \
    alsa-lib \
    at-spi2-atk \
    atk \
    cairo \
    cups-libs \
    dbus-libs \
    eudev-libs \
    expat \
    flac \
    gdk-pixbuf \
    glib \
    libgcc \
    libjpeg-turbo \
    libpng \
    libwebp \
    libx11 \
    libxcomposite \
    libxdamage \
    libxext \
    libxfixes \
    tzdata \
    libexif \
    udev \
    xvfb \
    zlib-dev \
    chromium \
    chromium-chromedriver \
    && apk add wqy-zenhei --update-cache --repository http://nl.alpinelinux.org/alpine/edge/testing --allow-untrusted \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && rm -rf /var/cache/apk/* \
    /usr/share/man \
    /tmp/*

RUN mkdir -p /data && ln -s /usr/lib/chromium/chrome /usr/bin/chrome
# ### inserted chrome


# ### insert myTOOL
# apk TOOL
RUN apk add --no-cache bash vim git

# apk nginx uwsgi python3
RUN apk update && apk add --no-cache nginx uwsgi python3 uwsgi-python3 \
	&& python3 -m pip install --upgrade pip \
	&& ln -s /usr/bin/python3 /usr/bin/python

# pip (django selenium)
RUN pip install xlrd xlwt \
	wheel urlopen urllib3 six setuptools selenium requests pytz \
	python-dateutil pycparser idna django==2.1.4 djangorestframework
	
# apk to pip
RUN apk add --no-cache py3-asn1crypto py3-cffi py3-cryptography py3-lxml 

# pip (PyMySQL)
RUN pip install PyMySQL 
# ### inserted myTOOL

RUN mkdir /home/uwsgi/

# ### build porjeact
#RUN cd /home/
#RUN git clone https://github.com/cczzrs/pac.git
#RUN python3 /home/pac/manage.py migrate
#RUN python3 /home/pac/manage.py collectstatic
#RUN uwsgi --ini /home/pac/my_uwsgi.ini
#RUN nginx -c /home/pac/nginx.conf
#RUN ps
#RUN tail -f /home/uwsgi/wsgi_mysite.log
# ### builded porjeact

