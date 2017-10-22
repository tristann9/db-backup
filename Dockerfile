FROM golang
MAINTAINER Tristan Everitt <tristan@binary.ie>

RUN go get github.com/rlmcpherson/s3gof3r/gof3r

RUN apt-get update
RUN apt-get install -y bash gzip groff less tar openssl ca-certificates gpg dirmngr wget lsb-release pv mysql-client 

# Install Percona xtrabackup.  Based on martinhelmich/xtrabackup
RUN wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb
RUN wget http://repo.percona.com/apt/pool/main/q/qpress/qpress_11-1.zesty_amd64.deb

RUN dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb
RUN apt-get update && apt-get install -y percona-xtrabackup-24
RUN dpkg -i qpress_11-1.zesty_amd64.deb

COPY s3backup /usr/bin/s3backup

VOLUME /var/lib/mysql
VOLUME /var/run/mysqld

CMD /s3backup backup
