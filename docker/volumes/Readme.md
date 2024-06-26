Use bind mounts instead of Docker volumes so that large DB data ends up here, instead of buried and mixed in `/var/lib/docker/`.

If you no longer need this project, removing its folder immediately frees up space without having to remember to delete the volumes before.

If you are low on disk space and have to import a big DB dump, just move the project's folder to an external hard drive. It needs to be formatted with ext4 though, or mount a disk image inside the external HD.

A disadvantage is that _Volumes on Docker Desktop have much higher performance than bind mounts from Mac and Windows hosts_ ([source](https://docs.docker.com/storage/volumes/)), so if using Mac you may wish to remove the symlink in `docker-compose.override.yml` and copy `docker/docker-compose.dev.yml` in its place, and add:
```diff
   postgres:
     restart: "no"
     network_mode: host
+    volumes:
+      - postgres-data:/var/lib/postgresql/data/
+
+volumes:
+  postgres-data:
```
