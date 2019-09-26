if pgrep -f "AMP_Event_Stream.py" &>/dev/null; then
    echo "it is already running"
    exit
else
    nohup /usr/local/bin/python3.7 /home/trae.horton\@DOMAIN.local/AMP/AMP_Events/AMP_Event_Stream.py &
fi

