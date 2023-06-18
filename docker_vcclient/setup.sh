#!/bin/bash

# 参考:https://programwiz.org/2022/03/22/how-to-write-shell-script-for-option-parsing/

set -eu
# 実行ユーザ作成
USER_ID=${LOCAL_UID:-9001}
GROUP_ID=${LOCAL_GID:-9001}

echo "exec with [UID : $USER_ID, GID: $GROUP_ID]"
if ! id $USER_ID; then
    useradd -u $USER_ID -o -m user
    groupmod -g $GROUP_ID user
fi

#su user
#echo "parameter: $@"
exec /usr/sbin/gosu $USER_ID /bin/bash exec.sh "$@"
#/bin/bash

