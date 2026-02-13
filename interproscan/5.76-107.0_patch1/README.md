# Modification

This version of the container has one subtle change, the inclusion of this line in the Dockerfile:

```Dockerfile
# Modify the interproscan.sh script to include $JAVA_OPTS so we can override Xms and Xmx
RUN sed -i 's/ -Xmx14G//g' /opt/interproscan/interproscan.sh
```

This was done because the official release of InterProScan has the value of `-Xmx` ([hard-coded](https://github.com/ebi-pf-team/interproscan/blob/5.76-107.0/core/jms-implementation/support-mini-x86-32/interproscan.sh#L54))

## patch1

This was selected as an addition to the container version, but the InterProScan version remains identical - `5.76-107.0`.