FROM centos:7

COPY app.py /app/app.py
COPY helpers.py /app/helpers.py
COPY data/misc/acc_mapping.feather /app/data/misc/acc_mapping.feather
COPY data/misc/tokenizer.pickle /app/data/misc/tokenizer.pickle
COPY ["model/model 2018-03-09 1424.h5", "/app/model/model 2018-03-09 1424.h5"]
COPY templates/index.html /app/templates/index.html
COPY static /app/static

RUN yum -y update && \
	yum -y install yum-utils && \
	yum -y install https://centos7.iuscommunity.org/ius-release.rpm && \
	yum -y install python36u python36u-pip && \
	pip3.6 install --no-cache-dir -Iv \
		flask==0.12 \
		pandas==0.22 \
		feather-format==0.4 \
		tensorflow==1.6 \
		tqdm==4.19.7 \
		h5py==2.7.1 && \
	yum -y clean all

EXPOSE 5000
WORKDIR /app
ENTRYPOINT ["python3.6"]
CMD ["app.py"]
