# RunbookSolution Network Agent


### Creating a Keytab File

```
docker run -it --rm \
            -v $(pwd):/output \
            -e PRINCIPAL=<user@EXAMPLE.COM> \
            simplesteph/docker-kerberos-get-keytab
```