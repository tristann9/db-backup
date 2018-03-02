# Modified s3backup to run under Docker

Stream MySQL/MariaDB Backups to AWS S3 and then have AWS Lambda propagate the backup to fit the daily/weekly/monthly/yearly rotating model.  Outside of this project's scope, S3 lifecycle and replication can be used to control backup expirations and redundancy.

This project is based on tanji/s3backup, but modified to allow AWS Lambda handle the backup rotation.  In other words, removed the date format YYYYMMDD from the code.


## Tools

The docker image already contains the prerequisites described in tanji/s3backup.  They are: 


- [s3gof3r](https://github.com/rlmcpherson/s3gof3r)

  s3gof3r provides fast, parallelized, pipelined streaming access to Amazon S3. It includes a command-line interface: gof3r
- [xtrabackup](http://www.percona.com/downloads/XtraBackup/LATEST/) >= 2.3

  Percona XtraBackup is an open-source hot backup utility for MySQL - based servers that doesn't lock your database during the backup.

## Configuration

Copy *s3backup.cnf.example* to */etc/s3backup.cnf* or *~/.s3backup.cnf* and edit it accordingly

Set AWS S3 Bucket Name to store backups

```
S3_BUCKET_NAME='bucket_name'
```

Set AWS S3 Bucket path to store backups. This is useful if you want to store all this backups in a dedicated directory

```
S3_BACKUP_PATH='latest/project_name/'
```

Set Backup path to store backups, e.g project_name

```
S3_BACKUP_NAME='app_name'
```

MySQL User user when running a backup.

```
MYSQL_USER='root'
```

MySQL User password user when running a backup.

```
MYSQL_PASSWORD='root'
```

MySQL host.

```
MYSQL_HOST='10.0.0.20'
```

MySQL Port.

```
MYSQL_PORT='3306'
```

Command to start mysql, based on your distro.

```
MYSQL_SERVICE_CMD="service mysql start"
```

Directory used to restore the backup. If you are using *full-restore* set this to MySQL datadir (e.g. /var/lib/mysql) otherwise set this to a temporal directory.

```
LOCAL_DIR='/tmp/restore_db'
```

AWS Region where S3 Bucket is located

```
AWS_REGION='s3-us-west-2.amazonaws.com'
```

AWS Access key

```
export AWS_ACCESS_KEY_ID='YOUR_AWS_ACCESS_KEY_ID'
```

AWS Secret key

```
export AWS_SECRET_ACCESS_KEY='YOUR_AWS_SECRET_ACCESS_KEY'
```

## Usage

Run the container

```
docker run -it --rm -v /etc/s3backup.cnf:/etc/s3backup.cnf  tristann9/db-backup s3backup <command>
```

Or to access the shell directly

```
docker run -it --rm -v /etc/s3backup.cnf:/etc/s3backup.cnf  tristann9/db-backup bash
```

Or to restore a local file use:

```
docker run -it --rm -v ~/test/etc/s3backup.cnf:/etc/s3backup.cnf -v ~/test/etc/key:/root/.s3backup/key -v ~/test/restores:/tmp/restore_db -v ~/test/input:/input tristann9/db-backup s3backup local-restore /input database_file.xbcrypt
```

Note: Use the docker command [--volumes-from database-container-id ] to map the MySQL/MariaDB volumes onto the s3backup container.

 

Generate the AES256 key for backups encryption

```
s3backup genkey
```

Upload a full backup to S3 Bucket

```
s3backup backup
```


Prepare a full backup restore from S3 Bucket.  If the backup path is specified then that file is downloaded else the latest backup is downloaded. This will leave a restore ready to run *innobackupex --move-back DIR*

```
s3backup restore <backup-path> 
```

Restore a full backup from S3 Bucket.  If the backup path is specified then that file is downloaded else the latest backup is downloaded. Set LOCAL_DIR to MySQL datadir, make sure this directory is empty and MySQL Service is not running.

```
s3backup full-restore <backup-path> 
```

## References

- https://github.com/tanji/s3backup

- https://mariadb.com/blog/streaming-mariadb-backups-cloud
