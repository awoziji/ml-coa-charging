FROM centos:7

COPY app.py /app
COPY helpers.py /app
COPY data/misc/acc_mapping.feather /app/data/misc
COPY data/misc/tokernizer.feather /app/data/misc
COPY "model/model 2018-03-09 1424.h5" /app/model

RUN yum -y update && \
	yum -y install yum-utils development && \
	yum -y insttall https://centos7.iuscommunity.org/ius-release.rpm && \
	yum -y install python36u python36u-pip && \
	pip3 install -Iv \
		flask==0.12 \
		pandas==0.22 \
		feather-format==0.4 \
		tensorflow==1.6 \
		tqdm==4.19

WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
