if [ "$1" == "-h" ] ; then
    echo "Usage:  `$0` [-h]"
    exit 0
fi

if type $1 2>&-; then
    echo "Found Python" >&2
else 
    echo "Python3 not found, attempting install..." >&2
fi
