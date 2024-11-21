#!/usr/bin/env bash

CYAN="\e[36m"
NC="\e[0m"

currdir=$(readlink -f $(dirname $0))
workdir=$(readlink -f $currdir/../vagrant)
echo "Working dir: $workdir"
pushd $workdir

for script in $(ls -1 quick-steps/*.sh | sort)
do
    fullname=$(cut -d / -f 2 <<<$script)
    name=$(cut -d - -f 2- <<<$(cut -d . -f 1 <<<$fullname))
    s1=$(cut -d - -f 1 <<<$name)
    printf "${CYAN}==> vagrant ssh -c '/vagrant/quick-steps/${fullname}' ${s1}${NC}\n"
    vagrant ssh -c "/vagrant/quick-steps/${fullname}" ${s1}
    if [[ $name == *-* ]]
    then
        s2=$(cut -d - -f 2 <<<$name)
        printf "${CYAN}==> vagrant ssh -c '/vagrant/quick-steps/${fullname}' ${s2}${NC}\n"
        vagrant ssh -c "/vagrant/quick-steps/${fullname}" ${s2}
    fi
done

popd



